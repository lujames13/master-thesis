# Chapter 3.1: 多聚合器架構方案 (3.5頁)

**Page Budget**: 3.5頁
**Goal**: 批判現有多聚合器方案的固定/靜態設計，突顯本研究的動態切換優勢

---

### 3.1.1 FLCoin - 委員會優化BFT (1.2頁)

**Content Outline**:

1. **貢獻** (0.3頁)
   - 滑動窗口委員會機制
   - 雙協議設計: 快速協議3階段、備用協議5階段
   - 通訊複雜度: O(n²) → O(3c-5c)
   - 引用Ch2的PBFT知識，說明如何優化

2. **性能數據** (0.2頁)
   - 委員會規模s=100: <5秒共識延遲
   - 安全概率: 98.4%（基於超幾何分佈）
   - 通訊量減少90%+ vs 標準PBFT

3. **局限性分析** (0.4頁)
   - **固定委員會規模**: 無法根據實時威脅等級調整
   - 威脅低時: 固定100個驗證者產生不必要開銷
   - 威脅高時: 固定規模可能不足
   - 缺乏威脅檢測與動態響應機制

4. **與本研究對比** (0.3頁)
   - 本研究: 正常情況O(R/N)樂觀執行（遠低於FLCoin的O(3c)）
   - 檢測到威脅時: 動態觸發PBFT，驗證範圍根據威脅等級調整
   - 效率提升: N×V/f倍 vs FLCoin的固定開銷
   - 安全性: 同樣達到f<n/3，但更靈活

**Content from deep_research (Precise References - NEW R2)**:
- **deep_research_1009.md Lines 16-18**: FLCoin技術概述
  - Line 17: 雙層區塊鏈設計、優化BFT協議（快速協議3階段、故障時5階段）
  - Line 17: 線性通訊模式O(3c)到O(5c)
  - Line 17: 委員會規模s=100時共識延遲<5秒，拜占庭安全概率98.4%
- **deep_research_1027.md Lines 14-21**: 2.1.2委員會共識機制、架構對比
  - Lines 16-18: FLCoin滑動窗口委員會機制詳細技術
  - Line 30 (表2.1): O(3c-5c)d複雜度、98.4%安全性

**Depth Control**:
- ✅ 引用Ch2的PBFT三階段，說明FLCoin如何優化（不重新解釋PBFT）
- ✅ 批判必須有具體技術差異（固定vs動態）
- ❌ 不重複解釋什麼是PBFT（Ch2已講）

---

### 3.1.2 MCFLM-CB - 動態分組PBFT (0.9頁)

**Content Outline**:

1. **貢獻** (0.2頁)
   - 動態分組PBFT (DG-PBFT)
   - 複雜度: O(n²) → O(log n)
   - 聲譽加權聚合 (R-WFA)

2. **技術細節** (0.2頁)
   - 基於延遲的動態分組
   - 組內PBFT並行，組間代表共識
   - 性能: 97%消息減少

3. **局限性分析** (0.3頁)
   - **聲譽系統脆弱性**: 易受Long Con攻擊
   - 惡意節點可長期建立高聲譽後突然攻擊
   - 聲譽操縱、冷啟動問題

4. **與本研究對比** (0.2頁)
   - 本研究: 不依賴單一聲譽指標
   - 多層威脅檢測: 統計異常+行為模式+PBFT共識
   - 即使聲譽被操縱，PBFT驗證仍可檢測惡意

**Content from deep_research**:
- deep_research_1009.md: MCFLM-CB的DG-PBFT流程、R-WFA公式
- deep_research_1027.md (2.5.3聲譽機制Gaming漏洞分析)

**Depth Control**:
- ✅ 簡要說明DG-PBFT原理（2-3句，引用Ch2 PBFT背景）
- ✅ 重點批判聲譽系統局限
- ❌ 不詳細解釋分組算法（那是MCFLM-CB論文的工作）

**壓縮選項 (R3)**: 若需壓縮，減至0.7頁（刪除技術細節，保留核心批判）

---

### 3.1.3 BlockDFL - PBFT投票+Krum (0.7頁)

**Content Outline**:

1. **貢獻** (0.2頁)
   - 雙層評分: 質押篩選 + 質量測試
   - Krum異常檢測 + PBFT投票
   - 40%惡意容錯實驗驗證

2. **性能** (0.1頁)
   - 99.29% MNIST準確率（40%惡意）
   - <3秒聚合+驗證

3. **局限性** (0.2頁)
   - **靜態PBFT**: 每輪都執行PBFT投票，無樂觀模式
   - 即使威脅為零，仍需O(V²)驗證開銷
   - Krum在Non-IID下容錯度降至f<n/5

4. **與本研究對比** (0.2頁)
   - 本研究: 正常情況O(R/N)樂觀執行（BlockDFL每輪O(V²)）
   - 僅檢測到威脅時才啟動PBFT
   - 平均複雜度: (1-p)·O(R/N) + p·O(R×V)，當p<10%時遠優於BlockDFL

**Content from deep_research**:
- deep_research_1009.md: BlockDFL雙層評分、Krum+PBFT機制
- deep_research_1027.md (2.4.2 Byzantine容錯聚合、Krum局限)

**Depth Control**:
- ✅ 簡述Krum原理（L2距離選擇，1句話+引用Ch2如有）
- ✅ 批判「靜態vs動態」的效率差異
- ❌ 不詳細解釋Krum算法（可引用但不展開）

---

### 3.1.4 BMA-FL - DRL優化多聚合器 (0.7頁)

**Content Outline**:

1. **貢獻** (0.2頁)
   - 異構多聚合器架構
   - 深度強化學習(DRL)優化客戶端分配
   - PBCM輕量共識

2. **優勢** (0.1頁)
   - 資源利用效率提升
   - 適應邊緣計算異構環境

3. **局限性** (0.2頁)
   - **聚合器間協調開銷**: O(m²)
   - DRL訓練速度慢，難以實時適應
   - 缺乏Byzantine容錯分析

4. **與本研究對比** (0.2頁)
   - 本研究: 輪替機制O(1)選擇，無協調開銷
   - 威脅檢測實時觸發，無需DRL訓練
   - 明確Byzantine容錯保證f<n/3

**Content from deep_research**:
- deep_research_1009.md: BMA-FL的DRL策略、PBCM共識
- deep_research_1027.md (2.1.2多聚合器協調架構)

**Depth Control**:
- ✅ 簡述DRL優化概念（不展開DRL算法）
- ✅ 批判協調複雜度
- ❌ 不詳細解釋DRL網絡結構

---
