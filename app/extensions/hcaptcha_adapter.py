# -*- coding: utf-8 -*-
from __future__ import annotations

import unicodedata
from contextlib import suppress
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from hcaptcha_challenger.agent.challenger import AgentV, RoboticArm
from loguru import logger

NUMBERED_LINE_KEYWORDS = ("drag", "segment", "right", "complete", "line")
_PROMPT_HOMOGLYPHS = str.maketrans({"Ѕ": "S", "ѕ": "s", "Ο": "O", "ο": "o", "О": "O", "о": "o"})

NUMBERED_LINE_SKILL = """
The visible instruction is: "Please drag the segment on the right to complete the line."

This is a numbered-sequence completion puzzle. The numbered sequence rule overrides generic
path tracing, semantic matching, color matching, and nearest-object heuristics.

1. Read the number N printed inside the black circle on the isolated draggable segment in the
   right-hand panel.
2. On the left canvas, locate the fixed segments numbered N-1 and N+1.
3. The black numbered circles only identify the segments. Never use or average their centers to
   calculate the destination. Trace each colored strip all the way to both visible outer tips.
4. Inspect the four tips of N-1 and N+1. The missing destination is the midpoint of the closest,
   directionally aligned tip pair whose separation fits the length and orientation of segment N.
5. Drag from the center of segment N to the center of that empty gap. The destination must be on
   the left canvas, adjacent to both neighboring segments, and must not be on any existing colored
   segment or on a numbered circle.
6. Return exactly one drag path. Before returning it, verify that inserting N at that destination
   produces the consecutive order N-1, N, N+1 and visually joins both ends of the line.
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


def _normalize_prompt(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    normalized = unicodedata.normalize("NFKC", value).translate(_PROMPT_HOMOGLYPHS)
    return " ".join(normalized.split()).strip()


def _is_numbered_line_prompt(value: Any) -> bool:
    prompt = _normalize_prompt(value).casefold()
    return all(keyword in prompt for keyword in NUMBERED_LINE_KEYWORDS)


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

    if not _is_numbered_line_prompt(_current_prompt(robotic_arm)):
        return raw, projection

    with suppress(Exception):
        challenge_view = frame_challenge.locator("//div[@class='challenge-view']")
        challenge_bbox = await challenge_view.bounding_box()
        if challenge_bbox:
            anchor = _detect_numbered_source_anchor(raw, challenge_bbox)
            robotic_arm._epic_numbered_source_anchor = anchor
            if anchor:
                logger.info("Detected numbered-line draggable anchor | anchor={}", anchor)

    return raw, projection


async def _perform_drag_drop_with_source_anchor(
    robotic_arm: RoboticArm, path: Any, steps: int = 25, delay_ms: int = 15
):
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


def apply_hcaptcha_patch() -> None:
    if getattr(AgentV, "_epic_prompt_patch_applied", False):
        return

    RoboticArm._match_user_prompt = _match_user_prompt_with_epic_skills
    RoboticArm._capture_spatial_mapping = _capture_spatial_mapping_with_source_anchor
    RoboticArm._perform_drag_drop = _perform_drag_drop_with_source_anchor
    AgentV._review_challenge_type = _review_challenge_type_with_dom_prompt
    AgentV._epic_prompt_patch_applied = True
    logger.info("hCaptcha prompt and numbered-line skill patch applied")
