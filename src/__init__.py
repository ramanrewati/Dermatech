from src.config import MODEL


def is_valid_model(model_name: str) -> bool:
    return model_name in MODEL
