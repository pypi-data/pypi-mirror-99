# pylint: disable=invalid-name
# pylint: disable=unused-argument
# pylint: disable=too-many-locals
# pylint: disable=no-member
# pylint: disable=bare-except

"""
Mie scattering calculations for perfect spheres.

Extensive documentation is at <https://miepython.readthedocs.io>

`miepython` is a pure Python module to calculate light scattering of
a plane wave by non-absorbing, partially-absorbing, or perfectly conducting
spheres.

The extinction efficiency, scattering efficiency, backscattering, and
scattering asymmetry for a sphere with complex index of refraction m,
diameter d, and wavelength lambda can be found by::

    qext, qsca, qback, g = miepython.ez_mie(m, d, lambda0)

The normalized scattering values for angles mu=cos(theta) are::

    Ipar, Iper = miepython.ez_intensities(m, d, lambda0, mu)

If the size parameter is known, then use::

    miepython.mie(m, x)

Mie scattering amplitudes S1 and S2 (complex numbers):

    miepython.mie_S1_S2(m, x, mu)

Normalized Mie scattering intensities for angles mu=cos(theta)::

    miepython.i_per(m, x, mu)
    miepython.i_par(m, x, mu)
    miepython.i_unpolarized(m, x, mu)
"""

import numpy as np

__all__ = ('ez_mie',
           'ez_intensities',
           'generate_mie_costheta',
           'i_par',
           'i_per',
           'i_unpolarized',
           'mie',
           'mie_S1_S2',
           'mie_cdf',
           'mie_mu_with_uniform_cdf',
           )


def _Lentz_Dn(z, N):
    """
    Compute the logarithmic derivative of the Ricatti-Bessel function.

    Args:
        z: function argument
        N: order of Ricatti-Bessel function

    Returns:
        This returns the Ricatti-Bessel function of order N with argument z
        using the continued fraction technique of Lentz, Appl. Opt., 15,
        668-671, (1976).
    """
    zinv = 2.0 / z
    alpha = (N + 0.5) * zinv
    aj = -(N + 1.5) * zinv
    alpha_j1 = aj + 1 / alpha
    alpha_j2 = aj
    ratio = alpha_j1 / alpha_j2
    runratio = alpha * ratio

    while abs(abs(ratio) - 1.0) > 1e-12:
        aj = zinv - aj
        alpha_j1 = 1.0 / alpha_j1 + aj
        alpha_j2 = 1.0 / alpha_j2 + aj
        ratio = alpha_j1 / alpha_j2
        zinv *= -1
        runratio = ratio * runratio

    return -N / z + runratio


def _D_downwards(z, N):
    """
    Compute the logarithmic derivative by downwards recurrence.

    Args:
        z: function argument
        N: order of Ricatti-Bessel function

    Returns:
        All the Ricatti-Bessel function values for orders from 0 to N for an
        argument z using the downwards recurrence relations.
    """
    D = np.zeros(N, dtype=complex)
    last_D = _Lentz_Dn(z, N)
    for n in range(N, 0, -1):
        last_D = n / z - 1.0 / (last_D + n / z)
        D[n - 1] = last_D
    return D


def _D_upwards(z, N):
    """
    Compute the logarithmic derivative by upwards recurrence.

    Args:
        z: function argument
        N: order of Ricatti-Bessel function

    Returns:
        All the Ricatti-Bessel function values for orders from 0 to N for an
        argument z using the upwards recurrence relations.
    """
    D = np.zeros(N, dtype=complex)
    exp = np.exp(-2j * z)
    D[1] = -1 / z + (1 - exp) / ((1 - exp) / z - 1j * (1 + exp))
    for n in range(2, N):
        D[n] = 1 / (n / z - D[n - 1]) - n / z
    return D


def _D_calc(m, x, N):
    """
    Compute the logarithmic derivative using best method.

    Args:
        m: the complex index of refraction of the sphere
        x: the size parameter of the sphere
        N: order of Ricatti-Bessel function

    Returns:
        The values of the Ricatti-Bessel function for orders from 0 to N.
    """
    n = m.real
    kappa = abs(m.imag)

    if n < 1 or n > 10 or kappa > 10 or x*kappa >= 3.9 - 10.8 * n + 13.78 * n**2:
        return _D_downwards(m*x, N)

    return _D_upwards(m*x, N)


