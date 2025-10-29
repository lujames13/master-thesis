# Chapter Writer Agent 使用指南

## 快速開始

### 1. 切換到agent目錄
```bash
cd .claude/agents/chapter-writer
```

### 2. 啟動agent開始寫作
```bash
# 方式1: 使用Claude Code CLI
claude

# 方式2: 直接輸入寫作指令
```

---

## 雙模式運作

```
Mode 1: 初始寫作
├─ 輸入: strategy.md
├─ 輸出: chapterX-name-v1.md
└─ 目的: 創建新的section

Mode 2: 根據Review修改
├─ 輸入: section-review-X.X-vN.md
├─ 輸出: chapterX-name-v2.md (更新版)
└─ 目的: 修正Review指出的問題
```

---

## Mode 1: 初始寫作

### 常用指令

#### 寫作新section
```
根據 ../../content-strategy/strategy-20250129.md，寫作 Chapter 1, Section 1.1
```

#### 繼續寫作（已完成前面section）
```
繼續寫作 Chapter 1, Section 1.2，保持與 Section 1.1 的風格和術語一致
```

#### 寫作特定章節
```
根據 strategy，寫作 Chapter 2, Section 2.3 - PBFT協議（包含算法、偽代碼、數學推導）
```

### 寫作流程

1. **檢查狀態**
   - 讀取 strategy.md
   - 確認 section 狀態為 ⏸️ Not Started

2. **讀取規劃**
   - 提取內容項目列表
   - 確認深度要求
   - 了解頁數預算
   - 理解 Goal（如何支撐創新）

3. **讀取已完成內容**
   - 保持寫作風格一致
   - 使用相同術語
   - 避免重複

4. **按深度標準寫作**
   - Ch1: ≤20字/技術
   - Ch2: Tutorial級
   - Ch3: 批判性分析

5. **自檢**
   - 深度正確？
   - 頁數合理？
   - 包含必要元素？

6. **輸出**
   - 儲存到 chapters/ 目錄
   - 標記狀態和字數

---

## Mode 2: 根據Review修改

### 常用指令

#### 修改section
```
根據 ../../reviews/section-review-1.1-v1.md，修改 Chapter 1, Section 1.1
```

#### 確認修改完成
```
我已完成所有HIGH priority修改，請檢查並標記checkboxes
```

### 修改流程

1. **讀取Review Report**
   ```markdown
   ### 🔴 HIGH Priority
   - [ ] #1: Section 1.1, 第2段 - 刪減到≤20字
   - [ ] #2: Section 1.3 - 添加過渡句
   ```

2. **逐項修改**
   - 理解問題本質
   - 進行修改
   - 標記完成時間

3. **在Review Report標記**
   ```markdown
   - [x] #1: Section 1.1, 第2段 - 刪減到≤20字
         ✅ Fixed at 2025-01-30 15:30 by Writer
         Changes: 從35字刪減到15字，只保留問題導向
   ```

4. **提交v2**
   - 更新章節文件
   - 更新review report
   - 提交給Review Agent重新審核

---

## 深度標準快速參考

### Chapter 1: Introduction

**目標**: 說服讀者「需要我的創新」

**規則**:
- ✅ ≤20字/技術
- ✅ 點出問題/缺陷
- ❌ 無技術細節
- ❌ 無歷史背景
- ❌ 無具體方案

**範例對比**:
```markdown
✅ "PBFT因O(n²)複雜度限制可擴展性"（12字）

❌ "PBFT（Practical Byzantine Fault Tolerance）協議由Castro
和Liskov於1999年提出，包含Pre-prepare、Prepare、Commit
三階段..." (太詳細，這是Ch2內容)
```

---

### Chapter 2: Background

**目標**: 讀者理解「技術如何運作」

**必須包含**:
- ✅ 算法流程（逐步說明）
- ✅ 偽代碼（Algorithm block）
- ✅ 數學推導（公式+證明）
- ✅ 複雜度分析（with計算）
- ✅ 流程圖（如適用）

**禁止**:
- ❌ 討論具體研究系統（FLCoin, opML等）
- ❌ 批判性分析
- ❌ 方案比較

