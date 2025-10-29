# Citation Manager Agent 使用指南

## 快速開始

### 1. 切換到agent目錄
```bash
cd .claude/agents/citation-manager
```

### 2. 啟動agent管理引用
```bash
# 方式1: 使用Claude Code CLI
claude

# 方式2: 直接輸入管理指令
```

---

## 核心任務總覽

```
Phase 1: 初始化 (專案開始)
├─ 輸入: deep_research_*.md
├─ 輸出: references.bib + citation-catalog.md
└─ 目的: 建立引用資料庫

Phase 2: Background即時驗證 (Ch2寫作時)
├─ 輸入: chapter2-background-v1.md
├─ 檢查: 引用存在？作者匹配？格式正確？
└─ 輸出: 警告報告（如有問題）

Phase 3: 後補引用 (Ch1/Ch3完成後)
├─ 輸入: 章節中的[TODO]
├─ 搜尋: citation-catalog.md
└─ 輸出: citation-suggestions.md

Phase 4: 最終驗證 (所有完成)
├─ 輸入: 所有章節 + references.bib
├─ 檢查: 缺失、未使用、格式問題
└─ 輸出: citation-report.md
```

---

## Phase 1: 初始化引用庫

### 常用指令

#### 建立引用資料庫
```
從 ../../deep_research_1009.md 和 ../../deep_research_1027.md 提取所有文獻，建立 references.bib
```

#### 生成分類目錄
```
根據 references.bib 生成 citation-catalog.md，按技術領域分類
```

### 工作流程

1. **提取文獻**
   - 讀取所有deep_research_*.md
   - 識別文獻引用格式
   - 轉換為BibTeX格式

2. **去重合併**
   - 檢查重複文獻（同一篇論文不同引用方式）
   - 保留最完整的版本
   - 統一引用編號

3. **生成目錄**
   - 按技術領域分類
   - 添加簡短描述
   - 創建查找索引

### 輸出範例

#### `references.bib`
```bibtex
@article{castro1999practical,
  author    = {M. Castro and B. Liskov},
  title     = {Practical Byzantine Fault Tolerance},
  journal   = {Proceedings of the Third Symposium on Operating Systems Design and Implementation},
  year      = {1999},
  pages     = {173--186},
  publisher = {USENIX Association}
}

@article{ren2021flcoin,
  author    = {Y. Ren and Y. Luo and N. N. Xiong and others},
  title     = {FLCoin: Blockchain-Based Federated Learning},
  journal   = {IEEE Transactions on Services Computing},
  year      = {2021},
  volume    = {14},
  number    = {6},
  pages     = {2096--2108}
}
```

#### `citation-catalog.md`
```markdown
# Citation Catalog

## By Technology Area

### PBFT & BFT Consensus
- **[7]** M. Castro and B. Liskov, "Practical Byzantine Fault Tolerance," OSDI 1999
  - 關鍵字: PBFT, Byzantine容錯, 三階段共識
  - 用於: Ch2 PBFT詳細說明

- **[9]** M. Yin et al., "HotStuff: BFT Consensus with Linearity and Responsiveness," PODC 2019
  - 關鍵字: HotStuff, 線性通訊複雜度
  - 用於: Ch2 優化方案比較

### Blockchain Federated Learning
- **[4]** Y. Ren et al., "FLCoin: Blockchain-Based Federated Learning," IEEE TSC 2021
  - 關鍵字: FLCoin, 滑動窗口, 委員會
  - 用於: Ch3 主要對比方案

- **[10]** K. Fan et al., "BlockDFL: Decentralized Federated Learning," IEEE TIFS 2022
  - 關鍵字: BlockDFL, 去中心化
  - 用於: Ch3 相關方案

## Quick Search Index
| Keyword | Citations |
|---------|-----------|
| PBFT | [7], [9], [12] |
| FLCoin | [4] |
| Byzantine容錯 | [7], [9], [14] |
| 聯邦學習 | [4], [10], [15], [18] |

## Usage Statistics (將持續更新)
| Citation | Ch1 | Ch2 | Ch3 | Total | Status |
|----------|-----|-----|-----|-------|--------|
| [7] | 0 | 0 | 0 | 0 | ⏸️ Not Used |
| [4] | 0 | 0 | 0 | 0 | ⏸️ Not Used |
```

