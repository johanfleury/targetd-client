import pytest

from targetd_client import TargetdClient


@pytest.mark.parametrize("insecure_skip_verify", [True, False])
def test_TargetdClient(insecure_skip_verify):
    t = TargetdClient("foo", "bar", "baz", insecure_skip_verify)

    assert hasattr(t, "url") and t.url == "foo"
    assert hasattr(t, "user") and t.user == "bar"
    assert hasattr(t, "password") and t.password == "baz"
    assert (
        hasattr(t, "insecure_skip_verify")
        and t.insecure_skip_verify == insecure_skip_verify
    )