def _mie_An_Bn(m, x):
    """
    Compute arrays of Mie coefficients A and B for a sphere.

    This estimates the size of the arrays based on Wiscombe's formula. The length
    of the arrays is chosen so that the error when the series are summed is
    around 1e-6.

    Args:
        m: the complex index of refraction of the sphere
        x: the size parameter of the sphere

    Returns:
        An, Bn: arrays of Mie coefficents
    """
    nstop = int(x + 4.05 * x**0.33333 + 2.0) + 1

    if m.real > 0.0:
        D = _D_calc(m, x, nstop + 1)

    a = np.zeros(nstop - 1, dtype=complex)
    b = np.zeros(nstop - 1, dtype=complex)

    psi_nm1 = np.sin(x)                   # nm1 = n-1 = 0
    psi_n = psi_nm1 / x - np.cos(x)       # n = 1
    xi_nm1 = complex(psi_nm1, np.cos(x))
    xi_n = complex(psi_n, np.cos(x) / x + np.sin(x))

    for n in range(1, nstop):
        if m.real == 0.0:
            a[n - 1] = (n * psi_n / x - psi_nm1) / (n * xi_n / x - xi_nm1)
            b[n - 1] = psi_n / xi_n
        else:
            temp = D[n] / m + n / x
            a[n - 1] = (temp * psi_n - psi_nm1) / (temp * xi_n - xi_nm1)
            temp = D[n] * m + n / x
            b[n - 1] = (temp * psi_n - psi_nm1) / (temp * xi_n - xi_nm1)

        xi = (2 * n + 1) * xi_n / x - xi_nm1
        xi_nm1 = xi_n
        xi_n = xi
        psi_nm1 = psi_n
        psi_n = xi_n.real

    return [a, b]


def _small_conducting_mie(m, x):
    """
    Calculate the efficiencies for a small conducting spheres.

    Typically used for small conducting spheres where x < 0.1 and
    m.real == 0

    Args:
        m: the complex index of refraction of the sphere
        x: the size parameter of the sphere

    Returns:
        qext: the total extinction efficiency
        qsca: the scattering efficiency
        qback: the backscatter efficiency
        g: the average cosine of the scattering phase function
    """
    ahat1 = complex(0, 2.0 / 3.0 * (1 - 0.2 * x**2)) / \
        complex(1 - 0.5 * x**2, 2.0 / 3.0 * x**3)
    bhat1 = complex(0.0, (x**2 - 10.0) / 30.0) / \
        complex(1 + 0.5 * x**2, -x**3 / 3.0)
    ahat2 = complex(0.0, x**2 / 30.)
    bhat2 = complex(0.0, -x**2 / 45.)

    qsca = x**4 * (6 * abs(ahat1)**2 + 6 * abs(bhat1)**2 + 10 * abs(ahat2)**2 +
                   10 * abs(bhat2)**2)
    qext = qsca
    g = ahat1.imag * (ahat2.imag + bhat1.imag)
    g += bhat2.imag * (5.0 / 9.0 * ahat2.imag + bhat1.imag)
    g += ahat1.real * bhat1.real
    g *= 6 * x**4 / qsca

    qback = 9 * x**4 * abs(ahat1 - bhat1 - 5 / 3 * (ahat2 - bhat2))**2

    return [qext, qsca, qback, g]


