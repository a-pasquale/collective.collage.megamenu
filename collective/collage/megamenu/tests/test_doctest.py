import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.Collage.tests.base import CollageFunctionalTestCase

from collective.collage.megamenu.tests import base

ztc.installProduct('collective.collage.megamenu')
ptc.setupPloneSite(products=['collective.collage.megamenu'])

import collective.collage.megamenu

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             collective.collage.megamenu)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='collective.collage.megamenu',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='collective.collage.megamenu.browser.helper',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'docs/vocabulary.txt', package='collective.collage.megamenu',
        #    test_class=base.FunctionalTestCase),
            
        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'docs/browser.txt', package='collective.collage.megamenu',
            test_class=base.FunctionalTestCaseWithContent),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='collective.collage.megamenu',
        #    test_class=base.FunctionalTestCase),


        #ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='collective.collage.megamenu',
        #    test_class=TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
