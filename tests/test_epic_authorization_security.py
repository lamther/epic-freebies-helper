import os

os.environ.setdefault("EPIC_EMAIL", "test@example.invalid")
os.environ.setdefault("EPIC_PASSWORD", "test-password")
os.environ.setdefault("GEMINI_API_KEY", "test-api-key")

from services.epic_authorization_service import EpicAuthorization


def test_cloudflare_security_page_is_not_treated_as_hcaptcha():
    page_text = "One more step\nVerify you are human\nCloudflare\nPrivacy - Help"

    assert EpicAuthorization._is_cloudflare_security_check_text(page_text)


def test_generic_hcaptcha_prompt_is_not_treated_as_cloudflare():
    assert not EpicAuthorization._is_cloudflare_security_check_text(
        "Please complete a security check to continue"
    )
