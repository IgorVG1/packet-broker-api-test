from faker import Faker


class Fake:
    """
    Класс для генерации случайных тестовых данных с использованием библиотеки Faker.
    """
    def __init__(self, faker: Faker):
        self.faker = faker


fake = Fake(faker=Faker(locale='ru_Ru'))