---

## Phase 2: Background即時驗證

### 常用指令

#### 驗證整個章節
```
檢查 ../../chapters/chapter2-background-v1.md 的所有引用是否正確
```

#### 驗證特定引用
```
驗證 chapter2 中 [7] 的引用：作者名稱、格式是否正確
```

### 檢查項目

#### Check 1: 引用存在性
```markdown
Writer寫: "Castro和Liskov[7]提出PBFT..."

檢查:
✅ [7] 存在於 references.bib
❌ [7] 不存在 → 錯誤報告
```

#### Check 2: 作者名稱匹配
```markdown
內文: "Castro和Liskov[7]"
BibTeX: author = {M. Castro and B. Liskov}

檢查:
✅ "Castro" 匹配 "M. Castro"
✅ "Liskov" 匹配 "B. Liskov"
❌ 不匹配 → 警告報告
```

#### Check 3: IEEE格式正確性
```markdown
檢查 references.bib[7]:
✅ 作者格式: "M. Castro" (首字母縮寫)
❌ 作者格式: "Miguel Castro" (完整名字) → 需修正
✅ 頁碼: "173--186" (兩個連字號)
❌ 頁碼: "173-186" (一個連字號) → 需修正
✅ 標題: Title Case
```

### 輸出報告範例

```markdown
# Background Citation Verification Report
Date: 2025-01-30
File: chapters/chapter2-background-v1.md

## Summary
- Total citations: 35
- Valid: 33
- Issues: 2

## 🔴 ERRORS (Must Fix)
### Error #1: Citation Not Found
- **Location**: Section 2.3.2, Line 156
- **Content**: "Yin等人[9]提出HotStuff..."
- **Problem**: [9] 不存在於 references.bib
- **Action**: 添加 HotStuff 文獻到 references.bib

## 🟡 WARNINGS (Should Fix)
### Warning #1: Author Name Mismatch
- **Location**: Section 2.1, Line 45
- **Content**: "Castro和Barbara[7]..."
- **BibTeX**: author = {M. Castro and B. Liskov}
- **Problem**: "Barbara" 應為 "Liskov"
- **Action**: 修正為 "Castro和Liskov[7]"

## 🟢 FORMAT ISSUES (Polish)
### Issue #1: BibTeX Format
- **Citation**: [7]
- **Problem**: pages = "173-186" (應為 "173--186")
- **Action**: 修正 references.bib
```

---

## Phase 3: 後補引用

### 常用指令

#### 找出所有TODO
```
找出 ../../chapters/chapter1-introduction-v1.md 的所有 [TODO] 引用
```

#### 建議引用
```
為 chapter1 的所有 [TODO] 建議合適的引用編號
```

#### 自動替換
```
根據 citation-suggestions.md，自動替換 chapter1 的 [TODO] 為正確引用
```

### 工作流程

1. **掃描[TODO]**
   ```markdown
   原文: "現有方案如FLCoin[TODO]和opML[TODO]各有局限..."

   提取:
   - Line 28: "FLCoin[TODO]"
   - Line 28: "opML[TODO]"
   ```

2. **搜尋匹配**
   ```markdown
   search_catalog("FLCoin") → 找到 [4]
   search_catalog("opML") → 找到 [15]
   ```

3. **生成建議**
   ```markdown
   Line 28: "FLCoin[TODO]" → Suggest [4] ✅
   Line 28: "opML[TODO]" → Suggest [15] ✅
   ```

