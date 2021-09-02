from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from .models import Thing


class ThingFactory(DjangoModelFactory):

    name = FuzzyText(prefix="NAME_", length=10)

    class Meta:
        model = Thing
