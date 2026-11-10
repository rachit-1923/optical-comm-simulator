from src.core.link import OpticalLinkSystem

def test_ideal_link():
    config = {
        "fiber_length_km": 10.0,
        "attenuation_db_km": 0.2,
        "tx_power_dbm": 5.0,
        "rx_sensitivity_dbm": -30.0,
        "modulation": "QPSK"
    }
    sys = OpticalLinkSystem(config)
    results = sys.simulate()
    
    assert results["rx_power_dbm"] == 3.0 # 5 dBm - (10km * 0.2)
    assert results["link_margin_db"] > 0
    assert results["ber"] == 0.0 # Ideal link should have no errors
    assert results["link_status"] == "PASS"
