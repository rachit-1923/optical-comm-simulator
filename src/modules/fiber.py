class OpticalFiber:
    def __init__(self, length_km=50.0, attenuation_db_km=0.2, dispersion_ps_nm_km=17.0):
        self.L, self.a, self.D = length_km, attenuation_db_km, dispersion_ps_nm_km
    def calculate_loss_db(self): return self.a * self.L
    def propagate_power(self, p): return p - self.calculate_loss_db()
    def pulse_broadening(self, w): return abs(self.D) * self.L * w
