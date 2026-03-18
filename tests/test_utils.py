from app import utils


def test_hash_creates_different_value_from_plain_text():
    plain = "super-secret"
    hashed = utils.hash(plain)

    assert hashed != plain
    assert isinstance(hashed, str)


def test_verify_accepts_valid_password_and_rejects_invalid_password():
    plain = "correct-password"
    hashed = utils.hash(plain)

    assert utils.verify(plain, hashed) is True
    assert utils.verify("wrong-password", hashed) is False
