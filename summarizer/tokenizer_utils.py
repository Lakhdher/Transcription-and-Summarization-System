import tiktoken


def tokenize(text: str, model_name: str = "gpt-4-turbo"):
    """
    Tokenizes the input text using the tiktoken library.
    """
    # Try using a more general tokenizer if your model is not recognized
    if model_name == "llama-3.1-70b-versatile":
        encoding = tiktoken.get_encoding(
            "cl100k_base"
        )  # Default encoding for many models
    else:
        encoding = tiktoken.encoding_for_model(model_name)

    return encoding.encode(text)
