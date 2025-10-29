# Master Thesis Writing Project - README

## 專案簡介

這是一個使用 Claude Code 多 Agent 系統協助撰寫碩士論文的專案。系統設計採用 DevSecOps 風格，通過 4 個專門化的 AI Agents 協作完成論文的 Introduction、Background 和 Related Work 三章。

**論文領域**: 區塊鏈聯邦學習  
**目標章節**: Chapter 1-3（共約 22-27 頁）  
**寫作語言**: 繁體中文  
**引用格式**: IEEE

---

## 系統架構

### 核心設計理念

1. **Single Source of Truth (SSOT)**: `strategy.md` 是所有 agents 的唯一依據
2. **Goal-Oriented Planning**: 所有內容圍繞論文的核心創新點
3. **Escalation Mechanism**: 區分寫作問題與架構問題，適時升級處理
4. **Quality Gates**: 每個關鍵節點都有嚴格的品質審核

### 4 個核心 Agents

```
┌─────────────────────────────────────────────────────────┐
│   framework-design.md (研究核心)                        │
│   + deep_research_*.md (文獻資料)                       │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│   Agent 1: Content Strategist                           │
│   規劃內容分配，建立 strategy.md (SSOT)                │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
     strategy.md (內容規劃)
             │
      ┌──────┴──────┐
      ▼             ▼
┌─────────┐   ┌─────────┐
│ Agent 3 │   │ Agent 2 │
│ Writer  │ → │ Review  │
└─────────┘   └────┬────┘
      ↑            │
      └────修改────┘
             │
             ▼
      Section Approved ✓
             │
             ▼
   ┌─────────────────┐
   │ Agent 4: Cite   │
   │ Background即時  │
   │ 其他後補        │
   └─────────────────┘
```

---

## 專案結構

```
master-thesis/
│
├── CLAUDE.md                          # 專案級配置（所有agents共用）
├── README.md                          # 本檔案（詳細文檔）
├── framework-design.md                # 你的研究核心（必備）⭐
├── deep_research_1009.md              # 文獻調查結果
├── deep_research_1027.md
│
├── .claude/
│   ├── agents/                        # Agent 配置
│   │   ├── content-strategist/
│   │   │   └── CLAUDE.md             # Agent 1 配置
│   │   ├── chapter-writer/
│   │   │   └── CLAUDE.md             # Agent 3 配置
│   │   ├── review-agent/
│   │   │   └── CLAUDE.md             # Agent 2 配置
│   │   └── citation-manager/
│   │       └── CLAUDE.md             # Agent 4 配置
│   │
│   ├── commands/                      # 自定義 slash commands
│   │   ├── plan-content.md
│   │   ├── write-section.md
│   │   └── review-quality.md
│   │
│   └── settings.json                  # Claude Code 設定
│
├── content-strategy/                  # Strategist 輸出
│   ├── research-core-analysis.md     # 研究核心分析
│   └── strategy-YYYYMMDD.md          # 內容分配策略（SSOT）
│
├── chapters/                          # Writer 輸出
│   ├── chapter1-introduction-v1.md
│   ├── chapter2-background-v1.md
│   └── chapter3-related-work-v1.md
│
├── reviews/                           # Review Agent 輸出
│   ├── strategy-review-v1.md
│   ├── section-review-1.1-v1.md
│   ├── cross-chapter-review-ch2.md
│   └── final-review.md
│
├── references.bib                     # Citation Manager 維護
├── citation-catalog.md                # 引用目錄
│
└── .gitignore
```

---

## 快速開始指南

### 前置準備

1. **準備研究核心文件**: `framework-design.md`

必須包含：
- 研究問題（你要解決什麼）
- 核心創新（3-4項主要貢獻）
- 關鍵技術（支撐創新的技術）
- 對比對象（與誰比較）

範例最簡結構：
```markdown
## 核心創新
1. 動態混合 Optimistic-PBFT 機制
2. 威脅感知動態切換算法
3. ...

## 關鍵技術
- PBFT（會用）
- Optimistic Rollup（會用）
- PoW（不會用）

## 主要對比
- FLCoin: 固定窗口 → 我的動態切換
- opML: 無BFT → 我的混合機制
```

