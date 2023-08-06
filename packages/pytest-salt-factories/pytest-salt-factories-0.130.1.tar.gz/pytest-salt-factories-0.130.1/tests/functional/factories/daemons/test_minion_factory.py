import pytest

from saltfactories.utils import random_string
from saltfactories.utils import running_username


def test_keyword_basic_config_defaults(salt_factories):
    minion_config = salt_factories.get_salt_minion_daemon(
        random_string("minion-"), config_defaults={"zzzz": True}
    ).config
    assert "zzzz" in minion_config


def test_interface_config_defaults(salt_factories):
    interface = "172.17.0.1"
    minion_config = salt_factories.get_salt_minion_daemon(
        random_string("minion-"), config_defaults={"interface": interface}
    ).config
    assert minion_config["interface"] != interface
    assert minion_config["interface"] == "127.0.0.1"


def test_master_config_defaults(salt_factories):
    master = "172.17.0.1"
    minion_config = salt_factories.get_salt_minion_daemon(
        random_string("minion-"), config_defaults={"master": master}
    ).config
    assert minion_config["master"] != master
    assert minion_config["master"] == "127.0.0.1"


def test_keyword_basic_config_overrides(salt_factories):
    minion_config = salt_factories.get_salt_minion_daemon(
        random_string("minion-"), config_overrides={"zzzz": True}
    ).config
    assert "zzzz" in minion_config


def test_interface_config_overrides(salt_factories):
    interface = "172.17.0.1"
    minion_config = salt_factories.get_salt_minion_daemon(
        random_string("minion-"), config_overrides={"interface": interface}
    ).config
    assert minion_config["interface"] == interface
    assert minion_config["interface"] != "127.0.0.1"


def test_master_config_overrides(salt_factories):
    master = "172.17.0.1"
    minion_config = salt_factories.get_salt_minion_daemon(
        random_string("minion-"), config_overrides={"master": master}
    ).config
    assert minion_config["master"] == master
    assert minion_config["master"] != "127.0.0.1"


def test_keyword_simple_overrides_override_defaults(salt_factories):
    minion_config = salt_factories.get_salt_minion_daemon(
        random_string("minion-"), config_defaults={"zzzz": False}, config_overrides={"zzzz": True}
    ).config
    assert "zzzz" in minion_config
    assert minion_config["zzzz"] is True


def test_keyword_nested_overrides_override_defaults(salt_factories):
    minion_config = salt_factories.get_salt_minion_daemon(
        random_string("minion-"),
        config_defaults={
            "zzzz": False,
            "user": "foobar",
            "colors": {"black": True, "white": False},
        },
        config_overrides={"colors": {"white": True, "grey": False}},
    ).config
    assert "zzzz" in minion_config
    assert minion_config["zzzz"] is False
    assert minion_config["colors"] == {"black": True, "white": True, "grey": False}


def test_provide_root_dir(pytester, salt_factories):
    root_dir = str(pytester.mkdir("custom-root"))
    config_defaults = {"root_dir": root_dir}
    minion_config = salt_factories.get_salt_minion_daemon(
        random_string("minion-"), config_defaults=config_defaults
    ).config
    assert minion_config["root_dir"] == root_dir


def configure_kwargs_ids(value):
    return "configure_kwargs={!r}".format(value)


@pytest.mark.parametrize(
    "configure_kwargs",
    [{"config_defaults": {"user": "blah"}}, {"config_overrides": {"user": "blah"}}, {}],
    ids=configure_kwargs_ids,
)
def test_provide_user(salt_factories, configure_kwargs):
    minion_config = salt_factories.get_salt_minion_daemon(
        random_string("minion-"), **configure_kwargs
    ).config
    if not configure_kwargs:
        # salt-factories injects the current username
        assert minion_config["user"] is not None
        assert minion_config["user"] == running_username()
    else:
        # salt-factories does not override the passed user value
        assert minion_config["user"] != running_username()
        assert minion_config["user"] == "blah"


@pytest.mark.parametrize(
    "configure_kwargs",
    [
        {"config_defaults": None},
        {"config_overrides": None},
        {},
        {"config_defaults": None, "config_overrides": {"user": "blah"}},
        {"config_defaults": {"user": "blah"}, "config_overrides": None},
        {"config_defaults": {"user": "blah"}, "config_overrides": {"user": "blah"}},
    ],
    ids=configure_kwargs_ids,
)
def test_pytest_config(salt_factories, configure_kwargs):
    master_id = random_string("master-")
    master = salt_factories.get_salt_master_daemon(master_id)
    config = master.get_salt_minion_daemon(random_string("the-id-"), **configure_kwargs).config
    config_key = "pytest-minion"
    assert config_key in config
    assert "log" in config[config_key]
    for key in ("host", "level", "port", "prefix"):
        assert key in config[config_key]["log"]
    assert "master-id" in config[config_key]
    assert config[config_key]["master-id"] == master_id
