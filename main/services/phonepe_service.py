import uuid

from django.conf import settings


def generate_merchant_order_id(prefix="TB"):
    """
    Generate a unique merchant order ID for PhonePe.
    """

    unique_id = uuid.uuid4().hex[:20].upper()

    return f"{prefix}_{unique_id}"


def get_phonepe_config():
    """
    Return PhonePe configuration from Django settings.

    Credentials can be added later through environment variables.
    """

    return {
        "client_id": getattr(
            settings,
            "PHONEPE_CLIENT_ID",
            "",
        ),
        "client_secret": getattr(
            settings,
            "PHONEPE_CLIENT_SECRET",
            "",
        ),
        "client_version": getattr(
            settings,
            "PHONEPE_CLIENT_VERSION",
            1,
        ),
        "environment": getattr(
            settings,
            "PHONEPE_ENV",
            "SANDBOX",
        ),
    }


def validate_phonepe_config():
    """
    Check whether required PhonePe credentials are available.
    """

    config = get_phonepe_config()

    missing = []

    if not config["client_id"]:
        missing.append("PHONEPE_CLIENT_ID")

    if not config["client_secret"]:
        missing.append("PHONEPE_CLIENT_SECRET")

    if missing:
        return {
            "valid": False,
            "missing": missing,
        }

    return {
        "valid": True,
        "missing": [],
    }