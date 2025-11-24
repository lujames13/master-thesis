# III. Related Work (Optimized Strategy)

## A. The Aggregator Verification Challenge (1.0頁)

### A.1 Core Challenge: Trust vs. Verification (0.7頁)

**段落1：問題定義**
- 多聚合器架構雖然解決了SPOF，但引入了新的驗證難題：如何確保聚合器在拜占庭環境下的計算正確性？
- 區分兩層威脅：Client層（投毒）vs Aggregator層（偽造/懶惰）。本研究聚焦於後者。

**段落2：三類技術路線概覽**
- **PBFT-based**：側重安全性，但受限於通訊複雜度（本節B）。
- **Optimistic**：側重效率，但受限於計算通用性（本節C）。
- **Zero-Knowledge**：側重隱私與數學完備性，但受限於證明生成開銷（本節D）。

### A.2 Scope (0.3頁)
- 聚焦：多聚合器、拜占庭容錯、驗證機制。
- 排除：單聚合器、純PoW/PoS共識。

---

## B. PBFT-based Approaches: The Scalability Bottleneck (3.5頁)

### B.1 Committee-based Approaches (FLCoin, VFChain) (1.0頁)

**段落1：機制與優勢**
- 機制：選舉小型委員會（如c=100）執行PBFT，降低通訊複雜度至O(c²)。
- 優勢：在短期內能有效提升共識速度。

**段落2：核心局限 - 潛伏攻擊 (Sleeper Attack)**
- **信任積累悖論**：攻擊者可通過長期誠實行為積累聲譽，進入委員會後再發動攻擊。
- **局部驗證盲區**：非委員會成員無法驗證，若委員會多數共謀（>c/3），系統將崩潰。

### B.2 ⭐ The Primary Baseline: BlockDFL (2.5頁)

**段落3：機制介紹**
- BlockDFL [Qin et al.] 是一個典型的基於區塊鏈的FL框架。
- 核心設計：為了緩解 PBFT 的通訊壓力，將驗證者限制在一個極小的委員會（Much smaller than N，例如 7 人）中。
- 驗證方式：基於哈希值的隨機角色輪替。

**段落4：⭐ 深度批判 - 概率性共謀漏洞 (Probabilistic Collusion)**
這將是本研究最核心的批判點（基於 BlockDFL_compare.md）：

1.  **效率的代價**：BlockDFL 承認為了效率必須限制驗證者數量，這直接導致了安全性的妥協。
2.  **隨機性的雙面刃**：
    *   雖然長期看隨機選擇是公平的，但在單一回合中，攻擊者（即使全網佔比僅30%）"運氣好"被選入委員會並佔據多數（>2/3，即7人中的5人）的概率並非為零。
3.  **攻擊路徑 (Attack Vector)**：
    *   **等待策略 (Waiting Strategy)**：攻擊者平時潛伏，一旦在某輪隨機抽選中控制了委員會，即可發動"毀滅性攻擊"，將帶毒模型寫入區塊鏈。
    *   **局部共識的脆弱性**：由於共識僅在小委員會內達成，外部節點無法及時阻斷這種合法的"惡意共識"。

**段落5：對比本研究**
- **BlockDFL**：安全性依賴於"壞人運氣不好"（概率性安全）。
- **本研究**：安全性依賴於"1-of-N 誠實假設"（只要全網有一個誠實節點發起挑戰即可阻斷）。
- **結論**：BlockDFL 在效率與安全之間做了錯誤的權衡，而本研究通過 Optimistic 機制解決了這一矛盾。

---

## C. Optimistic Approaches: The Generality Bottleneck (1.5頁)

### C.1 Optimistic Machine Learning (opML)

**段落1：機制與優勢**
- 機制：樂觀假設，挑戰期，欺詐證明（Fraud Proof）。
- 優勢：正常情況下通訊複雜度為O(1)，效率極高。

**段落2：核心局限 - FPVM 計算約束**
- **記憶體限制**：FPVM（如MIPS/WASM虛擬機）記憶體上限（通常4GB）無法容納大模型。
- **算法分解困難**：複雜算法（如FedProx、Krum）難以編譯為虛擬機指令。
- **結論**：opML 適合簡單模型，但無法支撐現代大模型FL的計算需求。

*(註：本節主要作為定性比較，不進行實驗數據對比)*

---

## D. Zero-Knowledge Approaches: The Performance Bottleneck (1.0頁)

### D.1 zkML (Zero-Knowledge Machine Learning)

**段落1：機制與優勢**
- 機制：將ML計算轉化為算術電路，生成zk-SNARK/STARK證明。
- 優勢：數學級別的完整性與隱私保護，Zero Trust。

**段落2：核心局限 - 算術化開銷**
- **證明生成時間**：比原生計算慢 100x-1000x。
- **模型規模限制**：電路規模隨參數量爆炸，目前僅能支援微型模型。
- **結論**：在FL實際部署中"Utterly Impractical"。

*(註：本節主要作為定性比較，不進行實驗數據對比)*

---

## E. Research Gap & Proposed Solution (1.0頁)

### E.1 The "Impossible Triangle" of FL Verification

總結現有方案面臨的**三難困境 (Trilemma)**，特別強調 BlockDFL 的位置：

| 方案 | 安全性 (Security) | 效率 (Efficiency) | 通用性 (Generality) | 核心缺陷 |
|------|------------------|-------------------|---------------------|----------|
| **BlockDFL (Baseline)** | ❌ **Probabilistic** | ✅ High (Committee) | ✅ High | **共謀攻擊風險** |
| **Optimistic (opML)** | ✅ High (1-of-N) | ✅ High (O(1)) | ❌ Low (FPVM) | 不支援大模型 |
| **ZK (zkML)** | ✅✅ Very High | ❌ Very Low | ❌ Low | 證明生成太慢 |

### E.2 Our Approach: Dynamic Optimistic-PBFT

本研究提出一種**打破三難困境**的混合架構：

1.  **效率 (Efficiency)**：採用 **Optimistic** 策略，正常情況下 O(1) 通訊，O(R/N) 計算。
2.  **通用性 (Generality)**：摒棄 FPVM/ZK，採用 **PBFT** 作為爭議仲裁機制，在原生環境（GPU）執行驗證。
3.  **安全性 (Security)**：
    *   **正常情況**：1-of-N 誠實假設（優於 BlockDFL 的概率性假設）。
    *   **異常情況**：回退至全網 PBFT（f<n/3），確保最終安全性。

**一句話定位**：
"Unlike **BlockDFL** which sacrifices security for efficiency via small committees, our approach achieves **Optimistic efficiency** without compromising **PBFT security**, while retaining **native computational generality**."
