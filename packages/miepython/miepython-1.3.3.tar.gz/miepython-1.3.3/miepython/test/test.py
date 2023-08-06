#! /usr/bin/env python3

"""
Copyright 2017-19 Scott Prahl

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import unittest
import numpy as np
import miepython

# the low level tests use functions that should not be exported.  These work
# but now that the higher level tests pass, these are skipped

# class low_level(unittest.TestCase):
# 
#     def test_01_log_derivatives(self):
#         m = 1.0
#         x = 1.0
#         nstop = 10
#         dn = miepython._D_calc(m,x,nstop)
#         self.assertAlmostEqual(dn[9].real, 9.95228198, delta=0.00001)
# 
#         x = 62
#         m = 1.28 - 1.37j
#         nstop = 50
#         dn = _D_calc(m,x,nstop)
#         self.assertAlmostEqual(dn[10].real, 0.004087, delta=0.00001)
#         self.assertAlmostEqual(dn[10].imag, 1.0002620, delta=0.00001)
# 
#     def test_02_an_bn(self):
#         m = 4.0/3.0
#         x = 50
#         a, b = miepython.mie_An_Bn(m,x)
# #        print(a)
#     #        self.assertAlmostEqual(a[0].real, 0.5311058892948411929, delta=0.00000001)
#     #        self.assertAlmostEqual(a[1].imag,-0.4990314856310943073, delta=0.00000001)
#     #        self.assertAlmostEqual(b[1].real, 0.093412567968, delta=0.00001)
#     #        self.assertAlmostEqual(b[1].imag,-0.067160541299, delta=0.00001)
# 
#         m = 1.5-1.1j
#         x = 2
#         a, b = miepython.mie_An_Bn(m,x)
#         self.assertAlmostEqual(a[0].real, 0.555091767665, delta=0.00001)
#         self.assertAlmostEqual(a[0].imag, 0.158587776121, delta=0.00001)
#         self.assertAlmostEqual(a[1].real, 0.386759705234, delta=0.00001)
#         self.assertAlmostEqual(a[1].imag, 0.076275273072, delta=0.00001)
#         self.assertAlmostEqual(b[1].real, 0.093412567968, delta=0.00001)
#         self.assertAlmostEqual(b[1].imag,-0.067160541299, delta=0.00001)
# 
#         m = 1.1-25j
#         x = 2
#         a, b = miepython.mie_An_Bn(m,x)
#         self.assertAlmostEqual(a[1].real, 0.324433578437, delta=0.0001)
#         self.assertAlmostEqual(a[1].imag, 0.465627763266, delta=0.0001)
#         self.assertAlmostEqual(b[1].real, 0.060464399088, delta=0.0001)
#         self.assertAlmostEqual(b[1].imag,-0.236805417045, delta=0.0001)


class non_absorbing(unittest.TestCase):

    def test_03_bh_dielectric(self):
        m = 1.55
        lambda0 = 0.6328
        radius = 0.525
        x = 2*np.pi*radius/lambda0
        qext, qsca, qback, g = miepython.mie(m,x)

        self.assertAlmostEqual(qext, 3.10543, delta=0.00001)
        self.assertAlmostEqual(qsca, 3.10543, delta=0.00001)
        self.assertAlmostEqual(qback,2.92534, delta=0.00001)
        self.assertAlmostEqual(g    ,0.63314, delta=0.00001)

    def test_05_wiscombe_non_absorbing(self):

		# MIEV0 Test Case 5
        m=complex(0.75, 0.0)
        x=0.099
        s1 = 1.81756e-8 - 1.64810e-4 * 1j
        G=abs(2*s1/x)**2
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 0.000007, delta=1e-6)
        self.assertAlmostEqual(g,    0.001448, delta=1e-6)
        self.assertAlmostEqual(qback, G, delta=1e-6)

		# MIEV0 Test Case 6
        m=complex(0.75, 0.0)
        x=0.101
        s1 = 2.04875E-08  -1.74965E-04 * 1j
        G=abs(2*s1/x)**2
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 0.000008, delta=1e-6)
        self.assertAlmostEqual(g,    0.001507, delta=1e-6)
        self.assertAlmostEqual(qback, G, delta=1e-6)

		# MIEV0 Test Case 7
        m=complex(0.75, 0.0)
        x=10.0
        s1 = -1.07857E+00  -3.60881E-02 * 1j
        G=abs(2*s1/x)**2
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 2.232265, delta=1e-6)
        self.assertAlmostEqual(g,    0.896473, delta=1e-6)
        self.assertAlmostEqual(qback, G, delta=1e-6)

		# MIEV0 Test Case 8
        m=complex(0.75, 0.0)
        x=1000.0
        s1= 1.70578E+01 + 4.84251E+02  *1j
        G=abs(2*s1/x)**2
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 1.997908, delta=1e-6)
        self.assertAlmostEqual(g,    0.844944, delta=1e-6)
        self.assertAlmostEqual(qback, G, delta=1e-6)

    def test_05_old_wiscombe_non_absorbing(self):

		# OLD MIEV0 Test Case 1
        m=complex(1.5, 0.0)
        x=10
        s1 = 4.322E+00 + 4.868E+00 * 1j
        G=abs(2*s1/x)**2
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 2.8820, delta=1e-4)
        self.assertAlmostEqual(qback, G, delta=1e-4)

		# OLD MIEV0 Test Case 2
        m=complex(1.5, 0.0)
        x=100
        s1 = 4.077E+01 + 5.175E+01  * 1j
        G=abs(2*s1/x)**2
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 2.0944, delta=1e-4)
        self.assertAlmostEqual(qback, G, delta=1e-4)

		# OLD MIEV0 Test Case 3
        m=complex(1.5, 0.0)
        x=1000
        G= 4 * 2.576E+06 / x**2
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 2.0139, delta=1e-4)
        self.assertAlmostEqual(qback, G, delta=1e-3)

		# OLD MIEV0 Test Case 4
        m=complex(1.5, 0.0)
        x=5000.0
        G= 4 * 2.378E+08 / x**2
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 2.0086, delta=1e-4)
        self.assertAlmostEqual(qback, G, delta=3e-3)

    def test_04_non_dielectric(self):
        m = 1.55-0.1j
        lambda0 = 0.6328
        radius = 0.525
        x = 2*np.pi*radius/lambda0
        qext, qsca, qback, g = miepython.mie(m,x)

        self.assertAlmostEqual(qext, 2.86165188243, delta=1e-7)
        self.assertAlmostEqual(qsca, 1.66424911991, delta=1e-7)
        self.assertAlmostEqual(qback,0.20599534080, delta=1e-7)
        self.assertAlmostEqual(g,    0.80128972639, delta=1e-7)

class absorbing(unittest.TestCase):
    def test_06_wiscombe_water_absorbing(self):

        #MIEV0 Test Case 9
        m=complex(1.33, -0.00001)
        x=1.0
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 0.093923, delta=1e-6)
        self.assertAlmostEqual(g,    0.184517, delta=1e-6)

        #MIEV0 Test Case 10
        m=complex(1.33, -0.00001)
        x=100.0
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 2.096594, delta=1e-6)
        self.assertAlmostEqual(g,    0.868959, delta=1e-6)

        #MIEV0 Test Case 11
        m=complex(1.33, -0.00001)
        x=10000.0
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(g,    0.907840, delta=1e-6)
        self.assertAlmostEqual(qsca, 1.723857, delta=1e-6)

    def test_07_wiscombe_absorbing(self):

        #MIEV0 Test Case 12
        m = 1.5-1j
        x = 0.055
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 0.000011, delta=1e-6)
        self.assertAlmostEqual(g,    0.000491, delta=1e-6)

        #MIEV0 Test Case 13
        m = 1.5-1j
        x = 0.056
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 0.000012, delta=1e-6)
        self.assertAlmostEqual(g,    0.000509, delta=1e-6)

        #MIEV0 Test Case 14
        m = 1.5-1j
        x = 1
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 0.6634538, delta=1e-6)
        self.assertAlmostEqual(g,    0.192136, delta=1e-6)

        #MIEV0 Test Case 15
        m = 1.5-1j
        x = 100
        x=100.0
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 1.283697, delta=1e-3)
        self.assertAlmostEqual(qext, 2.097502, delta=1e-2)
        self.assertAlmostEqual(g,    0.850252, delta=1e-3)

        #MIEV0 Test Case 16
        m = 1.5-1j
        x = 10000
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 1.236575, delta=1e-6)
        self.assertAlmostEqual(qext, 2.004368, delta=1e-6)
        self.assertAlmostEqual(g,    0.846309, delta=1e-6)

    def test_08_wiscombe_more_absorbing(self):

        #MIEV0 Test Case 17
        m = 10.0 - 10.0j
        x = 1.0
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 2.049405, delta=1e-6)
        self.assertAlmostEqual(g,   -0.110664, delta=1e-6)

        #MIEV0 Test Case 18
        m = 10.0 - 10.0j
        x = 100.0
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 1.836785, delta=1e-6)
        self.assertAlmostEqual(g,    0.556215, delta=1e-6)

        #MIEV0 Test Case 19
        m = 10.0 - 10.0j
        x = 10000.0
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 1.795393, delta=1e-6)
        self.assertAlmostEqual(g,    0.548194, delta=1e-6)

    def test_09_single_nonmagnetic(self):
        m = 1.5-0.5j
        x = 2.5
        qext, qsca, qback, g = miepython.mie(m,x)

        self.assertAlmostEqual(qext, 2.562873497454734, delta=1e-7)
        self.assertAlmostEqual(qsca, 1.097071819088392, delta=1e-7)
        self.assertAlmostEqual(qback,0.123586468179818, delta=1e-7)
        self.assertAlmostEqual(g,    0.748905978948507, delta=1e-7)

class perfectly_reflecting(unittest.TestCase):

    def test_11_wiscombe_perfectly_reflecting(self):

		# MIEV0 Test Case 0
        m=0
        x=0.001
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 3.3333E-12, delta=1e-13)

		# MIEV0 Test Case 1
        m=0
        x=0.099
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 0.000321, delta=1e-4)
        self.assertAlmostEqual(g,   -0.397357, delta=1e-3)

		# MIEV0 Test Case 2
        m=0
        x=0.101
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 0.000348, delta=1e-6)
        self.assertAlmostEqual(g,   -0.397262, delta=1e-6)

		# MIEV0 Test Case 3
        m=0
        x=100
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 2.008102, delta=1e-6)
        self.assertAlmostEqual(g,    0.500926, delta=1e-6)

		# MIEV0 Test Case 4
        m=0
        x=10000
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qsca, 2.000289, delta=1e-6)
        self.assertAlmostEqual(g,    0.500070, delta=1e-6)

class small(unittest.TestCase):

    def test_10_small_spheres(self):
		# MIEV0 Test Case 5
        m = 0.75
        x = 0.099
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qext, 0.000007, delta=1e-6)
        self.assertAlmostEqual(g,    0.001448, delta=1e-6)

		# MIEV0 Test Case 6
        m = 0.75
        x=0.101
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qext, 0.000008, delta=1e-6)
        self.assertAlmostEqual(g,    0.001507, delta=1e-6)

        m = 1.5 -1j
        x = 0.055
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qext, 0.101491, delta=1e-6)
        self.assertAlmostEqual(g,    0.000491, delta=1e-6)
        x=0.056
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qext, 0.103347, delta=1e-6)
        self.assertAlmostEqual(g,    0.000509, delta=1e-6)

        m = 1e-10 - 1e10j
        x=0.099
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qext, 0.000321, delta=1e-6)
        self.assertAlmostEqual(g,   -0.397357, delta=1e-4)
        x=0.101
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qext, 0.000348, delta=1e-6)
        self.assertAlmostEqual(g,   -0.397262, delta=1e-6)

        m = 0 - 1e10j
        x=0.099
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qext, 0.000321, delta=1e-6)
        self.assertAlmostEqual(g,   -0.397357, delta=1e-4)
        x=0.101
        qext, qsca, qback, g = miepython.mie(m,x)
        self.assertAlmostEqual(qext, 0.000348, delta=1e-6)
        self.assertAlmostEqual(g,   -0.397262, delta=1e-4)  

class angle_scattering(unittest.TestCase):

    def test_12_scatter_function(self):
        x=1.0
        m=1.5-1.0j
        theta = np.arange(0,181,30)
        mu = np.cos(theta * np.pi/180)

        qext, qsca, qback, g = miepython.mie(m,x)
        S1, S2 = miepython.mie_S1_S2(m,x,mu)
        S1 *= np.sqrt(np.pi*x**2*qext)
        S2 *= np.sqrt(np.pi*x**2*qext)
        
        self.assertAlmostEqual(S1[0].real, 0.584080, delta=1e-6)
        self.assertAlmostEqual(S1[0].imag, 0.190515, delta=1e-6)
        self.assertAlmostEqual(S2[0].real, 0.584080, delta=1e-6)
        self.assertAlmostEqual(S2[0].imag, 0.190515, delta=1e-6)

        self.assertAlmostEqual(S1[1].real, 0.565702, delta=1e-6)
        self.assertAlmostEqual(S1[1].imag, 0.187200, delta=1e-6)
        self.assertAlmostEqual(S2[1].real, 0.500161, delta=1e-6)
        self.assertAlmostEqual(S2[1].imag, 0.145611, delta=1e-6)

        self.assertAlmostEqual(S1[2].real, 0.517525, delta=1e-6)
        self.assertAlmostEqual(S1[2].imag, 0.178443, delta=1e-6)
        self.assertAlmostEqual(S2[2].real, 0.287964, delta=1e-6)
        self.assertAlmostEqual(S2[2].imag, 0.041054, delta=1e-6)

        self.assertAlmostEqual(S1[3].real, 0.456340, delta=1e-6)
        self.assertAlmostEqual(S1[3].imag, 0.167167, delta=1e-6)
        self.assertAlmostEqual(S2[3].real, 0.0362285, delta=1e-6)
        self.assertAlmostEqual(S2[3].imag,-0.0618265, delta=1e-6)

        self.assertAlmostEqual(S1[4].real, 0.400212, delta=1e-6)
        self.assertAlmostEqual(S1[4].imag, 0.156643, delta=1e-6)
        self.assertAlmostEqual(S2[4].real,-0.174875, delta=1e-6)
        self.assertAlmostEqual(S2[4].imag,-0.122959, delta=1e-6)

        self.assertAlmostEqual(S1[5].real, 0.362157, delta=1e-6)
        self.assertAlmostEqual(S1[5].imag, 0.149391, delta=1e-6)
        self.assertAlmostEqual(S2[5].real,-0.305682, delta=1e-6)
        self.assertAlmostEqual(S2[5].imag,-0.143846, delta=1e-6)

        self.assertAlmostEqual(S1[6].real, 0.348844, delta=1e-6)
        self.assertAlmostEqual(S1[6].imag, 0.146829, delta=1e-6)
        self.assertAlmostEqual(S2[6].real,-0.348844, delta=1e-6)
        self.assertAlmostEqual(S2[6].imag,-0.146829, delta=1e-6)

if __name__ == '__main__':
    unittest.main()
