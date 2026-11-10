from core.constants import C
class DWDMPlanner:
    @staticmethod
    def plan_channels(n, spacing=100.0, ref=193.1):
        f = [ref + (i*spacing/1000.0) for i in range(n)]
        return {"num_channels": n, "channel_frequencies_thz": f, "channel_wavelengths_nm": [(C/(freq*1e12))*1e9 for freq in f]}
