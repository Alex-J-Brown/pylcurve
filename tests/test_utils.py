import pylcurve.utils as utils
import pytest

def test_planck():
    assert utils.planck(5000, 3000) == pytest.approx(2.1704043e+16)


def test_get_Tbb():
    assert utils.get_Tbb(10000, 8.0, 'gs', 'hcam', star_type='WD', model='Claret') == 10332.55543


def test_get_ldcs_one_star_WD():
    ldcs = utils.get_ldcs(10000, 8.0, 'gs', 'WD')
    assert ldcs['ldc1_1'] == 0.3428
    assert ldcs['ldc1_2'] == 1.6572
    assert ldcs['ldc1_3'] == -2.1759
    assert ldcs['ldc1_4'] == 0.8352


def test_get_ldcs_one_star_MS():
    ldcs = utils.get_ldcs(2900, 5.0, 'gs', 'MS')
    assert ldcs['ldc1_1'] == 0.60015
    assert ldcs['ldc1_2'] == 0.29291
    assert ldcs['ldc1_3'] == 0.4273
    assert ldcs['ldc1_4'] == -0.24199


def test_get_ldcs_two_stars():
    ldcs = utils.get_ldcs(10000, 8.0, 'gs', "WD", 2900, 5.0, "MS")
    assert ldcs['ldc1_1'] == 0.3428
    assert ldcs['ldc1_2'] == 1.6572
    assert ldcs['ldc1_3'] == -2.1759
    assert ldcs['ldc1_4'] == 0.8352
    assert ldcs['ldc2_1'] == 0.60015
    assert ldcs['ldc2_2'] == 0.29291
    assert ldcs['ldc2_3'] == 0.4273
    assert ldcs['ldc2_4'] == -0.24199


def test_Rva_to_Rl1():
    assert utils.Rva_to_Rl1(0.1, 0.2) > 0.2
    assert utils.Rva_to_Rl1(0.1, 0.2) < 1
    assert utils.Rva_to_Rl1(0.1, 0.2) == pytest.approx(0.246, 0.001)


def test_log_g():
    assert utils.log_g(1, 1) == pytest.approx(4.44, 0.01)