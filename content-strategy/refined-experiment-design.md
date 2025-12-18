# Refined Experimental Design: Theoretical Simulation & Analysis

This document outlines the experimental design for the thesis, shifting from time-consuming Deep Learning training to **theoretical complexity analysis and Monte Carlo simulations**.

## Core Philosophy
1.  **Theoretical Foundation**: All results are derived from rigorous mathematical models of communication, computation, and consensus.
2.  **Simulation-Based**: We use Python scripts to simulate thousands of rounds to generate statistically significant data, rather than running a single slow real-world execution.
3.  **Visual-First**: Results are designed to be presented as multi-dimensional charts (X, Y, Z axes) rather than tables, to visually demonstrate trends and trade-offs.
4.  **Key Variable**: The **Challenge Rate ($p$)** is the central parameter, representing the trade-off between "Optimistic Efficiency" and "Pessimistic Security".

---

## Experiment 1: Communication Scalability Analysis

**Goal**: Demonstrate that our Optimistic approach ($O(n)$) scales significantly better than FLCoin ($O(n^2)$) and is comparable to BlockDFL ($O(c^2)$) but without its security flaws.

### Theoretical Model
*   **FLCoin (PBFT)**: $Comm_{FLCoin} = M \times (2N^2)$ (All-to-All broadcast)
*   **BlockDFL (Committee)**: $Comm_{BlockDFL} = M \times (2c^2 + N)$ (Committee consensus + Broadcast)
*   **Ours (Optimistic)**: $Comm_{Ours} = M \times [N + p \times (2N^2 - N)]$
    *   Normal Case ($1-p$): $N$ (Broadcast only)
    *   Challenge Case ($p$): $2N^2$ (Fallback to PBFT)

### Chart Design

#### Chart 1.1: Scalability with Network Size (Line Chart)
*   **X-axis**: Number of Nodes ($N$) [10, 20, ..., 100, 200]
*   **Y-axis**: Total Data Transmission per Round (GB) [Log Scale]
*   **Series**:
    1.  FLCoin
    2.  BlockDFL ($c=7$)
    3.  Ours ($p=0.01$)
    4.  Ours ($p=0.05$)
*   **Expected Insight**: FLCoin grows exponentially ($N^2$), quickly becoming infeasible. Ours grows linearly ($N$), hugging the bottom of the chart near BlockDFL.

#### Chart 1.2: Impact of Challenge Rate on Bandwidth (Area Chart)
*   **X-axis**: Challenge Rate ($p$) [0.0% to 10.0%]
*   **Y-axis**: Average Communication Overhead (Relative to FLCoin)
*   **Insight**: Shows the "Break-even point" where if $p$ is too high, our system degrades to FLCoin performance. We want to show we are far below this point in normal operation.

---

## Experiment 2: Computation & Validation Load

**Goal**: Highlight the "Lazy Verification" advantage where most nodes do not need to verify updates in the optimistic case.

### Theoretical Model
*   **FLCoin**: $Comp_{FLCoin} = N \times C_{verify}$ (Everyone verifies)
*   **BlockDFL**: $Comp_{BlockDFL} = c \times C_{verify}$ (Only committee verifies)
*   **Ours**: $Comp_{Ours} = [k + p \times (N-k)] \times C_{verify}$
    *   $k$: Number of active supervisors (e.g., 3-5)
    *   $p$: Probability of full verification

### Chart Design

#### Chart 2.1: Computational Savings (Bar Chart)
*   **X-axis**: Methods [FLCoin, BlockDFL, Ours ($p=0.01$), Ours ($p=0.05$)]
*   **Y-axis**: Average Verifications per Round
*   **Insight**: FLCoin is a full bar (100%). BlockDFL is small (~7%). Ours is even smaller (~3-5%) or slightly higher depending on $p$, but robustly low.

#### Chart 2.2: The Cost of Security (Line Chart)
*   **X-axis**: Challenge Rate ($p$)
*   **Y-axis**: Total System Computation Cost
*   **Insight**: A gentle slope showing that even with occasional challenges, the amortized cost remains low.

---

## Experiment 3: Security & Robustness (Monte Carlo Simulation)

**Goal**: Prove that BlockDFL's probabilistic security is insufficient compared to our deterministic security (given $k \ge 1$).

### Simulation Logic
*   **BlockDFL**: Randomly sample $c$ committee members from $N$ nodes. If malicious nodes $f > \frac{1}{3}c$ (or $\frac{2}{3}c$ depending on assumption), attack succeeds.
*   **Ours**: Attack succeeds only if **zero** honest nodes verify the update (i.e., $k=0$ or all supervisors are malicious).

### Chart Design

#### Chart 3.1: Attack Success Probability (The "Kill Shot" Chart)
*   **X-axis**: Malicious Node Ratio ($f$) [10% to 49%]
*   **Y-axis**: Probability of Successful Model Poisoning (%)
*   **Series**:
    1.  BlockDFL ($c=7$)
    2.  BlockDFL ($c=15$)
    3.  Ours ($k \ge 1$) -> **Flat line at 0%**
*   **Insight**: BlockDFL's risk rises sharply as $f$ increases. Ours remains secure (0% risk) because we don't rely on a majority vote of a small committee; we rely on *any* single honest verification.

#### Chart 3.2: Supervisor Reliability (Heatmap)
*   **X-axis**: Total Nodes ($N$)
*   **Y-axis**: Lazy Rate (Probability a node skips verification)
*   **Color**: Probability that $k=0$ (System Failure)
*   **Insight**: Shows that even if 90% of nodes are lazy, the probability of *total* failure is vanishingly small ($0.9^{100} \approx 0$).

---

## Experiment 4: End-to-End Latency Trade-off

**Goal**: Analyze the total time cost, factoring in the "Challenge Period" delay.

### Theoretical Model
*   $T_{total} = T_{comm} + T_{comp} + T_{consensus}$
*   **Ours**: $T_{Ours} = (1-p) \times T_{fast} + p \times (T_{fast} + T_{challenge} + T_{PBFT})$
    *   $T_{challenge}$: The dispute window (e.g., 5 minutes).

### Chart Design

#### Chart 4.1: Latency vs. Challenge Rate (3D Surface or Multi-line)
*   **X-axis**: Challenge Rate ($p$)
*   **Y-axis**: Model Size (MB) [Small CNN to Large VGG]
*   **Z-axis (Height)**: Average Round Latency
*   **Insight**:
    *   For **Small Models**, the Challenge Period dominates. High $p$ hurts.
    *   For **Large Models**, Transmission Time dominates. $p$ matters less because sending the model takes longer than the challenge window.
    *   This proves our method is particularly well-suited for **Large Language Models (LLMs)** or heavy Foundation Models where transmission is the bottleneck.

---

## Summary of Comparison

| Feature | FLCoin | BlockDFL | Ours |
| :--- | :--- | :--- | :--- |
| **Communication** | $O(N^2)$ (Heavy) | $O(c^2)$ (Light) | **$O(N)$ (Lightest)** |
| **Computation** | $100\%$ | $\sim 7\%$ | **$\sim 3-5\%$** |
| **Security** | Deterministic | Probabilistic (Risky) | **Deterministic (Safe)** |
| **Latency** | High (Tx delay) | Low | **Low (Amortized)** |

## Next Steps for "Simulation"
1.  Write a Python script to implement these formulas.
2.  Run the script with $N=100$, varying $p$ and $f$.
3.  Export the data to CSV/JSON.
4.  Plot these exact charts using Matplotlib/Seaborn.
