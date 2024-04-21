def truncate_text(text: str, length: int = 30) -> str:
    """
    Truncates the given text to a maximum length of `length` characters.
    - If the `text` is longer than `length`, it truncates the text and appends
      '...' to the truncated text.
    - If the `text` is shorter than `length`, it pads the text with spaces to
      make it `length` characters long.

    Args:
        text (str): The text to be truncated.
        length (int, optional): The maximum length of the truncated text.
            Defaults to 30.

    Returns:
        str: The truncated text.
    """
    shortend = text[: length - 3]
    return f"{shortend}..." if len(text) > length else text.ljust(length)
