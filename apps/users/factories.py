import factory

from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ["username"]

    username = factory.Faker("user_name")
    full_name = factory.Faker("name")
    email = factory.Faker("email")
    avatar = factory.django.ImageField()