2. **確保 Deep Research 文件就緒**
```bash
ls deep_research_1009.md
ls deep_research_1027.md
```

### Step 1: 規劃內容（Content Strategist）

```bash
cd .claude/agents/content-strategist
claude
```

**Prompt**:
```
請按照 CLAUDE.md 的指示：
1. 先閱讀 ../../framework-design.md 理解研究核心
2. 分析 ../../deep_research_*.md 的文獻資料
3. 創建目標導向的內容分配策略

輸出：
- ../../content-strategy/research-core-analysis.md
- ../../content-strategy/strategy-20250130.md
```

**預期輸出**: 
- 研究核心分析（問題、創新、技術、對比）
- 內容分配矩陣（每個技術在三章的分配）
- 狀態追蹤（所有 sections 初始為 ⏸️ Not Started）

### Step 2: 審核策略（Review Agent）

```bash
cd ../review-agent
claude
```

**Prompt**:
```
請審核 ../../content-strategy/strategy-20250130.md

檢查：
- 是否涵蓋所有關鍵技術？
- 三章頁數分配平衡嗎？
- Ch1 都是 ≤20字？
- Ch2 有算法細節規劃？
- Ch3 有批判性分析規劃？
- 是否標記了潛在重複？
```

**預期輸出**: `strategy-review-v1.md`

**人工確認**: 
- 閱讀 strategy-review-v1.md
- 如果 APPROVED → 進入寫作
- 如果 NEEDS REVISION → Strategist 修改

### Step 3: 開始寫作（Chapter Writer）

```bash
cd ../chapter-writer
claude
```

**Prompt**:
```
請讀取 ../../content-strategy/strategy-20250130.md
開始寫作 Chapter 1, Section 1.1 - 研究背景

要求：
- 嚴格遵守深度標準（Ch1: ≤20字/技術）
- 圍繞論文創新點
- 參考 strategy 的 Goal 欄位
```

**預期輸出**: `../../chapters/chapter1-introduction-v1.md`

### Step 4: 審核 Section（Review Agent）

```bash
cd ../review-agent
claude
```

**Prompt**:
```
請審核 ../../chapters/chapter1-introduction-v1.md 的 Section 1.1

Priority 1（必須立即修正）:
- 邏輯連貫性
- 深度正確性（是否 ≤20字？）
- 重複檢查

Priority 2（可稍後批量）:
- 引用完整性
- 術語一致性
```

**預期輸出**: `section-review-1.1-v1.md`

### Step 5: 根據 Review 修改（Chapter Writer）

```bash
cd ../chapter-writer
claude
```

**Prompt**:
```
請讀取 ../../reviews/section-review-1.1-v1.md
根據 Action Items 修改 Section 1.1

修改後：
- 在 review report 標記 checkbox
- 註明修改時間和內容
```

### Step 6: 循環直到通過

重複 Step 4-5 直到：
- Review Agent 回報 ✅ APPROVED
- strategy.md 的 status 更新為 ✅ Completed

### Step 7: 完成整章後 Cross-Chapter Review

```bash
cd ../review-agent
claude
```

**Prompt**:
```
Chapter 1 所有 sections 已完成，請進行 Cross-Chapter Review

檢查：
- 是否超出頁數預算？
- 是否使用了其他章規劃的內容？
- 內容量是否足夠？
- 術語在整章是否一致？
```

### Step 8: 重複 3-7 完成所有章節

---

## 詳細工作流程

### Workflow 1: 標準寫作流程

```
framework-design.md → Strategist → strategy.md
                                         ↓
                                    (人工確認)
                                         ↓
                        Writer 寫 Section 1.1 → Review 審核
                                    ↓            ↓
                                    ← 修改 ←─────┘
                                    ↓
                            Section 1.1 Approved ✓
                                    ↓
                        Writer 寫 Section 1.2 → Review...
                                    ↓
                            (循環直到整章完成)
                                    ↓
                    Cross-Chapter Review (檢查資源分配)
                                    ↓
                            Chapter 1 Approved ✓
                                    ↓
                            開始 Chapter 2...
```

