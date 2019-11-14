from factory import DictFactory, Sequence


class UserFactory(DictFactory):
    email = Sequence(lambda n: f"person{0}@example.com".format(n))
    password = Sequence(lambda n: f"password{0}".format(n))
