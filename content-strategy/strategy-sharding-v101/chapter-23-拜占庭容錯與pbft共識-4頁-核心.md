# Chapter 2.3: 拜占庭容錯與PBFT共識 (4頁) ⭐核心

**Page Budget**: 4頁
**Goal**: 深入理解PBFT協議、O(n²)複雜度來源、f<n/3條件

**Content Outline**:

### 2.3.1 Byzantine將軍問題 (0.8頁)
- 問題描述: 分散式系統中部分節點惡意或故障
- 拜占庭容錯定義: 系統能在部分節點Byzantine的情況下正確運作
- 理論界限: 需至少3f+1個節點容忍f個惡意節點

### 2.3.2 PBFT協議詳解 (2.2頁)
1. **三階段流程** (1.2頁)
   - **Pre-prepare階段**:
     - 主節點(primary)向所有副本(replicas)發送Pre-prepare消息
     - 包含提議值v和序列號n
     - 偽代碼

   - **Prepare階段**:
     - 副本收到Pre-prepare後，若接受則廣播Prepare消息
     - 收到2f個Prepare消息後進入prepared狀態
     - 偽代碼

   - **Commit階段**:
     - prepared狀態的副本廣播Commit消息
     - 收到2f+1個Commit消息後執行請求
     - 偽代碼

2. **安全性條件推導** (0.5頁)
   - Quorum規模: 2f+1
   - 兩個quorum交集至少f+1個節點
   - 證明: 至少一個誠實節點在交集中
   - 數學推導

3. **通訊複雜度分析** (0.5頁)
   - 每階段每個節點向所有其他節點發送消息
   - Pre-prepare: 1×(n-1) = O(n)
   - Prepare: n×n = O(n²)
   - Commit: n×n = O(n²)
   - 總計: O(n²)消息
   - 流程圖

### 2.3.3 PBFT變體簡述 (1頁)
1. **HotStuff** (0.5頁)
   - 使用門檻簽名將O(n²)降至O(n)
   - 管道化設計
   - 適用於大規模網絡

2. **Tendermint** (0.3頁)
   - 兩階段投票
   - 視圖切換O(n)

3. **與本研究的關聯** (0.2頁)
   - 本研究在挑戰模式下採用PBFT驗證
   - 未來可整合HotStuff降低挑戰時通訊開銷

**Content from framework-design (Precise References - NEW R2)**:
- **Lines 108-143**: 算法2 挑戰提交與驗證流程（完整偽代碼）
- **Lines 176-194**: 算法3 PBFT挑戰驗證程序（完整偽代碼）
- **Lines 254-273**: H. 安全假設（挑戰解決期間至少2f+1驗證者誠實）

**Content from deep_research (Precise References - NEW R2)**:
- **deep_research_1027.md Lines 37-44**: 2.2.1 PBFT詳解
  - Lines 39: 三階段協議（Pre-prepare, Prepare, Commit）
  - Lines 39: 消息複雜度O(n²)
  - Lines 39: n ≥ 3f + 1容錯條件
  - Lines 43: HotStuff/Tendermint變體
- **deep_research_1027.md Lines 41-42**: 在FL的應用（總複雜度O(R × V²)）

**Depth Control**:
- ✅ 必須包含完整偽代碼
- ✅ 必須有O(n²)數學推導
- ✅ 必須證明f<n/3條件
- ❌ 不討論FLCoin如何優化PBFT（Ch3）
- ❌ 不討論BlockDFL的PBFT投票機制（Ch3）

---
