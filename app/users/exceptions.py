from core.exceptions import AppError


class UserAlreadyExists(AppError):
  def __init__(self, entity_name: str, entity_id: int):
    message = f"{entity_name} with ID {entity_id} already exists"
    super().__init__(message, status_code=400)

class UserNotFoundError(AppError):
  def __init__(self, entity_id: int):
    message = f"User ID {entity_id} not found."
    super().__init__(message, status_code=400)

class InvalidRoleError(AppError):
  def __init__(self, invalid_role: str):
    message = f"User role {invalid_role} is invalid."
    super().__init__(message, status_code=400)



# api = NinjaAPI()

# class ServiceUnavailableError(Exception):
#     pass


# # initializing handler

# @api.exception_handler(ServiceUnavailableError)
# def service_unavailable(request, exc):
#     return api.create_response(
#         request,
#         {"message": "Please retry later"},
#         status=503,
#     )


# # some logic that throws exception

# @api.get("/service")
# def some_operation(request):
#     if random.choice([True, False]):
#         raise ServiceUnavailableError()
#     return {"message": "Hello"}