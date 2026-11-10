import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from core.utils import generate_random_bits
from modules.modulation import Modulator
from modules.receiver import Receiver

class ModulationClassifierML:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.labels = ["OOK", "BPSK", "QPSK", "16-QAM"]
        self.is_trained = False

    def extract_features(self, sig):
        m, p = np.abs(sig), np.angle(sig)
        return np.array([np.mean(m), np.var(m), np.max(m), np.mean(p), np.var(p)])

    def generate_data(self, samples=200):
        X, y = [], []
        rx = Receiver()
        for idx, mod in enumerate(self.labels):
            for _ in range(samples):
                bits = generate_random_bits(100)
                sig = getattr(Modulator, f"modulate_{mod.lower().replace('-','')}")(bits)
                noisy = rx.add_awgn_noise(sig, np.random.uniform(5, 20))
                X.append(self.extract_features(noisy)); y.append(idx)
        return np.array(X), np.array(y)

    def train_and_evaluate(self):
        X, y = self.generate_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self.is_trained = True
        return {"accuracy": accuracy_score(y_test, self.model.predict(X_test))}
