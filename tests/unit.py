from .tools import unitOperationsAMRest
from pullgerAuthJWT.tests import unit as unitAuthJWT
from rest_framework.test import APITestCase

class Test_000_REST(APITestCase):

    def setUp(self):
        unitAuthJWT.UnitOperations.CreateUser(self)
        unitAuthJWT.UnitOperations.GetToken(self)

    def test_001_Smoke(self):
        resultGet = self.client.get("/pullgerAM/api/ping/")
        self.assertEqual(resultGet.status_code, 200, "General API Critical error.")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        resultGet = self.client.get("/pullgerAM/api/pingAuth/")

        self.assertEqual(resultGet.status_code, 200, "General API Critical error with authentification.")

    def test_000_AccountAddforLinkedIN(self):
        unitOperationsAMRest.add_account_for_linkedin(self)