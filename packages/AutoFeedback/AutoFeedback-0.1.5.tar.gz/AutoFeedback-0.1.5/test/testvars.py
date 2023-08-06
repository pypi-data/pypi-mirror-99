import unittest
import numpy as np

import AssCheck.varchecks as vc

class tmod:
    x = 3
    y = np.linspace(0,1,3)

class UnitTests(unittest.TestCase) :
    def test_exists(self):
        assert(vc.exists('x',modname=tmod))

    def test_notexists(self):
        assert( not vc.exists('z',modname=tmod))

    def test_size(self):
        assert(vc.check_size([1,2,3],[4,5,6]))

    def test_notsize(self):
        assert(not vc.check_size([1,2],[4,5,6]))

    def test_np_size(self):
        assert(vc.check_size([1,2,3],np.array([4,5,6])))
    
    def test_notnp_size(self):
        assert(not vc.check_size([1,2,3],np.array([4,5])))

    def test_single_value(self):
        assert(vc.check_value(1.0,10.0/10))
    
    def test_notsingle_value(self):
        assert(not vc.check_value(1.0,10./9))

    def test_np_value(self):
        assert(vc.check_value([1,2,3],np.array([1.0,2.0,3.0])))
    
    def test_notnp_value(self):
        assert(not vc.check_value([1,2,3],np.array([1.0,32.0,3.0])))

    def test_tol_value(self):
        assert(vc.check_value(1.0,0.999999999))

    def test_not_tol_value(self):
        assert(not vc.check_value(1.0,1.0001))

class SystemTests(unittest.TestCase):
    def test_mod_varx(self):
        assert(vc.check_vars('x',3,modname=tmod,output=False))

    def test_mod_vary(self):
        assert(vc.check_vars('y',[0,0.5,1.0],modname=tmod,output=False))

    def test_notmod_varx(self):
        assert(not vc.check_vars('x',[2,3],modname=tmod,output=False))

    def test_notmod_vary(self):
        assert(not vc.check_vars('y',[0.1,0.5,1.0],modname=tmod,output=False))

