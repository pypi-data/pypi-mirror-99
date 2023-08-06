# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import warnings

import pytz
from werkzeug.utils import redirect
from werkzeug.exceptions import abort
from werkzeug.routing import Map, Submount
from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, validators, BooleanField
from flask_login import login_user, logout_user

from nereid import jsonify, flash, render_template, url_for, cache, \
    current_user, route, current_website
from nereid.globals import request
from nereid.exceptions import WebsiteNotFound
from nereid.helpers import login_required, key_from_list, get_flashed_messages
from nereid.signals import failed_login
from trytond.model import ModelView, ModelSQL, fields, Unique, DeactivableMixin
from trytond.transaction import Transaction
from trytond.pool import Pool
#from trytond.cache import Cache
from trytond.cache import MemoryCache as Cache
from trytond.tools import memoize
from nereid.contrib.locale import make_lazy_gettext


_ = make_lazy_gettext('nereid')


class LoginForm(Form):
    "Default Login Form"
    email = StringField(_('e-mail'), [validators.DataRequired(), validators.Email()])  # noqa
    password = PasswordField(_('Password'), [validators.DataRequired()])
    remember = BooleanField(_('Remember me'), default=False)


class WebSite(DeactivableMixin, ModelSQL, ModelView):
    """
    One of the most powerful features of Nereid is the ability to
    manage multiple websites from one back-end. A web site in nereid
    represents a collection or URLs, settings.

    :param name: Name of the web site
    :param base_url: The unique URL of the website, You cannot have two
                     websites, with the same base_url
    :param url_map: The active URL Map for the website (M2O URLMap)
    :param company: The company linked with the website.
    :param active: Whether the website is active or not.

    """
    __name__ = "nereid.website"

    #: The name field is used for both information and also as
    #: the site identifier for nereid. The WSGI application requires
    #: SITE argument. The SITE argument is then used to load URLs and
    #: other settings for the website. Needs to be unique
    name = fields.Char('Name', required=True, select=True)

    #: The company to which the website belongs. Useful when creating
    #: records like sale order which require a company to be present
    company = fields.Many2One('company.company', 'Company', required=True)

    #: The list of countries this website operates in. Used for generating
    #: Countries list in the registration form etc.
    countries = fields.Many2Many(
        'nereid.website-country.country', 'website', 'country',
        'Countries Available')

    #: Allowed currencies in the website
    currencies = fields.Many2Many(
        'nereid.website-currency.currency',
        'website', 'currency', 'Currencies Available')

    #: Default locale
    default_locale = fields.Many2One(
        'nereid.website.locale', 'Default Locale',
        required=True
    )

    #: Allowed locales in the website
    locales = fields.Many2Many(
        'nereid.website-nereid.website.locale',
        'website', 'locale', 'Languages Available')

    #: The res.user with which the nereid application will be loaded
    #:  .. versionadded: 0.3
    application_user = fields.Many2One(
        'res.user', 'Application User', required=True
    )

    timezone = fields.Function(
        fields.Selection(
            [(x, x) for x in pytz.common_timezones], 'Timezone', translate=False
        ), getter="get_timezone"
    )

    # TODO FIXME when running tests this file is initalized twice
    # Either use memoize or cache, but not both.
    if not 'nereid.website.url_adapter' in Cache._instances:
        _url_adapter_cache = Cache('nereid.website.url_adapter', context=False)

    def get_timezone(self, name):
        warnings.warn(
            "Website timezone is deprecated, use company timezone instead",
            DeprecationWarning, stacklevel=2
        )
        return self.company.timezone

    @staticmethod
    def default_company():
        return Transaction().context.get('company')

    @staticmethod
    def default_default_locale():
        ModelData = Pool().get('ir.model.data')

        if not Pool().test:
            return ModelData.get_id("nereid", "website_locale_en")

    @staticmethod
    def default_application_user():
        ModelData = Pool().get('ir.model.data')
        return ModelData.get_id("nereid", "web_user")

    @classmethod
    def __setup__(cls):
        super(WebSite, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('name_uniq', Unique(table, table.name),
             'Another site with the same name already exists!')
        ]

    @classmethod
    @route("/countries", methods=["GET"])
    def country_list(cls):
        """
        Return the list of countries in JSON
        """
        return jsonify(result=[
            {'key': c.id, 'value': c.name}
            for c in current_website.countries
        ])

    @classmethod
    @route("/subdivisions", methods=["GET"])
    def subdivision_list(cls):
        """
        Return the list of states for given country
        """
        Subdivision = Pool().get('country.subdivision')

        country = int(request.args.get('country', 0))
        if country not in [c.id for c in current_website.countries]:
            abort(404)
        subdivisions = Subdivision.search([('country', '=', country)])
        return jsonify(
            result=[s.serialize() for s in subdivisions]
        )

    def stats(self, **arguments):
        """
        Test method.
        """
        return 'Request: %s\nArguments: %s\nEnviron: %s\n' \
            % (request, arguments, request.environ)

    @classmethod
    @route('/')
    def home(cls):
        "A dummy home method which just renders home.jinja"
        return render_template('home.jinja')

    @classmethod
    @route('/login', methods=['GET', 'POST'])
    def login(cls):
        """
        Simple login based on the email and password

        Required post data see :class:LoginForm
        """
        login_form = LoginForm(request.form)

        if not current_user.is_anonymous and request.args.get('next'):
            return redirect(request.args['next'])

        if request.method == 'POST' and login_form.validate():
            NereidUser = Pool().get('nereid.user')
            user = NereidUser.authenticate(
                login_form.email.data, login_form.password.data
            )
            # Result can be the following:
            # 1 - Browse record of User (successful login)
            # 2 - None - Login failure without message
            # 3 - Any other false value (no message is shown. useful if you
            #       want to handle the message shown to user)
            if user:
                # NOTE: Translators leave %s as such
                flash(_("You are now logged in. Welcome %(name)s",
                        name=user.name))
                if login_user(user, remember=login_form.remember.data):
                    if request.is_xhr:
                        return jsonify({
                            'success': True,
                            'user': user.serialize(),
                        })
                    else:
                        return redirect(
                            request.values.get(
                                'next', url_for('nereid.website.home')
                            )
                        )
                else:
                    flash(_("Your account has not been activated yet!"))
            elif user is None:
                flash(_("Invalid login credentials"))

            failed_login.send(form=login_form)

            if request.is_xhr:
                rv = jsonify(message=str(_('Bad credentials')))
                rv.status_code = 401
                return rv

        return render_template('login.jinja', login_form=login_form)

    @classmethod
    @route('/logout')
    def logout(cls):
        "Log the user out"
        logout_user()
        flash(
            _('You have been logged out successfully. Thanks for visiting us')
        )
        return redirect(
            request.args.get('next', url_for('nereid.website.home'))
        )

    @classmethod
    @login_required
    @route('/login/token', methods=['POST'])
    def get_auth_token(cls):
        """
        A method that returns a login token and user information in a json
        response. This should probably be called with basic authentication in
        the header. The token generated could then be used for subsequent
        requests.
        """
        return jsonify({
            'user': current_user.serialize(),
            'token': current_user.get_auth_token(),
        })

    @staticmethod
    def account_context():
        """This fills the account context for the template
        rendering my account. Additional modules might want to fill extra
        data into the context
        """
        return dict(
            user=current_user,
            party=current_user.party,
        )

    @classmethod
    @route("/account", methods=["GET"])
    @login_required
    def account(cls):
        return render_template('account.jinja', **cls.account_context())

    def get_currencies(self):
        """Returns available currencies for current site

        .. note::
            A special method is required so that the fetch can be speeded up,
            by pushing the categories to the central cache which cannot be
            done directly on a browse node.
        """
        cache_key = key_from_list([
            Transaction().database.name,
            Transaction().user,
            'nereid.website.get_currencies',
        ])
        # The website is automatically appended to the cache prefix
        rv = cache.get(cache_key)
        if rv is None:
            rv = [{
                'id': c.id,
                'name': c.name,
                'symbol': c.symbol,
            } for c in self.currencies
            ]
            cache.set(cache_key, rv, 60 * 60)
        return rv

    @staticmethod
    def _user_status():
        """Returns the commonly required status parameters of the user

        This method could be inherited and components could be added
        """
        rv = {
            'messages': list(map(str, get_flashed_messages())),
        }
        if current_user.is_anonymous:
            rv.update({
                'logged_id': False
            })
        else:
            rv.update({
                'logged_in': True,
                'name': current_user.name
            })
        return rv

    @classmethod
    @route("/user_status", methods=["GET", "POST"])
    def user_status(cls):
        """
        Returns a JSON of the user_status
        """
        return jsonify(status=cls._user_status())

    @classmethod
    def get_from_host(cls, host, silent=False):
        """
        Returns the website with name as given host

        If not silent a website not found error is raised.
        """
        websites = cls.search([])
        if len(websites) == 1:
            return websites[0]
        try:
            website, = cls.search([('name', '=', host)])
        except ValueError:
            if not silent:
                raise WebsiteNotFound()
        else:
            return website

    def get_context(self):
        """
        Returns transaction context to be used by nereid dispatcher for this
        website
        """
        return {}


    @classmethod
    def clear_url_adapter_cache(cls, *args):
        """
        A method which conveniently clears the cache
        """
        cls._url_adapter_cache.clear()

    #@memoize(10)
    def get_url_adapter(self, app):
        """
        Returns the URL adapter for the website
        """
        cache_rv = self._url_adapter_cache.get(self.id)

        if cache_rv is not None:
            return cache_rv

        url_rules = app.get_urls()

        # Add custom URL rules
        custom_url_rules = []
        custom_url_rules = self.add_custom_url_rules(app, custom_url_rules)
        url_rules += custom_url_rules

        url_map = Map()
        if self.locales:
            # Create the URL map with locale prefix
            url_map.add(app.url_rule_class(
                    '/', redirect_to='/%s' % self.default_locale.code))
            url_map.add(Submount('/<locale>', url_rules))
            # Re-add the custom rules unprefixed
            for rule in custom_url_rules:
                url_map.add(rule)
        else:
            # Create a new map with the given URLs
            list(map(url_map.add, url_rules))

        # Add the rules from the application's url map filled through the
        # route decorator or otherwise
        for rule in app.url_map._rules:
            url_map.add(rule.empty())

        self._url_adapter_cache.set(self.id, url_map)

        return url_map

    def add_custom_url_rules(self, app, url_rules):
        '''
        Extend this function to add URL rules that should also exist
        unprefixed in localized environments
        (i.e. all sorts of static routes)
        '''
        # Add the static url
        url_rules.append(app.url_rule_class(
                app.static_url_path + '/<path:filename>',
                endpoint='static',))
        return url_rules

    def get_current_locale(self, req):
        """
        Returns the active record of the current locale.
        The locale could either be from the URL if the locale was specified
        in the URL, or the default locale from the website.
        """
        if req.view_args and 'locale' in req.view_args:
            for locale in self.locales:
                if locale.code == req.view_args['locale']:
                    return locale

        # Return the default locale
        return self.default_locale


