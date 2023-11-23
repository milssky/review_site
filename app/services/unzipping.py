import asyncio
import os

import patoolib
from fastapi.datastructures import UploadFile

from app.core.db import AsyncSessionLocal
from app.crud import solution_crud


async def load_file_to_database(
    file_path: str,
    solution_id: int,
):
    with open(file_path, "r") as file:
        lines = file.readlines()

    content = "".join([line if line.endswith("\n") else line + "\n" for line in lines])
    name = os.path.basename(file_path)
    async with AsyncSessionLocal() as session:
        await solution_crud.create_file(
            name=name,
            content=content,
            solution_id=solution_id,
            session=session,
        )


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


async def extract(
    file: UploadFile,
    solution_id: int,
) -> bool:
    project_dir = os.getcwd()
    temp_files_dir = os.path.join(project_dir, "temp")
    if not os.path.exists(temp_files_dir):
        os.makedirs(temp_files_dir)

    assert file.filename is not None

    archive_path = os.path.join(temp_files_dir, file.filename)
    with open(archive_path, "wb") as output:
        archive = await file.read()
        output.write(archive)
    try:
        patoolib.extract_archive(
            archive=archive_path,
            outdir=temp_files_dir,
        )
    except patoolib.util.PatoolError as e:
        print("Ошибка разархивации архива:", str(e))
        return False

    os.remove(archive_path)

    loop = asyncio.get_running_loop()
    loop.create_task(
        dir_traversal(
            path=temp_files_dir,
            solution_id=solution_id,
        )
    )
    return True
