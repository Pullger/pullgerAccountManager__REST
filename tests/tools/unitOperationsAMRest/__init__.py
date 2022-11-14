from rest_framework.test import APITestCase
from pullgerAccountManager.tests.tools import dataTemplatesAM


def add_account_for_linkedin(self: APITestCase):
    self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    LIA_Template = dataTemplatesAM.LinkedInAccount()
    LIA_Template['authorization'] = 'linkedin.general'

    resultGet = self.client.post('/pullgerAM/api/account/', LIA_Template)
    self.assertEqual(resultGet.status_code, 200, "General API Critical error with authentification.")
    uuidNew = resultGet.data['data']['uuid']
    self.assertEqual(len(uuidNew), 36, "incorrect uuid")

    resultGet = self.client.get("/pullgerAM/api/account/")
    self.assertEqual(resultGet.status_code, 200, "General API Critical error with authentification.")

    self.assertEqual(len(resultGet.data['data']), 1, "Incorrect ADD account.")

    for curAccount in resultGet.data['data']:
        self.assertEqual(curAccount['uuid'], uuidNew, 'Incorrect uuid in list.')
        self.assertEqual(LIA_Template['login'], curAccount['login'], 'Login information.')
        self.assertEqual(LIA_Template['authorization'], curAccount['authorization'], 'Login information.')
        self.assertEqual(True, bool(curAccount['active']), 'Incorrect value [active].')
        self.assertEqual(True, bool(curAccount['use']), 'Incorrect value [use].')