def _small_mie(m, x):
    """
    Calculate the efficiencies for a small sphere.

    Typically used for small spheres where x<0.1

    Args:
        m: the complex index of refraction of the sphere
        x: the size parameter of the sphere

    Returns:
        qext: the total extinction efficiency
        qsca: the scattering efficiency
        qback: the backscatter efficiency
        g: the average cosine of the scattering phase function
    """
    m2 = m * m
    x2 = x * x

    D = m2 + 2 + (1 - 0.7 * m2) * x2 - (8 * m**4 - 385 * m2 + 350) * x**4 / 1400.0 + \
        2j * (m2 - 1) * x**3 * (1 - 0.1 * x2) / 3
    ahat1 = 2j * (m2 - 1) / 3 * (1 - 0.1 * x2 + (4 * m2 + 5) * x**4 / 1400) / D
    bhat1 = 1j * x2 * (m2 - 1) / 45 * (1 + (2 * m2 - 5) /
                                       70 * x2) / (1 - (2 * m2 - 5) / 30 * x2)
    ahat2 = 1j * x2 * (m2 - 1) / 15 * (1 - x2 / 14) / \
        (2 * m2 + 3 - (2 * m2 - 7) / 14 * x2)

    T = abs(ahat1)**2 + abs(bhat1)**2 + 5 / 3 * abs(ahat2)**2
    temp = ahat2 + bhat1
    g = (ahat1 * temp.conjugate()).real / T

    qsca = 6 * x**4 * T

    if m.imag == 0:
        qext = qsca
    else:
        qext = 6 * x * (ahat1 + bhat1 + 5 * ahat2 / 3).real

    sback = 1.5 * x**3 * (ahat1 - bhat1 - 5 * ahat2 / 3)
    qback = 4*abs(sback)**2/x2

    return [qext, qsca, qback, g]


def _mie_scalar(m, x):
    """
    Calculate the efficiencies for a sphere when both m and x are scalars.

    Args:
        m: the complex index of refraction of the sphere
        x: the size parameter of the sphere

    Returns:
        qext: the total extinction efficiency
        qsca: the scattering efficiency
        qback: the backscatter efficiency
        g: the average cosine of the scattering phase function
    """
    if m.real == 0 and x < 0.1:
        return _small_conducting_mie(m, x)

    if m.real > 0.0 and abs(m) * x < 0.1:
        return _small_mie(m, x)

    a, b = _mie_An_Bn(m, x)

    nmax = len(a)
    n = np.arange(1, nmax + 1)
    cn = 2.0 * n + 1.0

    qext = 2 * np.sum(cn * (a.real + b.real)) / x**2
    qsca = qext

    if m.imag != 0:
        qsca = 2 * np.sum(cn * (abs(a)**2 + abs(b)**2)) / x**2

    qback = abs(np.sum((-1)**n * cn * (a - b)))**2 / x**2

    c1n = n * (n + 2) / (n + 1)
    c2n = cn / n / (n + 1)
    g = 0
    for i in range(nmax - 1):
        asy1 = c1n[i] * (a[i] * a[i + 1].conjugate() +
                         b[i] * b[i + 1].conjugate()).real
        asy2 = c2n[i] * (a[i] * b[i].conjugate()).real
        g += 4 * (asy1 + asy2) / qsca / x**2

    return [qext, qsca, qback, g]


def mie(m, x):
    """
    Calculate the efficiencies for a sphere where m or x may be arrays.

    Args:
        m: the complex index of refraction of the sphere
        x: the size parameter of the sphere

    Returns:
        qext: the total extinction efficiency
        qsca: the scattering efficiency
        qback: the backscatter efficiency
        g: the average cosine of the scattering phase function
    """
    try:
        mlen = len(m)
    except:
        mlen = 0
        mm = m

    try:
        xlen = len(x)
    except:
        xlen = 0
        xx = x

    if xlen == 0 and mlen == 0:
        return _mie_scalar(mm, xx)

    if xlen and mlen and xlen != mlen:
        raise RuntimeError('m and x arrays to mie must be same length')

    thelen = max(xlen, mlen)
    qext = np.empty(thelen)
    qsca = np.empty(thelen)
    qback = np.empty(thelen)
    g = np.empty(thelen)

    for i in range(thelen):
        if mlen > 0:
            mm = m[i]

        if xlen > 0:
            xx = x[i]

        qext[i], qsca[i], qback[i], g[i] = _mie_scalar(mm, xx)

    return qext, qsca, qback, g


