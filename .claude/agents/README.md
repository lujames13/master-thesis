# 4 Agent System for Master Thesis Writing

## 系統概覽

本專案使用4個專門的Claude Code agents協作完成碩士論文的Introduction、Background、Related Work三章撰寫。

```
                     ┌─────────────────────┐
                     │  framework-design   │
                     │  deep_research_*    │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │  Agent 1: Content   │
                     │    Strategist       │
                     └──────────┬──────────┘
                                │ strategy.md (SSOT)
                                ▼
            ┌───────────────────┴───────────────────┐
            │                                       │
            ▼                                       ▼
  ┌─────────────────────┐               ┌─────────────────────┐
  │  Agent 3: Chapter   │◄─────────────►│  Agent 2: Review    │
  │      Writer         │   review       │      Agent          │
  └──────────┬──────────┘   修改建議     └─────────────────────┘
            │                                       │
            │                                       │
            └───────────────────┬───────────────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │  Agent 4: Citation  │
                     │     Manager         │
                     └─────────────────────┘
```

---

## 4個Agents總覽

| Agent | 角色 | 核心功能 | 主要輸出 | 檔案大小 |
|-------|------|---------|---------|---------|
| **Agent 1** | Content Strategist | 內容規劃 | strategy.md (SSOT) | 5.8KB agent + 3.5KB guide |
| **Agent 2** | Review Agent | 品質審核 | section-review-*.md | 7.0KB agent + 9.4KB guide |
| **Agent 3** | Chapter Writer | 章節寫作 | chapter*.md | 8.9KB agent + 15KB guide |
| **Agent 4** | Citation Manager | 引用管理 | references.bib | 6.9KB agent + 23KB guide |

**總計**: 28.6KB agent prompts + 50.9KB guides = **79.5KB文檔**

---

## Agent 1: Content Strategist

### 位置
```bash
cd .claude/agents/content-strategist
```

### 核心任務
1. **Phase 0**: 理解研究核心 → `research-core-analysis.md`
2. **Phase 1**: 分析文獻 (deep_research_*.md)
3. **Phase 2**: 創建內容分配矩陣 → `strategy-YYYYMMDD.md`

### 關鍵輸出
**Content Distribution Matrix**:
| Content | Ch1 | Ch2 | Ch3 | Goal |
|---------|-----|-----|-----|------|
| PBFT | O(n²)問題 | 詳細機制3-4頁 | FLCoin優化但固定 | 對比動態 |

### 深度分配標準
- **Ch1**: ≤20字/技術（問題導向）
- **Ch2**: Tutorial級（算法+偽代碼+推導）
- **Ch3**: 批判性分析（貢獻+局限+對比）

### 狀態管理
- ⏸️ Not Started
- 🚧 In Progress
- ✅ Completed
- 🔄 Needs Revision

### 詳細文檔
[content-strategist/README.md](content-strategist/README.md)

---

## Agent 2: Review Agent

### 位置
```bash
cd .claude/agents/review-agent
```

### 核心任務
- **Stage 0**: Strategy Review（策略審核）
- **Stage 1**: Section Review（每section完成後）
- **Stage 2**: Cross-Chapter Review（每章完成後）
- **Stage 3**: Final Review（三章完成後）

### 審核優先級
- 🔴 **Priority 1** (阻擋進度): 邏輯、深度、重複
- 🟡 **Priority 2** (批量修改): 引用、術語
- ℹ️ **Priority 3** (Polish): 語言流暢度

### 關鍵決策
```
發現問題 → 判斷類型
├─ 寫作問題 → Writer修改
└─ 架構問題 → 升級到Strategist
```

### 升級條件
1. Ch2討論了具體研究系統
2. 頁數分配明顯不合理
3. 關鍵技術被遺漏
4. 深度分配策略有根本錯誤

### 輸出報告
- `strategy-review-v1.md`
- `section-review-X.X-vN.md`
- `cross-chapter-review-chX.md`
- `escalation-report-YYYYMMDD.md`（如需升級）
- `final-review.md`

### 詳細文檔
[review-agent/README.md](review-agent/README.md)

---

## Agent 3: Chapter Writer

### 位置
```bash
cd .claude/agents/chapter-writer
```

