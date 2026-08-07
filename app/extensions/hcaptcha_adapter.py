# -*- coding: utf-8 -*-
from __future__ import annotations

import unicodedata
from contextlib import suppress
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from hcaptcha_challenger.agent.challenger import AgentV, RoboticArm
from hcaptcha_challenger.models import SpatialPath
from loguru import logger

from extensions.numbered_line_solver import solve_numbered_line_drag

NUMBERED_LINE_KEYWORDS = ("drag", "segment", "right", "complete", "line")
MISSING_PIPE_PROMPT = "place the missing pipe so the emu can cross"
_PROMPT_HOMOGLYPHS = str.maketrans({"Ѕ": "S", "ѕ": "s", "Ο": "O", "ο": "o", "О": "O", "о": "o"})

NUMBERED_LINE_SKILL = """
The visible instruction is: "Please drag the segment on the right to complete the line."

This is a numbered-sequence completion puzzle. The numbered sequence rule overrides generic
path tracing, semantic matching, color matching, and nearest-object heuristics.

1. Read the number N printed inside the black circle on the isolated draggable segment in the
   right-hand panel.
2. On the left canvas, locate the centers of the numbered circles N-1 and N+1.
3. Drag from the center of circle N to the exact midpoint between circles N-1 and N+1. Ignore the
   colored strip tips; successful challenge evidence shows the numbered-circle midpoint is the
   scoring target.
4. Return exactly one drag path and verify that the destination lies between both neighboring
   numbered circles.
""".strip()

_PROMPT_SELECTORS = (
    ".prompt-text",
    "[class*='prompt-text']",
    "[class*='challenge-prompt']",
    "[class*='prompt']",
)

_original_match_user_prompt = RoboticArm._match_user_prompt
_original_review_challenge_type = AgentV._review_challenge_type
_original_capture_spatial_mapping = RoboticArm._capture_spatial_mapping
_original_perform_drag_drop = RoboticArm._perform_drag_drop
_original_challenge_image_drag_drop = RoboticArm.challenge_image_drag_drop


