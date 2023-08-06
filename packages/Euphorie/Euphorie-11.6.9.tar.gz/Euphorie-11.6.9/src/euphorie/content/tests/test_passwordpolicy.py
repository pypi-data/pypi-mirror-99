# coding=utf-8
from euphorie.content import MessageFactory as _
from euphorie.content.tests.utils import createSector
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from Products.membrane.config import TOOLNAME
from Products.membrane.interfaces import user as user_ifaces
from Products.statusmessages.interfaces import IStatusMessage


class PasswordPolicyTests(EuphorieIntegrationTestCase):
    def testPasswordPolicy(self):
        err_msg = _(
            u"password_policy_conditions",
            default=u"Your password must contain at least 5 characters, "
            u"including at least one capital letter, one number and "
            u"one special character (e.g. $, # or @).",
        )
        regtool = api.portal.get_tool("portal_registration")
        self.assertEqual(regtool.pasValidation("password", "secret"), err_msg)
        self.assertEqual(regtool.pasValidation("password", "Secret"), err_msg)
        self.assertEqual(regtool.pasValidation("password", "Secret1"), err_msg)
        self.assertIsNone(regtool.pasValidation("password", "Secret1!"))

    def testLockoutPolicy(self):
        sector = createSector(self.portal)
        mbtool = api.portal.get_tool(TOOLNAME)
        member = mbtool.getUserObject(login=sector.login)
        auth = user_ifaces.IMembraneUserAuth(member, None)
        status = IStatusMessage(auth.context.REQUEST)

        auth.applyLockoutPolicy(0)
        self.assertEqual(len(status.show()), 0)
        self.assertFalse(sector.locked)

        auth.applyLockoutPolicy(2)
        self.assertEqual(len(status.show()), 1)
        self.assertEqual(auth.context._v_login_attempts, 1)
        self.assertFalse(sector.locked)

        auth.applyLockoutPolicy(2)
        self.assertEqual(len(status.show()), 1)
        self.assertEqual(auth.context._v_login_attempts, 2)
        self.assertTrue(sector.locked)
