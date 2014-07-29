from uuid import uuid4
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe

from djchoices import DjangoChoices, ChoiceItem
from geopy import geocoders

# Make sure south can see the geodjango fields
from south.modelsinspector import add_introspection_rules, allowed_fields
add_introspection_rules([], ["^django\.contrib\.gis"])


class Location(models.Model):
    '''Geo enabled location that has motes'''
    name = models.CharField(max_length=255, default='Default location')
    address = models.CharField(max_length=255, default='110 E 9th St')
    city = models.CharField(max_length=255, default='Los Angeles')
    state = models.CharField(default='CA', max_length=255)
    postal_code = models.CharField(default='90031', max_length=255,
            blank=True, null=True)
    point = models.PointField(blank=True, null=True, srid=4326,
            default='POINT(-118.255389 34.040589)') 

    objects = models.GeoManager()

    def __unicode__(self):
        return '%s - %s - %s' % (self.name, self.city, self.state)

    def save(self, *args, **kwargs):
        if not self.point:
            # Geocode the lat/lon
            addr = "%s, %s, %s %s" % (self.address, self.city, 
                    self.state, self.postal_code)
            g = geocoders.ArcGIS()
            real_addr, (lat, lon) = g.geocode(addr)
            self.point = Point(lon, lat)
        super(Location, self).save(*args, **kwargs)


class Mote(models.Model):
    '''Remote BLE device'''
    class Meta:
        unique_together = (('uuid', 'major', 'minor'),)

    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location)
    uuid = models.CharField(max_length=255, default=lambda:uuid4().hex)
    major = models.CharField(max_length=255, default=0)
    minor = models.CharField(max_length=255, default=0)
    rssi = models.FloatField(default=-100,
            validators=[MaxValueValidator(-1),MinValueValidator(-100)])
    active = models.BooleanField(default=True)
    repeat_interval = models.IntegerField(default=5,
            validators=[MaxValueValidator(60),MinValueValidator(0)],
            help_text='''Repeat interval in minutes.  Zero for do not repeat''')

    objects = models.GeoManager()

    def __unicode__(self):
        if self.name:
            return self.name
        return "%s-%s-%s" % (self.uuid, self.major, self.minor)


class App(models.Model):
    '''Application allowed to access service with the BLE mote SDK'''
    class Meta:
        unique_together = (('identifier', 'platform'),)

    class Platform(DjangoChoices):
        ios = ChoiceItem('ios')
        android = ChoiceItem('android')

    name = models.CharField(max_length=255)
    # iOS BundleID, or android packageName
    identifier = models.CharField(max_length=255)
    platform = models.CharField(max_length=255, choices=Platform.choices)

    objects = models.GeoManager()

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.platform)

class GenderAction(models.Model):
    class TypeChoices(DjangoChoices):
        text = ChoiceItem('text')
        image = ChoiceItem('image')
        video = ChoiceItem('video')
        tv_video = ChoiceItem('tv-video')
        tv_image = ChoiceItem('tv-image')

    class GenderChoices(DjangoChoices):
        male = ChoiceItem('male')
        female = ChoiceItem('female')

    mote = models.ForeignKey(Mote)
    app = models.ForeignKey(App)
    gender = models.CharField(max_length=255, choices=GenderChoices.choices)
    action_type = models.CharField(max_length=255, choices=TypeChoices.choices)
    question = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    objects = models.GeoManager()



class Sighting(models.Model):
    mote = models.ForeignKey(Mote)
    app = models.ForeignKey(App)
    date = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=255, default=lambda:uuid4().hex)
    message = models.TextField(blank=True, null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return '%s - %s' % (self.app, self.date)
