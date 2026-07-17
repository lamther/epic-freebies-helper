# -*- coding: utf-8 -*-
from __future__ import annotations

from contextlib import suppress
from typing import Any

from hcaptcha_challenger.agent.challenger import AgentV, RoboticArm
from loguru import logger

NUMBERED_LINE_MARKER = "drag the segment on the right to complete the line"

NUMBERED_LINE_SKILL = """
The visible instruction is: "Please drag the segment on the right to complete the line."

This is a numbered-sequence completion puzzle. The numbered sequence rule overrides generic
path tracing, semantic matching, color matching, and nearest-object heuristics.

1. Read the number N printed inside the black circle on the isolated draggable segment in the
   right-hand panel.
2. On the left canvas, locate the fixed segments numbered N-1 and N+1.
3. Inspect both endpoints of those two fixed segments. The missing destination is the small empty
   gap between the closest, directionally aligned endpoint pair from N-1 and N+1.
4. Drag from the center of segment N to the center of that empty gap. The destination must be on
   the left canvas, adjacent to both neighboring segments, and must not be on any existing colored
   segment or on a numbered circle.
5. Return exactly one drag path. Before returning it, verify that inserting N at that destination
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


def _normalize_prompt(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.split()).strip()


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


def _match_user_prompt_with_epic_skills(robotic_arm: RoboticArm, job_type: Any) -> str:
    prompt = _current_prompt(robotic_arm)
    if NUMBERED_LINE_MARKER in prompt.lower():
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


def apply_hcaptcha_patch() -> None:
    if getattr(AgentV, "_epic_prompt_patch_applied", False):
        return

    RoboticArm._match_user_prompt = _match_user_prompt_with_epic_skills
    AgentV._review_challenge_type = _review_challenge_type_with_dom_prompt
    AgentV._epic_prompt_patch_applied = True
    logger.info("hCaptcha prompt and numbered-line skill patch applied")
