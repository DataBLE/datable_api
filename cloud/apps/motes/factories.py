import factory

from models import App, Location, Mote, GenderAction

class AppFactory(factory.DjangoModelFactory):
    FACTORY_FOR = App

    name = factory.Sequence(lambda n: 'App name {0}'.format(n))
    platform = 'ios'


class LocationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Location


class MoteFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Mote

    location = factory.SubFactory(LocationFactory)


class GenderActionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = GenderAction

    mote = factory.SubFactory(MoteFactory)
    app = factory.SubFactory(AppFactory)
