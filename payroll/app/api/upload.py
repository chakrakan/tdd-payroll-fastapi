# project/app/api/upload.py


from fastapi import APIRouter, File, UploadFile

# from app.api import crud


router = APIRouter()


@router.post("/v1/upload", status_code=201)
async def upload_csv(file: UploadFile = File(...)) -> None:
    """Endpoint to upload file. UploadFile type creates a spooled memory
    to read fast and process better.

    Args:
        file (UploadFile, optional): [description]. Defaults to File(...).

    Returns:
        [type]: [description]
    """
    # content = await file.read()
    # print(content)
    return {
        "filename": file.filename,
        "extension": file.content_type,
    }
