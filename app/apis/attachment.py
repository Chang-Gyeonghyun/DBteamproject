from fastapi import APIRouter, Depends
from app.service.attachment import AttachmentService

router = APIRouter(prefix="/attachment", tags=["Attachment"])

@router.get("/download/{attachmentID}")
async def download_attachment(
    attachmentID: int,
    attachment_service: AttachmentService = Depends()
):
    return await attachment_service.attachment_download(attachmentID)