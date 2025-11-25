# Blockchain Federated Learning: Incentive-Compatible Defense Against Vertical Collusion

## 1. Background

BCFL 介紹：解決中心化 FL 的 SPOF 和隱私問題。

## 2. Related Work (Committee & Consensus)

委員會機制（如 BlockDFL）是平衡效率的主流做法。

**Gap 1:** OpML/zkML 雖然安全，但限制了計算通用性（無法跑大模型/複雜聚合），因此我們仍需依賴 Native Execution（如 Krum）。

## 3. Related Work (Defense Limitations)

主流防禦（Krum, Trimmed Mean）主要針對 Data Poisoning（數據層）。

**Gap 2 (Critical):** 這些方法假設 Verifier 誠實執行算法。現有文獻忽略了 Verifier Collusion（共識層共謀）的風險。

## 4. Threat Model (The "Vertical Capture")

**攻擊者能力：** 理性節點，追求利益最大化。

**攻擊手段：** 潛伏 → 佔據多數 → Vertical Collusion（垂直共謀）。

**核心機制：** 惡意委員會通過 "Sub-optimal Update" 並排他性地分配獎勵（Strategic Starvation），導致誠實節點 Stake 停滯，惡意節點 Stake 指數增長。這不僅是破壞模型，更是接管網絡。

## 5. Framework Design (Incentive-Compatible Defense)

**Non-blocking Optimistic Challenge:** 正常流程樂觀執行，不阻塞訓練。

**Role: The Challenger (Bounty Hunter):** 任何節點（特別是被餓死的誠實節點）都可以擔任。

**Incentive Mechanism:** Internal Bounty from Slashing。挑戰成功的獎勵來自於被罰沒的惡意 Stake，無需外部基金會。

**Security Guarantee:** 只要 $Slashing \gg Potential\_Gain$，理性攻擊者就不敢作亂。

## 6. Complexity & Efficiency Analysis (Theoretical)

**理論推導：** 由於有了 Slashing 的核威懾，我們不需要維持龐大的委員會來防共謀。

**結果：** 委員會大小 $C$ 可以大幅縮減（僅需滿足 Liveness），通訊複雜度從 $O(C_{large}^2)$ 降為 $O(C_{small}^2 + p \cdot N^2)$。

## 7. Experimental Evaluation

**7-1 (Model Performance):** 對比 BlockDFL 在後期由於惡意 verifier 持續掠奪 stack，使被攻擊頻率持續上升 vs. 本方法維持收斂。

**7-2 (Stake Dynamics):** 關鍵圖表。BlockDFL 中惡意 Stake 曲線超越誠實曲線；本方法中惡意 Stake 在嘗試攻擊瞬間歸零（Slashing）。

**7-3 (Efficiency):** 展示在 "委員會人數更少" 的情況下，本方法依然保持了比 "大委員會 BlockDFL" 更高的安全性，證明了 Efficiency-Security Win-Win。
