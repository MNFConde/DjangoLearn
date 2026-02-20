from blogs.tests.stub.stub_faker import FactoryFaker

test_faker = FactoryFaker()


def test_factory_faker():
    assert test_faker.name() == "Norma Fisher"
