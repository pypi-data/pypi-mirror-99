# -*- coding: utf-8 -*-

from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.testing import z2
from plone.testing import zca
from Products.PloneMeeting.testing import PMLayer

import Products.MeetingCommunes


class MCLayer(PMLayer):
    """ """


MC_ZCML = zca.ZCMLSandbox(filename="testing.zcml",
                          package=Products.MeetingCommunes,
                          name='MC_ZCML')

MC_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, MC_ZCML),
                              name='MC_Z2')

MC_TESTING_PROFILE = MCLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingCommunes,
    additional_z2_products=('imio.dashboard',
                            'Products.MeetingCommunes',
                            'Products.PloneMeeting',
                            'Products.CMFPlacefulWorkflow',
                            'Products.PasswordStrength'),
    gs_profile_id='Products.MeetingCommunes:testing',
    name="MC_TESTING_PROFILE")

MC_TESTING_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(MC_TESTING_PROFILE,), name="MC_TESTING_PROFILE_FUNCTIONAL")

MC_DEMO_TESTING_PROFILE = MCLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingCommunes,
    additional_z2_products=('imio.dashboard',
                            'Products.MeetingCommunes',
                            'Products.PloneMeeting',
                            'Products.CMFPlacefulWorkflow',
                            'Products.PasswordStrength'),
    gs_profile_id='Products.MeetingCommunes:demo',
    name="MC_TESTING_PROFILE")

MC_TESTING_ROBOT = FunctionalTesting(
    bases=(
        MC_DEMO_TESTING_PROFILE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="MC_TESTING_ROBOT",
)
