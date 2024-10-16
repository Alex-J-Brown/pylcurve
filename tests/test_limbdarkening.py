import pytest
from pylcurve.limbdark import build_ld_interpolator


def test_build_ld_interpolator():
    build_ld_interpolator()


@pytest.fixture
def ld_interpolator():
    return build_ld_interpolator()


def test_ld_wd_gs(ld_interpolator):
    assert len(ld_interpolator['WD']['gs'](10000, 8.0)) == 4
    c1, c2, c3, c4 = ld_interpolator['WD']['gs'](10000, 8.0)
    assert c1 == 0.3428
    assert c2 == 1.6572
    assert c3 == -2.1759
    assert c4 == 0.8352


def test_ld_ms_gs(ld_interpolator):
    assert len(ld_interpolator['MS']['gs'](2900, 5.0)) == 4
    c1, c2, c3, c4 = ld_interpolator['MS']['gs'](2900, 5.0)
    assert c1 == 0.60015
    assert c2 == 0.29291
    assert c3 == 0.4273
    assert c4 == -0.24199

