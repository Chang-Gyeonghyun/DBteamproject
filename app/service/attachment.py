import mimetypes
from fastapi import Depends
from fastapi.responses import FileResponse
from app.entity.models import Attachment
from app.entity.repository.repository import RepositoryFactory
from app.utils.exceptions import CustomException, ExceptionEnum

class AttachmentService:
    def __init__(self, repository_factory: RepositoryFactory = Depends()):
        self.attachment_repository = repository_factory.get_attachment_repository()
    
    async def attachment_download(self, attachment_id: int) -> FileResponse:
        attachment: Attachment | None = await self.attachment_repository.get_attachment_by_id(attachment_id)
        if not attachment:
            raise CustomException(ExceptionEnum.ITEM_NOT_FOUND)
        
        mime_type, _ = mimetypes.guess_type(attachment.filePath)
        if not mime_type:
            mime_type = "application/octet-stream"
            
        return FileResponse(
            path=attachment.filePath,
            filename=attachment.fileName,
            media_type=mime_type
        )
