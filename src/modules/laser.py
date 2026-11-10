import numpy as np
from scipy.integrate import solve_ivp
from core.constants import Q
class SemiconductorLaser:
    def __init__(self, tau_n=1e-9, tau_p=3e-12, V=1.5e-16, Gamma=0.3, N_tr=1e24, g0=2.5e-12, beta=1e-4):
        self.tau_n, self.tau_p, self.V, self.Gamma, self.N_tr, self.g0, self.beta = tau_n, tau_p, V, Gamma, N_tr, g0, beta
    def rate_equations(self, t, y, I):
        N, S = y; G = self.g0 * (N - self.N_tr)
        return [(I/(Q*self.V)) - (N/self.tau_n) - G*S, self.Gamma*G*S + self.Gamma*self.beta*(N/self.tau_n) - (S/self.tau_p)]
    def simulate(self, I_inj, t_span, t_eval):
        sol = solve_ivp(self.rate_equations, t_span, [0, 0], t_eval=t_eval, args=(I_inj,), method='RK45')
        return sol.t, sol.y[0], sol.y[1]
