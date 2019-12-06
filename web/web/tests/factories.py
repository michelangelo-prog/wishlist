from factory import DictFactory, Sequence


class UserFactory(DictFactory):
    username = Sequence(lambda n: f"username{n}")
    email = Sequence(lambda n: f"person{n}@example.com")
    password = Sequence(lambda n: f"password{n}")