4. **替換（需確認）**
   ```markdown
   修改前: "現有方案如FLCoin[TODO]和opML[TODO]各有局限..."
   修改後: "現有方案如FLCoin[4]和opML[15]各有局限..."
   ```

### 輸出範例

#### `citation-suggestions.md`
```markdown
# Citation Suggestions for Chapter 1

## Summary
- Total [TODO] found: 8
- Matched: 7
- No match: 1

## Suggestions

### ✅ Matched (7)

#### 1. Line 28: FLCoin[TODO]
**Context**: "現有方案如FLCoin[TODO]和opML[TODO]..."

**Search Result**:
- [4] Y. Ren et al., "FLCoin: Blockchain-Based Federated Learning," IEEE TSC 2021

**Confidence**: HIGH (完全匹配)

**Suggested Replacement**:
```
"現有方案如FLCoin[4]和opML[TODO]..."
```

#### 2. Line 28: opML[TODO]
**Context**: "現有方案如FLCoin[TODO]和opML[TODO]..."

**Search Result**:
- [15] D. Li et al., "opML: Optimistic Machine Learning on Blockchain," ACM CCS 2022

**Confidence**: HIGH (完全匹配)

**Suggested Replacement**:
```
"現有方案如FLCoin[4]和opML[15]..."
```

### ❌ No Match (1)

#### 8. Line 156: "BlockFL系統[TODO]"
**Context**: "類似的BlockFL系統[TODO]也面臨相同問題..."

**Problem**: 在 citation-catalog.md 找不到 "BlockFL" 相關文獻

**Suggestions**:
- Option 1: 檢查是否拼寫錯誤（BlockDFL? BlockFLow?）
- Option 2: 添加該文獻到 references.bib
- Option 3: 刪除該引用（如果不重要）

**Action Required**: 人工確認
```

---

## Phase 4: 最終驗證

### 常用指令

#### 生成完整報告
```
生成完整的 citation-report.md，檢查所有章節的引用完整性
```

#### 檢查未使用引用
```
列出 references.bib 中所有未使用的引用
```

#### 更新使用統計
```
更新 citation-catalog.md 的 Usage Statistics
```

### 報告範例

