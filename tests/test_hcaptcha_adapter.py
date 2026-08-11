import asyncio
from types import SimpleNamespace

import cv2
import numpy as np

import extensions.hcaptcha_adapter as hcaptcha_adapter
from extensions.hcaptcha_adapter import (
    ANIMAL_COUNT_SKILL,
    _capture_spatial_mapping_with_source_anchor,
    _current_prompt,
    _detect_missing_pipe_source_anchor,
    _is_animal_count_prompt,
    _is_missing_pipe_prompt,
)


def test_missing_pipe_prompt_is_narrowly_recognized():
    assert _is_missing_pipe_prompt("Place the missing pipe so the emu can cross")
    assert not _is_missing_pipe_prompt("Please drag the segment on the right to complete the line")
    assert not _is_missing_pipe_prompt("Find where you can safely set down the item shown")
    assert not _is_missing_pipe_prompt("Cross-check the missing pipeline for emulsion")


def test_animal_count_prompt_is_narrowly_recognized_and_excludes_reference_panel():
    assert _is_animal_count_prompt("Find all animals the given number of times")
    assert not _is_animal_count_prompt("Find all animals in the image")
    assert "right-hand column is a reference list" in ANIMAL_COUNT_SKILL
    assert "Never click" in ANIMAL_COUNT_SKILL


def test_visible_prompt_has_priority_over_stale_payload_prompt():
    robotic_arm = SimpleNamespace(
        _challenge_prompt="Find where you can safely set down the item shown",
        captcha_payload=SimpleNamespace(
            get_requester_question=lambda: "Place the missing pipe so the emu can cross"
        ),
    )

    assert _current_prompt(robotic_arm) == "Find where you can safely set down the item shown"


def test_missing_pipe_anchor_uses_right_hand_tray_and_projects_to_page(tmp_path):
    image = np.full((471, 500, 3), (48, 48, 48), dtype=np.uint8)
    lime = (50, 220, 120)

    # The canvas contains a larger distractor, while the draggable pipe is in the tray.
    cv2.rectangle(image, (75, 183), (210, 221), lime, thickness=-1)
    cv2.line(image, (430, 162), (430, 190), lime, thickness=18)
    cv2.line(image, (430, 190), (458, 190), lime, thickness=18)

    screenshot = tmp_path / "pipe_challenge_view.png"
    assert cv2.imwrite(str(screenshot), image)

    anchor = _detect_missing_pipe_source_anchor(
        screenshot, {"x": 390, "y": 94, "width": 500, "height": 471}
    )

    assert anchor is not None
    assert 810 <= anchor[0] <= 860
    assert 245 <= anchor[1] <= 295


def test_missing_pipe_drag_replaces_only_the_model_source(monkeypatch):
    captured = {}

    async def record_drag(_robotic_arm, path, **_kwargs):
        captured["start"] = (path.start_point.x, path.start_point.y)
        captured["end"] = (path.end_point.x, path.end_point.y)
        return "dragged"

    monkeypatch.setattr(hcaptcha_adapter, "_original_perform_drag_drop", record_drag)
    robotic_arm = SimpleNamespace(
        _epic_numbered_drag_path=None,
        _epic_pipe_source_anchor=(829, 271),
    )
    path = SimpleNamespace(
        start_point=SimpleNamespace(x=836, y=341),
        end_point=SimpleNamespace(x=711, y=322),
    )

    result = asyncio.run(hcaptcha_adapter._perform_drag_drop_with_source_anchor(robotic_arm, path))

    assert result == "dragged"
    assert captured == {"start": (829, 271), "end": (711, 322)}
    assert robotic_arm._epic_pipe_source_anchor is None


def test_numbered_line_anchor_has_priority_over_pipe_anchor(monkeypatch):
    captured = {}

    async def record_drag(_robotic_arm, path, **_kwargs):
        captured["start"] = (path.start_point.x, path.start_point.y)
        captured["end"] = (path.end_point.x, path.end_point.y)
        return "dragged"

    monkeypatch.setattr(hcaptcha_adapter, "_original_perform_drag_drop", record_drag)
    robotic_arm = SimpleNamespace(
        _epic_numbered_drag_path=None,
        _epic_numbered_source_anchor=(430, 250),
        _epic_pipe_source_anchor=(829, 271),
    )
    path = SimpleNamespace(
        start_point=SimpleNamespace(x=400, y=250),
        end_point=SimpleNamespace(x=500, y=300),
    )

    result = asyncio.run(hcaptcha_adapter._perform_drag_drop_with_source_anchor(robotic_arm, path))

    assert result == "dragged"
    assert captured == {"start": (430, 250), "end": (530, 300)}


def test_stale_pipe_payload_does_not_anchor_a_replacement_challenge(monkeypatch, tmp_path):
    screenshot = tmp_path / "replacement_challenge_view.png"
    screenshot.write_bytes(b"not-read-by-this-test")
    projection = tmp_path / "replacement_spatial_helper.png"
    detector_called = False

    async def capture(_robotic_arm, _frame, _cache_key, _crumb_id):
        return screenshot, projection

    async def visible_prompt(_robotic_arm):
        return "Find where you can safely set down the item shown"

    def detect_pipe(*_args):
        nonlocal detector_called
        detector_called = True
        return (800, 300)

    monkeypatch.setattr(hcaptcha_adapter, "_original_capture_spatial_mapping", capture)
    monkeypatch.setattr(hcaptcha_adapter, "_read_visible_prompt", visible_prompt)
    monkeypatch.setattr(hcaptcha_adapter, "_detect_missing_pipe_source_anchor", detect_pipe)
    robotic_arm = SimpleNamespace(
        _challenge_prompt="Place the missing pipe so the emu can cross",
        captcha_payload=SimpleNamespace(
            get_requester_question=lambda: "Place the missing pipe so the emu can cross"
        ),
    )

    raw, actual_projection = asyncio.run(
        _capture_spatial_mapping_with_source_anchor(robotic_arm, object(), tmp_path, 0)
    )

    assert (raw, actual_projection) == (screenshot, projection)
    assert robotic_arm._challenge_prompt == "Find where you can safely set down the item shown"
    assert robotic_arm._epic_pipe_source_anchor is None
    assert not detector_called
