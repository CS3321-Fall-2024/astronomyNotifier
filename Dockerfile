FROM python:3.11-alpine

# Define build-time argument
ARG NASA_API

WORKDIR /app

COPY . .

RUN pip install poetry

RUN poetry install

RUN poetry run pytest

EXPOSE 5000

# Set environment variable to pass ARG at runtime (Optional)
ENV NASA_API=${NASA_API}

CMD ["poetry", "run", "python", "src/main.py"]
