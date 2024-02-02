FROM python:3.11

RUN apt-get update && \
  apt-get install -y pkg-config default-libmysqlclient-dev --no-install-recommends \
  build-essential && \
  pip install --no-cache-dir poetry 

RUN poetry config virtualenvs.create false

WORKDIR /app
COPY ./pyproject.toml ./
RUN poetry install 

COPY ./ ./

RUN chmod a+x migrations.sh
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
