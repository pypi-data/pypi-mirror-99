# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class CookieConsentPanel(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import rer.cookieconsent
        import collective.regjsonify
        self.loadZCML(package=collective.regjsonify)
        # xmlconfig registration below only needed for Plone 4.2 compatibility
        self.loadZCML(package=rer.cookieconsent)
        z2.installProduct(app, 'rer.cookieconsent')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'rer.cookieconsent:default')
        # quickInstallProduct(portal, 'rer.cookieconsent')


COOKIECONSENT_FIXTURE = CookieConsentPanel()
COOKIECONSENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COOKIECONSENT_FIXTURE, ),
    name='CookieConsent:Integration',
)
COOKIECONSENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COOKIECONSENT_FIXTURE, ),
    name='CookieConsent:Functional',
)

COOKIECONSENT_ROBOT_TESTING = FunctionalTesting(
    bases=(
        COOKIECONSENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE),
    name="CookieConsent:Robot")