```markdown
# Citation Completeness Report
Generated: 2025-01-30 16:00

## Executive Summary
- **Total citations in bib**: 87
- **Used citations**: 63 (72.4%)
- **Unused citations**: 24 (27.6%)
- **Missing citations**: 3
- **Format issues**: 5

---

## 🔴 HIGH: Missing Citations

### 1. Ch1, Line 28: Missing Citation
**Content**: "Castro和Liskov的研究顯示..."
**Problem**: 提到作者但缺少引用
**Suggestion**: 添加 [7]
**Fixed**:
```markdown
"Castro和Liskov[7]的研究顯示..."
```

### 2. Ch3, Line 156: Missing Citation
**Content**: "Ren等人的FLCoin系統採用..."
**Problem**: 提到具體研究但缺少引用
**Suggestion**: 添加 [4]

### 3. Ch2, Line 89: Missing Citation
**Content**: "HotStuff協議簡化了視圖切換..."
**Problem**: 提到具體協議但缺少引用
**Suggestion**: 添加 [9]

---

## 🟡 MEDIUM: Format Issues

### 1. [23] - Author Format Error
**Current**: author = {M.Yin and others}
**Problem**: 缺少空格
**Fixed**: author = {M. Yin and others}

### 2. [45] - Pages Format Error
**Current**: pages = {173-186}
**Problem**: 應使用兩個連字號
**Fixed**: pages = {173--186}

### 3. [12] - Title Case Error
**Current**: title = {Practical byzantine fault tolerance}
**Problem**: 應使用 Title Case
**Fixed**: title = {Practical Byzantine Fault Tolerance}

### 4. [18] - Missing Volume
**Current**: @article 缺少 volume 欄位
**Action**: 補充 volume = {14}

### 5. [31] - Duplicate Entry?
**Problem**: 與 [7] 可能是同一篇文獻
**Action**: 人工確認，如重複則合併

---

## ℹ️ INFO: Unused Citations (24)

以下文獻在 references.bib 但未在三章中使用：

**PBFT相關** (3篇):
- [18] T. Distler, "Byzantine Fault-Tolerant State Machine Replication," 2014
- [22] J. Sousa et al., "BFT-SMaRt: A Modular Library," 2014
- [31] (可能與[7]重複)

**聯邦學習相關** (8篇):
- [25], [27], [28], [29], [33], [35], [42], [51]

**區塊鏈基礎** (6篇):
- [13], [19], [24], [38], [43], [47]

**其他** (7篇):
- [16], [21], [26], [30], [36], [41], [49]

**Recommendation**:
- Option 1: 確認是否應在論文中引用（可能遺漏）
- Option 2: 從 references.bib 移除（非必要文獻）

---

## 📊 Usage Statistics by Chapter

### Chapter 1: Introduction (5 citations)
| Citation | Count | Content |
|----------|-------|---------|
| [7] | 1 | PBFT問題 |
| [4] | 1 | FLCoin系統 |
| [15] | 1 | opML系統 |
| [10] | 1 | BlockDFL系統 |
| [20] | 1 | 區塊鏈FL綜述 |

### Chapter 2: Background (35 citations)
| Citation | Count | Content |
|----------|-------|---------|
| [7] | 8 | PBFT詳細說明 |
| [9] | 5 | HotStuff優化 |
| [12] | 4 | Byzantine容錯理論 |
| [1] | 3 | 區塊鏈基礎 |
| [2] | 3 | 聯邦學習基礎 |
| Others | 12 | 其他技術 |

**Most Used**: [7] (PBFT) - 8次

### Chapter 3: Related Work (23 citations)
| Citation | Count | Content |
|----------|-------|---------|
| [4] | 5 | FLCoin系統 |
| [15] | 4 | opML系統 |
| [10] | 3 | BlockDFL系統 |
| [11] | 2 | 其他BFL系統 |
| Others | 9 | 相關研究 |

**Most Used**: [4] (FLCoin) - 5次

---

## 🔍 Cross-Reference Analysis

### Citation [7] (PBFT)
- Ch1: 1次 (問題導向)
- Ch2: 8次 (詳細解釋)
- Ch3: 3次 (方案對比)
- **Total**: 12次
- **Status**: ✅ 使用合理（重要核心技術）

### Citation [4] (FLCoin)
- Ch1: 1次 (簡單提及)
- Ch2: 0次 (✅ 正確，不在Background討論具體系統)
- Ch3: 5次 (詳細批判分析)
- **Total**: 6次
- **Status**: ✅ 使用合理（主要對比方案）

---

## ✅ Recommended Actions

### Immediate (HIGH Priority)
1. 補充3個缺失引用（Ch1: Line 28, Ch3: Line 156, Ch2: Line 89）
2. 修正5個格式問題

### Review (MEDIUM Priority)
3. 確認[31]是否與[7]重複
4. 檢查24個未使用引用是否應刪除

### Optional (LOW Priority)
5. 統一作者名稱風格（全部用 "Castro和Liskov" 或 "Castro等人"）
6. 為高頻引用添加註解（例如[7]被引用12次）
```

---

## IEEE格式詳細規範

### BibTeX類型與必須欄位

#### @article (期刊論文)
```bibtex
@article{castro1999practical,
  author    = {M. Castro and B. Liskov},      % 必須
  title     = {Practical Byzantine Fault Tolerance},  % 必須
  journal   = {IEEE Transactions on Dependable and Secure Computing},  % 必須
  year      = {1999},                         % 必須
  volume    = {10},                           % 強烈建議
  number    = {3},                            % 建議
  pages     = {173--186},                     % 必須
  doi       = {10.1109/TDSC.2012.45}         % 建議
}
```

