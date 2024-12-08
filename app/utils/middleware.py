from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class RemoveEmptyFileMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.headers.get("content-type", "").startswith("multipart/form-data"):
            form = await request.form()
            
            cleaned_form = {}
            for key, value in form.items():
                if isinstance(value, str) and value == "":
                    cleaned_form[key] = None
                else:
                    cleaned_form[key] = value
        
            request._form = cleaned_form
        response = await call_next(request)
        return response
