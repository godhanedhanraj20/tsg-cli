from utils.path_utils import normalize_path, is_valid_path

def test_normalize_path():
    assert normalize_path(None) == "/"
    assert normalize_path("") == "/"
    assert normalize_path("anime/naruto") == "/anime/naruto/"
    assert normalize_path("/anime//naruto") == "/anime/naruto/"
    assert normalize_path("///anime//naruto///") == "/anime/naruto/"

def test_is_valid_path():
    assert is_valid_path("/anime/naruto/") == True
    assert is_valid_path("/anime//naruto") == False
    assert is_valid_path("anime\\naruto") == False
