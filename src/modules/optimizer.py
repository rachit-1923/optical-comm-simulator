
"""Constrained configuration search for the optical link simulator.

The fibre span and attenuation are treated as fixed link requirements. The
optimizer searches transmitter power, modulation and optional EDFA settings.
"""
import numpy as np

from src.core.link import OpticalLinkSystem


class LinkOptimizer:
    @staticmethod
    def optimize(
        base_config,
        tx_power_candidates=None,
        modulation_candidates=None,
        edfa_gains_db=None,
        target_ber=None,
        random_state=42,
    ):
        """Find the lowest-transmit-power feasible configuration.

        Fixed physical link inputs (including fibre length and attenuation) are
        copied from ``base_config`` and never optimized. Feasibility requires
        both BER <= target BER and non-negative receiver link margin, as
        reported by OpticalLinkSystem.

        Ranking is lexicographic: lowest Tx power first, then no EDFA, then
        lower EDFA gain, then lower modulation order. This is a transparent
        engineering proxy; the project does not currently model EDFA electrical
        consumption or monetary equipment costs.
        """
        if not isinstance(base_config, dict):
            raise TypeError("base_config must be a dictionary")

        fixed_config = dict(base_config)
        target = float(target_ber if target_ber is not None else fixed_config.get("target_ber", 1e-3))
        if not 0 < target < 1:
            raise ValueError("target_ber must be between 0 and 1")
        fixed_config["target_ber"] = target

        if tx_power_candidates is None:
            tx_power_candidates = [-10, -5, 0, 5, 10, 15, 20]
        if "tx_power_dbm" in fixed_config:
            tx_power_candidates = sorted(set(float(x) for x in tx_power_candidates) | {float(fixed_config["tx_power_dbm"])})
        if modulation_candidates is None:
            modulation_candidates = ["OOK", "BPSK", "QPSK", "16-QAM"]
        if edfa_gains_db is None:
            edfa_gains_db = [10, 15, 20, 25, 30]

        candidates = []
        for tx in tx_power_candidates:
            for modulation in modulation_candidates:
                candidates.append((float(tx), modulation, False, float(fixed_config.get("edfa_gain_db", 20.0))))
                for gain in edfa_gains_db:
                    candidates.append((float(tx), modulation, True, float(gain)))

        evaluations = []
        feasible = []
        # Make each candidate reproducible and comparable, while restoring the
        # caller's NumPy random state when optimization completes.
        prior_rng_state = np.random.get_state()
        try:
            for tx, modulation, edfa_enabled, gain in candidates:
                candidate_config = dict(fixed_config)
                candidate_config.update({
                    "tx_power_dbm": tx,
                    "modulation": modulation,
                    "edfa_enabled": edfa_enabled,
                    "edfa_gain_db": gain,
                })
                try:
                    np.random.seed(random_state)
                    result = OpticalLinkSystem(candidate_config).simulate()
                    row = {
                        "tx_power_dbm": tx,
                        "modulation": modulation,
                        "edfa_enabled": edfa_enabled,
                        "edfa_gain_db": gain if edfa_enabled else None,
                        "fiber_length_km": candidate_config.get("fiber_length_km", 50.0),
                        "ber": result["ber"],
                        "rx_power_dbm": result["rx_power_dbm"],
                        "link_margin_db": result["link_margin_db"],
                        "link_status": result["link_status"],
                    }
                    evaluations.append(row)
                    if result["ber"] <= target and result["link_margin_db"] >= 0:
                        modulation_rank = {"OOK": 0, "BPSK": 1, "QPSK": 2, "16-QAM": 3}.get(modulation, 99)
                        rank = (tx, edfa_enabled, gain if edfa_enabled else 0.0, modulation_rank)
                        feasible.append((rank, candidate_config, result))
                except Exception as exc:
                    evaluations.append({
                        "tx_power_dbm": tx,
                        "modulation": modulation,
                        "edfa_enabled": edfa_enabled,
                        "edfa_gain_db": gain if edfa_enabled else None,
                        "fiber_length_km": candidate_config.get("fiber_length_km", 50.0),
                        "link_status": "ERROR",
                        "error": str(exc),
                    })
        finally:
            np.random.set_state(prior_rng_state)

        if not feasible:
            return {
                "status": "FAILED",
                "config": None,
                "results": None,
                "evaluations": evaluations,
                "feasible_count": 0,
                "target_ber": target,
                "objective": "Minimize Tx power; prefer no EDFA and lower gain as tie-breakers.",
            }

        _, best_config, best_result = min(feasible, key=lambda item: item[0])
        return {
            "status": "SUCCESS",
            "config": best_config,
            "results": best_result,
            "evaluations": evaluations,
            "feasible_count": len(feasible),
            "target_ber": target,
            "objective": "Minimize Tx power; prefer no EDFA and lower gain as tie-breakers.",
        }