#### @inproceedings (會議論文)
```bibtex
@inproceedings{yin2019hotstuff,
  author    = {M. Yin and D. Malkhi and others},  % 必須
  title     = {HotStuff: BFT Consensus with Linearity and Responsiveness},  % 必須
  booktitle = {Proceedings of the 2019 ACM Symposium on Principles of Distributed Computing},  % 必須
  year      = {2019},                         % 必須
  pages     = {347--356},                     % 必須
  address   = {Toronto, Canada},              % 建議
  publisher = {ACM}                           % 建議
}
```

#### @misc (arXiv, 網站等)
```bibtex
@misc{li2022opml,
  author       = {D. Li and others},
  title        = {opML: Optimistic Machine Learning on Blockchain},
  howpublished = {arXiv preprint arXiv:2201.12345},
  year         = {2022},
  note         = {Available: https://arxiv.org/abs/2201.12345}
}
```

### 格式細節

#### 作者格式
```bibtex
✅ 正確:
author = {M. Castro and B. Liskov}              % 2位作者
author = {M. Castro and B. Liskov and others}   % 3位以上

❌ 錯誤:
author = {Miguel Castro and Barbara Liskov}     % 不要完整名字
author = {M.Castro and B.Liskov}                % 缺少空格
author = {Castro M. and Liskov B.}              % 順序錯誤
```

#### 標題格式
```bibtex
✅ 正確:
title = {Practical Byzantine Fault Tolerance}   % Title Case

❌ 錯誤:
title = {practical byzantine fault tolerance}   % 全小寫
title = {PRACTICAL BYZANTINE FAULT TOLERANCE}   % 全大寫
```

#### 頁碼格式
```bibtex
✅ 正確:
pages = {173--186}      % 兩個連字號

❌ 錯誤:
pages = {173-186}       % 一個連字號
pages = {173 - 186}     % 有空格
pages = {173~186}       % 波浪號
```

#### 期刊名稱
```bibtex
✅ 正確:
journal = {IEEE Transactions on Services Computing}           % 完整名稱
journal = {Proc. ACM Symp. Principles of Distributed Computing}  % 縮寫（會議）

❌ 錯誤:
journal = {IEEE TSC}    % 過度縮寫
```

---

## 常見問題處理

### Problem 1: 作者名稱不一致

**症狀**:
```markdown
Ch1: "Castro和Liskov[7]..."
Ch2: "Castro等人[7]..."
Ch3: "M. Castro和B. Liskov[7]..."
```

**診斷**: 全文未統一作者引用方式

**解決**:
```markdown
建議統一為: "Castro和Liskov[7]"（2位作者應列出兩位）

或者: 如果文中一致使用"等人"，可改為 "Castro等人[7]"
但BibTeX必須保持完整: author = {M. Castro and B. Liskov}
```

---

### Problem 2: 引用號碼跳號

**症狀**: [7], [8], [10], [11] (缺[9])

**診斷**:
1. 檢查references.bib是否有[9]
2. 檢查是否被誤刪
3. 檢查deep_research中是否有[9]

**解決**:
- 如果[9]確實不需要 → 重新編號 [10]→[9], [11]→[10]
- 如果[9]遺漏 → 補充回references.bib

---

### Problem 3: 重複引用

**症狀**:
```bibtex
@article{castro1999practical, ...}  # [7]
@article{castro1999pbft, ...}       # [23]
# 實際是同一篇！
```

**診斷**: 檢查title, author, year是否相同

**解決**:
1. 保留最完整的entry (例如[7])
2. 刪除重複entry ([23])
3. 全文搜尋[23]，替換為[7]
4. 重新編號後續引用

---

### Problem 4: Deep Research的引用編號與最終不同

**症狀**: Deep Research中是[4]，但references.bib中變成[12]

**原因**: 重新編號或合併時改變

