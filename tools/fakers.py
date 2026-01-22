from faker import Faker


class Fake:
    """
    Класс для генерации случайных тестовых данных с использованием библиотеки Faker.
    """
    def __init__(self, faker: Faker):
        self.faker = faker


    def ip(self) -> str:
        """
        Генерирует случайный IPv4.

        :return: Случайный IPv4.
        """
        return self.faker.ipv4()

    def boolean(self) -> bool:
        return self.faker.boolean()


fake = Fake(faker=Faker(locale='ru_Ru'))
print(fake.boolean())