**Algorithm Block 範例**:
```markdown
**Algorithm 1**: PBFT Pre-prepare Phase
```
Input: Client request m
Output: ⟨PRE-PREPARE, v, n, d⟩ message
1: upon receiving request m from client do
2:   assign sequence number n
3:   compute digest d ← hash(m)
4:   broadcast ⟨PRE-PREPARE, v, n, d⟩ to all replicas
5: end upon
```
```

**數學推導範例**:
```markdown
在Prepare階段，每個備份節點需要：
1. 向其他n-1個節點發送PREPARE消息
2. 接收來自其他n-1個節點的PREPARE消息

因此，Prepare階段的總消息數為：
  M_prepare = n × (n-1) ≈ O(n²)

當n=10時：10×9 = 90條消息
當n=100時：100×99 = 9,900條消息
當n=1000時：1000×999 ≈ 1,000,000條消息
```

---

### Chapter 3: Related Work

**目標**: 證明「我的創新是必要且優越的」

**標準句型**:
```markdown
[作者]等人[ref]提出[方案]，採用[核心技術]實現[主要貢獻]，
[關鍵性能指標]。然而，該系統[主要局限性]，且[未解決問題]。
相較之下，本研究[我們的優勢]。
```

**必須包含**:
- ✅ 方案的主要貢獻
- ✅ 關鍵性能指標（數字）
- ✅ 主要局限性
- ✅ 與「本研究」的對比

**範例**:
```markdown
✅ Good:
Ren等人[4]提出FLCoin系統，採用滑動窗口委員會機制將
通訊複雜度從O(n²)降至O(c)，在100節點下實現<5秒共識延遲。
然而，該系統採用固定委員會窗口，無法根據實時威脅動態調整
安全強度，且容錯度仍受限於f<c/3（約30%）。相較之下，本研究
提出的動態切換機制能根據威脅等級自適應調整共識模式，在
低風險時達到O(R/N)效率，高風險時提供完整Byzantine容錯。
```

---

## 引用處理規則

### Background (Ch2) - 必須即時添加
```markdown
✅ "Castro和Liskov[7]提出PBFT協議..."
✅ "HotStuff[12]簡化了視圖切換過程..."

❌ "Castro和Liskov提出PBFT協議[TODO]..."（不可！）
```

### Introduction & Related Work - 可使用TODO
```markdown
✅ "現有方案如FLCoin[TODO]和opML[TODO]各有局限..."
✅ "區塊鏈聯邦學習[TODO]近年來受到關注..."
```

最後由Citation Manager統一補充。

---

## 術語使用規範

### 首次出現格式
```markdown
"實用拜占庭容錯（Practical Byzantine Fault Tolerance, PBFT）協議"

格式：中文全稱（英文全稱, 縮寫）
```

### 後續使用
```markdown
選項1: "PBFT協議的三階段..."（推薦，簡潔）
選項2: "實用拜占庭容錯協議..."（可，但較長）

統一選擇一種！
```

### 一致性檢查
```markdown
✅ 全文統一用 "拜占庭容錯"
❌ 混用 "拜占庭容錯" / "Byzantine容錯" / "BFT"
```

---

## Git 提交規範

### 完成新section
```bash
git add chapters/chapter1-introduction-v1.md
git commit -m "Complete: Ch1, Section 1.1 - 研究背景"
```

### 修改後提交
```bash
git add chapters/chapter1-introduction-v1.md
git add reviews/section-review-1.1-v1.md
git commit -m "Review: Section 1.1 - v2 (fixed depth issues)"
```

### 完成整章
```bash
git add chapters/chapter1-introduction-v1.md
git commit -m "Complete: Chapter 1 - Introduction (all sections)"
```

---

## 常見錯誤與解決方案

### 錯誤1: Ch1過於詳細
**症狀**: Review說"Section 1.X超過20字"

**診斷**:
```markdown
❌ 你寫了: "PBFT協議由Castro和Liskov於1999年提出，通過
Pre-prepare、Prepare、Commit三階段達成共識，可容忍f<n/3
個惡意節點..." (50+字)

✅ 應該是: "PBFT因O(n²)複雜度限制可擴展性" (12字)
```

**解決**:
1. 重新讀Ch1深度標準
2. 只保留「問題導向」的描述
3. 刪除技術細節、歷史、階段說明

---

### 錯誤2: Ch2缺少算法細節
**症狀**: Review說"Section 2.X太簡單，缺少偽代碼"

