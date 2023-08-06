from .gmie import lngmie, dlngmie_drho, d2lngmie_drho


def achain(x0, eta, x0_a1, a1sb_a1, da1m_deta, x03, nsigma, alpha, tetha,
           x0_a2, a1sb_a2, da2m_new_deta, khs, d, deta_drho, rho, beta, eps,
           c, ms, ring):
    lng = lngmie(x0, eta, x0_a1, a1sb_a1, da1m_deta, x03, nsigma, alpha, tetha,
                 x0_a2, a1sb_a2, da2m_new_deta, khs, d, deta_drho, rho, beta,
                 eps, c, ms)
    ac = - (ms - 1. + ring*eta)*lng
    return ac


def dachain_drho(x0, eta, x0_a1, a1sb_a1, da1m_deta, x03, nsigma, alpha, tetha,
                 x0_a2, a1sb_a2, da2m_new_deta, khs, d, deta_drho, rho, beta,
                 eps, c, ms, ring):
    dlng = dlngmie_drho(x0, eta, x0_a1, a1sb_a1, da1m_deta, x03, nsigma, alpha,
                        tetha, x0_a2, a1sb_a2, da2m_new_deta, khs, d,
                        deta_drho, rho, beta, eps, c, ms)
    dac = - (ms - 1. + ring*eta)*dlng
    return dac


def d2achain_drho(x0, eta, x0_a1, a1sb_a1, da1m_deta, x03, nsigma, alpha,
                  tetha, x0_a2, a1sb_a2, da2m_new_deta, khs, d, deta_drho, rho,
                  beta, eps, c, ms, ring):
    d2lng = d2lngmie_drho(x0, eta, x0_a1, a1sb_a1, da1m_deta, x03, nsigma,
                          alpha, tetha, x0_a2, a1sb_a2, da2m_new_deta, khs,
                          d, deta_drho, rho, beta, eps, c, ms)
    d2ac = - (ms - 1. + ring*eta)*d2lng
    return d2ac
