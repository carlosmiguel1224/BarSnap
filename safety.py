import re

def pre_parser(raw_response):
    """
    Strips markdown-style code fences and unwanted formatting from LLM output.
    This allows valid JSON to be parsed even if the LLM adds ```json ... ``` around it.
    """
    if not raw_response:
        return ""

    # Remove triple backticks and optional language hint (e.g., ```json)
    cleaned = re.sub(r"```(?:json)?", "", raw_response, flags=re.IGNORECASE)
    cleaned = cleaned.replace("```", "")

    return cleaned.strip()




def safe_json_parse(raw_output):
    import json

    if isinstance(raw_output, str):
        text = raw_output.strip()

        # Attempt auto-wrapping if it's a partial list
        if text.startswith("{") and not text.startswith("["):
            text = "[" + text.rstrip(",") + "]"

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            print("❌ Failed to parse JSON:", e)
            print("🧾 Offending content:", repr(text))
            return []
    elif isinstance(raw_output, list):
        return raw_output
    else:
        print("❌ Unexpected response type:", type(raw_output))
        return []




MEANINGLESS_WORDS = {
    "serve", "chilled", "refrigerate", "opened", "opening", "after",
    "shake", "mix", "blend", "pour", "drink", "bottle", "bottled",
    "vintner", "vintage", "alc", "alcohol", "alcoholic", "beverages",
    "contains", "gluten", "free", "warning", "general", "surgeon", "health",
    "problems", "volume", "vol", "government", "birth", "risk", "impair",
    "drive", "operate", "machinery", "net", "oz", "ml", "liter", "l", "size",
    "natural", "flavors", "premium", "classic", "quality", "smooth", "rich",
    "extra", "fine", "special", "imported", "original", "select", "crafted",
    "established", "est", "estd", "since", "www", "com"
}

def filter_meaningless_words(raw_tokens):
    cleaned_tokens = []

    for token in raw_tokens:
        if not isinstance(token, str):
            continue

        token_lower = token.strip().lower()

        # Remove if the whole token is meaningless (e.g., "chilled", "premium")
        if token_lower in MEANINGLESS_WORDS:
            continue

        # Otherwise, preserve the phrase
        cleaned_tokens.append(token.strip())

    return cleaned_tokens


def filter_meaningful_multiline_block(raw_tokens):
    for token in raw_tokens:
        if isinstance(token, str) and '\n' in token:
            lines = re.split(r'[\n\r]+', token)
            cleaned_lines = [
                line.strip()
                for line in lines
                if line.strip().lower() not in MEANINGLESS_WORDS and line.strip() != ''
            ]
            return cleaned_lines
    return []