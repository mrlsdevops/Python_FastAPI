import importlib

from fastapi import HTTPException


def test_create_and_verify_access_token(monkeypatch):
    monkeypatch.setenv("DATABASE_HOSTNAME", "localhost")
    monkeypatch.setenv("DATABASE_PORT", "5432")
    monkeypatch.setenv("DATABASE_PASSWORD", "dummy")
    monkeypatch.setenv("DATABASE_NAME", "dummy")
    monkeypatch.setenv("DATABASE_USERNAME", "dummy")
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")
    monkeypatch.setenv("ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

    oauth2 = importlib.import_module("app.oauth2")
    oauth2 = importlib.reload(oauth2)

    token = oauth2.create_access_token({"user_id": 123})
    credentials_exception = HTTPException(status_code=401, detail="bad credentials")
    token_data = oauth2.verify_access_token(token, credentials_exception)

    assert str(token_data.id) == "123"
