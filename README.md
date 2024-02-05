<h3>ReviewSite</h3>

## Установка
* Docker
    ```sh
    git clone https://github.com/milssky/review_site
    cd review_site
    docker compose up --build -d
    ```

* Если требуются миграции
    ```sh
    docker compose exec api alembic upgrade head 
    docker compose restart api
    ```

* Source
    ```sh
    git clone https://github.com/hikaary/ymcli
    cd ymcli 

    # Install python deps
    poetry install

    # Run app 
    uvicorn app.main:app --host 0.0.0.0 --port 80
    ```

## Документация
* 127.0.0.1/docs - OpenApi

