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
        """
        Генерирует случайный boolean.

        :return: Случайный bool.
        """
        return self.faker.boolean()


    def filtration_type(self) -> str:
        """
        Генерирует случайный filtration_type.

        :return: Случайный "pass"/"miss".
        """
        return self.faker.random_element(["pass","miss"])


    def port_name(self) -> str:
        """
        Генерирует случайный port_name.

        :return: Случайное имя сконфигурированного порта.
        """
        return self.faker.color_name()


fake = Fake(faker=Faker(locale='ru_Ru'))
print(fake.filtration_type())