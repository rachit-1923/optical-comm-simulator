from core.link import OpticalLinkSystem
class LinkOptimizer:
    @staticmethod
    def optimize(base_config):
        bc, br = None, None
        for edfa in [False, True]:
            for mod in ["OOK", "BPSK", "QPSK"]:
                for tx in [0.0, 5.0, 10.0]:
                    tc = base_config.copy()
                    tc.update({"edfa_enabled": edfa, "modulation": mod, "tx_power_dbm": tx})
                    try:
                        res = OpticalLinkSystem(tc).simulate()
                        if res["link_status"] == "PASS":
                            cc = (100 if edfa else 0) + tx
                            if bc is None or cc < ((100 if bc["edfa_enabled"] else 0) + bc["tx_power_dbm"]):
                                bc, br = tc, res
                    except: continue
        return {"status": "SUCCESS", "config": bc, "results": br} if bc else {"status": "FAILED"}