### 雙模式運作
- **Mode 1**: 初始寫作（根據strategy.md）
- **Mode 2**: 根據Review修改（根據review report）

### 輸入優先級
```
1️⃣ strategy.md (最高優先級 - SSOT)
2️⃣ 已完成章節內容 (保持一致性)
3️⃣ review report (修改建議)
4️⃣ deep_research_*.md (補充細節)
```

### 三章深度標準

#### Chapter 1: Introduction
- 長度: ≤20字/技術
- 視角: 問題導向
- 禁止: 技術細節、歷史、具體方案

#### Chapter 2: Background
- 必須: 算法流程、偽代碼、數學推導、複雜度分析
- 禁止: 討論具體研究系統
- 引用: 即時添加（不可TODO）

#### Chapter 3: Related Work
- 標準句型: [方案]+[貢獻]+[指標]+**然而**+[局限]+對比
- 必須: 貢獻、性能指標、局限性、對比本研究
- 禁止: 重複解釋技術原理

### 術語規範
- **首次**: 中文全稱（English Full Name, ABC）
- **後續**: ABC 或 中文全稱（統一）

### Git規範
```bash
git commit -m "Complete: Ch1, Section 1.1 - 研究背景"
git commit -m "Review: Section 1.1 - v2 (fixed depth issues)"
```

### 詳細文檔
[chapter-writer/README.md](chapter-writer/README.md)

---

## Agent 4: Citation Manager

### 位置
```bash
cd .claude/agents/citation-manager
```

### 核心任務
- **Phase 1**: 初始化引用庫（專案開始）
- **Phase 2**: Background即時驗證（Ch2寫作時）
- **Phase 3**: 後補引用（Ch1/Ch3完成後）
- **Phase 4**: 最終驗證（所有完成）

### IEEE格式規範

#### 作者格式
```bibtex
✅ M. Castro and B. Liskov
❌ Miguel Castro and Barbara Liskov
```

#### 頁碼格式
```bibtex
✅ pages = {173--186}  % 兩個連字號
❌ pages = {173-186}   % 一個連字號
```

#### 標題格式
```bibtex
✅ title = {Practical Byzantine Fault Tolerance}  % Title Case
❌ title = {practical byzantine fault tolerance}  % 全小寫
```

### 引用處理規則
- **Background (Ch2)**: 必須即時添加 ❌ 不可用[TODO]
- **Introduction (Ch1)**: 可用[TODO]
- **Related Work (Ch3)**: 可用[TODO]

### 輸出文件
- `references.bib` - 主要引用庫
- `citation-catalog.md` - 分類索引
- `citation-suggestions.md` - [TODO]替換建議
- `citation-report.md` - 最終完整性報告

### 詳細文檔
[citation-manager/README.md](citation-manager/README.md)

---

## 完整工作流程

### Phase 1: 規劃階段
```bash
cd .claude/agents/content-strategist
```

**任務**: 創建content strategy

**輸入**:
- `framework-design.md`
- `deep_research_*.md`

**輸出**:
- `content-strategy/research-core-analysis.md`
- `content-strategy/strategy-YYYYMMDD.md` ⭐ SSOT

**提交**:
```bash
cd ../../.claude/agents/review-agent
# 審核策略
```

---

### Phase 2: 寫作階段（循環）

```
┌─► Chapter Writer ──► 寫 Section X.X ──► v1
│         │
│         ▼
│   Review Agent ──► 審核 ──┬──► ✅ APPROVED → 下一個section
│         │                 │
│         │                 └──► ⚠️ NEEDS REVISION
│         ▼                           │
│   生成 review report ◄───────────────┘
│         │ (action items)
│         ▼
│   Chapter Writer ──► 修改 ──► v2
│         │           (標記checkboxes)
│         ▼
└───Review Agent ──► 再次審核
```

**特殊情況**: 如果Review發現架構問題 🚨
```
Review Agent → escalation report → Content Strategist
                                           │
                                           ▼
                               更新 strategy v++
                                           │
                                           ▼
                               Chapter Writer 重寫
```

---

### Phase 3: 引用管理

