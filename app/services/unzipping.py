import asyncio
import os

import patoolib

from app.core import settings
from app.core.db import get_async_session


async def load_file_to_database(file_path: str, solution_id: int):
    # TODO: Сохранение файлов в базу
    session = get_async_session().__anext__()
    with open(file_path, "r") as file:
        lines = file.readlines()

    content = "".join([line if line.endswith("\n") else line + "\n" for line in lines])
    name = os.path.basename(file_path)
    print(name)


async def dir_traversal(path: str, solution_id: int):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        item_name: str = os.path.basename(item_path)
        if item_name.startswith(".") or "pycache" in item_name:
            continue

        if os.path.isdir(item_path):
            await dir_traversal(
                item_path,
                solution_id,
            )
        else:
            await load_file_to_database(
                item_path,
                solution_id,
            )

    patoolib.shutil.rmtree(path)


async def extract(archve_name: str, solution_id: int) -> bool:
    project_dir = os.getcwd()
    temp_files_dir = os.path.join(project_dir, "temp_folder")

    try:
        patoolib.extract_archive(
            archive=settings.archives_save_path + archve_name,
            outdir=temp_files_dir,
        )
    except patoolib.util.PatoolError as e:
        print("Ошибка разархивации архива:", str(e))
        return False

    await dir_traversal(
        path=temp_files_dir,
        solution_id=solution_id,
    )
    return True


asyncio.run(extract("test.zip", 1))
