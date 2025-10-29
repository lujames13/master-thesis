# Review Agent 使用指南

## 快速開始

### 1. 切換到agent目錄
```bash
cd .claude/agents/review-agent
```

### 2. 啟動agent進行審核
```bash
# 方式1: 使用Claude Code CLI
claude

# 方式2: 直接輸入審核指令
```

---

## 審核階段總覽

```
Strategy完成 → Stage 0: Strategy Review
      ↓
Section完成 → Stage 1: Section Review (循環N次)
      ↓
Chapter完成 → Stage 2: Cross-Chapter Review
      ↓
全部完成 → Stage 3: Final Review
```

---

## 常用審核指令

### Stage 0: 審核策略
```
審核 ../../content-strategy/strategy-20250129.md 的合理性
```

輸出：`reviews/strategy-review-v1.md`

### Stage 1: 審核Section
```
審核 ../../chapters/chapter1-introduction-v1.md 的 Section 1.1
```

輸出：`reviews/section-review-1.1-v1.md`

### Stage 2: 跨章節審核
```
進行 Chapter 1 的 Cross-Chapter Review，檢查資源分配和內容洩漏
```

輸出：`reviews/cross-chapter-review-ch1.md`

### Stage 3: 最終審核
```
進行三章的 Final Review，檢查整體一致性
```

輸出：`reviews/final-review.md`

### 審核修改後的版本
```
審核 Section 1.1 的 v2 版本，確認 action items 是否完成
```

---

## 審核優先級說明

### 🔴 Priority 1 - MUST FIX
這些問題會**阻擋進度**，必須立即修正：

1. **邏輯連貫性** - 論點推進不合理
2. **深度正確性** - Ch1太詳細 / Ch2缺算法 / Ch3無批判
3. **重複檢查** - 與其他章節 verbatim 重複

**處理**: Writer必須修正後才能進入下一個section

### 🟡 Priority 2 - SHOULD FIX
這些問題可以**批量修改**：

4. **引用完整性** - 缺少引用（Background除外）
5. **術語一致性** - 術語使用不一致

**處理**: 可以累積後一起修改

### ℹ️ Priority 3 - POLISH
這些是**語言優化**：

6. **語言流暢度** - 語言不夠學術

**處理**: Polish階段再處理

---

## 關鍵判斷：寫作 vs 架構問題

### ✅ 寫作問題 → Writer修改
```
問題：Section 2.3 缺少PBFT的偽代碼
判斷：Strategy有規劃，Writer沒寫 → 寫作問題
處理：Writer補充偽代碼
```

### 🚨 架構問題 → 升級到Strategist
```
問題：Ch2用了4頁討論FLCoin系統
判斷：具體研究系統應在Ch3 → 架構問題
處理：
1. 生成 escalation-report-20250129.md
2. Strategist重新規劃Ch2/Ch3邊界
3. 更新strategy → v1.1
4. Writer根據新strategy重寫
```

### 升級條件（4種情況）
1. **邊界模糊**: Ch2討論了具體研究系統
2. **頁數不足**: 3頁內容塞到1頁
3. **遺漏技術**: 關鍵技術被遺漏
4. **深度錯誤**: 深度分配策略本身有問題

---

## 輸出文件說明

### 1. Section Review Report
**檔名**: `section-review-X.X-vN.md`

**結構**:
- 🎯 Executive Summary
- 📊 Priority 1-3 Checks
- 🚨 寫作/架構問題判斷
- ✅ Action Items (帶checkbox)
- 📊 Quality Metrics
- 🔄 Next Steps

**範例**:
```markdown
## ✅ Action Items Summary

### 🔴 HIGH Priority
- [ ] **#1**: 1.2節第3段過於詳細 - 刪減到≤20字
- [ ] **#2**: 1.3節缺少與1.2的過渡句

### 🟡 MEDIUM Priority
- [ ] **#3**: "共識機制"首次出現需中英並列
```

### 2. Cross-Chapter Review Report
**檔名**: `cross-chapter-review-chX.md`

**重點**:
- 資源使用分析（實際 vs 規劃頁數）
- 內容洩漏檢查（Ch2是否討論研究系統）
- 術語一致性（整章內）

### 3. Escalation Report
**檔名**: `escalation-report-YYYYMMDD.md`

**內容**:
- 問題描述
- 為何是架構問題
- 建議調整方向
- 影響範圍

---

## 審核心態指南

### 你是嚴格但公正的教授

✅ **Do**:
- 標準極高，絕不妥協
- 給予具體可行的改善建議
- 明確指出問題所在位置
- 提供修改範例

❌ **Don't**:
- 不要模糊說「語言不夠好」
- 不要接受「差不多就好」
- 不要忽略小問題

### 審核循環預期
```
v1 → 通常有5-10個issues → NEEDS REVISION
v2 → 修正後剩2-3個 → NEEDS REVISION
v3 → 全部通過 → APPROVED
```

第一版有問題是**正常的**，重點是提供**可追蹤的改善路徑**。

---

## 與其他Agent協作

### ← 接收來自 Chapter Writer
```
Writer完成section → 提交審核
```

### → 反饋給 Chapter Writer
```
產生review report → Writer修改 → 再次審核
```

