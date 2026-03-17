"""
Login Lambda handler — POST /login

Standalone stateless auth function that mirrors app/routers/auth.py.
Reads secrets at cold start from AWS Secrets Manager (cached for warm invocations).
Connects to the same RDS PostgreSQL instance used by the EKS-hosted FastAPI app.
"""

import json
import os
import boto3
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
import psycopg

# ── Secret caching (avoid Secrets Manager call on every warm invocation) ──────
_cached_secrets: dict | None = None

def _get_secrets() -> dict:
    global _cached_secrets
    if _cached_secrets:
        return _cached_secrets

    client = boto3.client("secretsmanager", region_name=os.environ["AWS_REGION"])
    response = client.get_secret_value(SecretId=os.environ["SECRET_NAME"])
    _cached_secrets = json.loads(response["SecretString"])
    return _cached_secrets


# ── DB helper ─────────────────────────────────────────────────────────────────
def _get_connection(secrets: dict):
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", 5432)),
        dbname=os.environ["DB_NAME"],
        user=secrets["db_username"],
        password=secrets["db_password"],
    )


# ── Password verify ───────────────────────────────────────────────────────────
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _verify_password(plain: str, hashed: str) -> bool:
    return _pwd_context.verify(plain, hashed)


# ── JWT creation ──────────────────────────────────────────────────────────────
def _create_token(user_id: int, secret_key: str, algorithm: str, expire_minutes: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=expire_minutes),
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)


# ── Response helpers ──────────────────────────────────────────────────────────
def _response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


# ── Handler ───────────────────────────────────────────────────────────────────
def handler(event: dict, context) -> dict:
    # API Gateway HTTP API sends body as a string
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return _response(400, {"detail": "Invalid JSON body"})

    email = body.get("username") or body.get("email")
    password = body.get("password")

    if not email or not password:
        return _response(422, {"detail": "username and password are required"})

    secrets = _get_secrets()

    try:
        with _get_connection(secrets) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT id, password FROM "Users" WHERE email = %s LIMIT 1',
                    (email,),
                )
                row = cur.fetchone()
    except Exception as exc:
        print(f"DB error: {exc}")
        return _response(500, {"detail": "Internal server error"})

    if not row or not _verify_password(password, row[1]):
        return _response(403, {"detail": "Invalid credentials"})

    token = _create_token(
        user_id=row[0],
        secret_key=secrets["secret_key"],
        algorithm=secrets.get("algorithm", "HS256"),
        expire_minutes=int(secrets.get("access_token_expire_minutes", 30)),
    )

    return _response(200, {"access_token": token, "token_type": "bearer"})
