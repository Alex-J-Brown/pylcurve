import numpy as np
from os import path
from scipy.integrate import simpson
import astropy.units as u
from glob import glob
from scipy.interpolate import interp1d
from collections import OrderedDict
from pkg_resources import resource_filename


class filters:
    """
    Class to hold wavelength and transmission arrays for both SDSS,
    super SDSS (HiPERCAM/ULTRACAM), ULTRASPEC, Gaia, & 2MASS filter profiles
    """
    
    def __init__(self, instrument='hcam',
                 fpath=resource_filename('pylcurve', 'data/filter_profiles/')):

        choices = ['hcam', 'ucam', 'ucam_s', 'ucam_super', 'ucam_sloan',
                   'ucam_old', 'uspec', 'sdss', 'usno40', 'panstarrs',
                   'gaiadr3', '2mass', 'galex', 'wise', 'tess', 'jwst_nircam',
                   'ztf']
        self.inst = instrument
        if self.inst not in choices:
            raise ValueError('"{}" is not a valid instrument'
                             .format(self.inst))
        self.fpath = fpath
        self.wl, self.trans, self.bands = self.load_bandpasses(self.fpath, self.inst)
        self.eff_wl = self.get_pivot_wl()
        self.vega_syn_zp = dict(G=-26.48986, BP=-25.96551, RP=-27.21639,
                                J=-28.76149, H=-29.864425, Ks=-30.92063)


    def load_bandpasses(self, fpath, inst):
        """
        Loads filter throughputs from file
        """

        wl = dict()
        trans = dict()

        if (inst == 'ucam_sloan') or (inst == 'ucam_old'):
            inst = 'ucam'
            fnames = [path.split(f)[1] for f in glob(fpath + 'ucam_*.txt')
                      if 's' not in path.split(f)[1]]
            bands = [path.splitext(fname)[0].split('_')[-1] for fname in fnames]
        elif inst == 'ucam' or inst == 'ucam_s' or inst == 'ucam_super':
            inst = 'ucam'
            fnames = [path.split(f)[1] for f in glob(fpath +  'ucam_*.txt')
                      if 's' in path.split(f)[1]]
            bands = [path.splitext(fname)[0].split('_')[-1] for fname in fnames]
        else:
            fnames = glob(fpath + inst + '_*.txt')
            fnames_cut = [fname.split('_')[-1] for fname in fnames]
            bands = [fname.split('.')[0] for fname in fnames_cut]
        
        for band in bands:
            file = (fpath + inst + '_{}.txt'.format(band))
            wl[band], trans[band] = np.loadtxt(file, unpack=True)
            wl[band] *= u.AA
        return wl, trans, bands


    def pivot_wl(self, wave, trans):
        """
        Calculates pivot wavelength given wavelength and throughput arrays.
        """
        top = simpson(trans, x=wave)
        bottom = simpson(trans * wave**-2, x=wave)
        pivot = (top / bottom)**0.5
        return pivot


    def get_pivot_wl(self):
        """
        Calculates pivot wavelength for all filters in filter system.
        Returns as dictionary, ordered by ascending wavelength.
        """

        self.eff_wl = OrderedDict()
        eff_wls = np.array([self.pivot_wl(self.wl[band], self.trans[band]) for band in self.bands])
        self.bands = [x for _,x in sorted(zip(eff_wls,self.bands))]
        eff_wls = sorted(eff_wls) * u.AA  # dictionary??
        for i, band in enumerate(self.bands):
            self.eff_wl[band] = eff_wls[i]
        return self.eff_wl


    def synphot(self, wave, flux, band):
        """
        Mean (energy weighted) flux density for a given spectrum through the
        chosen filter. Calculations done in /Angstrom units. Outputs in units
        of erg/s/cm^2/Angstrom
        """

        flux = flux.to(u.Jansky, equivalencies=u.spectral_density(wave))
        trans_interpolator = interp1d(self.wl[band], self.trans[band],
                                    bounds_error=False, fill_value=0)
        trans_new = trans_interpolator(wave)
        filtered_spec = flux * trans_new
        fLam = (simpson(filtered_spec, x=wave) / simpson(trans_new, x=wave))
        return fLam * u.Jansky


    def synphot_ccd(self, wave, flux, band):
        """
        Mean (photon weighted) flux density for a given spectrum through the
        chosen filter. Calculations done in /Hz units. Outputs in units
        of Janskys
        """
        
        flux = flux.to(u.Jansky, equivalencies=u.spectral_density(wave))
        trans_interpolator = interp1d(self.wl[band], self.trans[band],
                                      bounds_error=False, fill_value=0)
        trans_new = trans_interpolator(wave)
        out = simpson(flux * trans_new * (1/wave), x=wave) / simpson(trans_new / wave, x=wave)
        return out * u.Jansky


    def synphot_ABmag(self, wave, flux, band):
        """
        Calculates mean (photon weighted) flux density in Janskys for a given
        spectrum through the chosen filter and outputs this in AB magnitudes.
        """
        
        mag = self.synphot_ccd(wave, flux, band).to_value(u.ABmag)
        return mag
    

    def synphot_ccd_lam(self, wave, flux, band):
        """
        Mean (photon weighted) flux density for a given spectrum through the
        chosen filter. Calculations done in /Angstrom units. Outputs in units
        of erg/s/cm^2/Angstrom
        """
        if flux.unit != u.erg/u.s/u.cm/u.cm/u.AA:
            flux = flux.to(u.erg/u.s/u.cm/u.cm/u.AA, equivalencies=u.spectral_density(wave))
        trans_interpolator = interp1d(self.wl[band], self.trans[band],
                                      bounds_error=False, fill_value=0)
        trans_new = trans_interpolator(wave)
        out = simpson(flux * trans_new * wave, x=wave) / simpson(trans_new * wave, x=wave)
        return out * (u.erg/u.s/u.cm/u.cm/u.AA)


    def synphot_vega_mag(self, wave, flux, band):
        """
        Calculates mean (photon weighted) flux density from given spectrum in
        erg/s/cm^2/Angstrom through a given GAIA or 2MASS filter and outputs
        in Vega mag according to the survey zeropoints (eDR3 for GAIA).
        """
        
        if band not in ['G', 'BP', 'RP', 'J', 'H', 'Ks']:
            raise ValueError('{} not a GAIA/2MASS passband'.format(band))
        target_flux = self.synphot_ccd_lam(wave, flux, band)
        vega_mag = -2.5 * np.log10(target_flux.to_value(u.W/u.m/u.m/u.nm)) + self.vega_syn_zp[band]
        return vega_mag