# FastAPI Social Posts API

FastAPI backend with JWT auth, PostgreSQL, SQLAlchemy, pytest, Ruff, and AWS/Terraform deployment scaffolding.

## Quick Start

```bash
# 1) Install dependencies
uv sync --dev

# 2) Run tests
uv run pytest -q

# 3) Run lint checks
uv run ruff check app tests

# 4) Start API
uv run uvicorn app.main:app --reload

# 5) Bootstrap Terraform remote state (one-time)
cd terraform/envs/bootstrap && terraform init && terraform plan
```

## First Day Setup (Copy/Paste)

```bash
# 1) Install deps and verify app
uv sync --dev
uv run ruff check app tests
uv run pytest -q

# 2) Bootstrap Terraform remote state (one-time)
cd terraform/envs/bootstrap
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
terraform output
```

After `terraform output`, set these in GitHub repository environment `network`:

- `AWS_NETWORK_ROLE_ARN`
- `AWS_REGION`
- `PROJECT_NAME`
- `VPC_CIDR`
- `PUBLIC_SUBNET_CIDRS`
- `PRIVATE_SUBNET_CIDRS`
- `AVAILABILITY_ZONES`
- `TF_STATE_BUCKET` (from bootstrap output `state_bucket_name`)
- `TF_LOCK_TABLE` (from bootstrap output `lock_table_name`)

Then run GitHub Action `.github/workflows/network-provision.yml` with:

- `action=plan` and `env=dev`
- review and approve `network` environment gate
- rerun with `action=apply` and `env=dev`

## Post-Network Next Step

After network apply succeeds:

- Confirm outputs exist in remote state at `network/dev/terraform.tfstate`
- Push changes to `main` that include app infrastructure or manifests
- Trigger app deployment workflows:
	- `.github/workflows/deploy-eks.yml` for EKS/RDS/ECR and Kubernetes rollout
	- `.github/workflows/deploy-lambda.yml` for Lambda package and code update

Tip: run EKS deployment first so the core API and database are available, then deploy Lambda/API Gateway integration.

## Highlights

- User registration and login (OAuth2 password flow)
- CRUD for posts
- Vote and unvote posts
- Protected routes with bearer JWT tokens
- Terraform modules for VPC, EKS, RDS, ECR, Lambda, and API Gateway
- Isolated network pipeline and bootstrap workflow for remote state infrastructure

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL via psycopg
- Pydantic v2
- python-jose for JWT
- passlib + bcrypt for password hashing
- uv for dependency and environment management
- pytest + Ruff
- Terraform + GitHub Actions + AWS OIDC

## Repository Layout

```text
.
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── oauth2.py
│   ├── schemas.py
│   ├── utils.py
│   └── routers/
├── tests/
├── terraform/
│   ├── envs/
│   │   ├── bootstrap/
│   │   ├── network/
│   │   └── app/
│   └── modules/
├── k8s/
├── lambda/
├── .github/workflows/
├── pyproject.toml
├── Makefile
└── pytest.ini
```

## Python Project Setup

Project metadata now lives at the repository root in `pyproject.toml`.

Install dependencies:

```bash
uv sync --dev
```

Run quality checks:

```bash
uv run ruff check app tests
uv run pytest -q
```

Useful shortcuts:

```bash
make install
make lint
make test
make ci
```

## Run API Locally

Run from repository root:

```bash
uv run uvicorn app.main:app --reload
```

Docs:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Environment Variables

Create `.env` in repository root:

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password
DATABASE_NAME=your_db_name
DATABASE_USERNAME=your_db_user
SECRET_KEY=your_random_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## API Summary

Public:

- `GET /`
- `POST /users/`
- `GET /users/{id}`
- `POST /login`

Protected:

- `GET /posts/`
- `GET /posts/{id}`
- `POST /posts/`
- `PUT /posts/{id}`
- `DELETE /posts/{id}`
- `POST /vote/`

Vote direction values:

- `1` = add vote
- `0` = remove vote

## Infrastructure Workflow

### 1. Bootstrap remote state (one time per AWS account/environment)

Creates S3 state bucket and DynamoDB lock table using local backend:

```bash
cd terraform/envs/bootstrap
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
terraform output
```

Use outputs for GitHub secrets:

- `TF_STATE_BUCKET`
- `TF_LOCK_TABLE`

### 2. Provision network (VPC only)

Workflow: `.github/workflows/network-provision.yml`

- Trigger manually with `action=plan` first
- Approve protected `network` environment
- Then run `action=apply`

Required `network` environment secrets include:

- `AWS_NETWORK_ROLE_ARN`
- `AWS_REGION`
- `PROJECT_NAME`
- `VPC_CIDR`
- `PUBLIC_SUBNET_CIDRS`
- `PRIVATE_SUBNET_CIDRS`
- `AVAILABILITY_ZONES`
- `TF_STATE_BUCKET`
- `TF_LOCK_TABLE`

### 3. Provision app stack

After network is applied, app workflows consume remote state for EKS/RDS/Lambda/API Gateway.

## Troubleshooting

Relative import error:

- Cause: running module from inside `app/`
- Fix: run from repo root using `uv run uvicorn app.main:app --reload`

Terraform version mismatch:

- Use `tfenv` and pin via `.terraform-version`
- Current pinned version: `1.14.7`

