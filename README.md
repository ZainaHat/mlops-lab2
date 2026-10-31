# Lab 2 — Customer Churn API

[![CI](https://github.com/ZainaHat/mlops-lab2/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ZainaHat/mlops-lab2/actions/workflows/ci.yml)

A Logistic Regression model from the AI381 Lab 1 Starter Kit,
served through FastAPI with validated inputs.

## Start with one command

Requirements: Docker Engine and Docker Compose v2.
Run from the repository root, with port 8000 available:

```bash
docker compose up -d --build --wait
```

This builds the image, trains the model, starts the service,
and waits for the container health check to pass.

Interactive API documentation: http://localhost:8000/docs

## Health check

```bash
curl -fsS http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## Prediction

```bash
curl -fsS -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"tenure_months":5,"monthly_charges":89.9,"contract":"month-to-month","internet_service":"fiber","support_calls":3}'
```

The response contains `churn_probability`, between 0 and 1.
Missing fields, invalid categories, negative values, and extra
fields are rejected with HTTP 422.

## Local development and tests

Using Python 3.12:

```bash
python3.12 -m venv .venv312
source .venv312/bin/activate
python -m pip install -r requirements.txt
python -m src.train.train
python -m ruff check src tests
python -m pytest -v
```

The 12 test cases cover health, model loading, the API response
contract, missing fields, invalid inputs, zero values, and
deterministic predictions.

## Docker

The multi-stage Dockerfile trains the model during the build.
The base image is pinned by digest. The runtime uses UID 10001
and includes a HEALTHCHECK.

## CI and publishing

GitHub Actions runs lint, training, tests, image building, and
Trivy scanning on pull requests and pushes to the development branch.

Trivy blocks fixable HIGH and CRITICAL vulnerabilities.
Unfixed vulnerabilities are excluded from this blocking policy.

On main, after successful checks, the image is pushed to:

```text
ghcr.io/zainahat/mlops-lab2:<full-commit-sha>
```

The published image digest is recorded in the Actions run summary.
All referenced GitHub Actions are pinned to full commit SHAs.
The Trivy container image is pinned by digest.

Main requires a pull request and successful checks before merging.

## Stop the service

```bash
docker compose down
```

## Data source

AI381 Lab 1 Starter Kit: churn_v1.csv.
