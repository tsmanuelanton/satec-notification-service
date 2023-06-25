from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from api.views.services import ServiceDetails
from rest_framework import status
from api.tests.views.util import create_conector, create_service, create_user, create_subscription, create_subscription_group
from api.serializers import SubscriptionGroupsSerializer
from api.views.subscription_groups import SubscriptionGroupsList

endpoint = "/v1/groups"

class TestGetSubscriptionGroups(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_autheticated_no_groups(self):
        '''Comprueba que se devuelve una lista vacía cuando no hay grupos'''

        user, token = create_user()

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
    
    def test_authenticated_groups_owned_and_not_owned(self):
        '''Comprueba que se devuelve sólo los'''

        user, token = create_user()
        service = create_service(user)
        group1 = create_subscription_group(service)
        group2 = create_subscription_group(service)

        another_user, _ = create_user()
        service_not_owned = create_service(another_user)
        # group_not_owned
        create_subscription_group(service_not_owned)

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)
        force_authenticate(request, user, token)

        # Llamamos a la vista
        response = SubscriptionGroupsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [SubscriptionGroupsSerializer(group1).data,
                                         SubscriptionGroupsSerializer(group2).data ])

    def test_not_authenticated(self):
        '''Comprueba que se lanza un error cuando el usuario no está autenticado'''

        # Apuntamos el endpoint con el método get
        request = self.factory.get(endpoint)

        # Llamamos a la vista
        response = SubscriptionGroupsList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."}
        )
    