### Workflow 2: 遇到架構問題升級

```
Review 發現 Ch2 討論了 FLCoin（應在 Ch3）
                ↓
        是寫作問題還是架構問題？
                ↓
        ┌───────┴───────┐
        │               │
   寫作問題         架構問題
   (Writer改)      (升級)
        │               ↓
        │      Strategist 重新規劃
        │               ↓
        │      更新 strategy v1.1
        │               ↓
        │      重置 section 狀態 🔄
        │               ↓
        └──→   Writer 根據新規劃重寫
```

### Workflow 3: 引用管理

```
專案開始 → Citation Manager 建立 references.bib
                    ↓
         Writer 寫 Background
                    ↓
         [即時] Citation Manager 驗證每個引用
                    ↓
         Writer 寫 Introduction/Related Work
         (可用 [TODO] 佔位)
                    ↓
         章節完成 → Citation Manager 補充引用
                    ↓
         全部完成 → Citation Manager 最終驗證
                    ↓
         生成 citation-report.md
```

---

## 章節深度標準（關鍵！）

### Chapter 1: Introduction (3-4頁)

**目標**: 說服讀者「我的創新是必要的」

**深度標準**:
- 每個技術 ≤1句話（≤20字）
- 只點出問題/缺陷
- 不解釋原理、不提歷史、不討論具體方案

**範例對比**:

✅ **Good** (符合 Ch1 標準):
```markdown
"現有區塊鏈聯邦學習面臨效率與安全的兩難：PBFT協議因
O(n²)複雜度限制可擴展性，Optimistic執行雖高效但缺乏
Byzantine容錯能力。"
```

❌ **Bad** (這是 Ch2 的內容):
```markdown
"PBFT（Practical Byzantine Fault Tolerance）協議由Castro
和Liskov於1999年提出，包含Pre-prepare、Prepare、Commit
三階段，採用狀態機複製方法實現拜占庭容錯..."
```

---

### Chapter 2: Background (10-12頁)

**目標**: 讀者理解「技術如何運作」

**深度標準**:
- Tutorial級別（像教科書一樣詳細）
- 必須包含：算法流程、偽代碼、數學推導、複雜度分析
- 可以包含：流程圖、公式證明
- 絕對禁止：討論具體研究系統（FLCoin, opML等）

**範例對比**:

✅ **Good** (符合 Ch2 標準):
```markdown
"### 2.3.2 Prepare階段

備份節點驗證Pre-prepare消息後，廣播Prepare消息...

**Algorithm 2**: PBFT Prepare Phase
```
Input: ⟨PRE-PREPARE, v, n, d⟩ from primary
Output: ⟨PREPARE, v, n, d, i⟩ to all replicas

1: upon receiving ⟨PRE-PREPARE, v, n, d⟩ do
2:   if validate_message(v, n, d) then
3:     broadcast ⟨PREPARE, v, n, d, i⟩
4:   end if
5: end upon
```

#### 2.3.4 通訊複雜度分析

在Prepare階段，每個節點需要：
M = n × (n-1) = n² - n ≈ O(n²)

當n=100時，需要約9,900條消息..."
```

❌ **Bad** (這是 Ch3 的內容):
```markdown
"FLCoin系統[4]採用PBFT協議，但通過滑動窗口委員會將
複雜度降至O(c)，在100節點下實現<5秒共識延遲。然而，
該系統採用固定窗口配置..."
```

---

### Chapter 3: Related Work (9-11頁)

**目標**: 證明「我的創新是優越的」

**深度標準**:
- 批判性分析（不是單純描述）
- 每個方案都要指出「缺少我有的特性」
- 必須包含：貢獻、性能指標、局限性、與本研究對比
- 禁止：重複解釋技術原理（Ch2已解釋）

**標準句型**:
```
[作者]等人[ref]提出[方案]，採用[技術]實現[貢獻]，[性能]。
然而，該系統[局限]，無法[我能做的]。
```

**範例對比**:

