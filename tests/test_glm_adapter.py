import json
from types import SimpleNamespace

import pytest

from hcaptcha_challenger.models import (
    ChallengeRouterResult,
    ImageAreaSelectChallenge,
    ImageBboxChallenge,
    ImageBinaryChallenge,
    ImageDragDropChallenge,
)

from extensions.llm_adapter import (
    _GLMAsyncModels,
    _coerce_json_response_payload,
    _coerce_payload_for_schema,
    _extract_json_payload,
    _normalize_glm_payload,
    _structured_output_contract,
)


def _parse_glm_response(text, schema):
    client = _GLMAsyncModels(settings=None, storage={})
    return client._parse_response(text, SimpleNamespace(response_schema=schema))


def test_schema_then_answer_array_uses_only_the_valid_answer():
    answer = {
        "challenge_prompt": "Find where you can safely set down the item shown",
        "points": [{"x": 747, "y": 396}],
    }
    text = json.dumps([ImageAreaSelectChallenge.model_json_schema(), answer])

    payload = _coerce_json_response_payload(text, ImageAreaSelectChallenge)
    challenge = ImageAreaSelectChallenge(**payload)

    assert challenge.challenge_prompt == answer["challenge_prompt"]
    assert [point.model_dump() for point in challenge.points] == answer["points"]

    parsed = _parse_glm_response(text, ImageAreaSelectChallenge)
    assert [point.model_dump() for point in parsed.points] == answer["points"]


def test_schema_echo_with_root_answer_is_accepted():
    answer = {
        "challenge_prompt": "Find where you can safely set down the item shown",
        "points": [{"x": 730, "y": 385}],
    }
    text = json.dumps({**ImageAreaSelectChallenge.model_json_schema(), **answer})

    parsed = _parse_glm_response(text, ImageAreaSelectChallenge)

    assert parsed.challenge_prompt == answer["challenge_prompt"]
    assert [point.model_dump() for point in parsed.points] == answer["points"]


def test_schema_only_object_is_rejected_at_adapter_boundary():
    text = json.dumps(ImageAreaSelectChallenge.model_json_schema())

    assert _parse_glm_response(text, ImageAreaSelectChallenge) is None


def test_schema_then_drag_alias_answer_uses_candidate_local_text():
    answer = {
        "source_coordinates": {"x": 847, "y": 335},
        "target_coordinates": {"x": 586, "y": 495},
    }
    text = json.dumps([ImageDragDropChallenge.model_json_schema(), answer])

    parsed = _parse_glm_response(text, ImageDragDropChallenge)

    assert parsed.paths[0].start_point.model_dump() == answer["source_coordinates"]
    assert parsed.paths[0].end_point.model_dump() == answer["target_coordinates"]


def test_schema_only_array_is_not_accepted_as_an_answer():
    text = json.dumps([ImageAreaSelectChallenge.model_json_schema()])

    with pytest.raises(ValueError, match="did not contain a valid answer"):
        _coerce_json_response_payload(text, ImageAreaSelectChallenge)


def test_multiple_valid_array_answers_are_rejected_as_ambiguous():
    answer = {"challenge_prompt": "", "points": [{"x": 747, "y": 396}]}

    with pytest.raises(ValueError, match="multiple valid answers"):
        _coerce_json_response_payload(json.dumps([answer, answer]), ImageAreaSelectChallenge)


def test_multiple_valid_drag_answers_do_not_fall_back_to_the_first_answer():
    first_answer = {
        "challenge_prompt": "Place the missing pipe so the emu can cross",
        "paths": [{"start_point": {"x": 819, "y": 322}, "end_point": {"x": 711, "y": 322}}],
    }
    second_answer = {
        "challenge_prompt": "Place the missing pipe so the emu can cross",
        "paths": [{"start_point": {"x": 847, "y": 335}, "end_point": {"x": 586, "y": 495}}],
    }

    assert (
        _parse_glm_response(json.dumps([first_answer, second_answer]), ImageDragDropChallenge)
        is None
    )


def test_area_select_box_answer_is_converted_to_click_points():
    text = '{"answer":[[781,525,889,624],[1031,525,1139,624]]}'

    payload = _coerce_payload_for_schema(
        _normalize_glm_payload(_extract_json_payload(text)), ImageAreaSelectChallenge, text
    )
    challenge = ImageAreaSelectChallenge(**payload)

    assert challenge.points[0].model_dump() == {"x": 835, "y": 574}
    assert challenge.points[1].model_dump() == {"x": 1085, "y": 574}


