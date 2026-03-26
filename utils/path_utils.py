def normalize_path(path: str) -> str:
    if not path:
        return "/"

    path = path.strip()

    if not path.startswith("/"):
        path = "/" + path

    if not path.endswith("/"):
        path += "/"

    while "//" in path:
        path = path.replace("//", "/")

    return path

def is_valid_path(path: str) -> bool:
    invalid_chars = ["\\", "//"]
    return not any(x in path for x in invalid_chars)
