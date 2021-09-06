import datetime

from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDecimal, FuzzyInteger, FuzzyText
from faker import Faker

from .models import Property, Thing

fake = Faker()


class ThingFactory(DjangoModelFactory):

    name = FuzzyText(prefix="NAME_", length=10)
    number = FuzzyInteger(low=0, high=1000)
    decimal_number = FuzzyDecimal(low=0, precision=2)
    timestamp = fake.date()

    class Meta:
        model = Thing


class PropertyFactory(DjangoModelFactory):
    name = FuzzyText(prefix="NAME_", length=10)
    creator = None

    class Meta:
        model = Property