def test_area_select_dict_boxes_are_converted_to_click_points():
    payload = {
        "answer": [
            {"x_min": 10, "y_min": 20, "x_max": 30, "y_max": 60},
            {"x_min": 101, "y_min": 201, "x_max": 200, "y_max": 300},
        ]
    }
    text = json.dumps(payload)

    coerced = _coerce_payload_for_schema(
        _normalize_glm_payload(payload), ImageAreaSelectChallenge, text
    )
    challenge = ImageAreaSelectChallenge(**coerced)

    assert [point.model_dump() for point in challenge.points] == [
        {"x": 20, "y": 40},
        {"x": 150, "y": 250},
    ]


def test_area_select_coordinates_string_with_single_quotes_is_converted():
    text = (
        '{"Challenge Prompt":"","Coordinates":"['
        "{'x': 889, 'y': 613}, {'x': 996, 'y': 538}, {'x': 817, 'y': 761}"
        ']"}'
    )

    payload = _coerce_payload_for_schema(
        _normalize_glm_payload(_extract_json_payload(text)), ImageAreaSelectChallenge, text
    )
    challenge = ImageAreaSelectChallenge(**payload)

    assert challenge.challenge_prompt == ""
    assert [point.model_dump() for point in challenge.points] == [
        {"x": 889, "y": 613},
        {"x": 996, "y": 538},
        {"x": 817, "y": 761},
    ]


def test_area_select_bare_csv_point_is_converted():
    text = '{"answer":"1139, 729"}'

    payload = _coerce_payload_for_schema(
        _normalize_glm_payload(_extract_json_payload(text)), ImageAreaSelectChallenge, text
    )
    challenge = ImageAreaSelectChallenge(**payload)

    assert challenge.challenge_prompt == ""
    assert [point.model_dump() for point in challenge.points] == [{"x": 1139, "y": 729}]


def test_drag_source_coordinates_are_converted_to_paths():
    payload = {
        "source_coordinates": {"x": 765, "y": 545},
        "target_coordinates": {"x": 960, "y": 545},
    }
    text = json.dumps(payload)

    coerced = _coerce_payload_for_schema(
        _normalize_glm_payload(payload), ImageDragDropChallenge, text
    )
    challenge = ImageDragDropChallenge(**coerced)

    assert challenge.challenge_prompt == ""
    assert challenge.paths[0].start_point.model_dump() == {"x": 765, "y": 545}
    assert challenge.paths[0].end_point.model_dump() == {"x": 960, "y": 545}


def test_router_answer_single_select_is_converted_to_challenge_type():
    text = '{"answer":"image_label_single_select"}'

    payload = _coerce_payload_for_schema(
        _normalize_glm_payload(_extract_json_payload(text)), ChallengeRouterResult, text
    )
    challenge = ChallengeRouterResult(**payload)

    assert challenge.challenge_prompt == ""
    assert challenge.challenge_type.value == "image_label_single_select"


def test_router_drag_multi_alias_matches_current_schema_enum():
    text = '{"answer":"image_drag_multi"}'

    payload = _coerce_payload_for_schema(
        _normalize_glm_payload(_extract_json_payload(text)), ChallengeRouterResult, text
    )
    challenge = ChallengeRouterResult(**payload)

    assert challenge.challenge_prompt == ""
    assert challenge.challenge_type.value == "image_drag_multi"


@pytest.mark.parametrize(
    ("schema", "answer", "contract_fragment"),
    [
        (
            ImageAreaSelectChallenge,
            {"challenge_prompt": "prompt", "points": [{"x": 1, "y": 2}]},
            '"points":[{"x":0,"y":0}]',
        ),
        (
            ImageDragDropChallenge,
            {
                "challenge_prompt": "prompt",
                "paths": [{"start_point": {"x": 1, "y": 2}, "end_point": {"x": 3, "y": 4}}],
            },
            '"paths":[{"start_point":{"x":0,"y":0}',
        ),
        (
            ImageBinaryChallenge,
            {"challenge_prompt": "prompt", "coordinates": [{"box_2d": [0, 0]}]},
            '"coordinates":[{"box_2d":[0,0]}]',
        ),
        (
            ImageBboxChallenge,
            {
                "challenge_prompt": "prompt",
                "bounding_boxes": {
                    "top_left_x": 1,
                    "top_left_y": 2,
                    "bottom_right_x": 3,
                    "bottom_right_y": 4,
                },
            },
            '"bounding_boxes":{"top_left_x":0,"top_left_y":0',
        ),
        (
            ChallengeRouterResult,
            {"challenge_prompt": "prompt", "challenge_type": "image_drag_multi"},
            '"image_label_single_select"',
        ),
    ],
)
def test_compact_output_contracts_are_schema_compatible(schema, answer, contract_fragment):
    contract = _structured_output_contract(schema)
    parsed = _parse_glm_response(json.dumps(answer), schema)

    assert contract is not None
    assert '"$defs"' not in contract
    assert '"properties"' not in contract
    assert contract_fragment in contract
    assert parsed is not None