### → 升級到 Content Strategist
```
發現架構問題 → 產生escalation report → Strategist重新規劃
```

### → 配合 Citation Manager
```
Final Review時 → 檢查引用完整性
```

---

## 專項檢查指南

### 深度正確性檢查

#### Chapter 1 標準
```
❌ FAIL: "PBFT是一種共識協議，由Castro和Liskov於1999年提出..."
✅ PASS: "PBFT因O(n²)導致效能瓶頸"
```

#### Chapter 2 標準
```
❌ FAIL: "PBFT是一種拜占庭容錯共識機制"（太簡略）
✅ PASS: [包含算法流程、偽代碼、數學推導、複雜度分析]
```

#### Chapter 3 標準
```
❌ FAIL: "FLCoin採用PBFT進行共識"（無批判）
✅ PASS: "FLCoin採用固定滑動窗口優化PBFT。然而，固定窗口無法適應不同威脅等級，導致[問題]。"
```

### 重複檢查方法
1. 搜尋相同關鍵詞（PBFT, Byzantine等）
2. 比對是否 verbatim 重複
3. 檢查視角是否不同：
   - Ch1: 問題導向（O(n²)問題）
   - Ch2: 原理導向（算法流程）
   - Ch3: 對比導向（FLCoin vs 我的）

---

## 範例：完整審核流程

### 情境：Writer提交 Section 1.1 v1

#### Step 1: 讀取文件
```
讀取 ../../chapters/chapter1-introduction-v1.md 的 Section 1.1
讀取 ../../content-strategy/strategy-20250129.md 的 1.1 規劃
```

#### Step 2: 執行審核
```
進行 Section 1.1 的審核
```

#### Step 3: Agent輸出
```markdown
# Section Review Report

## 🎯 Executive Summary
- **Overall Status**: ⚠️ NEEDS REVISION
- **Critical Issues**: 2 HIGH priority
- **Estimated Fix Time**: 30分鐘

## 📊 Priority 1 Checks (MUST FIX)

### 2️⃣ 深度正確性
**Status**: ❌ FAIL

#### Issue #1: 1.1節第2段過於詳細 🔴 HIGH
**Location**: Section 1.1, 第2段
**Current**: "PBFT是一種實用拜占庭容錯協議，由Castro和Liskov於1999年提出，通過三階段投票達成共識..."（35字）
**Problem**: Ch1應 ≤20字，此處過於詳細
**Required Fix**: 只保留問題導向的描述
**Action**:
- [ ] 改為 "PBFT因O(n²)通訊複雜度限制可擴展性"（15字）

#### Issue #2: 1.1節第5段缺少過渡
...

## ✅ Action Items Summary
### 🔴 HIGH Priority
- [ ] **#1**: 1.1節第2段 - 刪減到≤20字
- [ ] **#2**: 1.1節第5段 - 添加過渡句
```

#### Step 4: Writer修改
Writer根據action items修改，標記checkbox

#### Step 5: 再次審核
```
審核 Section 1.1 v2，確認修正完成
```

---

## 提交前檢查清單

審核報告產生前，確保：

- [ ] 所有HIGH priority issues都有具體位置
- [ ] Action Items具體可執行（不是"改善語言"）
- [ ] 明確判斷了「寫作 vs 架構」
- [ ] 如果要升級，有escalation report
- [ ] Quality Metrics數據正確
- [ ] Next Steps清楚

---

## 故障排除

### Q: 如何判斷是否為架構問題？
**A**: 問自己「Writer能否在現有strategy下修正？」
- 能 → 寫作問題
- 不能（需重新規劃）→ 架構問題

### Q: Writer不同意我的判斷怎麼辦？
**A**: 在報告中說明理由。如果有爭議，升級到人工決策。

### Q: 第一版有很多問題怎麼辦？
**A**: 正常！重點是優先修正Priority 1問題。

---

## 檔案結構

```
master-thesis/
├── .claude/agents/review-agent/
│   ├── agent.md       # Agent prompt
│   └── README.md      # 本文件
├── reviews/
│   ├── strategy-review-v1.md
│   ├── section-review-1.1-v1.md
│   ├── section-review-1.1-v2.md
│   ├── cross-chapter-review-ch1.md
│   ├── escalation-report-20250129.md
│   └── final-review.md
├── content-strategy/
│   └── strategy-20250129.md   # 審核依據
└── chapters/
    └── chapter1-introduction-v1.md  # 被審核文件
```

---

## 快速參考卡

```
┌─────────────────────────────────────────────┐
│ Review Agent Quick Reference                │
├─────────────────────────────────────────────┤
│ Stage 0: Strategy Review                    │
│ Stage 1: Section Review (主要工作)          │
│ Stage 2: Cross-Chapter Review               │
│ Stage 3: Final Review                       │
├─────────────────────────────────────────────┤
│ Priority 1: 邏輯/深度/重複 → 阻擋進度       │
│ Priority 2: 引用/術語 → 批量修改            │
│ Priority 3: 語言 → Polish階段               │
├─────────────────────────────────────────────┤
│ 寫作問題 → Writer修改                       │
│ 架構問題 → 升級到Strategist                 │
└─────────────────────────────────────────────┘
```