✅ **Good** (符合 Ch3 標準):
```markdown
"Ren等人[4]提出FLCoin系統，採用滑動窗口委員會機制將
通訊複雜度從O(n²)降至O(c)，在100節點下實現<5秒共識延遲。
然而，該系統採用固定委員會窗口（c=20），無法根據實時威脅
動態調整安全強度，且容錯度仍受限於f<c/3（約30%）。相較之下，
本研究提出的動態切換機制能根據威脅等級自適應調整，在低風險時
達到O(R/N)效率，高風險時提供完整Byzantine容錯（f<n/3）。"
```

❌ **Bad** (重複 Ch2 原理):
```markdown
"FLCoin採用PBFT協議。PBFT包含三階段：Pre-prepare階段
主節點發送消息，Prepare階段各節點廣播..."
```

❌ **Bad** (缺乏批判):
```markdown
"FLCoin是一個很好的區塊鏈聯邦學習系統，實現了高效的
共識機制和安全的模型聚合。"
```

---

## 常見問題與解決

### Q1: Review Agent 總是找到很多問題，正常嗎？

**A**: 完全正常！我們的審核標準非常嚴格。

**應對策略**:
1. 優先修改 🔴 HIGH priority 問題
2. 🟡 MEDIUM 可以累積後批量處理
3. ℹ️ LOW 留到 polish 階段

通常循環 2-3 次後，質量會明顯提升。

---

### Q2: 如何判斷是「寫作問題」還是「架構問題」？

**寫作問題**（Writer 修改）:
- 缺少算法/推導（strategy有規劃但Writer沒寫）
- 引用格式錯誤
- 語言不夠學術
- 與其他章輕微重疊（改寫即可）

**架構問題**（升級到 Strategist）:
- Ch2 討論了具體研究系統（邊界模糊）
- 頁數分配明顯不合理（3頁內容塞到1頁）
- 關鍵技術被遺漏
- 深度分配策略有根本錯誤

**經驗法則**: 問「strategy 有沒有規劃這個？」
- 有規劃但Writer沒做好 → 寫作問題
- strategy 本身有問題 → 架構問題

---

### Q3: 章節之間重複怎麼辦？

**解決方案**: 用不同視角

| 章節 | 視角 | 範例 |
|------|------|------|
| Ch1 | 問題導向 | "PBFT因O(n²)導致效能瓶頸" |
| Ch2 | 技術原理 | "PBFT三階段...複雜度推導...偽代碼..." |
| Ch3 | 對比優勢 | "FLCoin優化PBFT但固定窗口 → 我的動態" |

**關鍵**: 同一技術在三章都出現是正常的，只要視角不同就不算重複。

---

### Q4: strategy 可以中途修改嗎？

**A**: 可以，而且應該！Strategy 是 living document。

**修改流程**:
1. Review Agent 發現架構問題 → 生成 escalation report
2. Strategist 重新規劃 → 版本號 +1 (v1.0 → v1.1)
3. Change Log 記錄修改原因和影響
4. 重置受影響 sections 的狀態為 🔄 Needs Revision
5. Writer 根據新 strategy 重寫

---

### Q5: 如何確保術語一致性？

**方法 1**: 在 strategy 定義術語表
```markdown
## Terminology Standards
- "實用拜占庭容錯（Practical Byzantine Fault Tolerance, PBFT）" - 首次
- "PBFT" 或 "PBFT協議" - 後續
- 全文統一，不混用 "Byzantine容錯" / "拜占庭容錯" / "BFT"
```

**方法 2**: Review Agent 會在審核時檢查
```markdown
### 術語一致性
Issue: Line 5 用 "拜占庭容錯"，Line 23 用 "Byzantine容錯"
Recommendation: 統一為 "拜占庭容錯（BFT）"
```

---

## Git 使用指南

### 提交規範

```bash
# 完成新 section
git add chapters/chapter1-introduction-v1.md
git commit -m "Complete: Ch1, Section 1.1 - 研究背景"

# 修改後提交
git add chapters/ reviews/
git commit -m "Review: Section 1.1 - v2 (fixed depth issues)"

# 更新 strategy
git add content-strategy/
git commit -m "Update: Strategy v1.1 - 調整Ch2/Ch3邊界"

# 完成一章
git add chapters/ reviews/
git commit -m "Complete: Chapter 1 - Introduction (all sections approved)"
```

