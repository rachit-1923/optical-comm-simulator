import numpy as np
class Modulator:
    @staticmethod
    def modulate_ook(b): return np.array(b, dtype=float)
    @staticmethod
    def demodulate_ook(s, t=0.5): return (np.real(s)>t).astype(int)
    @staticmethod
    def modulate_bpsk(b): return 2*np.array(b, dtype=float)-1+0j
    @staticmethod
    def demodulate_bpsk(s): return (np.real(s)>0).astype(int)
    @staticmethod
    def modulate_qpsk(b):
        if len(b)%2!=0: b=np.append(b,0)
        return ((b[0::2]*2-1) + 1j*(b[1::2]*2-1))/np.sqrt(2)
    @staticmethod
    def demodulate_qpsk(s):
        b = np.zeros(2*len(s), dtype=int); b[0::2] = (np.real(s)>0).astype(int); b[1::2] = (np.imag(s)>0).astype(int)
        return b
    @staticmethod
    def modulate_16qam(b):
        if len(b)%4>0: b=np.append(b, np.zeros((4-len(b)%4)%4, dtype=int))
        m = {(0,0):-3, (0,1):-1, (1,1):1, (1,0):3}
        return np.array([m[tuple(b[i:i+2])] + 1j*m[tuple(b[i+2:i+4])] for i in range(0,len(b),4)])/np.sqrt(10)
    @staticmethod
    def demodulate_16qam(s):
        s = s*np.sqrt(10); d = lambda v: [0,0] if v<-2 else [0,1] if v<0 else [1,1] if v<2 else [1,0]
        return np.array([bit for sym in s for bit in d(np.real(sym)) + d(np.imag(sym))])
