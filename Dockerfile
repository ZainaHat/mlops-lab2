FROM python@sha256:e697c81897302a4c4333bade000d98038fbb21eb064f8ee1fd42d02ebcd9d337 AS builder

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY churn_v1.csv .
RUN python -m src.train.train

FROM python@sha256:e697c81897302a4c4333bade000d98038fbb21eb064f8ee1fd42d02ebcd9d337 AS runtime

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid appuser --no-create-home appuser

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app/src ./src
COPY --from=builder /app/artifacts ./artifacts

USER 10001:10001

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; r = urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3); assert r.status == 200"

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
