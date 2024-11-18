FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip install poetry

#RUN pipx install poetry

#ENV PATH="/root/.local/bin:${PATH}"

RUN poetry install

RUN poetry run pytest

CMD ["poetry", "run", "python", "src/calculator/calculator.py"]