def _normalize_prompt(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    normalized = unicodedata.normalize("NFKC", value).translate(_PROMPT_HOMOGLYPHS)
    return " ".join(normalized.split()).strip()


def _is_numbered_line_prompt(value: Any) -> bool:
    prompt = _normalize_prompt(value).casefold()
    return all(keyword in prompt for keyword in NUMBERED_LINE_KEYWORDS)


def _is_missing_pipe_prompt(value: Any) -> bool:
    return _normalize_prompt(value).casefold() == MISSING_PIPE_PROMPT


def _current_prompt(robotic_arm: RoboticArm) -> str:
    if robotic_arm.captcha_payload:
        with suppress(Exception):
            prompt = _normalize_prompt(robotic_arm.captcha_payload.get_requester_question())
            if prompt and prompt.lower() != "unknown":
                return prompt
    return _normalize_prompt(robotic_arm._challenge_prompt)


async def _read_visible_prompt(robotic_arm: RoboticArm) -> str:
    frame = await robotic_arm.get_challenge_frame_locator()
    if frame is None:
        return ""

    for selector in _PROMPT_SELECTORS:
        with suppress(Exception):
            candidates = frame.locator(selector)
            count = min(await candidates.count(), 6)
            for index in range(count):
                candidate = candidates.nth(index)
                if not await candidate.is_visible(timeout=300):
                    continue
                prompt = _normalize_prompt(await candidate.inner_text(timeout=500))
                if prompt:
                    return prompt
    return ""


def _detect_numbered_source_anchor(
    challenge_screenshot: Path, challenge_bbox: dict[str, float]
) -> tuple[int, int] | None:
    image = cv2.imread(str(challenge_screenshot))
    if image is None:
        return None

    height, width = image.shape[:2]
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(
        cv2.GaussianBlur(grayscale, (3, 3), 0),
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=20,
        param1=80,
        param2=25,
        minRadius=6,
        maxRadius=14,
    )
    if circles is None:
        return None

    yy, xx = np.indices(grayscale.shape)
    candidates: list[tuple[float, int, int, int]] = []
    for x, y, radius in np.round(circles[0]).astype(int):
        if x <= width * 0.75 or y <= height * 0.31:
            continue

        inner_radius = max(3, radius - 3)
        inner = (xx - x) ** 2 + (yy - y) ** 2 <= inner_radius**2
        inner_mean = float(np.mean(grayscale[inner]))
        inner_std = float(np.std(grayscale[inner]))
        if inner_mean >= 110 or inner_std <= 15:
            continue
        candidates.append((inner_mean, x, y, radius))

    if not candidates:
        return None

    _, source_x, source_y, source_radius = min(candidates)
    scale_x = challenge_bbox["width"] / width
    scale_y = challenge_bbox["height"] / height
    anchor = (
        round(challenge_bbox["x"] + source_x * scale_x),
        round(challenge_bbox["y"] + source_y * scale_y),
    )

    debug_image = image.copy()
    cv2.circle(debug_image, (source_x, source_y), source_radius + 4, (0, 0, 255), 2)
    debug_path = challenge_screenshot.with_name(
        challenge_screenshot.name.replace("_challenge_view.png", "_source_anchor.png")
    )
    cv2.imwrite(str(debug_path), debug_image)
    return anchor


def _detect_missing_pipe_source_anchor(
    challenge_screenshot: Path, challenge_bbox: dict[str, float]
) -> tuple[int, int] | None:
    """Find the bright pipe inside the right-hand drag tray.

    The missing-pipe puzzle keeps the draggable part in a dark tray at the right of the
    challenge. Restricting detection to that tray prevents the connected pipes on the main
    canvas from becoming a false source. The deepest point in the colored component is a
    dependable location to press without needing to infer the pipe's shape or destination.
    """
    image = cv2.imread(str(challenge_screenshot))
    if image is None:
        return None

    height, width = image.shape[:2]
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lime_mask = cv2.inRange(hsv, np.array((35, 80, 100)), np.array((95, 255, 255)))
    tray_start = round(width * 0.78)
    lime_mask[:, :tray_start] = 0

    component_count, labels, stats, _centers = cv2.connectedComponentsWithStats(lime_mask)
    candidates: list[tuple[float, int, int]] = []
    for label in range(1, component_count):
        x, y, component_width, component_height, area = stats[label]
        if (
            x < tray_start
            or y < height * 0.25
            or component_width < 12
            or component_height < 12
            or area < 100
        ):
            continue

        component_mask = np.where(labels == label, 255, 0).astype(np.uint8)
        distance = cv2.distanceTransform(component_mask, cv2.DIST_L2, 5)
        _min_distance, max_distance, _min_location, _max_location = cv2.minMaxLoc(distance)
        if max_distance >= 5:
            candidates.append((max_distance, area, label))

    if not candidates:
        return None

    _max_distance, _area, source_label = max(candidates)
    component_mask = np.where(labels == source_label, 255, 0).astype(np.uint8)
    distance = cv2.distanceTransform(component_mask, cv2.DIST_L2, 5)
    _min_distance, _max_distance, _min_location, source_local = cv2.minMaxLoc(distance)
    source_x, source_y = source_local

    scale_x = challenge_bbox["width"] / width
    scale_y = challenge_bbox["height"] / height
    anchor = (
        round(challenge_bbox["x"] + source_x * scale_x),
        round(challenge_bbox["y"] + source_y * scale_y),
    )

    debug_image = image.copy()
    cv2.circle(debug_image, (source_x, source_y), 7, (0, 0, 255), 2)
    debug_path = challenge_screenshot.with_name(
        challenge_screenshot.name.replace("_challenge_view.png", "_pipe_source_anchor.png")
    )
    cv2.imwrite(str(debug_path), debug_image)
    return anchor


def _match_user_prompt_with_epic_skills(robotic_arm: RoboticArm, job_type: Any) -> str:
    prompt = _current_prompt(robotic_arm)
    if _is_numbered_line_prompt(prompt):
        logger.info("Using numbered-line hCaptcha skill | prompt={!r}", prompt)
        return NUMBERED_LINE_SKILL
    return _original_match_user_prompt(robotic_arm, job_type)


async def _review_challenge_type_with_dom_prompt(agent: AgentV):
    challenge_type = await _original_review_challenge_type(agent)
    prompt = await _read_visible_prompt(agent.robotic_arm)
    if prompt:
        agent.robotic_arm._challenge_prompt = prompt
        logger.debug("Read visible hCaptcha prompt from DOM | prompt={!r}", prompt)
    return challenge_type


async def _capture_spatial_mapping_with_source_anchor(
    robotic_arm: RoboticArm, frame_challenge: Any, cache_key: Path, crumb_id: int | str
):
    raw, projection = await _original_capture_spatial_mapping(
        robotic_arm, frame_challenge, cache_key, crumb_id
    )
    robotic_arm._epic_numbered_source_anchor = None
    robotic_arm._epic_numbered_drag_path = None
    robotic_arm._epic_pipe_source_anchor = None

    prompt = _current_prompt(robotic_arm)
    if not (_is_numbered_line_prompt(prompt) or _is_missing_pipe_prompt(prompt)):
        return raw, projection

    with suppress(Exception):
        challenge_view = frame_challenge.locator("//div[@class='challenge-view']")
        challenge_bbox = await challenge_view.bounding_box()
        if challenge_bbox and _is_numbered_line_prompt(prompt):
            solution = solve_numbered_line_drag(raw, challenge_bbox)
            if solution:
                robotic_arm._epic_numbered_source_anchor = solution.start
                robotic_arm._epic_numbered_drag_path = (solution.start, solution.end)
                logger.info(
                    "Solved numbered-line drag deterministically | layout=1-{} source={} "
                    "score={:.3f} path={} -> {}",
                    solution.digit_count,
                    solution.source_label,
                    solution.score,
                    solution.start,
                    solution.end,
                )
                return raw, projection

            anchor = _detect_numbered_source_anchor(raw, challenge_bbox)
            robotic_arm._epic_numbered_source_anchor = anchor
            if anchor:
                logger.info("Detected numbered-line draggable anchor | anchor={}", anchor)
        elif challenge_bbox and _is_missing_pipe_prompt(prompt):
            anchor = _detect_missing_pipe_source_anchor(raw, challenge_bbox)
            robotic_arm._epic_pipe_source_anchor = anchor
            if anchor:
                logger.info("Detected missing-pipe draggable anchor | anchor={}", anchor)

    return raw, projection


async def _perform_drag_drop_with_source_anchor(
    robotic_arm: RoboticArm, path: Any, steps: int = 25, delay_ms: int = 15
):
    deterministic_path = getattr(robotic_arm, "_epic_numbered_drag_path", None)
    if deterministic_path:
        original_start = (path.start_point.x, path.start_point.y)
        original_end = (path.end_point.x, path.end_point.y)
        start, end = deterministic_path
        path.start_point.x, path.start_point.y = start
        path.end_point.x, path.end_point.y = end
        logger.info(
            "Applied deterministic numbered-line circle midpoint | "
            "input={} -> {} deterministic={} -> {}",
            original_start,
            original_end,
            start,
            end,
        )
        robotic_arm._epic_numbered_drag_path = None
        return await _original_perform_drag_drop(robotic_arm, path, steps=steps, delay_ms=delay_ms)

    anchor = getattr(robotic_arm, "_epic_numbered_source_anchor", None)
    if anchor:
        original_start = (path.start_point.x, path.start_point.y)
        original_end = (path.end_point.x, path.end_point.y)
        delta_x = anchor[0] - original_start[0]
        delta_y = anchor[1] - original_start[1]

        if abs(delta_x) <= 100 and abs(delta_y) <= 100:
            path.start_point.x = anchor[0]
            path.start_point.y = anchor[1]
            path.end_point.x += delta_x
            path.end_point.y += delta_y
            logger.info(
                "Snapped numbered-line drag to visible source anchor | original={} -> {} "
                "corrected={} -> {}",
                original_start,
                original_end,
                (path.start_point.x, path.start_point.y),
                (path.end_point.x, path.end_point.y),
            )
        return await _original_perform_drag_drop(robotic_arm, path, steps=steps, delay_ms=delay_ms)

    pipe_anchor = getattr(robotic_arm, "_epic_pipe_source_anchor", None)
    if pipe_anchor:
        original_start = (path.start_point.x, path.start_point.y)
        original_end = (path.end_point.x, path.end_point.y)
        path.start_point.x, path.start_point.y = pipe_anchor
        logger.info(
            "Corrected missing-pipe drag source from visible tray | original={} -> {} "
            "corrected={} -> {}",
            original_start,
            original_end,
            pipe_anchor,
            original_end,
        )
        robotic_arm._epic_pipe_source_anchor = None
        return await _original_perform_drag_drop(robotic_arm, path, steps=steps, delay_ms=delay_ms)

    return await _original_perform_drag_drop(robotic_arm, path, steps=steps, delay_ms=delay_ms)


async def _challenge_image_drag_drop_with_numbered_solver(robotic_arm: RoboticArm, job_type: Any):
    if not _is_numbered_line_prompt(_current_prompt(robotic_arm)):
        return await _original_challenge_image_drag_drop(robotic_arm, job_type)

    frame_challenge = await robotic_arm.get_challenge_frame_locator()
    if frame_challenge is None:
        return await _original_challenge_image_drag_drop(robotic_arm, job_type)

    crumb_count = await robotic_arm.check_crumb_count()
    cache_key = robotic_arm.config.create_cache_key(robotic_arm.captcha_payload)

    for crumb_id in range(crumb_count):
        await robotic_arm.page.wait_for_timeout(
            robotic_arm.config.WAIT_FOR_CHALLENGE_VIEW_TO_RENDER_MS
        )
        await robotic_arm._capture_spatial_mapping(frame_challenge, cache_key, crumb_id)
        deterministic_path = getattr(robotic_arm, "_epic_numbered_drag_path", None)
        if not deterministic_path:
            logger.warning(
                "Deterministic numbered-line solver could not establish a confident path; "
                "falling back to the configured spatial model"
            )
            return await _original_challenge_image_drag_drop(robotic_arm, job_type)

        start, end = deterministic_path
        path = SpatialPath(
            start_point={"x": start[0], "y": start[1]}, end_point={"x": end[0], "y": end[1]}
        )
        await robotic_arm._perform_drag_drop(path)

        with suppress(TimeoutError):
            submit_btn = frame_challenge.locator("//div[@class='button-submit button']")
            await robotic_arm.click_by_mouse(submit_btn)


def apply_hcaptcha_patch() -> None:
    if getattr(AgentV, "_epic_prompt_patch_applied", False):
        return

    RoboticArm._match_user_prompt = _match_user_prompt_with_epic_skills
    RoboticArm._capture_spatial_mapping = _capture_spatial_mapping_with_source_anchor
    RoboticArm._perform_drag_drop = _perform_drag_drop_with_source_anchor
    RoboticArm.challenge_image_drag_drop = _challenge_image_drag_drop_with_numbered_solver
    AgentV._review_challenge_type = _review_challenge_type_with_dom_prompt
    AgentV._epic_prompt_patch_applied = True
    logger.info("hCaptcha prompt and numbered-line skill patch applied")
