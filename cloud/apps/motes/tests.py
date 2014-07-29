import json
from django_webtest import WebTest
from django.core.urlresolvers import reverse

from factories import AppFactory, MoteFactory, GenderActionFactory
from models import Sighting


class ApiTestCase(WebTest):
    def setUp(self):
        self.ios_app = AppFactory(platform='ios', identifier='com.foo.bar')
        self.mote = MoteFactory()
        self.action = GenderActionFactory(app=self.ios_app, 
                mote=self.mote, gender='male', action_type='text',
                question='foo', value='bar')

class DiscoverAndConfirmTestCase(ApiTestCase):
    def setUp(self):
        super(DiscoverAndConfirmTestCase, self).setUp()
        self.discover_url = reverse('mote-discovered')
        self.confirm_url = reverse('mote-confirm')

    def test_discover_invalid_mote(self):
        # make sure there's no sightings
        self.assertEqual(Sighting.objects.count(), 0)
        post_data = {'app': self.ios_app.identifier,
                'platform': self.ios_app.platform,
                'gender': 'male',
                'major': self.mote.major, 'minor': self.mote.minor, 
                'mote': 'invalid mote'}
        # Expect a 400 error
        res = self.app.post(self.discover_url, params=post_data, status=400)
        # make sure there's still no sightings
        self.assertEqual(Sighting.objects.count(), 0)

    def test_discover_valid(self):
        # Make sure there's no sightings
        self.assertEqual(Sighting.objects.count(), 0)
        post_data = {'app': self.ios_app.identifier,
                'platform': self.ios_app.platform,
                'gender': self.action.gender,
                'major': self.mote.major, 'minor': self.mote.minor, 
                'mote': self.mote.uuid}
        res = self.app.post(self.discover_url, params=post_data)
        data = json.loads(res.content)
        # Make sure there's 1 sighting
        self.assertEqual(Sighting.objects.count(), 1)
        # Make sure there was a sighting uuid returned
        self.assertTrue(data.get('uuid', False))
        # Make sure there's data in the message
        sighting = Sighting.objects.get()
        message = json.loads(sighting.message)
        self.assertEqual(message['confirmed'], False)
        return data

    def test_confirm_invalid_uuid(self):
        # Do not discover first
        post_data = {'app': self.ios_app.identifier,
                'platform': self.ios_app.platform,
                'gender': self.action.gender,
                'uuid': 'invalid uuid',
                'major': self.mote.major, 'minor': self.mote.minor, 
                'mote': self.mote.uuid}
        res = self.app.post(self.confirm_url, params=post_data, status=400)

    def test_confirm(self):
        data = self.test_discover_valid()  # Discover for the first time
        uuid = data['uuid']
        post_data = {'app': self.ios_app.identifier,
                'platform': self.ios_app.platform,
                'gender': self.action.gender,
                'uuid': uuid,
                'major': self.mote.major, 'minor': self.mote.minor, 
                'mote': self.mote.uuid}
        res = self.app.post(self.confirm_url, params=post_data)
        data = json.loads(res.content)
        # Make sure there was no sighting uuid returned
        self.assertFalse('uuid' in data)
        # Make sure the message data was updated
        sighting = Sighting.objects.get()
        message = json.loads(sighting.message)
        self.assertEqual(message['confirmed'], True)
        self.assertTrue('confirmed_time' in message)