**診斷**:
```markdown
❌ 你寫了: "PBFT採用三階段共識機制實現拜占庭容錯。"
（太簡略，像Ch1）

✅ 應該包含:
1. 三階段詳細流程
2. Algorithm block（偽代碼）
3. 數學推導
4. 複雜度分析（with計算）
```

**解決**:
1. 重新讀Ch2深度標準
2. 添加偽代碼
3. 添加數學推導
4. 添加具體數字範例（n=10, 100, 1000）

---

### 錯誤3: Ch3缺少批判
**症狀**: Review說"Section 3.X只描述，無批判"

**診斷**:
```markdown
❌ 你寫了: "FLCoin採用滑動窗口委員會機制，實現了高效共識。"
（純描述，無批判）

✅ 應該包含:
"FLCoin採用滑動窗口委員會機制將複雜度降至O(c)，在100節點
下實現<5秒延遲。然而，該系統採用固定窗口，無法動態調整
安全強度。相較之下，本研究的動態切換機制..."
```

**解決**:
1. 使用標準句型
2. 必須包含「然而」或「但是」指出局限
3. 必須包含與「本研究」的對比

---

### 錯誤4: 與其他章重複
**症狀**: Review說"與Ch2重複"

**診斷**:
```markdown
問題: Ch3重複解釋了PBFT三階段

原因: 忽略了「視角不同」原則
- Ch1: 問題（O(n²)問題）
- Ch2: 原理（三階段流程）
- Ch3: 對比（FLCoin的固定窗口 vs 我的動態）
```

**解決**:
1. 檢查strategy的Overlaps區
2. 改變視角，不要重複解釋技術原理
3. Ch3聚焦在「方案的局限」和「與我的對比」

---

### 錯誤5: 忽略strategy規劃
**症狀**: Review說"你寫了strategy沒規劃的內容"

**診斷**:
```markdown
問題: Strategy只規劃了PBFT和Optimistic，但你寫了PoW

原因: 沒有以strategy為準
```

**解決**:
1. **立即停止**
2. 重新讀strategy.md
3. 如果認為應該添加 → 升級給Strategist重新規劃
4. **不要自行決定改變規劃**

---

## 自檢清單

寫完section後，使用這個清單自檢：

### 所有章節通用
- [ ] 深度符合本章標準？
- [ ] 頁數在預算內？
- [ ] 沒有與其他章verbatim重複？
- [ ] 術語使用一致？（首次中英並列，後續統一）
- [ ] 語調學術正式？（無口語、無第一人稱）

### Chapter 1專用
- [ ] 每個技術 ≤20字？
- [ ] 只點出問題，無技術細節？
- [ ] 無歷史背景？
- [ ] 無具體方案討論？

### Chapter 2專用
- [ ] 包含算法流程？
- [ ] 包含偽代碼（Algorithm block）？
- [ ] 包含數學推導？
- [ ] 包含複雜度分析（with具體數字）？
- [ ] 無討論具體研究系統？
- [ ] 引用完整（不可用TODO）？

### Chapter 3專用
- [ ] 每個方案都有貢獻？
- [ ] 每個方案都有性能指標（數字）？
- [ ] 每個方案都有批判（「然而」）？
- [ ] 每個方案都與「本研究」對比？
- [ ] 無重複解釋技術原理？

---

## 與其他Agent協作

### ← 接收來自 Content Strategist
```
Strategist完成strategy → Writer開始寫作
```

### → 提交給 Review Agent
```
Writer完成section → 提交審核 → Review生成報告
```

### ← 接收來自 Review Agent
```
Review完成 → Writer根據action items修改 → 再次提交
```

### → 配合 Citation Manager
```
Ch1/Ch3使用[TODO] → Citation Manager最後補充完整引用
```

---

## 範例：完整寫作循環

### Round 1: 初始寫作

**指令**:
```
根據 strategy-20250129.md，寫作 Chapter 1, Section 1.1 - 研究背景
```

**Writer輸出**:
```markdown
# Chapter 1: Introduction

## 1.1 研究背景

區塊鏈技術與聯邦學習結合為隱私保護的分散式機器學習提供
新方向[TODO]。然而，現有方案面臨效率與安全的兩難：實用
拜占庭容錯（Practical Byzantine Fault Tolerance, PBFT）
協議因O(n²)通訊複雜度限制可擴展性...

---
Status: 🚧 In Progress
Word Count: 850
Last Updated: 2025-01-30 14:00
```

