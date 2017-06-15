import numpy as np


from .. core.system_of_units_c import units
from .. reco                   import peak_functions as pf

class S12Selector:
    def __init__(self,
                 S1_Nmin     = 0,
                 S1_Nmax     = 1000,
                 S1_Emin     = 0,
                 S1_Emax     = np.inf,
                 S1_Lmin     = 0,
                 S1_Lmax     = np.inf,
                 S1_Hmin     = 0,
                 S1_Hmax     = np.inf,
                 S1_Ethr     = 0,

                 S2_Nmin     = 0,
                 S2_Nmax     = 1000,
                 S2_Emin     = 0,
                 S2_Emax     = np.inf,
                 S2_Lmin     = 0,
                 S2_Lmax     = np.inf,
                 S2_Hmin     = 0,
                 S2_Hmax     = np.inf,
                 S2_NSIPMmin = 1,
                 S2_NSIPMmax = np.inf,
                 S2_Ethr     = 0):

        self.S1_Nmin     = S1_Nmin
        self.S1_Nmax     = S1_Nmax
        self.S1_Emin     = S1_Emin
        self.S1_Emax     = S1_Emax
        self.S1_Lmin     = S1_Lmin
        self.S1_Lmax     = S1_Lmax
        self.S1_Hmin     = S1_Hmin
        self.S1_Hmax     = S1_Hmax
        self.S1_Ethr     = S1_Ethr

        self.S2_Nmin     = S2_Nmin
        self.S2_Nmax     = S2_Nmax
        self.S2_Emin     = S2_Emin
        self.S2_Emax     = S2_Emax
        self.S2_Lmin     = S2_Lmin
        self.S2_Lmax     = S2_Lmax
        self.S2_Hmin     = S2_Hmin
        self.S2_Hmax     = S2_Hmax
        self.S2_NSIPMmin = S2_NSIPMmin
        self.S2_NSIPMmax = S2_NSIPMmax
        self.S2_Ethr     = S2_Ethr

    def select_S1(self, s1s):
        return pf.select_peaks(s1s,
                               self.S1_Emin, self.S1_Emax,
                               self.S1_Lmin, self.S1_Lmax,
                               self.S1_Hmin, self.S1_Hmax,
                               self.S1_Ethr)

    def select_S2(self, s2s, sis):
        s2s = pf.select_peaks(s2s,
                              self.S2_Emin, self.S2_Emax,
                              self.S2_Lmin, self.S2_Lmax,
                              self.S2_Hmin, self.S2_Hmax,
                              self.S2_Ethr)
        sis = pf.select_Si(sis,
                           self.S2_NSIPMmin, self.S2_NSIPMmax)

        valid_peaks = set(s2s) & set(sis)
        s2s = {peak_no: peak for peak_no, peak in s2s.items() if peak_no in valid_peaks}
        sis = {peak_no: peak for peak_no, peak in sis.items() if peak_no in valid_peaks}
        return s2s, sis


def s1s2_filter(selector, s1s, s2s, sis):

    S1     = selector.select_S1(s1s)
    S2, Si = selector.select_S2(s2s, sis)

    return (selector.S1_Nmin <= len(S1) <= selector.S1_Nmax and
            selector.S2_Nmin <= len(S2) <= selector.S2_Nmax)
