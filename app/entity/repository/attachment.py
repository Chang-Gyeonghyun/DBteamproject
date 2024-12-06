import os
from typing import List
from fastapi import Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_database
from app.entity.models import Attachment

class AttachmentRepository:
    def __init__(self, session: AsyncSession = Depends(get_database)):
        self.session = session
        
    async def create_attachment(self, post_id: int, files: List[UploadFile]):
        for file in files:
            new_attachment = Attachment(
                postID=post_id,
                fileName=file.filename,
                filePath=f"./uploads/attachments/{file.filename}",
            )
            self.session.add(new_attachment)
        await self.session.commit()
    