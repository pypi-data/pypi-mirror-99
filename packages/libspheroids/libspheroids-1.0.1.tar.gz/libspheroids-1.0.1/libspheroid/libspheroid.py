import _libspheroid as lsd

__ALL__=['SpheroidCalc','lsd']

class SpheroidCalc(object):
    def __init__(self, input_fname):
        self.input_fname = input_fname
        # читаем файл с настройками
        lsd.dls_read_input(input_fname)
        # выделяем памят для хранения промежуточных массивов
        lsd.alloc_dls_array(lsd.mo_dls.key,
                                     lsd.mo_dls.keyel, 1)
    def finalize(self):
        lsd.alloc_dls_array(lsd.mo_dls.key,
                                     lsd.mo_dls.keyel, 2)
    
    def set_refr_index(self, m):
        lsd.mo_dls.rn.flat[0] = m.real
        lsd.mo_dls.rk.flat[0] = m.imag
    
    def get_refr_index(self):
        m = complex(lsd.mo_dls.rn.flat[0], lsd.mo_dls.rk.flat[0])
        return m
    
    def set_wvl(self, wvl):
        lsd.mo_dls.wl = wvl
    
    def get_wvl(self):
        wvl = float(lsd.mo_dls.wl)
        return wvl
    
    def get_knots_count(self):
        return int(lsd.mo_dls.kn)
    
    def set_knots_count(self, knots_count):
        lsd.mo_dls.kn = knots_count
    
    def set_radii(self, rr):
        kn = len(rr)
        self.knots_count = kn
        lsd.mo_dls.rrr[:kn] = rr[:]
        
    def set_sd(self, sd):
        kn = len(sd)
        if kn!= self.knots_count:
            raise Exception("Invalid SD len")
        
        lsd.mo_dls.sd[:kn] = sd[:]
        
    def get_radii(self):
        return lsd.mo_dls.rrr[:self.knots_count]
    
    def get_sd(self):
        return lsd.mo_dls.sd[:self.knots_count]
    
    def set_psd(self, psd):
        try:
            rr, SD = psd
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        else:
            self.radii = rr
            self.sd = SD
    
    def get_psd(self):
        return self.radii, self.sd
    
    def calc(self):
        lsd.optchar(lsd.mo_dls.ndp)
    
    def get_ext(self):
        return float(lsd.mo_dls.xext)
    
    def get_sca(self):
        return float(lsd.mo_dls.xsca)
    
    def get_abs(self):
        return float(lsd.mo_dls.xabs)
    
    def get_lbr(self):
        return float(lsd.mo_dls.xblr)
    
    def get_ldr(self):
        return float(lsd.mo_dls.xldr)

    psd = property(get_psd, set_psd)
    radii = property(get_radii, set_radii)
    sd = property(get_sd, set_sd)
    midx = property(get_refr_index, set_refr_index)
    wvl  = property(get_wvl, set_wvl)
    knots_count = property(get_knots_count, set_knots_count)
    ext = property(get_ext)
    sca = property(get_sca)
    absb = property(get_abs)
    lbr = property(get_lbr)
    ldr = property(get_ldr)