def _small_mie_conducting_S1_S2(m, x, mu):
    """
    Calculate the scattering amplitudes for small conducting spheres.

    The spheres are small perfectly conducting (reflecting) spheres (x<0.1).
    The amplitude functions have been normalized so that when integrated
    over all 4𝜋 solid angles, the integral will be qext(𝜋x²).

    The units are weird, sr**(-0.5)

    Args:
        m: the complex index of refraction of the sphere
        x: the size parameter of the sphere
        mu: the angles, cos(theta), to calculate scattering amplitudes

    Returns:
        S1, S2: the scattering amplitudes at each angle mu [sr**(-0.5)]
    """
    ahat1 = 2j / 3 * (1 - 0.2 * x**2) / (1 - 0.5 * x**2 + 2j / 3 * x**3)
    bhat1 = 1j / 3 * (0.1 * x**2 - 1) / (1 + 0.5 * x**2 - 1j / 3 * x**3)
    ahat2 = 1j / 30 * x**2
    bhat2 = -1j * x**2 / 45

    S1 = 1.5 * x**3 * (ahat1 + bhat1 * mu + 5 / 3 * ahat2 *
                       mu + 5 / 3 * bhat2 * (2 * mu**2 - 1))
    S2 = 1.5 * x**3 * (bhat1 + ahat1 * mu + 5 / 3 * bhat2 *
                       mu + 5 / 3 * ahat2 * (2 * mu**2 - 1))

    qext = x**4 * (6 * abs(ahat1)**2 + 6 * abs(bhat1)**2 + 10 * abs(ahat2)**2 +
                   10 * abs(bhat2)**2)
    norm = np.sqrt(qext * np.pi * x**2)
    S1 /= norm
    S2 /= norm

    return [S1, S2]


def _small_mie_S1_S2(m, x, mu):
    """
    Calculate the scattering amplitude functions for small spheres (x<0.1).

    The amplitude functions have been normalized so that when integrated
    over all 4*pi solid angles, the integral will be qext*pi*x**2.

    The units are weird, sr**(-0.5)

    Args:
        m: the complex index of refraction of the sphere
        x: the size parameter of the sphere
        mu: the angles, cos(theta), to calculate scattering amplitudes

    Returns:
        S1, S2: the scattering amplitudes at each angle mu [sr**(-0.5)]
    """
    m2 = m * m
    m4 = m2 * m2
    x2 = x * x
    x3 = x2 * x
    x4 = x2 * x2

    D = m2 + 2 + (1 - 0.7 * m2) * x2 - (8 * m4 - 385 * m2 + 350) * x4 / 1400.0 + \
        2j * (m2 - 1) * x3 * (1 - 0.1 * x2) / 3
    ahat1 = 2j * (m2 - 1) / 3 * (1 - 0.1 * x2 + (4 * m2 + 5) * x4 / 1400) / D
    bhat1 = 1j * x2 * (m2 - 1) / 45 * (1 + (2 * m2 - 5) /
                                       70 * x2) / (1 - (2 * m2 - 5) / 30 * x2)
    ahat2 = 1j * x2 * (m2 - 1) / 15 * (1 - x2 / 14) / \
        (2 * m2 + 3 - (2 * m2 - 7) / 14 * x2)

    S1 = 1.5 * x3 * (ahat1 + bhat1 * mu + 5 / 3 * ahat2 * mu)
    S2 = 1.5 * x3 * (bhat1 + ahat1 * mu + 5 / 3 * ahat2 * (2 * mu**2 - 1))

    # norm = sqrt(qext*pi*x**2)
    norm = np.sqrt(np.pi * 6 * x**3 * (ahat1 + bhat1 + 5 * ahat2 / 3).real)
    S1 /= norm
    S2 /= norm

    return [S1, S2]


def mie_S1_S2(m, x, mu):
    """
    Calculate the scattering amplitude functions for spheres.

    The amplitude functions have been normalized so that when integrated
    over all 4*pi solid angles, the integral will be qext*pi*x**2.

    The units are weird, sr**(-0.5)

    Args:
        m: the complex index of refraction of the sphere
        x: the size parameter of the sphere
        mu: the angles, cos(theta), to calculate scattering amplitudes

    Returns:
        S1, S2: the scattering amplitudes at each angle mu [sr**(-0.5)]
    """
    a, b = _mie_An_Bn(m, x)

    nangles = len(mu)
    S1 = np.zeros(nangles, dtype=complex)
    S2 = np.zeros(nangles, dtype=complex)

    nstop = len(a)
    for k in range(nangles):
        pi_nm2 = 0
        pi_nm1 = 1
        for n in range(1, nstop):
            tau_nm1 = n * mu[k] * pi_nm1 - (n + 1) * pi_nm2
            S1[k] += (2 * n + 1) * (pi_nm1 * a[n - 1] +
                                    tau_nm1 * b[n - 1]) / (n + 1) / n
            S2[k] += (2 * n + 1) * (tau_nm1 * a[n - 1] +
                                    pi_nm1 * b[n - 1]) / (n + 1) / n

            temp = pi_nm1
            pi_nm1 = ((2 * n + 1) * mu[k] * pi_nm1 - (n + 1) * pi_nm2) / n
            pi_nm2 = temp

    # calculate norm = sqrt(pi * Qext * x**2)
    n = np.arange(1, nstop + 1)
    norm = np.sqrt(2 * np.pi * np.sum((2 * n + 1) * (a.real + b.real)))

    S1 /= norm
    S2 /= norm

    return [S1, S2]


