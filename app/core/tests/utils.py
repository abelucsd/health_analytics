from django.test import Client

json_content_type = "application/json"
dummy_token = "Bearer test"


class AuthenticatedClient(Client):
  def __init__(self, client: Client):
    self.client = client

  def post(self, *args, **kwargs):
    return self.client.post(
      headers={"Authorization": dummy_token},
      content_type=json_content_type,
      *args,
      **kwargs
    )
  

  def get(self, *args, **kwargs):
    return self.client.get(
      headers={"Authorization": dummy_token},
      content_type=json_content_type,
      *args,
      **kwargs
    )
  

  def put(self, *args, **kwargs):
    return self.client.put(
      headers={"Authorization": dummy_token},
      content_type=json_content_type,
      *args,
      **kwargs
    )
  

  def delete(self, *args, **kwargs):
    return self.client.delete(
      headers={"Authorization": dummy_token},
      content_type=json_content_type,
      *args,
      **kwargs
    )