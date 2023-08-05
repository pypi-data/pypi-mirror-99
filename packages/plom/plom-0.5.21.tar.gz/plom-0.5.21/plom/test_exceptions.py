from pytest import raises

import plom.plom_exceptions
from plom.plom_exceptions import *


def test_plom_exc_string():
    e = PlomException("foo")
    assert str(e) == "foo"


def test_exc_inheritance():
    e = PlomAuthenticationException()
    assert isinstance(e, PlomException)


def test_exc_auth_has_default_msg():
    e = PlomAuthenticationException()
    assert "authenticate" in str(e).lower()
    e = PlomAuthenticationException("foo")
    assert str(e) == "foo"


def test_exc_all_print_properly():
    excs = [eval(e) for e in dir(plom.plom_exceptions) if e.startswith("Plom")]
    assert len(excs) > 10  # we have some exceptions
    for exc in excs:
        assert str(exc("foo")) == "foo"
