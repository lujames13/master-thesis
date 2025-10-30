# Chapter 2.1: 聯邦學習基礎 (1.5頁)

**Page Budget**: 1.5頁
**Goal**: 理解FL訓練流程、聚合算法、為何需要聚合器

**Content Outline**:
1. **FL架構與流程** (0.5頁)
   - 客戶端-聚合器架構
   - 訓練流程: 模型分發 → 本地訓練 → 模型上傳 → 聚合 → 新輪次

2. **FedAvg聚合算法** (0.5頁)
   - 加權平均公式: w_{t+1} = Σ(n_k/n)w_k^t
   - 計算複雜度: O(K×d)
   - 偽代碼

3. **聚合器角色與挑戰** (0.5頁)
   - 聚合器負責收集、聚合、分發模型
   - 單聚合器瓶頸: 計算負載、通訊開銷、單點故障

**Content from framework-design**:
- Lines 38-77 (4.2系統工作流程): 訓練階段、聚合階段（技術細節，無具體系統名稱）

**Content from deep_research**:
- deep_research_1027.md Lines 5-9 (2.1.1 FedAvg算法細節)
- 禁止: 討論FLCoin等具體系統

**Depth Control**:
- ✅ 必須有FedAvg偽代碼
- ✅ 必須推導O(K×d)複雜度
- ❌ 不討論Byzantine-robust聚合算法（Krum等在Ch3）

---
