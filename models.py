# models.py
import google.generativeai as genai

def get_model(model_name: str) -> genai.GenerativeModel:
    """
    Gets a GenerativeModel instance by name.

    Args:
        model_name (str): The name of the model.

    Returns:
        genai.GenerativeModel: The model instance.
    """
    return genai.GenerativeModel(model_name=model_name)