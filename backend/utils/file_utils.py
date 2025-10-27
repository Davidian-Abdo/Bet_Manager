import os
from fastapi import UploadFile
import uuid

UPLOAD_DIR = "storage/uploads"

def save_file(file: UploadFile, project_id: int) -> str:
    ext = file.filename.split(".")[-1]
    filename = f"{project_id}_{uuid.uuid4()}.{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(file.file.read())
    return path

def delete_file(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)