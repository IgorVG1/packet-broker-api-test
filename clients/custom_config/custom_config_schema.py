from pydantic import BaseModel, FilePath, Field, ConfigDict

from config import settings


class UploadCustomConfigRequestSchema(BaseModel):
    """
    Описание структуры запроса на загрузка файла конфигурации.
    Attributes:
        config: str - required
    """
    # путь к файлу на локальной машине, который будет загружен
    config: FilePath = Field(default=settings.test_data.custom_config_json_file)




class GetSwitchInfoResponseSchema(BaseModel):
    """
    Описание структуры ответа на получение системной информации коммутатора.
    Attributes:
        sn: str
        uptime: str
        packet_broker_version (packetBrokerVersion): str
        packet_broker_web_server_version (packetBrokerWebServerVersion): str
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    sn: str
    uptime: str
    packet_broker_version: str              = Field(alias="packetBrokerVersion")
    packet_broker_web_server_version: str   = Field(alias="packetBrokerWebServerVersion")