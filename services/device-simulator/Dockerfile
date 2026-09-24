FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /simulator
COPY services/device-simulator/simulator.py ./simulator.py

USER 10001
CMD ["python", "simulator.py"]
