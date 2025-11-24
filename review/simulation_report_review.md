# Simulation Report Review

## 1. Overall Assessment
The `simulation_report.md` successfully captures the quantitative results defined in the `refined-experiment-design.md`. It effectively highlights the **Scalability**, **Computation Load**, and **Latency** advantages.

However, compared to the `research-core-analysis.md`, the report is **missing the "Computational Generality" argument**. The core analysis emphasizes that your solution supports LLMs and complex logic (unlike opML/zkML), which is a critical qualitative advantage that should be mentioned alongside the quantitative simulation results.

## 2. "Naive" Data Presentation Check
Is the data presentation too naive? Here are specific points to address:

### A. Security Claims ("0% Risk")
*   **Current Text**: "Attack success rate is always 0%."
*   **Critique**: This sounds too "perfect" and might trigger skepticism. In distributed systems, "0%" usually implies a strong assumption.
*   **Suggestion**: Rephrase to emphasize the condition.
    *   *Better*: "Security is deterministic ($0\%$ failure) **as long as $k \ge 1$ honest supervisor exists**."
    *   This connects better with the "Supervisor Reliability Heatmap" which shows the probability of $k \ge 1$.

### B. Challenge Rate in Exp 1
*   **Current Text**: Mentions "Even at 10% Challenge Rate".
*   **Critique**: A 10% challenge rate is extremely high for an "Optimistic" system (usually $<1\%$). Showing it handles 10% is good for robustness, but might imply the system expects frequent failures.
*   **Suggestion**: Clarify that 10% is a **stress test** value.
    *   *Add*: "While typical operation expects $p < 1\%$, stress tests show the system remains efficient even at an exaggerated $10\%$ challenge rate."

### C. Missing "Generality" Context
*   **Critique**: The report proves the system is *fast* and *secure*, but doesn't explicitly prove it is *more capable* (i.e., can run LLMs that opML cannot).
*   **Suggestion**: Add a brief section or a note in the Conclusion comparing "Native Execution" vs "FPVM/Circuit constraints". This aligns with **Advantage Analysis 2** in your Core Analysis.

## 3. Specific Recommendations for Revision

### Add "Computational Generality" Section
Insert a brief qualitative comparison before the Conclusion.
> **5. 計算通用性分析 (Computational Generality)**
> 除了效率與安全外，本方案採用原生執行 (Native Execution)，突破了 opML (受限於 FPVM 記憶體) 與 zkML (受限於電路規模) 的限制。這使得本架構成為目前唯一能有效支援 **7B+ 參數大型語言模型 (LLM)** 進行去中心化聯邦學習的方案。

### Refine Experiment 3 (Security)
Update the description to be more precise about the trust model.
> **Original**: ...攻擊成功率恆為 0%。
> **Revised**: ...在滿足 $k \ge 1$ (至少一位誠實監督者) 的條件下，系統具備確定性安全 (Deterministic Security)，攻擊成功率為 0%。熱圖分析進一步顯示，即便在 90% 節點「偷懶」的極端情況下，系統崩潰 ($k=0$) 的機率仍趨近於零。

### Enhance Experiment 1 (Scalability)
Clarify the "Linear vs Exponential" narrative.
> **Add**: "FLCoin 的通訊量隨節點數平方增長 ($O(N^2)$)，限制了其擴展性。本方案透過樂觀路徑將複雜度降至 $O(N)$，在 $N=100$ 的模擬中，頻寬消耗降低了約 98.5%。"

## 4. Conclusion
The report is a solid summary of the *simulation*, but to fully reflect the *thesis core value*, it needs to bridge the gap between "Numbers" (Simulation) and "Capability" (Generality). Adding the qualitative argument makes the report much stronger.
