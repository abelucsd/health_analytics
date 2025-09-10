from core.exceptions import AppError


class HealthMetricsAlreadyExists(AppError):
  def __init__(self, entity_name: str, entity_id: int):
    message = f"{entity_name} with ID {entity_id} already exists"
    super().__init__(message, status_code=400)

class HealthMetricsNotFoundError(AppError):
  def __init__(self, entity_id: int):
    message = f"Health Metrics ID {entity_id} not found."
    super().__init__(message, status_code=400)

class InvalidGenderError(AppError):
  def __init__(self, invalid_gender: str):
    message = f"Health Metrics gender {invalid_gender} is invalid."
    super().__init__(message, status_code=400)
