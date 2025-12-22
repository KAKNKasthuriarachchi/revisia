def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def format_chat_message(chat):
    if chat["role"] == "user":
        return f"**You:** {chat['message']}"
    else:
        return f"**Assistant:** {chat['message']}"


def sanitize_input(user_input):
    import html
    return html.escape(user_input)