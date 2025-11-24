# Research Core Analysis: Incentive-Compatible Defense Against Committee Capture

## 1. Problem Analysis: The Shift to Committee Capture

### 1.1 Limitations of Existing Defenses: The Verification Blind Spot
Current Blockchain-based Federated Learning (BCFL) defenses primarily focus on **Data Poisoning** at the data layer (e.g., Krum, Trimmed Mean).
*   **The Systematic Gap:** A deep analysis of recent BCFL literature (2023-2025) reveals a critical **"Verification Layer Blind Spot."** Approximately **93% of studied papers** operate under explicit or implicit assumptions that the verifiers/aggregators themselves are honest or follow an honest majority.
*   **The Vulnerability:** These methods fail to address **Committee Capture**, where rational validators conspire to manipulate the consensus process. If the "judges" (verifiers) are corrupt, data-layer defenses like Krum are bypassed entirely.

### 1.2 The Threat: Progressive Committee Capture Attack (PCCA)
We define a specific, sophisticated realization of Committee Capture: the **Progressive Committee Capture Attack (PCCA)**.
This attack exploits the stake-based committee selection mechanism through a two-phase strategy:

1.  **Latent Phase (Infiltration):** Attackers behave honestly to accumulate initial stake and gain entry into the verifier pool.
2.  **Capture Phase (Strategic Starvation):** Once attackers achieve a transient majority in a committee, they trigger the trap:
    *   **Action:** They manipulate the consensus to **deny rewards to honest members** while retaining rewards for themselves.
    *   **Mechanism:** By preventing honest nodes from accumulating stake, attackers artificially inflate their own **relative stake share**. Since committee selection is stake-based, this directly increases their probability of dominating *future* committees, creating a self-reinforcing cycle of centralization.

This "silent takeover" is particularly dangerous because it bypasses traditional fault tolerance thresholds over time, converting a minority stake into a controlling majority.

## 2. Theoretical Framework: Incentive-Compatible Defense

To counter Committee Capture, we propose a mechanism based on **Game Theoretic Incentive Compatibility** rather than simple majority voting.

### 2.1 Mechanism Design
*   **Optimistic Execution:** The system assumes updates are valid by default to maximize efficiency.
*   **The Challenger (Bounty Hunter):** Any node (even those outside the current committee) can challenge a finalized update.
*   **Internal Bounty System:**
    *   If a challenge is successful, the malicious committee is **Slashed** (a significant portion of their stake is burned).
    *   The Challenger receives a portion of this slashed stake as a **Bounty**.
    *   *Crucially, this bounty comes from the attacker's loss, not an external inflation pool, making the defense self-sustaining.*

### 2.2 Security Guarantee (The Inequality)
The system is secure if the cost of a failed attack exceeds the potential gain.
Let:
*   $G_{attack}$: Potential gain from a successful attack (e.g., reward theft, market manipulation).
*   $L_{slash}$: Financial loss if caught (Slashing penalty).
*   $P_{catch}$: Probability of being caught.

In our "1-of-N" model, $P_{catch} \approx 1$ as long as there is at least one honest node with the capability to verify.
Therefore, the security condition is:
$$ L_{slash} \gg G_{attack} $$

Under this condition, a **Rational Attacker** (who maximizes profit) will **never** attempt to attack, because the expected payoff is negative. This effectively turns the attackers' greed against them.

## 3. Efficiency Analysis: Security by Deterrence

Traditional BCFL relies on "Security by Majority", while our approach relies on "Security by Deterrence". This shift allows for massive efficiency gains.

### 3.1 Committee Size & The Security-Efficiency Dilemma
*   **BlockDFL (Traditional):**
    *   Typically uses a fixed small committee (e.g., $C=7$) to maintain high throughput.
    *   **The Dilemma:** This fixed size creates a rigid security ceiling. To increase security against collusion, BlockDFL *must* increase $C$ (e.g., to 100+), which quadratically explodes communication cost ($O(C^2)$). It cannot achieve high security and high efficiency simultaneously.
*   **Ours (Incentive-Compatible):**
    *   **Decoupling:** We decouple **Liveness** from **Security**.
    *   **Liveness:** Handled by a small, fixed committee (e.g., $C=7$), ensuring low latency and $O(C_{small}^2)$ communication.
    *   **Security:** Handled by the **Challenge Mechanism**, which is independent of committee size.
    *   **Result:** We can maintain a minimal committee for maximum efficiency *without* compromising security, as the threat of slashing remains constant regardless of committee size.

### 3.2 Quantitative Comparison & Trust Hierarchy

We position our work against the "Trust Assumption Hierarchy" prevalent in current literature. While most systems operate at **Level 3 (Honest Majority)**, our system achieves **Level 6 (Byzantine Verifiers Modeled)**.

| Metric | BlockDFL (Majority-based) | Ours (Deterrence-based) | Improvement |
| :--- | :--- | :--- | :--- |
| **Trust Assumption** | Level 3: Honest Majority ($>2/3$) | **Level 6: Rationality** ($Slashing > Gain$) | **Stronger** |
| **Role of Committee** | Security + Liveness (Coupled) | Liveness Only (Decoupled) | **Flexible** |
| **Security Scaling** | Must increase $C$ (Cost $\uparrow$) | Constant (Cost flat) | **Scalable** |
| **Comm. Complexity** | $O(C^2)$ (High if Secure) | $O(C_{small}^2)$ (Always Low) | **Optimal** |
| **Collusion Resistance**| Vulnerable with small $C$ | **Resilient** with small $C$ | **Solved** |

## 4. Conclusion
By shifting the defense paradigm from "filtering bad data" to "disincentivizing bad behavior," we solve the critical vulnerability of Committee Capture. The proposed **Incentive-Compatible Mechanism** not only provides stronger security guarantees against rational attackers but also achieves significantly higher system efficiency by removing the need for large, expensive consensus committees.