### 分支策略

```bash
# 主分支
main                    # 穩定版本

# 功能分支
chapter-1-draft         # Ch1 寫作中
chapter-2-draft         # Ch2 寫作中

# 修正分支
fix-ch1-duplication     # 修正重複問題
fix-citation-format     # 修正引用格式

# 實驗分支
experiment-new-intro    # 嘗試新的 Introduction 結構
```

### 常用命令

```bash
# 創建新分支開始寫作
git checkout -b chapter-1-draft

# 提交進度
git add .
git commit -m "Progress: Ch1 Section 1.1-1.3 completed"

# 完成後合併
git checkout main
git merge chapter-1-draft

# 如果需要回滾
git log                 # 找到之前的 commit
git reset --hard <commit-hash>
```

---

## 進度追蹤

建議在根目錄維護 `progress.md`:

```markdown
# Thesis Writing Progress

## Overall Status
Last Updated: 2025-01-30

- [x] Setup project structure
- [x] Content Strategy v1.0 created
- [x] Chapter 1 (5/5 sections, Cross-Chapter Review passed) ✅
- [ ] Chapter 2 (2/6 sections completed) 🚧
- [ ] Chapter 3 (0/4 sections) ⏸️

## Current Sprint
**Goal**: Complete Chapter 2 by Feb 15
- [x] Section 2.1 - FL基礎 ✅
- [x] Section 2.2 - 區塊鏈技術 ✅
- [ ] Section 2.3 - PBFT協議 (in review v2) 🚧
- [ ] Section 2.4 - Optimistic Rollup
- [ ] Section 2.5 - 其他技術

## Quality Metrics
| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Verbatim Repetitions | 0 | 0 | 🟢 |
| Depth Violations | <3 | 1 | 🟢 |
| Missing Citations (Ch2) | 0 | 3 | 🟡 |
| Terminology Consistency | 100% | 95% | 🟡 |

## Active Issues
- [ ] HIGH: Ch2 Section 2.3 needs complexity derivation
- [ ] MEDIUM: Add 3 missing citations in Ch2
- [ ] LOW: Unify terminology "拜占庭容錯" vs "Byzantine容錯"

## Lessons Learned
- ✅ 每個 section 寫完立即 review 比累積後處理更有效
- ✅ Strategy 的深度規劃非常重要，減少了很多返工
- ⚠️ Ch2 一開始頁數預算不夠，已調整 strategy v1.1

## Next Milestones
- Feb 5: Complete Ch2 Section 2.3-2.4
- Feb 10: Complete Ch2 all sections
- Feb 12: Ch2 Cross-Chapter Review
- Feb 15: Start Ch3
- Mar 1: Complete all 3 chapters
```

---

## 品質標準檢查清單

### 提交前最終檢查

#### Strategy 階段
- [ ] 研究核心清楚定義（問題、創新、技術、對比）
- [ ] 內容分配矩陣完整（每個技術都有 Ch1/Ch2/Ch3 規劃）
- [ ] 深度標準明確（Ch1: ≤20字, Ch2: Tutorial, Ch3: Critical）
- [ ] 潛在重複已標記並有區分策略
- [ ] 頁數分配合理（Ch1: 3-4, Ch2: 10-12, Ch3: 9-11）

#### 寫作階段
- [ ] 每個 section 都通過 Review Agent 審核
- [ ] 深度控制正確（符合本章標準）
- [ ] 沒有與其他章 verbatim 重複
- [ ] 術語使用一致
- [ ] 引用完整（Ch2必須，Ch1/Ch3可後補）
- [ ] 語調學術正式

#### Cross-Chapter Review
- [ ] 沒有超出頁數預算
- [ ] 沒有使用其他章規劃的內容
- [ ] 沒有內容洩漏（Ch2討論研究系統、Ch3重複原理）
- [ ] 整章術語一致

#### Final Review
- [ ] 三章深度階梯分明
- [ ] 引用格式統一（IEEE）
- [ ] 術語全文一致
- [ ] 交叉引用正確（"詳見X.X節"）
- [ ] 無邏輯跳躍或矛盾