def mie_cdf(m, x, num):
    """
    Create a CDF for unpolarized scattering uniformly spaced in cos(theta).

    The CDF covers scattered (exit) angles ranging from 180 to 0 degrees.
    (The cosines are uniformly distributed over -1 to 1.) Because the angles
    are uniformly distributed in cos(theta), the scattering function is not
    sampled uniformly and therefore huge array sizes are needed to adequately
    sample highly anisotropic phase functions.

    Since this is a cumulative distribution function, the maximum value
    should be 1.

    Args:
        m: the complex index of refraction of the sphere
        x: the size parameter of the sphere
        num: length of desired CDF array

    Returns:
        mu: array of cosines of angles
        cdf: array of cumulative distribution function values
    """
    mu = np.linspace(-1, 1, num)
    s1, s2 = mie_S1_S2(m, x, mu)

    s = (abs(s1)**2 + abs(s2)**2) / 2

    cdf = np.zeros(num)
    total = 0
    for i in range(num):
        # need the extra 2pi because scattering normalized over 4π steradians
        total += s[i] * 2 * np.pi * (2 / num)
        cdf[i] = total

    return mu, cdf


def mie_mu_with_uniform_cdf(m, x, num):
    """
    Create a CDF for unpolarized scattering for uniform CDF.

    The CDF covers scattered (exit) angles ranging from 180 to 0 degrees.
    (The cosines are uniformly distributed over -1 to 1.) These angles mu
    correspond to uniform spacing of the cumulative distribution function
    for unpolarized Mie scattering where cdf[i] = i/(num-1).

    This is a brute force implementation that solves the problem by
    calculating the CDF at many points and then scanning to find the
    specific angles that correspond to uniform interval of the CDF.

    Since this is a cumulative distribution function, the maximum value
    should be 1.

    Args:
        m: the complex index of refraction of the sphere
        x: the size parameter of the sphere
        num: length of desired CDF array

    Returns:
        mu: array of cosines of angles (irregularly spaced)
        cdf: array of cumulative distribution function values
    """
    big_num = 2000                  # large to work with x up to 10
    big_mu, big_cdf = mie_cdf(m, x, big_num)
    mu = np.empty(num)
    cdf = np.empty(num)

    mu[0] = -1                       # cos[180 degrees] is -1
    cdf[0] = 0                       # initial cdf is zero

    big_k = 0                        # index into big_cdf
    for k in range(1, num - 1):

        target = k / (num - 1)
        while big_cdf[big_k] < target:
            big_k += 1

        delta = big_cdf[big_k] - target
        delta_cdf = big_cdf[big_k] - big_cdf[big_k - 1]
        delta_mu = big_mu[big_k] - big_mu[big_k - 1]

        mu[k] = big_mu[big_k] - delta / delta_cdf * delta_mu   # interpolate
        cdf[k] = target

#       print(' mu[',k,']=% .5f'%mu[k],' cdf[',k,']=% .5f'%cdf[k],
#       'cdf=',big_cdf[big_k], fraction)

    mu[num - 1] = 1                    # cos[0 degrees] is 1
    cdf[num - 1] = 1                   # last cdf is one

    return [mu, cdf]


def generate_mie_costheta(mu_cdf):
    """
    Generate a new scattering angle using a cdf.

    A uniformly spaced cumulative distribution function (CDF) is needed.
    New random angles are generated by selecting a random interval
    mu[i] to mu[i+1] and choosing an angle uniformly distributed over
    the interval.

    Args:
       mu_cdf: a cumulative distribution function

    Returns
       The cosine of the scattering angle
    """
    # the following should be equivalent to these four lines
    # index = np.random.randint(0, high=len(mu_cdf))
    num = len(mu_cdf) - 1
    index = int(np.random.random() * num)
    if index >= num:
        index = num - 1

    x = mu_cdf[index]
    x += (mu_cdf[index + 1] - mu_cdf[index]) * np.random.random()

    return x


