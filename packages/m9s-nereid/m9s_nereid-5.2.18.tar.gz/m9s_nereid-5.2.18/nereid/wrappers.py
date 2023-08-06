# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from werkzeug._internal import _missing
from flask.wrappers import Request as RequestBase, Response as ResponseBase

from .globals import request
from .signals import transaction_stop


class cached_property(object):
    """A decorator that converts a function into a lazy property.  The
    function wrapped is called the first time to retrieve the result
    and then that calculated result is used the next time you access
    the value::

        class Foo(object):

            @cached_property
            def foo(self):
                # calculate something important here
                return 42

    The class has to have a `__dictcache__` in order for this property to
    work.

    If the transaction has changed then the cache is invalidated

    Based on werkzeug.utils.cached_property
    """

    # implementation detail: this property is implemented as non-data
    # descriptor.  non-data descriptors are only invoked if there is
    # no entry with the same name in the instance's __dictcache__.
    # this allows us to completely get rid of the access function call
    # overhead.  If one choses to invoke __get__ by hand the property
    # will still work as expected because the lookup logic is replicated
    # in __get__ for manual invocation.

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dictcache__.get(self.__name__, _missing)
        if value is _missing:
            value = self.func(obj)
            obj.__dictcache__[self.__name__] = value
        return value


class Request(RequestBase):
    "Request Object"

    def __init__(self, *args, **kwargs):
        super(Request, self).__init__(*args, **kwargs)
        self.__dictcache__ = {}

    @staticmethod
    @transaction_stop.connect
    def clear_dictcache(app):
        """
        Clears the dictcache which stored the cached values of the records
        below.
        """
        request.__dictcache__ = {}

    @property
    def is_xhr(self):
        """
        This property was deprecated by werkzeug for the following reason:

        True if the request was triggered via a JavaScript XMLHttpRequest.
        This only works with libraries that support the ``X-Requested-With``
        header and set it to "XMLHttpRequest".  Libraries that do that are
        prototype, jQuery and Mochikit and probably some more.

        .. deprecated:: 0.13
            ``X-Requested-With`` is not standard and is unreliable. You
            may be able to use :attr:`AcceptMixin.accept_mimetypes`
            instead.

        Nevertheless this is currently the only working solution when testing
        with old jquery versions. accept_mimetypes returns wrong/unreliable
        results as well.

        For the time being we leave is_xhr as is, so we override it
        until we find a better solution to detect javascript requests from the
        browser which could be to set an according Accept Header in the
        template code.
        S.a.
        https://stackoverflow.com/questions/43871003/identify-if-flask-request-is-from-javascript-or-not
        https://www.quora.com/How-do-I-send-custom-headers-using-jQuery-Ajax-in-post-type

        TODO: check with recent jquery versions.
        import warnings
        warnings.warn(
            "is_xhr replacement",
            DeprecationWarning,
            stacklevel=2,
        )
        print(dir(self))
        print(20, self.headers)
        print(30, self.content_type)
        print(40, self.accept_mimetypes.accept_json)
        print(50, self.accept_mimetypes.accept_xhtml)
        return (self.accept_mimetypes.accept_json or
            self.accept_mimetypes.accept_xhtml)
        """
        return self.environ.get("HTTP_X_REQUESTED_WITH", "").lower() == "xmlhttprequest"

    @property
    def is_json(self):
        """Indicates if this request is JSON or not.  By default a request
        is considered to include JSON data if the mimetype is
        ``application/json`` or ``application/*+json``.

        This feature is forward ported from flask 0.11. When flask is released
        this will be removed from nereid code

        .. versionadded:: 3.0.4.0
        """
        mt = self.mimetype
        if mt == 'application/json':
            return True
        if mt.startswith('application/') and mt.endswith('+json'):
            return True
        return False


class Response(ResponseBase):
    pass