---

## 效能優化建議

### Token 效率

**問題**: CLAUDE.md 過長消耗太多 context

**解決**: 
- ✅ 專案 CLAUDE.md: 150-200行（核心規範）
- ✅ Agent CLAUDE.md: 200-350行（專門化指引）
- ✅ 詳細文檔: 放在 README.md（agents 不自動載入）

### 審核效率

**問題**: 每個小改動都要完整審核

**解決**:
- ✅ 優先級系統（Priority 1-3）
- ✅ v2 審核只檢查修改部分
- ✅ 批量處理 MEDIUM/LOW issues

### 寫作效率

**問題**: 一次寫太多導致大量返工

**解決**:
- ✅ Section-by-section 寫作
- ✅ 每個 section 立即審核
- ✅ 問題不累積

---

## 技術規格

### 環境要求
- Claude Code (latest version)
- Git 2.x+
- Markdown editor (推薦 VS Code with Markdown extension)
- Python 3.8+ (optional, for Citation Manager scripts)

### 檔案規範
- 編碼: UTF-8
- 換行: LF (Unix style)
- 語言: Traditional Chinese (zh-TW)
- 引用: IEEE format

### 命名規範
- 檔案: 小寫 + 連字號，例如 `chapter1-introduction-v1.md`
- 資料夾: 小寫 + 連字號，例如 `content-strategy/`
- Git branch: 小寫 + 連字號，例如 `chapter-1-draft`
- Git commit: 英文，首字母大寫，例如 "Complete: Ch1, Section 1.1"

---

## 學習資源

