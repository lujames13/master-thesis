# Chapter 2.6: 經濟激勵與質押機制 (1頁)

**Page Budget**: 1頁
**Goal**: 理解質押防止惡意、獎勵分配機制

**Content Outline (Enhanced - R5)**:

### 2.6.1 質押機制 (0.5頁)
- 聚合器/驗證者需質押代幣參與
- 最小質押門檻設計: 10-20×回合獎勵
- Slashing條件: 挑戰成功、協議違規

### 2.6.2 獎勵與懲罰 (0.5頁)

**獎勵公式** (0.2頁):
- Reward = α·DataQuality + β·DataVolume + γ·ComputeCost
- 參數α, β, γ設計原理：平衡數據貢獻與計算成本
- 範例計算：假設DataQuality=0.9, DataVolume=1000, ComputeCost=50

**懲罰機制** (0.2頁):
- 懲罰比例設計：輕微違規30%、嚴重違規100%質押損失
- Slashing條件枚舉：(1) 挑戰成功、(2) 超時未響應、(3) 提交無效數據
- 懲罰資金分配：50%獎勵挑戰者、50%進入獎勵池

**經濟安全性證明** (0.1頁):
- 誠實策略期望收益：E[Honest] = Reward - Stake·r（r為資金成本）
- 攻擊策略期望收益：E[Attack] = p·Gain - (1-p)·Penalty
- 安全條件：E[Honest] > E[Attack]，推導最小質押門檻

**Content from framework-design**:
- Lines 68-71 (4.2獎勵分配階段): 規則描述
- Lines 271-273 (H. 安全假設): 質押金額足以阻止惡意行為

**Content from deep_research**:
- deep_research_1027.md (2.5.2激勵與懲罰): 質押門檻、Slashing、獎勵公式

**Depth Control**:
- ✅ 解釋基本質押和獎勵原理
- ❌ 不詳述Shapley值、Stackelberg博弈（過於理論，可略）
- ❌ 不討論具體系統的激勵設計（PoFL等在Ch3）

---
