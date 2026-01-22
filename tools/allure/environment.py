from config import settings
import platform, sys


def create_allure_environment_file():

    items = [f'{key}={value}' for key, value in settings.model_dump().items()]
    items.append(f'os_info={platform.system()}, {platform.release()}')
    items.append(f'python_version={sys.version}')

    properties = '\n'.join(items)

    # Открываем файл ./allure-results/environment.properties на запись
    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w+') as f:
        f.write(properties)