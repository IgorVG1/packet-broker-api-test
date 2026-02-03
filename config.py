from typing import Self
from pydantic import BaseModel, HttpUrl, DirectoryPath, FilePath, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class HTTPClientConfig(BaseModel):
    url: HttpUrl
    timeout: float

    @property
    def client_url(self):
        return str(self.url)        # pydantic.HttpUrl автоматически добавляет завершающий /


class UserDataConfig(BaseModel):
    username: str
    password: str


class TestDataConfig(BaseModel):
    custom_config_json_file: FilePath
    invalid_custom_config_json_file: FilePath


class XdistGroupNamesConfig(BaseModel):
    """
    Добавляем маркировку @pytest.mark.xdist_group(name="__name__") к нашим тестам, чтобы они выполнялись в одном потоке.

    Attributes:
        negative_tests: str - Имя потока (xdist_group) при параллельном запуске тестов
    """
    negative_tests: str = Field(description='Поток авто-тестов для проверки негативных сценариев')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='allow',
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='.')

    xdist_group_names: XdistGroupNamesConfig
    test_data: TestDataConfig
    user_data: UserDataConfig
    http_client: HTTPClientConfig
    allure_results_dir: DirectoryPath

    @classmethod
    def initialize(cls) -> Self:
        allure_results_dir = DirectoryPath('./allure-results')
        allure_results_dir.mkdir(exist_ok=True)

        return Settings(allure_results_dir=allure_results_dir)


settings = Settings.initialize()    # Инициализируем настройки с созданием папки allure_results при условии ее отсутствия