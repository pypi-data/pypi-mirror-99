import uuid
import json
from datetime import datetime, timedelta

from djangoldp.serializers import LDListMixin, LDPSerializer
from rest_framework.test import APITestCase, APIClient

from djangoldp_account.models import LDPUser


class SomethingTestCase(APITestCase):
    # Django runs setUp automatically before every test
    def setUp(self):
        # we set up a client, that allows us
        self.client = APIClient()
        LDListMixin.to_representation_cache.reset()
        LDPSerializer.to_representation_cache.reset()

    # we have custom set up functions for things that we don't want to run before *every* test, e.g. often we want to
    # set up an authenticated user, but sometimes we want to run a test with an anonymous user
    def setUpLoggedInUser(self, is_superuser=False):
        self.user = LDPUser(email='test@mactest.co.uk', first_name='Test', last_name='Mactest', username='test',
                            password='glass onion', is_superuser=is_superuser)
        self.user.save()
        # this means that our user is now logged in (as if they had typed username and password)
        self.client.force_authenticate(user=self.user)

    # we write functions like this for convenience - we can reuse between tests
    def _get_random_user(self):
        return LDPUser.objects.create(email='{}@test.co.uk'.format(str(uuid.uuid4())), first_name='Test',
                                      last_name='Test', username=str(uuid.uuid4()))

    def _get_context(self):
        return {
                '@vocab': "http://happy-dev.fr/owl/#",
                'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
                'ldp': "http://www.w3.org/ns/ldp#",
                'foaf': "http://xmlns.com/foaf/0.1/",
                'name': "rdfs:label",
                'acl': "http://www.w3.org/ns/auth/acl#",
                'permissions': "acl:accessControl",
                'mode': "acl:mode",
                'inbox': "http://happy-dev.fr/owl/#inbox",
                'object': "http://happy-dev.fr/owl/#object",
                'author': "http://happy-dev.fr/owl/#author",
                'account': "http://happy-dev.fr/owl/#account",
                'jabberID': "foaf:jabberID",
                'picture': "foaf:depiction",
                'firstName': "http://happy-dev.fr/owl/#first_name",
                'lastName': "http://happy-dev.fr/owl/#last_name",
                'isAdmin': "http://happy-dev.fr/owl/#is_admin"
            }

    def test_something(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()

        self.assertEqual(True, True)