**解決**:
- 維護一個mapping table:
  ```
  Deep Research → Final
  [4] → [12]
  [7] → [7]
  [9] → 刪除（重複）
  ```
- 在citation-catalog.md註明

---

### Problem 5: [TODO]無法匹配

**症狀**: "BlockFL系統[TODO]" 但catalog找不到

**診斷**:
1. 拼寫錯誤？(BlockDFL?)
2. Deep Research中確實沒有？
3. 應該引用但遺漏？

**解決**:
1. 搜尋相似名稱
2. 詢問Writer是否應刪除或修正
3. 如需要，添加該文獻到references.bib

---

## 與其他Agents協作

### ← 接收來自 Content Strategist
```
Strategist完成strategy → 了解哪些文獻重要
```

### ↔ 配合 Chapter Writer
```
Writer寫Background → 即時驗證引用
Writer寫Ch1/Ch3 → 後補[TODO]引用
```

### → 提供給 Review Agent
```
Final Review時 → 提供citation-report.md
Review Agent檢查引用完整性
```

---

## 工作流程完整範例

### 情境：管理整個專案的引用

#### Step 1: 初始化 (專案開始)
```bash
cd .claude/agents/citation-manager
```

**指令**:
```
從 ../../deep_research_1009.md 和 ../../deep_research_1027.md 提取所有文獻，
建立 references.bib 和 citation-catalog.md
```

**輸出**:
- `references.bib` (87篇文獻)
- `citation-catalog.md` (分類索引)

**Git提交**:
```bash
git add references.bib citation-catalog.md
git commit -m "Init: 建立引用資料庫 (87篇文獻)"
```

---

#### Step 2: Background即時驗證 (Ch2寫作中)

**Writer完成Section 2.3** → 切換到Citation Manager

**指令**:
```
檢查 ../../chapters/chapter2-background-v1.md 的 Section 2.3 所有引用
```

**輸出**: `background-citation-verification.md`
```markdown
## Issues Found
### Error #1: [9] 不存在
- Location: Section 2.3.2, Line 156
- Action: 添加 HotStuff 文獻
```

**修正**:
1. 添加[9]到references.bib
2. 通知Writer

**Git提交**:
```bash
git add references.bib
git commit -m "Add: HotStuff [9] 引用"
```

---

#### Step 3: 後補引用 (Ch1完成)

**Writer完成Chapter 1** → 切換到Citation Manager

**指令**:
```
找出 ../../chapters/chapter1-introduction-v1.md 的所有 [TODO]，
建議合適的引用
```

**輸出**: `citation-suggestions-ch1.md`
```markdown
## Suggestions
1. Line 28: "FLCoin[TODO]" → [4]
2. Line 28: "opML[TODO]" → [15]
3. Line 45: "區塊鏈聯邦學習[TODO]" → [20]
```

**確認後替換**:
```
根據 citation-suggestions-ch1.md 自動替換 chapter1 的 [TODO]
```

**Git提交**:
```bash
git add chapters/chapter1-introduction-v1.md
git commit -m "Update: Ch1 補充引用 ([4], [15], [20])"
```

---

#### Step 4: 最終驗證 (三章完成)

**所有章節完成** → 切換到Citation Manager

**指令**:
```
生成完整的 citation-report.md，包含：
1. 缺失引用
2. 未使用引用
3. 格式問題
4. 使用統計
```

**輸出**: `citation-report.md`
```markdown
## Summary
- Missing: 3
- Format issues: 5
- Unused: 24
```

**修正所有HIGH priority問題**

**更新catalog統計**:
```
更新 citation-catalog.md 的 Usage Statistics
```

**Git提交**:
```bash
git add citation-report.md citation-catalog.md
git commit -m "Final: 引用完整性驗證報告"
```

---

## 輸出文件說明

### 1. references.bib
**用途**: 主要引用資料庫
**格式**: BibTeX (IEEE格式)
**維護**: 持續更新

