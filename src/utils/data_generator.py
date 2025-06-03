from faker import Faker


fake = Faker()


class DataGenerator:

    @staticmethod
    def generate_random_word():
        return fake.word()
