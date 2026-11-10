import numpy as np
from core.utils import generate_random_bits, calculate_ber
from modules.modulation import Modulator
from modules.fiber import OpticalFiber
from modules.edfa import EDFA
from modules.receiver import Receiver
class OpticalLinkSystem:
    def __init__(self, config):
        self.c = config
        self.fiber = OpticalFiber(self.c.get("fiber_length_km", 50.0), self.c.get("attenuation_db_km", 0.2), self.c.get("dispersion_ps_nm_km", 17.0))
        self.edfa = EDFA(self.c.get("edfa_gain_db", 20.0), self.c.get("edfa_psat_dbm", 15.0), self.c.get("edfa_nf_db", 5.0)) if self.c.get("edfa_enabled", False) else None
        self.receiver = Receiver(self.c.get("rx_sensitivity_dbm", -20.0))
    def simulate(self):
        res = {}
        tx_b = generate_random_bits(self.c.get("n_bits", 10000))
        m = self.c.get("modulation", "OOK")
        tx_s = getattr(Modulator, f"modulate_{m.lower().replace('-','')}")(tx_b)
        rx_p = self.fiber.propagate_power(self.c.get("tx_power_dbm", 0.0))
        pb = self.fiber.pulse_broadening(self.c.get("spectral_width_nm", 0.1))
        if self.edfa:
            rx_p, ag = self.edfa.amplify(rx_p)
            res["edfa_actual_gain_db"] = ag
            res["ase_noise_w"] = self.edfa.calculate_ase_noise(ag)
        snr = 10.0 + (rx_p - self.receiver.sens)
        if pb > self.c.get("max_dispersion_tolerance_ps", 100): snr -= 3.0
        rx_s = self.receiver.add_awgn_noise(tx_s, snr)
        rx_b = getattr(Modulator, f"demodulate_{m.lower().replace('-','')}")(rx_s)
        ber = calculate_ber(tx_b, rx_b)
        lm = self.receiver.check_link_margin(rx_p)
        res.update({"rx_power_dbm": rx_p, "link_margin_db": lm, "ber": ber, "pulse_broadening_ps": pb, "snr_db": snr, "link_status": "PASS" if (ber <= self.c.get("target_ber", 1e-3) and lm >= 0) else "FAIL"})
        return res