### 2. citation-catalog.md
**用途**: 分類索引，方便查找
**包含**: 技術領域分類、關鍵字索引、使用統計
**維護**: Phase 1創建，Phase 4更新統計

### 3. citation-suggestions.md
**用途**: [TODO]替換建議
**生成時機**: Phase 3 (Ch1/Ch3完成後)
**一次性**: 替換後可刪除

### 4. background-citation-verification.md
**用途**: Background章節引用驗證
**生成時機**: Phase 2 (Ch2寫作時)
**頻率**: 每次Writer完成section後

### 5. citation-report.md
**用途**: 最終完整性報告
**生成時機**: Phase 4 (所有完成)
**包含**: 所有問題匯總、統計分析

---

## 提交前檢查清單

### Phase 1完成時
- [ ] references.bib 格式符合IEEE？
- [ ] 所有entry都有必須欄位？
- [ ] 去除了重複引用？
- [ ] citation-catalog.md 分類清楚？

### Phase 2驗證時
- [ ] 所有引用都存在於bib？
- [ ] 作者名稱匹配？
- [ ] 格式問題都已標記？

### Phase 3後補時
- [ ] 所有[TODO]都有建議？
- [ ] 建議的confidence標記清楚？
- [ ] 無法匹配的都說明原因？

### Phase 4最終時
- [ ] citation-report.md 完整？
- [ ] 所有HIGH priority問題已修正？
- [ ] Usage Statistics已更新？
- [ ] 未使用引用已檢視？

---

## 檔案結構

```
master-thesis/
├── .claude/agents/citation-manager/
│   ├── agent.md       # Agent prompt
│   └── README.md      # 本文件
├── references.bib     # 主要引用庫 (Phase 1創建)
├── citation-catalog.md   # 分類索引 (Phase 1創建, Phase 4更新)
├── citation-suggestions-ch1.md   # Ch1建議 (Phase 3)
├── citation-suggestions-ch3.md   # Ch3建議 (Phase 3)
├── background-citation-verification.md   # Background驗證 (Phase 2)
├── citation-report.md   # 最終報告 (Phase 4)
├── chapters/
│   ├── chapter1-introduction-v1.md    # 檢查對象
│   ├── chapter2-background-v1.md      # 檢查對象
│   └── chapter3-related-work-v1.md    # 檢查對象
└── deep_research_*.md   # 文獻來源
```

---

## 快速參考卡

```
┌─────────────────────────────────────────────┐
│ Citation Manager Quick Reference            │
├─────────────────────────────────────────────┤
│ Phase 1: 初始化 (專案開始)                  │
│ Phase 2: Background即時驗證 (Ch2寫作時)     │
│ Phase 3: 後補引用 (Ch1/Ch3完成後)           │
│ Phase 4: 最終驗證 (所有完成)                │
├─────────────────────────────────────────────┤
│ 作者格式: M. Castro (首字母縮寫)            │
│ 頁碼格式: 173--186 (兩個連字號)             │
│ 標題格式: Title Case                        │
├─────────────────────────────────────────────┤
│ Background: 即時驗證 (不可TODO)             │
│ Ch1/Ch3: 可用TODO，後補                     │
└─────────────────────────────────────────────┘
```

---

## 故障排除

### Q: Deep Research的引用格式不統一怎麼辦？
**A**: 提取時統一轉換為IEEE BibTeX格式，保留最完整的資訊。

### Q: 同一篇論文有多種引用方式？
**A**: 合併為一個entry，選擇最完整的版本，更新所有引用編號。

### Q: Writer不同意我的格式要求？
**A**: IEEE格式是標準，不可協商。在報告中說明具體規則出處。

### Q: [TODO]太多無法一次處理？
**A**: 按優先級處理：
1. 先處理有明確匹配的
2. 再處理需要人工確認的
3. 最後處理無法匹配的

---

恭喜！所有4個agents都已創建完成！🎉
