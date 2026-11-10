import numpy as np
def dbm_to_linear(dbm): return 10**(dbm/10.0)*1e-3
def linear_to_dbm(pw): return -np.inf if pw<=0 else 10*np.log10(pw/1e-3)
def generate_random_bits(n): return np.random.randint(0,2,n)
def calculate_ber(t,r): return 0.0 if len(t)==0 else np.sum(t[:min(len(t),len(r))]!=r[:min(len(t),len(r))])/min(len(t),len(r))
