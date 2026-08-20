import pytest
from bildock_lib.security import create_access_token, decode_token, hash_password, verify_password


def test_password_hash_and_verify():
    hashed = hash_password("qwerty")
    assert verify_password("qwerty", hashed)
    assert not verify_password("wrong", hashed)


def test_token_roundtrip():
    token = create_access_token(42)
    assert decode_token(token)["sub"] == "42"


def test_invalid_token():
    with pytest.raises(ValueError):
        decode_token("not-a-token")
