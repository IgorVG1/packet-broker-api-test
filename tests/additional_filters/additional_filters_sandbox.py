import requests

from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema
from config import settings


def delete_additional_filters():
    public_users_client = get_authentication_client()
    authentication_request = LoginRequestSchema()
    authentication_response = public_users_client.login(request=authentication_request)

    delete_additional_filters_response = requests.delete(url=f'{settings.http_client.client_url}/api/additional_filters/',
                                                         headers={"Authorization": f"Bearer {authentication_response.access}"},
                                                         json=[
                                                             {
                                                                 "direction": "Src+Dst",
                                                                 "logicGroup": 1,
                                                                 "value": "1.1.1.1",
                                                                 "type": "pass"
                                                             }
                                                         ])

    print()
    print(delete_additional_filters_response.status_code)


# delete_additional_filters()