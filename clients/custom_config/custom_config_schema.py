from pydantic import BaseModel, FilePath, Field

from config import settings


class UploadCustomConfigRequestSchema(BaseModel):
    """
    Описание структуры запроса на загрузка файла конфигурации.
    Attributes:
        config: str - required
    """
    # путь к файлу на локальной машине, который будет загружен
    config: FilePath = Field(default=settings.test_data.custom_config_json_file)