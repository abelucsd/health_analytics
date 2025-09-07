from ninja.errors import HttpError

class AppError(Exception):
  def __init__(self, message, status_code=400):
    self.message = message
    self.status_code = status_code
    super().__init__(message)

def app_error_handler(request, exc: AppError):
  return {"error": exc.message}, exc.status_code


class ValidationError(AppError):
  def __init__(self, message):    
    super().__init__(message, 404)

# # Usage in service.py
# def create_user(payload):
#   if not payload.email:
#     raise AppError("Email is required", 400)