def i_per(m, x, mu):
    """
    Return the scattered intensity in a plane normal to the incident light.

    This is the scattered intensity in a plane that is perpendicular to the
    field of the incident plane wave. The intensity is normalized such
    that the integral of the unpolarized intensity over 4π steradians
    is equal to the single scattering albedo.

    Args:
       m: the complex index of refraction of the sphere
       x: the size parameter of the sphere
       mu: the angles, cos(theta), to calculate intensities

    Returns
       The intensity at each angle in the array mu.  Units [1/sr]
    """
    s1, _ = mie_S1_S2(m, x, mu)
    intensity = abs(s1)**2
    return intensity.astype('float')


def i_par(m, x, mu):
    """
    Return the scattered intensity in a plane parallel to the incident light.

    This is the scattered intensity in a plane that is parallel to the
    field of the incident plane wave. The intensity is normalized such
    that the integral of the unpolarized intensity over 4π steradians
    is equal to the single scattering albedo.

    Args:
       m: the complex index of refraction of the sphere
       x: the size parameter
       mu: the cos(theta) of each direction desired

    Returns
       The intensity at each angle in the array mu.  Units [1/sr]
    """
    _, s2 = mie_S1_S2(m, x, mu)
    intensity = abs(s2)**2
    return intensity.astype('float')


def i_unpolarized(m, x, mu):
    """
    Return the unpolarized scattered intensity at specified angles.

    This is the average value for randomly polarized incident light.
    The intensity is normalized such
    that the integral of the unpolarized intensity over 4π steradians
    is equal to the single scattering albedo.

    Args:
       m: the complex index of refraction of the sphere
       x: the size parameter
       mu: the cos(theta) of each direction desired

    Returns
       The intensity at each angle in the array mu.  Units [1/sr]
    """
    s1, s2 = mie_S1_S2(m, x, mu)
    intensity = (abs(s1)**2 + abs(s2)**2) / 2
    return intensity.astype('float')


def ez_mie(m, d, lambda0, n_env=1.0):
    """
    Calculate the efficiencies of a sphere.

    Args:
        m: the complex index of refraction of the sphere [-]
        d: the diameter of the sphere                    [same units as lambda0]
        lambda0: wavelength in a vacuum                  [same units as d]
        n_env: real index of medium around sphere        [-]

    Returns:
        qext: the total extinction efficiency                  [-]
        qsca: the scattering efficiency                        [-]
        qback: the backscatter efficiency                      [-]
        g: the average cosine of the scattering phase function [-]
    """
    m_env = m / n_env
    x_env = np.pi*d/(lambda0/n_env)
    return mie(m_env, x_env)


def ez_intensities(m, d, lambda0, mu, n_env=1.0):
    """
    Return the scattered intensities from a sphere.

    These are the scattered intensities in a plane that is parallel (ipar) and
    perpendicular (iper) to the field of the incident plane wave.

    The scattered intensity is normalized such that the integral of the
    unpolarized intensity over 4𝜋 steradians is equal to the single scattering
    albedo.  The scattered intensity has units of inverse steradians [1/sr].

    The unpolarized scattering is the average of the two scattered intensities.

    Args:
        m: the complex index of refraction of the sphere [-]
        d: the diameter of the sphere                    [same units as lambda0]
        lambda0: wavelength in a vacuum                  [same units as d]
        mu: the cos(theta) of each direction desired     [-]
        n_env: real index of medium around sphere        [-]

    Returns:
        ipar, iper: scattered intensity in parallel and perpendicular planes [1/sr]
    """
    m_env = m / n_env
    lambda_env = lambda0 / n_env
    x_env = np.pi*d/lambda_env
    s1, s2 = mie_S1_S2(m_env, x_env, mu)
    ipar = abs(s2)**2
    iper = abs(s1)**2
    Ipar = ipar.astype('float')
    Iper = iper.astype('float')
    return Ipar, Iper
