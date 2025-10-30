# Chapter 3.3: 混合共識方案 (2頁)

**Page Budget**: 2頁
**Goal**: 批判現有混合方案的「靜態混合」vs 本研究的「動態切換」

---

### 3.3.1 EPP-BCFL - PoS+BFT混合 (1頁)

**Content Outline**:

1. **貢獻** (0.3頁)
   - PoS驗證器選擇 + BFT共識
   - 環形MPC聚合
   - 性能: 95.2%準確率，43%開銷降低

2. **技術細節** (0.2頁)
   - PoS階段: 質押選擇驗證器
   - BFT階段: 委員會共識
   - 固定流程: 每輪都執行兩階段

3. **局限性** (0.3頁)
   - **靜態混合**: 每輪固定執行PoS+BFT，無法跳過
   - 非威脅感知: 無論威脅等級都相同流程
   - 缺乏動態調整驗證強度機制

4. **與本研究對比** (0.2頁)
   - 本研究: 威脅檢測觸發切換（非固定流程）
   - 正常情況可完全跳過驗證（樂觀執行）
   - 威脅等級決定驗證範圍（輕量級→完整PBFT）

**Content from deep_research**:
- deep_research_1009.md: EPP-BCFL的PoS+BFT機制、環形MPC
- deep_research_1027.md (2.2.3混合共識方法)

**Depth Control**:
- ✅ 說明PoS+BFT組合（引用Ch2 PBFT，簡述PoS）
- ✅ 批判「靜態vs動態」核心差異
- ❌ 不詳細解釋PoS機制（與本研究無關）

---

### 3.3.2 Layer 1 + Layer 2結合 (0.6頁)

**Content Outline**:

1. **IEEE 9223754混合區塊鏈** (0.3頁)
   - 公鏈層(PoS)處理價值轉移
   - 聯盟鏈層(PBFT)處理FL更新
   - 局限: 層級固定，非威脅感知

2. **FLock - Off-chain聚合** (0.3頁)
   - Off-chain聚合 + On-chain記錄
   - Gas成本節省95%
   - 局限: Off-chain階段無Byzantine容錯

**Content from deep_research**:
- deep_research_1027.md (2.2.3 Layer 1 + Layer 2結合方案)

**Depth Control**:
- ✅ 每個方案簡要批判（0.3頁）
- ❌ 不展開公鏈/聯盟鏈技術細節

**壓縮選項 (R3)**: 若需壓縮，減至0.4頁（各0.2頁）

---

### 3.3.3 Stake-based PBFT (0.4頁)

**Content Outline**:

1. **BlockDFL的質押PBFT** (0.2頁)
   - 質押驅動驗證器選擇
   - 實驗: 40%惡意容錯

2. **局限與對比** (0.2頁)
   - 質押機制增強安全但仍靜態PBFT
   - 本研究: 質押+動態切換，雙重增強

**Content from deep_research**:
- deep_research_1027.md (2.2.3 Stake-based PBFT)

**壓縮選項 (R3)**: 若需壓縮，減至0.3頁（簡化為對3.1.3 BlockDFL的引用）

---
