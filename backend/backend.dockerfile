FROM python:3.11

WORKDIR /app/

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root --without dev

COPY ./scripts/ /

RUN chmod +x /start.sh /start-reload.sh

COPY ./ /app
ENV PYTHONPATH=/app

CMD ["/start.sh"]
