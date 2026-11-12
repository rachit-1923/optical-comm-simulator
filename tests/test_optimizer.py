from src.modules.optimizer import LinkOptimizer


def test_optimizer_preserves_fixed_fiber_length_and_attenuation():
    base = {
        "fiber_length_km": 150.0,
        "attenuation_db_km": 0.2,
        "tx_power_dbm": 0.0,
        "modulation": "OOK",
        "edfa_enabled": False,
        "edfa_gain_db": 20.0,
        "rx_sensitivity_dbm": -20.0,
        "target_ber": 1e-3,
        "n_bits": 2000,
    }
    result = LinkOptimizer.optimize(
        base,
        tx_power_candidates=[0.0, 5.0, 10.0],
        modulation_candidates=["OOK", "BPSK"],
        edfa_gains_db=[20.0],
    )
    assert result["evaluations"]
    assert all(row["fiber_length_km"] == 150.0 for row in result["evaluations"])
    if result["status"] == "SUCCESS":
        assert result["config"]["fiber_length_km"] == 150.0
        assert result["config"]["attenuation_db_km"] == 0.2
        assert result["results"]["ber"] <= 1e-3
        assert result["results"]["link_margin_db"] >= 0


def test_optimizer_reports_failure_when_no_candidate_is_feasible():
    base = {
        "fiber_length_km": 150.0,
        "attenuation_db_km": 0.2,
        "tx_power_dbm": 0.0,
        "modulation": "OOK",
        "target_ber": 1e-12,
        "n_bits": 1000,
    }
    result = LinkOptimizer.optimize(
        base,
        tx_power_candidates=[-10.0],
        modulation_candidates=["OOK"],
        edfa_gains_db=[10.0],
    )
    assert result["status"] == "FAILED"
    assert result["config"] is None
    assert result["results"] is None
