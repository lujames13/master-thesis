# Master Thesis Writing Project

## 專案簡介
碩士論文寫作專案，使用多 Agent 系統撰寫 Introduction、Background、Related Work 三章。

**語言**: 繁體中文 | **引用**: IEEE | **目標**: 3章 約22-27頁

---

## 核心檔案位置

```
master-thesis/
├── CLAUDE.md                    # 本檔案
├── framework-design.md          # 研究核心（必讀）⭐
├── deep_research_*.md           # 文獻資料
├── .claude/agents/              # 各 Agent 配置
├── content-strategy/            # 內容規劃（SSOT）
├── chapters/                    # 章節輸出
├── reviews/                     # 審核報告
└── references.bib               # 引用庫
```

---

## 4 個核心 Agents

### 切換 Agent
```bash
cd .claude/agents/content-strategist   # 規劃內容
cd .claude/agents/chapter-writer       # 寫作/修改
cd .claude/agents/review-agent         # 審核品質
cd .claude/agents/citation-manager     # 管理引用
```

### 工作流程
```
framework-design.md → Agent 1 → strategy.md (SSOT)
                                      ↓
                     Agent 3 寫 Section → Agent 2 審核 → 修改 → ✓
                                      ↓
                              完成一章 → Cross-Chapter Review
```

---

## 章節深度標準（關鍵！）

### Chapter 1: Introduction (3-4頁)
- **深度**: 1句話 ≤20字/技術
- **禁止**: 技術細節、歷史、具體方案
- **範例**: ✅ "PBFT因O(n²)導致效能瓶頸" ❌ "PBFT由Castro於1999年提出..."

### Chapter 2: Background (10-12頁)
- **深度**: Tutorial級（算法+推導+偽代碼）
- **必須**: 流程圖、數學推導、複雜度分析
- **禁止**: 討論具體研究系統（FLCoin、opML等）

### Chapter 3: Related Work (9-11頁)
- **深度**: 批判性分析（貢獻+局限+對比）
- **必須**: 每方案都指出「缺少我有的特性」
- **句型**: "[方案]實現[貢獻]。然而，[局限]，無法[我能做的]。"

---

## 核心原則

### 1. Single Source of Truth
`content-strategy/strategy.md` 是唯一依據，所有 Agent 都遵守它。

### 2. Goal-Oriented
所有內容圍繞論文創新點：
- Ch1: 為什麼需要我的創新？
- Ch2: 如何支撐我的創新？
- Ch3: 為什麼我的更好？

### 3. 問題升級
```
Review 發現問題 →
├─ 寫作問題 → Writer 修改
└─ 架構問題 → Strategist 重新規劃 → 更新 strategy → Writer 重寫
```

---

## 常用 Bash 命令

### Git 提交規範
```bash
git add chapters/chapter1-introduction-v1.md
git commit -m "Complete: Ch1, Section 1.1 - 研究背景"
git commit -m "Review: Section 1.1 - v2 (fixed depth issues)"
git commit -m "Update: Strategy v1.1 - 調整Ch2/Ch3邊界"
```

### 快速開始
```bash
# 1. 規劃內容
cd .claude/agents/content-strategist
claude -p "讀取 ../../framework-design.md 和 Deep Research，創建 strategy"

# 2. 寫作
cd ../chapter-writer
claude -p "根據 strategy 寫 Chapter 1, Section 1.1"

# 3. 審核
cd ../review-agent
claude -p "審核 Section 1.1"
```

---

## 寫作規範

### 語言
- 繁體中文、學術正式語調
- 術語首次: "實用拜占庭容錯（Practical Byzantine Fault Tolerance, PBFT）"
- 後續: "PBFT" 或 "PBFT協議"

### 引用
- **Background**: 立即添加精確引用 [7]
- **Introduction & Related Work**: 可用 [TODO] 佔位
- **格式**: IEEE - "[數字] 作者, 標題, 期刊, 年份"

### 品質門檻
- Priority 1: 邏輯、深度、重複（必須通過）
- Priority 2: 引用、術語（可批量修改）
- Priority 3: 語言（polish階段）

---

## 檔案命名規範
- 章節: `chapter1-introduction-v1.md`
- 審核: `section-review-1.1-v2.md`
- 策略: `strategy-20250129.md`
- 分支: `chapter-1-draft`, `fix-duplication`

---

## 快速參考

### Agent 1 輸出
`content-strategy/strategy-YYYYMMDD.md` - 內容分配矩陣 + 狀態追蹤

### Agent 2 輸出
`reviews/section-review-X.X-vN.md` - Action Items + 優先級

### Agent 3 工作模式
- Mode 1: 初始寫作（讀 strategy）
- Mode 2: 根據 review 修改（打勾 checkbox）

### Agent 4 工作模式
- Background: 即時驗證引用
- 其他: 最後統一補充

---

## 成功標準
- [ ] Strategy 圍繞創新點
- [ ] 每 section 通過審核
- [ ] Cross-Chapter Review 無 HIGH issues
- [ ] 引用完整且格式正確
- [ ] 術語使用一致
- [ ] 深度控制正確

詳細文檔見 `README.md`
