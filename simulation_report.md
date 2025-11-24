# 樂觀共識機制 (Optimistic Consensus) 模擬實驗報告

## 1. 摘要 (Executive Summary)
本報告旨在透過理論模擬，驗證「樂觀共識」架構相較於傳統 FLCoin (PBFT) 與 BlockDFL (委員會機制) 的優勢。實驗結果證實，本方案在**通訊開銷**與**計算負載**上具有顯著的擴展性優勢，同時在**安全性**上解決了 BlockDFL 的機率性漏洞，實現了低成本與高安全的最佳平衡。

---

## 2. 實驗結果分析

### 實驗一：通訊擴展性 (Communication Scalability)
本方案展現了 $O(N)$ 的線性通訊複雜度，顯著優於 FLCoin 的 $O(N^2)$ 指數增長。即使在 10% 的挑戰率 (Challenge Rate) 下，額外開銷仍極低，證明了系統在大規模網路下的可行性。

| 網路規模擴展性 | 挑戰率對頻寬的影響 |
| :---: | :---: |
| ![Scalability](plots/1.1_scalability_network_size.png) | ![Challenge Impact](plots/1.2_challenge_rate_impact.png) |

### 實驗二：計算與驗證負載 (Computation & Validation Load)
透過「惰性驗證 (Lazy Verification)」機制，絕大多數節點無需進行模型驗證。數據顯示，本方案的平均計算負載僅為 FLCoin 的 3-5%，且隨著挑戰率增加，系統總成本仍保持在低位。

| 計算節省比較 | 安全性成本分析 |
| :---: | :---: |
| ![Comp Savings](plots/2.1_computational_savings.png) | ![Cost of Security](plots/2.2_cost_of_security.png) |

### 實驗三：安全性與穩健性 (Security & Robustness)
BlockDFL 的安全性隨著惡意節點比例 ($f$) 增加而急劇下降 (機率性失效)。相比之下，本方案只要有**至少一個**誠實監督者 (Supervisor) 進行驗證，即可保證系統安全 (Deterministic Security)，攻擊成功率恆為 0%。

| 攻擊成功率比較 | 監督者可靠度熱圖 |
| :---: | :---: |
| ![Attack Prob](plots/3.1_attack_success_probability.png) | ![Reliability](plots/3.2_supervisor_reliability.png) |

### 實驗四：端對端延遲 (End-to-End Latency)
針對大型模型 (如 LLM)，傳輸時間主導了整體延遲。模擬顯示，雖然挑戰期 (Challenge Period) 會引入延遲，但在大模型場景下，其影響被傳輸時間稀釋，證明本方案特別適用於大型基礎模型的聯邦學習。

![Latency Tradeoff](plots/4.1_latency_tradeoff.png)

---

## 3. 結論 (Conclusion)
模擬實驗有力地支持了論文的核心論點：**樂觀共識機制透過引入極低機率的「挑戰-回退」流程，成功打破了傳統拜占庭容錯在擴展性、安全性與效率之間的不可能三角。**
