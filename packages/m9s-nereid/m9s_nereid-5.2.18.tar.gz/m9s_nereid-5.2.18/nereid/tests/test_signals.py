# -*- coding: utf-8 -*-
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest

from .test_templates import BaseTestCase
from trytond.tests.test_tryton import with_transaction
from trytond.pool import PoolMeta

import flask
import nereid
from nereid import route
from nereid.testing import POOL as Pool


class SignalsTestCase(BaseTestCase):

    @with_transaction()
    def test_template_rendered(self):
        self.setup_defaults()
        app = self.get_app()
        # app.testing = True # propagate exceptions
        # dispatch the patched home func as a method
        app.dispatch_function_as_method = True

        # Patch the home page method
        @route('/')
        def home_func():
            return nereid.render_template(
                'home.jinja', whiskey=42
            )

        app.view_functions['nereid.website.home'] = home_func

        recorded = []

        def record(sender, template, context):
            recorded.append((template, context))

        flask.template_rendered.connect(record, app)
        try:
            app.test_client().get('/')
            self.assertEqual(len(recorded), 1)
            template, context = recorded[0]
            self.assertEqual(template.name, 'home.jinja')
            self.assertEqual(context['whiskey'], 42)
        finally:
            flask.template_rendered.disconnect(record, app)

    @with_transaction()
    def test_request_signals(self):
        self.setup_defaults()
        app = self.get_app()
        # dispatch the patched home func as a method
        app.dispatch_function_as_method = True

        calls = []

        def before_request_signal(sender):
            calls.append('before-signal')

        def after_request_signal(sender, response):
            self.assertEqual(response.data, b'stuff')
            calls.append('after-signal')

        @app.before_request
        def before_request_handler():
            calls.append('before-handler')

        @app.after_request
        def after_request_handler(response):
            calls.append('after-handler')
            response.data = 'stuff'
            return response

        # Patch the home page method
        @route('/')
        def home_func():
            calls.append('handler')
            return 'ignored anyway'

        app.view_functions['nereid.website.home'] = home_func

        flask.request_started.connect(before_request_signal, app)
        flask.request_finished.connect(after_request_signal, app)

        try:
            rv = app.test_client().get('/')
            self.assertEqual(rv.data, b'stuff')

            self.assertEqual(
                calls, [
                    'before-signal', 'before-handler', 'handler',
                    'after-handler', 'after-signal'
                ]
            )
        finally:
            flask.request_started.disconnect(before_request_signal, app)
            flask.request_finished.disconnect(after_request_signal, app)

    @with_transaction()
    def test_request_exception_signal(self):
        self.setup_defaults()
        app = self.get_app()
        # dispatch the patched home func as a method
        app.dispatch_function_as_method = True
        app.config['DEBUG'] = False

        recorded = []

        # Patch the home page method
        @route('/')
        def home_func():
            1 // 0

        app.view_functions['nereid.website.home'] = home_func

        def record(sender, exception):
            recorded.append(exception)

        flask.got_request_exception.connect(record, app)
        try:
            self.assertEqual(
                app.test_client().get('/').status_code, 500
            )
            self.assertEqual(len(recorded), 1)
            assert isinstance(recorded[0], ZeroDivisionError)
        finally:
            flask.got_request_exception.disconnect(record, app)

    @with_transaction()
    def test_appcontext_signals(self):
        self.setup_defaults()
        app = self.get_app()
        recorded = []

        def record_push(sender, **kwargs):
            recorded.append('push')

        def record_pop(sender, **kwargs):
            recorded.append('pop')

        @app.route('/')
        def index():
            return 'Hello'

        flask.appcontext_pushed.connect(record_push, app)
        flask.appcontext_popped.connect(record_pop, app)
        try:
            with app.test_client() as c:
                rv = c.get('/')
                self.assertEqual(rv.data, b'Hello')
                self.assertEqual(recorded, ['push'])
            self.assertEqual(recorded, ['push', 'pop'])
        finally:
            flask.appcontext_pushed.disconnect(record_push, app)
            flask.appcontext_popped.disconnect(record_pop, app)

    @with_transaction()
    def test_flash_signal(self):
        self.setup_defaults()
        app = self.get_app()
        # dispatch the patched home func as a method
        app.dispatch_function_as_method = True
        app.config['SECRET_KEY'] = 'secret'

        # Patch the home page method
        @route('/')
        def home_func():
            flask.flash('This is a flash message', category='notice')
            return nereid.render_template(
                'home.jinja', whiskey=42
            )
        app.view_functions['nereid.website.home'] = home_func

        recorded = []

        def record(sender, message, category):
            recorded.append((message, category))

        flask.message_flashed.connect(record, app)
        try:
            client = app.test_client()
            with client.session_transaction():
                client.get('/')
                self.assertEqual(len(recorded), 1)
                message, category = recorded[0]
                self.assertEqual(message, 'This is a flash message')
                self.assertEqual(category, 'notice')
        finally:
            flask.message_flashed.disconnect(record, app)


def suite():
    "Nereid Helpers test suite"
    test_suite = unittest.TestSuite()
    test_suite.addTests([
        unittest.TestLoader().loadTestsFromTestCase(SignalsTestCase),
    ])
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