#### 初始化（專案開始時）
```bash
cd .claude/agents/citation-manager
# 建立 references.bib 和 citation-catalog.md
```

#### Background寫作時（即時驗證）
```
Writer寫Ch2 → Citation Manager驗證引用 → 發現問題 → Writer修正
```

#### Ch1/Ch3完成後（後補引用）
```
Writer完成Ch1 → Citation Manager掃描[TODO] → 建議引用 → Writer替換
```

#### 最終驗證
```
所有完成 → Citation Manager生成 citation-report.md → 修正問題
```

---

### Phase 4: 最終審核

```bash
cd .claude/agents/review-agent
# Final Review
```

**檢查項目**:
- Cross-chapter完整性
- 引用完整性（與Citation Manager配合）
- 術語一致性（全文）
- 交叉引用正確性

**輸出**: `reviews/final-review.md`

---

## 文件結構

```
master-thesis/
├── .claude/
│   └── agents/
│       ├── README.md  ◄── 本文件
│       ├── content-strategist/
│       │   ├── agent.md (5.8KB)
│       │   └── README.md (3.5KB)
│       ├── review-agent/
│       │   ├── agent.md (7.0KB)
│       │   └── README.md (9.4KB)
│       ├── chapter-writer/
│       │   ├── agent.md (8.9KB)
│       │   └── README.md (15KB)
│       └── citation-manager/
│           ├── agent.md (6.9KB)
│           └── README.md (23KB)
│
├── content-strategy/
│   ├── research-core-analysis.md
│   └── strategy-YYYYMMDD.md  ⭐ SSOT
│
├── chapters/
│   ├── chapter1-introduction-vN.md
│   ├── chapter2-background-vN.md
│   └── chapter3-related-work-vN.md
│
├── reviews/
│   ├── strategy-review-v1.md
│   ├── section-review-X.X-vN.md
│   ├── cross-chapter-review-chX.md
│   ├── escalation-report-YYYYMMDD.md
│   └── final-review.md
│
├── references.bib
├── citation-catalog.md
├── citation-suggestions.md
├── citation-report.md
│
├── framework-design.md  (研究核心)
├── deep_research_1009.md  (文獻資料)
├── deep_research_1027.md  (文獻資料)
├── CLAUDE.md  (專案指引)
└── README.md  (專案說明)
```

---

## 快速開始指南

### 第一次使用

#### 1. 創建content strategy
```bash
cd .claude/agents/content-strategist
```
輸入:
```
讀取 ../../framework-design.md 和所有 deep_research 文件，創建完整的 content strategy
```

#### 2. 審核策略
```bash
cd ../review-agent
```
輸入:
```
審核 ../../content-strategy/strategy-20250129.md 的合理性
```

#### 3. 開始寫作
```bash
cd ../chapter-writer
```
輸入:
```
根據 strategy，寫作 Chapter 1, Section 1.1
```

#### 4. 初始化引用庫
```bash
cd ../citation-manager
```
輸入:
```
從 deep_research 文件建立 references.bib 和 citation-catalog.md
```

---

### 日常寫作循環

```bash
# 1. 寫作
cd .claude/agents/chapter-writer
# "根據 strategy 寫作 Section X.X"

# 2. 審核
cd ../review-agent
# "審核 Section X.X"

# 3. 修改
cd ../chapter-writer
# "根據 review report 修改 Section X.X"

# 4. 再次審核
cd ../review-agent
# "審核 Section X.X v2"

# 5. 通過後繼續下一個
```

---

## 關鍵原則

### 1. Single Source of Truth
`content-strategy/strategy.md` 是唯一依據，所有agents都遵守它。

### 2. Goal-Oriented
所有內容圍繞論文創新點：
- Ch1: 為什麼需要我的創新？
- Ch2: 如何支撐我的創新？
- Ch3: 為什麼我的更好？

### 3. Section-by-Section
絕不一次寫完整章，必須逐section寫作和審核。

### 4. 深度控制嚴格
- Ch1: ≤20字/技術
- Ch2: Tutorial級（算法+偽代碼+推導）
- Ch3: 批判性分析（貢獻+局限+對比）

### 5. 問題升級機制
```
發現問題 → 判斷
├─ 寫作問題 → Writer修改
└─ 架構問題 → 升級到Strategist → 更新strategy
```

