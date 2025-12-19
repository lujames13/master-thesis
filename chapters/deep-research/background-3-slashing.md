# 區塊鏈激勵與罰沒機制文獻調查

權益質押(Staking)與罰沒(Slashing)構成現代 PoS 共識系統的經濟安全基石。本文獻調查涵蓋六篇核心文獻，建立「攻擊成本必須超過潛在收益」的加密經濟安全原則。

## 核心文獻摘要

### 1. Casper FFG — Ethereum 經濟終局性基礎

**引用**: V. Buterin and V. Griffith, "Casper the Friendly Finality Gadget," arXiv:1710.09437, 2017.

**核心機制**: 驗證者透過存入押金獲得投票權重，採用兩階段終局化（Justification → Finalization），需 **2/3 超級多數**達成共識。**罰沒條件**包含雙重投票(同一目標高度發布不同投票)與環繞投票(新投票包圍舊投票的 source-target 範圍)。

**經濟安全模型**: 若兩個衝突檢查點被終局化，**至少 1/3 總質押必被罰沒**，此為「可問責安全性」(Accountable Safety)。攻擊成本以 2025 年計約 **350 億美元**以上。

**已知漏洞**: Nothing-at-stake 透過罰沒解決；Long-range attacks 透過弱主觀性檢查點(約 36 天解綁期)緩解。

---

### 2. Gasper — Ethereum 完整共識協議

**引用**: V. Buterin et al., "Combining GHOST and Casper," arXiv:2003.03052, 2020.

**核心機制**: 結合 **LMD GHOST**(分叉選擇)與 **Casper FFG**(終局性)。驗證者需質押 32 ETH，每 12 秒 slot 進行區塊提議與見證。罰沒懲罰分三階段：即時懲罰(1/32 有效餘額)、36 天退出期持續扣款、**相關性懲罰**(第 18 天，依同期被罰沒總量線性擴大至 100%)。

**經濟安全模型**: 相關性懲罰設計確保協調攻擊代價遠超個體違規，**大規模攻擊將損失全部質押**。

**已知漏洞**: Balancing Attack 與 Avalanche Attack 可延遲終局化，已透過 Proposer Boosting 機制緩解。

---

### 3. Tendermint BFT — 拜占庭容錯共識

**引用**: E. Buchman, J. Kwon, and Z. Milosevic, "The latest gossip on BFT consensus," arXiv:1807.04938, 2018.

**核心機制**: 採用委託權益證明(DPoS)，投票權與質押量成正比。驗證者違反「Prevote-the-lock」規則或雙重簽名將被罰沒。下線懲罰為質押的 **1%**，雙重簽名懲罰為 **5%**。

**經濟安全模型**: **≥1/3 拜占庭投票權**才能違反安全性，**>2/3 誠實投票權**確保活性。Fork-accountability 性質保證違規者可被加密證據識別。

**已知漏洞**: Long-range attacks 透過 3 週解綁期與弱主觀性模型緩解；≥1/3 聯盟可發動審查攻擊或停機攻擊。

---

### 4. Cosmos Whitepaper — 跨鏈經濟安全

**引用**: J. Kwon and E. Buchman, "Cosmos: A Network of Distributed Ledgers," cosmos.network, 2016.

**核心機制**: 驗證者與委託者共同承擔罰沒風險。創新引入 **ReportHackTx** 系統：被駭驗證者可自我舉報，駭客獲得 5% 賞金，驗證者/委託者損失 5%，降低隱瞞誘因。

**經濟安全模型**: Zone 安全性取決於其驗證者集合；Hub 不驗證 Zone 交易，需用戶自行信任。跨鏈橋攻擊需 >2/3 拜占庭投票權。

---

### 5. Polkadot NPoS — 提名權益證明

**引用**: G. Wood, "Polkadot: Vision for a Heterogeneous Multi-Chain Framework," Web3 Foundation, 2016.

**核心機制**: 驗證者由**提名人**選舉產生(基於 Phragmén 比例代表演算法)，確保質押均勻分布以最大化最小驗證者支持量。罰沒採**漸進式設計**(0.01%–100%)，根據違規嚴重程度調整。

**經濟安全模型**: 所有平行鏈共享中繼鏈的「池化安全性」(Pooled Security)。長達 3 個月的解綁期允許事後發現違規並追溯懲罰。

---

### 6. 激勵相容性理論基礎

**引用**: J. Chiu and T. V. Koeppl, "Incentive Compatibility on the Blockchain," Bank of Canada Staff Working Paper 2018-34, 2018.

**核心框架**: 將區塊鏈安全形式化為機制設計問題，提出 **No-Double-Spending (NoDS) 約束**——類比經典激勵相容約束。關鍵公式 `p < RN(N-1)` 定義支付規模上限與確認區塊數的關係。

**理論貢獻**: 指出純 PoS 缺乏 PoW 的「沉沒成本」特性，**罰沒機制彌補此缺陷**，使違規者承擔不可恢復的損失。

---

## 總結：經濟安全設計原則

上述文獻共同確立三項核心原則：(1) **可問責性**——違規行為必須可被加密證據識別並歸責；(2) **攻擊成本 > 收益**——透過大額質押與罰沒確保理性攻擊者無利可圖；(3) **相關性懲罰**——協調攻擊的邊際成本遞增，防範委員會佔領攻擊。這些機制為後續分析經濟動機攻擊提供理論基礎。