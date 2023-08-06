# -*- coding: utf-8 -*-
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import warnings

import jinja2
from .test_templates import BaseTestCase
from trytond.pool import PoolMeta
from trytond.tests.test_tryton import with_transaction
from nereid import url_for, template_filter
from nereid.testing import POOL as Pool


class TestURLfor(BaseTestCase):
    """
    Test the functionality of the url_for helper
    """

    @with_transaction()
    def test_0010_simple(self):
        """
        Generate a simple URL
        """
        self.setup_defaults()
        app = self.get_app()

        with app.test_request_context('/'):
            self.assertEqual(url_for('nereid.website.home'), '/')

    @with_transaction()
    def test_0020_external(self):
        """
        Create an external URL
        """
        self.setup_defaults()
        app = self.get_app()

        with app.test_request_context('/'):
            self.assertEqual(url_for('nereid.website.home', _external=True),
                'http://localhost/')

    @with_transaction()
    def test_0030_schema(self):
        """
        Change the schema to https
        """
        self.setup_defaults()
        app = self.get_app()

        with app.test_request_context('/'):
            self.assertEqual(url_for('nereid.website.home', _external=True,
                    _scheme='https'), 'https://localhost/')

        with app.test_request_context('/'):
            # Check for the to be deprecated _secure argument
            with warnings.catch_warnings(record=True) as w:
                self.assertEqual(url_for('nereid.website.home', _secure=True),
                    'https://localhost/')
                self.assertEqual(len(w), 1)


class NereidWebsite(metaclass=PoolMeta):
    __name__ = 'nereid.website'

    @classmethod
    @template_filter()
    def reverse_test(cls, s):
        return s[::-1]


class TestHelperFunctions(BaseTestCase):
    '''
    Test case to test various helper functions introduced by nereid
    '''

    @classmethod
    def setUpClass(cls):
        Pool.register(NereidWebsite, module='nereid', type_='model')
        Pool.init(update=['nereid'])

    @classmethod
    def tearDownClass(cls):
        mpool = Pool.classes['model'].setdefault('nereid', [])
        del(mpool[NereidWebsite])
        Pool.init(update=['nereid'])

    @with_transaction()
    def test_template_filter(self):
        '''
        Test the template filter decorator implementation
        '''
        self.setup_defaults()
        templates = {
            'home.jinja': "{{ 'abc'|reverse_test }}"
            }
        app = self.get_app()
        # loaders is usually lazy loaded
        # Pre-fetch it so that the instance attribute _loaders will exist
        app.jinja_loader.loaders
        app.jinja_loader._loaders.insert(0, jinja2.DictLoader(templates))

        with app.test_client() as c:
            response = c.get('/')
            self.assertEqual(response.data, b'cba')


def suite():
    "Nereid Helpers test suite"
    test_suite = unittest.TestSuite()
    test_suite.addTests([
        unittest.TestLoader().loadTestsFromTestCase(TestURLfor),
        unittest.TestLoader().loadTestsFromTestCase(TestHelperFunctions),
    ])
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
