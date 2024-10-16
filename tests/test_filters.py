import pytest
from pylcurve.filters import filters
import numpy as np
import astropy.units as u


def test_initialise_hcam():
    cam = filters('hcam')
    assert len(cam.wl['gs']) == 4217
    assert cam.bands == ['us', 'gs', 'rs', 'is', 'zs']


def test_initialise_ucam():
    cam = filters('ucam')
    assert len(cam.wl['gs']) == 3400
    assert cam.bands == ['us', 'gs', 'rs', 'is', 'zs']


def test_initialise_ucam_sloan():
    cam = filters('ucam_sloan')
    assert len(cam.wl['g']) == 3800
    assert cam.bands == ['u', 'g', 'r', 'i', 'z']


def test_initialise_uspec():
    cam = filters('uspec')
    assert len(cam.wl['g']) == 12311
    assert cam.bands == ['u', 'g', 'kg5', 'r', 'i', 'z']


def test_initialise_sdss():
    cam = filters('sdss')
    assert len(cam.wl['g']) == 89
    assert cam.bands == ['u', 'g', 'r', 'i', 'z']


def test_initialise_ztf():
    cam = filters('ztf')
    assert len(cam.wl['g']) == 2000
    assert cam.bands == ['g', 'r', 'i']


def test_initialise_tess():
    cam = filters('tess')
    assert len(cam.wl['tess']) == 400
    assert cam.bands == ['tess']


def test_initialise_gaia():
    cam = filters('gaiadr3')
    assert len(cam.wl['G']) == 781
    assert cam.bands == ['BP', 'G', 'RP']


def test_initialise_2mass():
    cam = filters('2mass')
    assert len(cam.wl['H']) == 58
    assert cam.bands == ['J', 'H', 'Ks']


def test_initialise_panstarrs():
    cam = filters('panstarrs')
    assert len(cam.wl['g']) == 172
    assert cam.bands == ['g', 'r', 'i', 'z', 'y']


def test_initialise_wise():
    cam = filters('wise')
    assert len(cam.wl['W1']) == 141
    assert cam.bands == ['W1', 'W2', 'W3', 'W4']


def test_initialise_nircam():
    cam = filters('jwst_nircam')
    assert len(cam.wl['F070W']) == 304
    assert cam.bands == ['F070W', 'F090W', 'F115W', 'F140M', 'F150W', 'F150W2',
                         'F162M', 'F164N', 'F182M', 'F187N', 'F200W', 'F210M',
                         'F212N', 'WLP4', 'F250M', 'F277W', 'F300M', 'F322W2',
                         'F323N', 'F335M', 'F356W', 'F360M', 'F405N', 'F410M',
                         'F430M', 'F444W', 'F460M', 'F466N', 'F470N', 'F480MA',
                         'F480MB']


def test_initialise_galex():
    cam = filters('galex')
    assert len(cam.wl['NUV']) == 1321
    assert cam.bands == ['FUV', 'NUV']


@pytest.fixture
def cam():
    return filters('hcam')


def test_synphot_ccd(cam):
    test_wavelengths = np.linspace(2000, 12000, 10000) * u.AA
    test_fluxes = 0.05*np.ones(10000) * u.Jy
    out = cam.synphot_ccd(test_wavelengths, test_fluxes, 'gs')
    assert out.value == pytest.approx(0.05)
    assert isinstance(out, u.Quantity)
    assert out.unit == (u.Jy)


def test_synphot_ABmag(cam):
    test_wavelengths = np.linspace(2000, 12000, 10000) * u.AA
    test_fluxes = 0.05*np.ones(10000) * u.Jy
    out = cam.synphot_ABmag(test_wavelengths, test_fluxes, 'gs')
    assert out == pytest.approx(12.1526, 0.0001)
    assert isinstance(out, float)


def test_synphot_ccd_lam(cam):
    test_wavelengths = np.linspace(2000, 12000, 10000) * u.AA
    test_fluxes = 5e-16*np.ones(10000) * u.erg/u.s/u.cm/u.cm/u.AA
    out = cam.synphot_ccd_lam(test_wavelengths, test_fluxes, 'gs')
    assert out.value == pytest.approx(5e-16)
    assert isinstance(out, u.Quantity)
    assert out.unit == (u.erg/u.s/u.cm/u.cm/u.AA)


