class FBGSensor:
    def __init__(self, n_eff=1.45, Lambda_nm=534.5, k_T=10.0, k_epsilon=1.2):
        self.n, self.L, self.k_T, self.k_e = n_eff, Lambda_nm, k_T, k_epsilon
    def calculate_bragg_wavelength(self): return 2 * self.n * self.L
    def measure_shift(self, dT, e):
        b = self.calculate_bragg_wavelength()
        return {"original_wavelength_nm": b, "temperature_shift_nm": (self.k_T*dT)/1000.0, "strain_shift_nm": (self.k_e*e)/1000.0, "final_wavelength_nm": b + (self.k_T*dT + self.k_e*e)/1000.0}