---

## 品質門檻

### Priority 1 (阻擋進度)
- 邏輯連貫性
- 深度正確性
- 重複檢查

必須通過才能進入下一section

### Priority 2 (批量修改)
- 引用完整性（Background除外）
- 術語一致性

可累積後一起修改

### Priority 3 (Polish階段)
- 語言流暢度

最後統一優化

---

## Git提交規範

```bash
# Content Strategist
git commit -m "Complete: Strategy v1.0 - 初始內容規劃"
git commit -m "Update: Strategy v1.1 - 調整Ch2/Ch3邊界"

# Chapter Writer
git commit -m "Complete: Ch1, Section 1.1 - 研究背景"
git commit -m "Review: Section 1.1 - v2 (fixed depth issues)"

# Review Agent
git commit -m "Review: Section 1.1 - 發現2個HIGH priority issues"
git commit -m "Escalation: Ch2邊界問題 - 需重新規劃"

# Citation Manager
git commit -m "Init: 建立引用資料庫 (87篇文獻)"
git commit -m "Update: Ch1 補充引用 ([4], [15], [20])"
git commit -m "Final: 引用完整性驗證報告"
```

---

## 成功標準

### Strategy階段
- [ ] Strategy圍繞創新點
- [ ] 三章頁數分配合理
- [ ] 標記了潛在重複並提供區分策略
- [ ] 通過Review Agent審核

### 寫作階段
- [ ] 每section通過Priority 1審核
- [ ] 深度控制正確
- [ ] 無與其他章verbatim重複

### 引用階段
- [ ] Background引用即時且正確
- [ ] Ch1/Ch3的[TODO]都已補充
- [ ] references.bib格式符合IEEE
- [ ] 無缺失引用、無格式錯誤

### 最終階段
- [ ] 通過Cross-Chapter Review（無HIGH issues）
- [ ] 通過Final Review
- [ ] Citation Report無HIGH issues
- [ ] 術語使用一致
- [ ] 總頁數：Ch1(3-4) + Ch2(10-12) + Ch3(9-11) = 22-27頁

---

## 常見問題

### Q: 如何在agents之間切換？
**A**: 使用 `cd .claude/agents/[agent-name]`

### Q: Strategy需要修改怎麼辦？
**A**: 由Review Agent發現架構問題 → 生成escalation report → Strategist更新strategy → 版本號+1 → 重置受影響sections狀態

### Q: 如何保持4個agents的一致性？
**A**: Strategy是SSOT，所有agents都讀取並遵守它。

### Q: Review發現問題但Writer不同意？
**A**: Review Agent的標準是基於學術規範，不可妥協。如有爭議，升級到人工決策。

### Q: 引用編號變了怎麼辦？
**A**: Citation Manager維護mapping table，並在catalog註明。

---

## 進度追蹤

### 使用strategy.md的狀態emoji
```markdown
### Chapter 1: 3-4頁
- 1.1: 1頁 - ⏸️ Not Started
- 1.2: 1頁 - 🚧 In Progress
- 1.3: 1頁 - ✅ Completed
- 1.4: 1頁 - 🔄 Needs Revision
```

### 版本控制
每次重大修改都更新版本號：
- strategy v1.0 → v1.1
- chapter-v1.md → chapter-v2.md
- section-review-v1.md → section-review-v2.md

---

## 效能優化建議

### 1. 並行工作
- Writer寫Ch1時，Citation Manager可初始化引用庫
- Writer寫Section 1.2時，Reviewer可審核Section 1.1

### 2. 批量處理
- Priority 2問題可累積後一起修改
- Ch1/Ch3的[TODO]可最後統一處理

### 3. 提前準備
- 在寫Background前先完成引用庫初始化
- 在寫Ch3前先確保Ch2沒有討論研究系統

---

## 聯絡與支援

如有問題或建議，請參考：
- 各agent的詳細README.md
- 專案根目錄的CLAUDE.md
- Git commit history

---

**版本**: v1.0
**最後更新**: 2025-01-30
**總文檔大小**: 79.5KB
**Agents數量**: 4

祝寫作順利！🎓
