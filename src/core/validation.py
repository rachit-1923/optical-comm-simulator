def validate_link_parameters(c):
    e = []
    if c.get('fiber_length_km',0)<0: e.append('Fiber length negative.')
    if c.get('tx_power_dbm',0)>30: e.append('Tx power > 30 dBm.')
    if c.get('modulation','OOK') not in ['OOK','BPSK','QPSK','16-QAM']: e.append('Invalid mod.')
    return e
