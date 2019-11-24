from factory import DictFactory, Sequence


class UserFactory(DictFactory):
    username = Sequence(lambda n: f"username{0}".format(n))
    email = Sequence(lambda n: f"person{0}@example.com".format(n))
    password = Sequence(lambda n: f"password{0}".format(n))
