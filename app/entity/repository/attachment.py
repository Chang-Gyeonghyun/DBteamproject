import os
from typing import List
from sqlalchemy import delete, select
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
        return

    async def delete_attachments_by_post_id(self, post_id: int):
        attachments = await self.session.scalars(
            select(Attachment.filePath).where(Attachment.postID == post_id)
        )
        file_paths = [attachment.filePath for attachment in attachments]

        await self.session.execute(
            delete(Attachment).where(Attachment.postID == post_id)
        )
        await self.session.commit()
        return file_paths
