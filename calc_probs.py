from scipy.stats import hypergeom
import math

def calc_prob(N, f, C, threshold_ratio):
    M = int(N * f) # Malicious nodes
    # Threshold: Strictly greater than threshold_ratio * C
    k_min = math.floor(threshold_ratio * C) + 1
    
    prob = 0
    for k in range(k_min, C + 1):
        prob += hypergeom.pmf(k, N, M, C)
        
    return prob, k_min

N = 100
f = 0.3
Cs = [5, 7, 9, 11, 13]

print(f"--- Calculating New Threshold (> 2/3) for N={N}, f={f} ---")
for C in Cs:
    prob, k_min = calc_prob(N, f, C, 2/3)
    print(f"C={C}, k_min={k_min}, Prob={prob:.4%}")