### 官方文檔
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Claude Code Best Practices](https://www.anthropic.com/news/claude-code-best-practices)

### 專案文檔
- `CLAUDE.md`: 快速參考
- 本 `README.md`: 完整指南
- `architecture-update-framework-integration.md`: 架構設計說明

### Agent 配置
- `.claude/agents/content-strategist/CLAUDE.md`: Strategist 詳細指引
- `.claude/agents/chapter-writer/CLAUDE.md`: Writer 深度標準
- `.claude/agents/review-agent/CLAUDE.md`: Review 審核維度
- `.claude/agents/citation-manager/CLAUDE.md`: 引用格式規範

---

## 致謝

本專案的設計參考了：
- Claude Code 官方最佳實踐
- DevSecOps 質量管理理念
- 學術論文寫作標準

---

## License

本專案配置為學術研究使用，請遵守學術誠信原則。

---

**祝你論文寫作順利！ 🎓**

如有問題，請參考本 README 或查閱各 Agent 的 CLAUDE.md 配置。

---

# Byzantine-Robust Optimistic Aggregation: A Multi-Aggregator Framework for Blockchain-based Federated Learning
# 具拜占庭容錯能力的樂觀聚合：多聚合器區塊鏈聯邦學習框架
# Abstract
## 中文摘要

聯邦學習作為一種保護隱私的分散式機器學習技術，已成為現代人工智慧發展的重要方向。然而，傳統聯邦學習架構依賴單一中央聚合器，面臨單點故障風險、信任假設問題及缺乏惡意聚合器檢測機制等挑戰。雖然區塊鏈技術的引入為聯邦學習提供了去中心化解決方案，但現有的區塊鏈聯邦學習方案多採用傳統拜占庭容錯（PBFT）共識機制，因其密集的多輪通信需求和高計算開銷導致嚴重的效能瓶頸。

本研究提出一個創新的混合Optimistic-PBFT安全聚合框架，成功將Optimistic Rollup的樂觀原理系統性地應用於區塊鏈聯邦學習。該框架在樂觀情況下採用輕量級輪詢選擇機制，每輪僅需單一聚合器執行聚合運算，相較於傳統PBFT方法中所有聚合器都必須參與每輪計算，大幅提升了系統效率；當檢測到可疑行為時，啟動多驗證者並行驗證機制，需要至少2f+1個驗證者參與共識，實現效能與安全性的動態平衡。

系統核心創新包括：（1）異步挑戰機制設計，實現挑戰處理與主要訓練流程的完全解耦，確保聯邦學習過程永不中斷；（2）多聚合器協作與動態排除機制，通過輪詢演算法公平分配聚合任務，並在檢測到惡意行為後自動回滾至安全狀態；（3）經濟激勵與技術安全機制的深度整合，通過質押與獎懲機制防止惡意行為並鼓勵誠實參與。

本研究基於Flower聯邦學習框架開發完整的原型系統，通過模擬各種攻擊場景驗證系統安全性。實驗結果顯示，在正常運作情況下，該框架的計算複雜度為O(R/N)每聚合器，相較於傳統PBFT的O(R×V)每驗證者實現了顯著的效能提升。在面對惡意聚合器攻擊時，系統能夠有效檢測並回滾至安全狀態，同時通過經濟懲罰機制維持系統的長期安全性。

本研究的混合Optimistic-PBFT機制首次實現了區塊鏈聯邦學習中效能與安全性的最佳平衡，為該領域的實際部署與應用奠定重要基礎，同時為未來的去中心化人工智慧基礎架構研究提供新的技術路徑。

關鍵詞： 聯邦學習、區塊鏈、Optimistic Rollup、拜占庭容錯、安全聚合、多聚合器

## 英文摘要 (Abstract)
Federated Learning (FL) has emerged as a crucial privacy-preserving distributed machine learning paradigm for modern artificial intelligence development. However, traditional FL architectures rely on a single central aggregator, facing challenges including single point of failure risks, trust assumption issues, and lack of malicious aggregator detection mechanisms. While blockchain technology offers decentralized solutions for FL, existing blockchain-based FL schemes predominantly adopt traditional Byzantine Fault Tolerance (PBFT) consensus mechanisms, resulting in severe performance bottlenecks due to intensive multi-round communication requirements and high computational overhead.

This research proposes an innovative Hybrid Optimistic-PBFT secure aggregation framework that systematically applies Optimistic Rollup principles to blockchain-based federated learning. Under optimistic conditions, the framework employs a lightweight round-robin selection mechanism requiring only one aggregator per round for aggregation computation, significantly improving efficiency compared to traditional PBFT approaches where all aggregators must participate in every round. When suspicious behavior is detected, it activates a multi-validator parallel verification mechanism requiring at least 2f+1 validators to participate in consensus, achieving dynamic balance between performance and security.

The core innovations include: (1) An asynchronous challenge mechanism design that completely decouples challenge processing from the main training workflow, ensuring uninterrupted federated learning processes; (2) Multi-aggregator collaboration with dynamic exclusion mechanisms that fairly distribute aggregation tasks through round-robin algorithms and automatically rollback to safe states upon detecting malicious behavior; (3) Deep integration of economic incentives with technical security mechanisms, preventing malicious behavior and encouraging honest participation through staking and reward-penalty mechanisms.

This research develops a complete prototype system based on the Flower federated learning framework and validates system security through simulations of various attack scenarios. Experimental results demonstrate that under normal operation, the framework achieves computational complexity of O(R/N) per aggregator, representing significant performance improvements compared to traditional PBFT's O(R×V) per validator. When facing malicious aggregator attacks, the system effectively detects and rolls back to safe states while maintaining long-term security through economic penalty mechanisms.

The Hybrid Optimistic-PBFT mechanism presented in this research represents the first achievement of optimal balance between performance and security in blockchain-based federated learning, establishing important foundations for practical deployment and applications in this field, while providing new technical pathways for future decentralized artificial intelligence infrastructure research.
Keywords: Federated Learning, Blockchain, Optimistic Rollup, Byzantine Fault Tolerance, Secure Aggregation, Multi-Aggregator

# I. Introduction
[introduction](introduction.md)
# II. Background
[background](background.md)
# III. Related work
[related-work](related-work.md)
# IV. Framework design
[framework-design](framework-design.md)
# V. Implementation
[implementation](implementation.md)
# VI. Evaluation
[evaluation](evaluation.md)
# VII. Conclutions and future work
[conclutions-and-future-work](conclutions-and-future-work.md)
# Reference
