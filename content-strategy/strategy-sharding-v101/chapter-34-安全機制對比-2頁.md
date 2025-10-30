# Chapter 3.4: 安全機制對比 (2頁)

**Page Budget**: 2頁
**Goal**: 對比Byzantine容錯方法，證明本研究的多層檢測+PBFT驗證優勢

---

### 3.4.1 Byzantine容錯聚合算法 (1.2頁)

**Content Outline**:

1. **Krum** (0.4頁)
   - 原理: L2距離選擇最近鄰居更新
   - 複雜度: O(n²·d)
   - 局限: Non-IID下f<n/5，Adaptive attack可破解
   - 對比: 本研究PBFT提供理論f<n/3保證

2. **Trimmed Mean** (0.4頁)
   - 原理: Coordinate-wise trimming
   - 局限: Trim attack繞過，忽略參數關聯
   - 對比: 本研究重新計算完整聚合而非trimming

3. **FLTrust** (0.4頁)
   - 原理: Trust score based on trusted dataset
   - 局限: 需trusted dataset（違反FL隱私），Long con破解
   - 對比: 本研究無需trusted dataset，PBFT共識驗證

**Content from deep_research**:
- deep_research_1027.md (2.4.2現有防禦機制（Krum、Trimmed Mean、FLTrust詳細分析）)
- 表2.4安全機制對比

**Depth Control**:
- ✅ 每個算法說明原理+局限+對比（0.4頁）
- ❌ 不提供算法偽代碼（那是各論文的工作）
- ❌ 不展開數學推導

---

### 3.4.2 密碼學方法 (0.5頁)

**Content Outline**:

1. **同態加密** (0.2頁)
   - 優勢: 隱私保護
   - 局限: **不防model poisoning**，30-100×計算開銷

2. **TEE (SGX)** (0.2頁)
   - 優勢: Remote attestation
   - 局限: **惡意aggregator本身無效**，Side-channel攻擊

3. **對比總結** (0.1頁)
   - 密碼學方法解決隱私，非Byzantine容錯
   - 本研究: PBFT解決Byzantine，可與密碼學組合

**Content from deep_research**:
- deep_research_1027.md (2.4.2密碼學方法（同態加密、SMC、TEE）)
- 表2.4安全機制對比

**壓縮選項 (R3)**: 若需壓縮，減至0.3頁（同態加密、TEE各0.1頁，刪除SMC）

---

### 3.4.3 本研究優勢總結 (0.3頁)

**Content Outline**:
- **動態威脅檢測**: 統計異常+行為模式+Cross-validation
- **自適應響應**: 輕量級監控→Targeted PBFT→全網PBFT
- **分散式檢測**: 避免單點trust假設
- **理論保證**: f<n/3拜占庭容錯
- **效率提升**: N×V/f倍 vs 純PBFT

---
