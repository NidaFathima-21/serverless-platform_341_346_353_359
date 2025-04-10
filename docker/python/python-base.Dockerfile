FROM python:3.11-slim
WORKDIR /app
COPY entrypoint.py .
CMD ["sleep", "infinity"]
