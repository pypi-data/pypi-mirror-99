import pytest

from cashews.key import get_cache_key, get_cache_key_template, get_template_and_func_for, register_template


async def func1(a):
    ...


async def func2(a, k=None, **kwargs):
    ...


TEPLATE_FUNC1 = "func1:{a}"
TEPLATE_FUNC2 = "func2:{k}:user:{user}"

register_template(func1, TEPLATE_FUNC1)
register_template(func2, TEPLATE_FUNC2)


@pytest.mark.parametrize(
    ("key", "template"),
    (
        ("func1:test", TEPLATE_FUNC1.format(a="*")),
        ("func1:", TEPLATE_FUNC1.format(a="*")),
        ("prefix:func1:test", TEPLATE_FUNC1.format(a="*")),
        ("func2:-:user:1", TEPLATE_FUNC2.format(k="*", user="*")),
        ("func:1", None),
        ("prefix:func2:test:user:1:1", None),
        ("func2:user:1", None),
        ("func2:user:1", None),
    ),
)
def test_detect_template_by_key(key, template):
    assert get_template_and_func_for(key)[0] == template


def test_cache_func_key_dict():
    async def func(user):
        ...

    obj = type("user", (), {"name": "test", "one": True})()

    assert get_cache_key(func, template="test_key:{user.name}", args=(obj,)) == "test_key:test"

    obj.name = "new"
    assert get_cache_key(func, template="test_key:{user.name}", args=(obj,)) == "test_key:new"


@pytest.mark.parametrize(
    ("args", "kwargs", "template", "key"),
    (
        (
            ("a1", "a2", "a3"),
            {"kwarg1": "k1", "kwarg3": "k3"},
            "{arg1}:{kwarg1}-{kwarg3}",
            "a1:k1-k3",
        ),
        (
            ("a1", "a2", "a3"),
            {"kwarg1": "k1", "kwarg3": "k3"},
            None,
            "tests.test_key:func:arg1:a1:arg2:a2:kwarg1:k1:kwarg2:true",
        ),
        (
            ("a1", "a2", "a3"),
            None,
            "{arg1}-{kwarg1}-{kwarg3}",
            "a1--",
        ),
        (
            ("a1",),
            {"arg2": 2, "kwarg1": "k1"},
            "{arg2}-{kwarg1}-{kwarg3}",
            "2-k1-",
        ),
        (
            ("a1",),
            {"arg2": 2, "kwarg1": "k1", "kwarg3": "k3"},
            "{arg2}:{kwarg1}:{kwarg3}",
            "2:k1:k3",
        ),
        (
            ("a1",),
            {"kwarg1": "k1", "arg2": 2},
            "{arg2}:{kwarg1}:{kwarg3}",
            "2:k1:",
        ),
        (("a1", "a2"), {"kwarg1": "test"}, "{kwarg1:len}", "4"),
        (("a1", "a2"), {"user": type("user", (), {"name": "test"})()}, "{user.name:len}", "4"),
        (("a1", "a2"), {"kwarg1": "test"}, "{kwarg1:hash}", "098f6bcd4621d373cade4e832627b4f6"),
        (("a1", "a2"), {"kwarg1": "test"}, "{kwarg1:hash(md5)}", "098f6bcd4621d373cade4e832627b4f6"),
        (
            ("a1", "a2"),
            {"kwarg1": "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidGVzdCJ9.n75bSCIEuSemX5iop0sCF3HmXwMQWF1zI6TzckzHUKY"},
            "{kwarg1:jwt(user)}",
            "test",
        ),
    ),
)
def test_cache_key_args_kwargs(args, kwargs, template, key):
    async def func(arg1, arg2, *args, kwarg1=None, kwarg2=b"true", **kwargs):
        ...

    assert get_cache_key(func, template, args=args, kwargs=kwargs) == key


@pytest.mark.parametrize(
    ("func", "key", "template"),
    (
        (func1, None, "tests.test_key:func1:a:{a}"),
        (func2, None, "tests.test_key:func2:a:{a}:k:{k}"),
        (func2, "key:{k}", "key:{k}"),
    ),
)
def test_get_key_template(func, key, template):
    assert get_cache_key_template(func, key) == template


def test_get_key_template_error():
    with pytest.raises(ValueError) as exc:
        get_cache_key_template(func1, "key:{wrong_key}:{a}")
    exc.match("wrong_key")
