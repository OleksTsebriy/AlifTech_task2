import os


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    else:
        return False


APP_CONFIG = {
    "SERVER_HOST": os.getenv("SERVER_HOST", "0.0.0.0"),
    "SERVER_PORT": int(os.getenv("SERVER_PORT", 7777)),
    "DEBUG": str2bool(os.getenv("DEBUG", False)),
}

REQUIRED_FEATURES = ["gender", "age", "credit_sum", "credit_month", "score_shk", "monthly_income"]


SCHEMA = {
    "gender": (str, None),
    "age": (int, None),
    "marital_status": (str, "MAR"),
    "job_position": (str, "SPC"),
    "credit_sum": (float, None),
    "credit_month": (int, None),
    "tariff_id": (str, "1.6"),
    "score_shk": (float, None),
    "education": (str, "GRD"),
    "living_region": (str, "undefined"),
    "monthly_income": (int, None),
    "credit_count": (int, 0),
    "overdue_credit_count": (int, 0),
}
