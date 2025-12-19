# Blockchain Federated Learning: Incentive-Compatible Defense Against Committee Capture

## Section II. Background
本章節的目的是建立必要的技術背景，不進行批判，僅做教科書式的說明。
A. Federated Learning and Byzantine Resilience
介紹 FL 的基本架構，並定義何謂 Byzantine Fault Tolerance (BFT)。說明在分散式學習中，單個 Server 的故障或惡意行為會摧毀整個模型，這奠定了去中心化架構（BCFL）的必要性。
B. Blockchain-based Federated Learning (BCFL)
簡述區塊鏈如何取代中央伺服器，利用共識機制紀錄更新。重點說明 Stake-based participation（基於質押的參與）與獎勵分配的基本邏輯，這是後續討論經濟漏洞的基礎。
C. Incentive and Slashing Foundations
解釋區塊鏈中的經濟約束力。定義何謂質押（Staking）以及處罰（Slashing）。這裡要強調「代幣經濟安全性（Crypto-economic Security）」：即攻擊成本必須高於潛在收益。
## Section III. Related Work
本章節採取「漏斗原則」，逐步縮小範圍並指出前人工作的局限性。
A. Scaling BCFL: Layer-2 Approaches
* 內容： 探討現有的 zk-proof (zkML) 與早期借鑑 L2 的驗證方法。
* 批判點： 雖然這些方法保證了正確性，但 zkML 的運算開銷極大，且傳統驗證方法通常需要停止訓練（Blocking）來等待證明生成，限制了處理大模型或高頻更新的能力。
B. Efficiency via Committee-based Consensus
* 內容： 探討如 BlockDFL 等主流的 Layer-1 委員會方法。
* 批判點： 這些方法主要透過「隨機選取委員會」來換取 $O(1)$ 或 $O(C^2)$ 的效率。然而，如 FedBlock [2024] 所指出的，這些方法高度依賴「誠實大多數」假設。一旦惡意節點透過 Stake 累積佔領委員會，系統缺乏有效的自愈能力。
C. Vulnerabilities: From Data Poisoning to Model Manipulation
* 內容： 區分傳統的數據投毒（Data Poisoning）與更高級的惡意聚合攻擊（Malicious Aggregation）。
* 批判點： 強調現有防禦算法（如 Krum）多假設聚合者（Aggregator）是誠實的。當聚合者本身就是攻擊者時，這些防禦會失效。
* Gap 定位： 目前缺乏一種機制能「偵測並清除」這些具備合法權限的惡意驗證者，而這正是本研究要解決的核心問題。

## Section IV. Framework Design (Incentive-Compatible Defense)

**Non-blocking Optimistic Challenge:** 正常流程樂觀執行，不阻塞訓練，正常運行仍維持小型委員會選取使用Krum選取決定採納aggregators提供的具體哪個updates作為model update $O(c^2)$。

**Role: The Challenger (Bounty Hunter):** 任何節點（特別是被餓死的誠實節點）都可以擔任。

**Incentive Mechanism:** Internal Bounty from Slashing。挑戰成功的獎勵來自於被罰沒的惡意 Stake，無需外部基金會。

**Security Guarantee:** 只要 $Slashing \gg Potential\_Gain$，理性攻擊者就不敢作亂。

## Section V. Complexity & Efficiency Analysis (Theoretical)

**理論推導：** 由於有了 Slashing 的核威懾，我們不需要維持龐大的委員會來防共謀。

**結果：** 委員會大小 $C$ 可以大幅縮減（僅需滿足 Liveness），通訊複雜度從 $O(C_{large}^2)$ 降為 $O(C_{small}^2 + p \cdot N^2)$。

## Section VI. Experimental Evaluation

**VI-1 (Model Performance):** 對比 BlockDFL 在後期由於惡意 verifier 持續掠奪 stack，使被攻擊頻率持續上升 vs. 本方法維持收斂。

**VI-2 (Stake Dynamics):** 關鍵圖表。BlockDFL 中惡意 Stake 曲線超越誠實曲線；本方法中惡意 Stake 在嘗試攻擊瞬間歸零（Slashing）。

**VI-3 (Efficiency):** 展示在 "委員會人數更少" 的情況下，本方法依然保持了比 "大委員會 BlockDFL" 更高的安全性，證明了 Efficiency-Security Win-Win。
