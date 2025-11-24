# Advanced Experiment Brainstorming: Moving Beyond "Naive" Charts

此文檔旨在規劃新一輪實驗，目標是將原本較為理論/理想化的圖表（Naive），轉化為具備**工程落地感**與**經濟現實感**的數據分析。

## 核心改進方向
1.  **從「複雜度 ($O(N)$)」轉向「實際成本 (Gas/USD)」**：不僅是趨勢線，而是具體的 Ethereum Gas 消耗估算。
2.  **從「驗證次數」轉向「系統總算力 (FLOPs/Energy)」**：強調綠色計算與資源效率。
3.  **從「攻擊機率」轉向「經濟賽局 (Cost of Corruption)」**：證明攻擊本系統在經濟上是不理性的。

---

## Proposal 1: On-Chain Gas Consumption Analysis (The "Real Money" Metric)
**取代目標**：原本單純的 "Communication Scalability" (只講頻寬)。
**痛點解決**：頻寬在 Web2 系統不值錢，但在區塊鏈上 (Data Availability + Execution) 非常昂貴。

### 設計概念
模擬在 Ethereum (Layer 1) 或 L2 (Arbitrum/Optimism) 上的 Gas 消耗。
*   **FLCoin (PBFT)**: 每個節點都要發送 Pre-prepare/Prepare/Commit 交易，Gas 消耗隨 $N^2$ 爆炸。
*   **BlockDFL**: 委員會成員需發送投票交易，聚合者發送聚合交易。
*   **Ours (Optimistic)**:
    *   **Happy Path**: 只有聚合者發送 1 筆 `submitTask` 交易 (包含 Merkle Root)。
    *   **Challenge Path**: 挑戰者發送 `challenge` 交易 + 隨後的 PBFT 投票交易。

### 預期圖表 (Bar Chart / Stacked Area)
*   **X軸**: 網路規模 ($N$) 或 挑戰率 ($p$)
*   **Y軸**: 每輪聚合的總 Gas 消耗 (Gas Unit 或 USD)
*   **視覺效果**:
    *   FLCoin 的柱狀圖會高到突破天際 (紅色)。
    *   BlockDFL 居中 (黃色)。
    *   Ours (Happy Path) 幾乎貼地 (綠色)。
    *   **關鍵細節**: 即使加上 1% 的挑戰懲罰，Ours 的平均 Gas 仍遠低於 BlockDFL。

---

## Proposal 2: Total System Computation & Energy Efficiency (The "Green" Metric)
**取代目標**：原本的 "Computation Load" (只講驗證次數)。
**痛點解決**：單純講「驗證次數」不夠直觀，轉換為「總運算量」或「能源消耗」更具現代學術價值 (Green AI)。

### 設計概念
計算全網在每一輪訓練中浪費在「重複驗證」上的算力。
*   **Metric**: Total System FLOPs = (Training FLOPs) + (Verification FLOPs $\times$ Verifying Nodes).
*   **假設**: 訓練一個 ResNet-50 需要 $X$ FLOPs，驗證需要 $0.2X$ FLOPs。

### 預期圖表 (Line Chart)
*   **X軸**: 參與節點數量 ($N$)
*   **Y軸**: 系統總算力消耗 (Total FLOPs) [Log Scale]
*   **Series**:
    *   **Ideal (Centralized)**: 只有訓練消耗，沒有驗證浪費 (基準線)。
    *   **Ours**: 緊貼 Ideal 線 (因為只有 $k$ 個節點驗證)。
    *   **FLCoin**: 斜率極大，因為 $N$ 個節點都在做無用的重複驗證。
*   **Insight**: 強調本系統是**環保且高效**的，將算力集中在訓練而非共識上。

---

## Proposal 3: Economic Security & Slashing Analysis (The "Game Theory" Metric)
**取代目標**：原本的 "Attack Success Probability" (0% 看起來太假)。
**痛點解決**：在區塊鏈中，沒有絕對的安全，只有「攻擊成本 > 獲利」的經濟安全。

### 設計概念
分析攻擊者為了破壞模型需要付出的代價 (Slashing) 與潛在獲利。
*   **Cost of Corruption (CoC)**: 賄賂足夠多的節點 (BlockDFL) 或 承擔被 Slash 的風險 (Ours) 所需的資金。
*   **BlockDFL**: 只要賄賂委員會的 $1/3$ (相對少量的節點) 即可破壞，且無原生 Slashing 機制 (通常)。
*   **Ours**: 必須賄賂**所有**潛在的監督者 (因為只要有一個誠實就失敗)，或者承擔巨大的質押金 (Stake) 被沒收的風險。

### 預期圖表 (Double Y-axis Chart)
*   **X軸**: 網路規模 ($N$)
*   **左Y軸 (Bar)**: 破壞系統所需的最小賄賂成本 (Min Cost to Attack)。
*   **右Y軸 (Line)**: 攻擊成功率 (Attack Success Prob)。
*   **視覺效果**:
    *   BlockDFL 的賄賂成本隨 $N$ 增加緩慢 (因為委員會大小 $c$ 固定或增長慢)。
    *   Ours 的賄賂成本隨 $N$ 線性甚至超線性增長 (因為潛在監督者變多，且 Slashing 懲罰重)。
    *   **結論**: 雖然 BlockDFL 有機率安全，但 Ours 具備更高的**經濟安全性 (Crypto-economic Security)**。

---

## Proposal 4: Throughput vs Latency Trade-off (The "Performance" Metric)
**取代目標**：原本單一的 "Latency" 圖。
**痛點解決**：單看延遲忽略了系統吞吐量 (TPS)。

### 設計概念
模擬在高併發情況下 (多個 Global Rounds 同時進行或流水線進行)，系統的極限吞吐量。
*   **Ours**: 由於 Happy Path 不佔用區塊鏈狀態 (State Bloat) 且計算輕量，可以支援更高的併發聚合。
*   **FLCoin**: 區塊鏈塞車，吞吐量極低。

### 預期圖表 (Scatter Plot / Heatmap)
*   **X軸**: 併發請求數 (Concurrency)
*   **Y軸**: 平均完成時間 (Avg Completion Time)
*   **Insight**: FLCoin 在併發增加時延遲垂直上升 (擁堵)，Ours 保持平穩。

---

## 總結建議
建議優先實作 **Proposal 1 (Gas)** 和 **Proposal 3 (Economic Security)**。這兩者最能體現「區塊鏈 + AI」的跨領域深度，且能有效消除 "Naive" 的感覺，將討論層次從「演算法複雜度」提升到「系統經濟學」。
