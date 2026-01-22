import requests

from clients.additional_filters.additional_filters_client import get_private_users_client
from clients.additional_filters.additional_filters_schema import CreateAdditionalFiltersRequestSchema, \
    CreateAdditionalFiltersSchema, UpdateAdditionalFiltersRequestSchema
from clients.authentication_client.authentication_client import get_authentication_client
from clients.authentication_client.authentication_schema import LoginRequestSchema
from clients.private_http_builder import AuthenticationUserSchema


def create_additional_filters():
    authentication_user = AuthenticationUserSchema(username='admin',
                                                   password='Admin2012')
    private_users_client = get_private_users_client(user=authentication_user)
    create_additional_filters_request = CreateAdditionalFiltersRequestSchema(
        [
            CreateAdditionalFiltersSchema(direction='Src+Dst',
                                          group_id='1',
                                          ip='1.1.1.1',
                                          type="pass")
        ]
    )
    create_additional_filters_response = private_users_client.create_additional_filters_api(request=create_additional_filters_request)

    print()
    print(create_additional_filters_response.status_code)
    print(create_additional_filters_response.reason_phrase)

def test_create_additional_filters():
    pass


def update_additional_filters():
    authentication_user = AuthenticationUserSchema()
    private_users_client = get_private_users_client(user=authentication_user)
    update_additional_filters_request = UpdateAdditionalFiltersRequestSchema(logic_id='1',
                                                                             filterIPWhiteEnable=False,
                                                                             filterIPBlackEnable=False)
    update_additional_filters_response = private_users_client.update_additional_filters_api(request=update_additional_filters_request)

    print()
    print(update_additional_filters_response.status_code)
    print(update_additional_filters_response.reason_phrase)


def delete_additional_filters():
    public_users_client = get_authentication_client()
    authentication_request = LoginRequestSchema()
    authentication_response = public_users_client.login(request=authentication_request)

    delete_additional_filters_response = requests.delete(url='http://192.168.7.57/api/additional_filters/',
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


# create_additional_filters()
# update_additional_filters()
# delete_additional_filters()