**Git提交**:
```bash
git commit -m "Complete: Ch1, Section 1.1 - 研究背景"
```

---

### Round 2: Review

**切換到Review Agent**:
```bash
cd ../review-agent
```

**指令**:
```
審核 ../../chapters/chapter1-introduction-v1.md 的 Section 1.1
```

**Review Agent輸出**: `section-review-1.1-v1.md`
```markdown
## 🎯 Executive Summary
- **Overall Status**: ⚠️ NEEDS REVISION
- **Critical Issues**: 1 HIGH priority

## ✅ Action Items
### 🔴 HIGH Priority
- [ ] #1: 第3行過於詳細 - "實用拜占庭容錯"應簡化為"PBFT"
```

---

### Round 3: 修改

**切換回Writer**:
```bash
cd ../chapter-writer
```

**指令**:
```
根據 ../../reviews/section-review-1.1-v1.md，修改 Section 1.1
```

**Writer**:
1. 讀取review report
2. 修改章節內容
3. 標記checkbox:
   ```markdown
   - [x] #1: 第3行過於詳細
         ✅ Fixed at 2025-01-30 15:30
         Changes: 簡化為"PBFT因O(n²)複雜度限制可擴展性"
   ```

**Git提交**:
```bash
git add chapters/chapter1-introduction-v1.md
git add reviews/section-review-1.1-v1.md
git commit -m "Review: Section 1.1 - v2 (simplified terminology)"
```

---

### Round 4: 再次審核

**Review Agent**:
```
審核 Section 1.1 v2
```

**結果**: ✅ APPROVED

**繼續下一個section**:
```
根據 strategy，寫作 Chapter 1, Section 1.2
```

---

## 輸出文件格式

### 章節文件命名
```
chapters/chapter1-introduction-v1.md
chapters/chapter2-background-v1.md
chapters/chapter3-related-work-v1.md
```

### 文件結構
```markdown
# Chapter X: [章節名稱]

## X.1 [Section 1 標題]

[內容]

## X.2 [Section 2 標題]

[內容]

---
Status: 🚧 In Progress / ✅ Completed
Word Count: [總字數]
Last Updated: YYYY-MM-DD HH:MM
```

---

## 故障排除

### Q: 不確定深度是否正確？
**A**: 對照README中的「範例對比」，特別是「✅ Good」vs「❌ Bad」部分。

### Q: Review說我偏離strategy怎麼辦？
**A**:
1. 重新讀strategy.md
2. 確認你寫的內容是否在規劃內
3. 如果不確定，詢問Review Agent

### Q: 多個HIGH priority無法同時修正？
**A**:
1. 一個一個修
2. 每修正一個就標記checkbox
3. 如果衝突，在review report註明原因

---

## 檔案結構

```
master-thesis/
├── .claude/agents/chapter-writer/
│   ├── agent.md       # Agent prompt
│   └── README.md      # 本文件
├── content-strategy/
│   └── strategy-20250129.md   # 寫作依據（SSOT）
├── chapters/
│   ├── chapter1-introduction-v1.md
│   ├── chapter2-background-v1.md
│   └── chapter3-related-work-v1.md
├── reviews/
│   └── section-review-1.1-v1.md   # 修改依據
└── deep_research_*.md  # 補充細節參考
```

---

## 快速參考卡

```
┌─────────────────────────────────────────────┐
│ Chapter Writer Quick Reference              │
├─────────────────────────────────────────────┤
│ Mode 1: 初始寫作 (根據strategy)             │
│ Mode 2: 根據Review修改                      │
├─────────────────────────────────────────────┤
│ Ch1: ≤20字/技術, 問題導向                   │
│ Ch2: Tutorial級, 算法+偽代碼+推導           │
│ Ch3: 批判性分析, 貢獻+局限+對比             │
├─────────────────────────────────────────────┤
│ Ch2引用: 即時添加 (不可TODO)                │
│ Ch1/Ch3引用: 可用TODO                       │
├─────────────────────────────────────────────┤
│ 術語首次: 中文（English, ABC）              │
│ 術語後續: ABC 或 中文（統一）               │
└─────────────────────────────────────────────┘
```
