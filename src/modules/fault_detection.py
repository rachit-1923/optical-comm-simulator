class FaultDetector:
    @staticmethod
    def diagnose(res, config):
        f = []
        if res.get("rx_power_dbm", 0) < config.get("rx_sensitivity_dbm", -20): f.append({"fault": "Low Received Power", "severity": "CRITICAL", "action": "Increase Tx power or use EDFA."})
        if res.get("ber", 1.0) > config.get("target_ber", 1e-3): f.append({"fault": "High BER", "severity": "CRITICAL", "action": "Improve SNR or change modulation."})
        if res.get("link_margin_db", 0) < 0: f.append({"fault": "Negative Link Margin", "severity": "HIGH", "action": "Add EDFA or improve receiver sensitivity."})
        return f