class WebSiteLocale(ModelSQL, ModelView):
    'Web Site Locale'
    __name__ = "nereid.website.locale"
    _rec_name = 'code'

    code = fields.Char('Code', required=True)
    language = fields.Many2One(
        'ir.lang', 'Default Language', required=True
    )
    currency = fields.Many2One(
        'currency.currency', 'Currency', ondelete='CASCADE', required=True
    )

    @classmethod
    def __setup__(cls):
        super(WebSiteLocale, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints += [
            ('unique_code', Unique(table, table.code),
                'Code must be unique'),
        ]


class WebsiteCountry(ModelSQL):
    "Website Country Relations"
    __name__ = 'nereid.website-country.country'

    website = fields.Many2One('nereid.website', 'Website')
    country = fields.Many2One('country.country', 'Country')


class WebsiteCurrency(ModelSQL):
    "Currencies to be made available on website"
    __name__ = 'nereid.website-currency.currency'
    _table = 'website_currency_rel'

    website = fields.Many2One(
        'nereid.website', 'Website',
        ondelete='CASCADE', select=1, required=True)
    currency = fields.Many2One(
        'currency.currency', 'Currency',
        ondelete='CASCADE', select=1, required=True)


class WebsiteWebsiteLocale(ModelSQL):
    "Languages to be made available on website"
    __name__ = 'nereid.website-nereid.website.locale'
    _table = 'website_locale_rel'

    website = fields.Many2One(
        'nereid.website', 'Website',
        ondelete='CASCADE', select=1, required=True)
    locale = fields.Many2One(
        'nereid.website.locale', 'Locale',
        ondelete='CASCADE', select=1, required=True)
