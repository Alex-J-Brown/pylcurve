import pytest
from pylcurve.gravitydark import build_gdark_interpolator


def test_build_gdark_interpolator():
    build_gdark_interpolator()


@pytest.fixture
def gdark_interpolator():
    return build_gdark_interpolator()[0]


@pytest.fixture
def beta_interpolator():
    return build_gdark_interpolator()[1]


def test_gdark_us(gdark_interpolator):
    y1, y2 = gdark_interpolator['us'](2900, 5.0)
    assert y1 == 4.2465
    assert y2 == -0.4138


def test_gdark_u(gdark_interpolator):
    assert gdark_interpolator['u'](2900, 5.0) == pytest.approx(0.45913242)


def test_gdark_gs(gdark_interpolator):
    y1, y2 = gdark_interpolator['gs'](2900, 5.0)
    assert y1 == 3.3627
    assert y2 == -0.0814


def test_gdark_g(gdark_interpolator):
    assert gdark_interpolator['g'](2900, 5.0) == pytest.approx(0.57637215)


def test_gdark_rs(gdark_interpolator):
    y1, y2 = gdark_interpolator['rs'](2900, 5.0)
    assert y1 == 3.363
    assert y2 == -0.0306


def test_gdark_r(gdark_interpolator):
    assert gdark_interpolator['r'](2900, 5.0) == pytest.approx(0.584403)


def test_gdark_is(gdark_interpolator):
    y1, y2 = gdark_interpolator['is'](2900, 5.0)
    assert y1 == 1.8354
    assert y2 == 0.0015


def test_gdark_i(gdark_interpolator):
    assert gdark_interpolator['i'](2900, 5.0) == pytest.approx(0.43661705)


def test_gdark_zs(gdark_interpolator):
    y1, y2 = gdark_interpolator['zs'](2900, 5.0)
    assert y1 == 1.2666
    assert y2 == 0.0191


def test_gdark_z(gdark_interpolator):
    assert gdark_interpolator['z'](2900, 5.0) == pytest.approx(0.31362514)


def test_gdark_tess(gdark_interpolator):
    assert gdark_interpolator['tess'](3500, 5.0) == pytest.approx(0.29859934)


def test_beta(beta_interpolator):
    assert beta_interpolator(3.5180) == 0.17
