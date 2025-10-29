# Content Strategist Agent 使用指南

## 快速開始

### 1. 切換到agent目錄
```bash
cd .claude/agents/content-strategist
```

### 2. 啟動agent
```bash
# 方式1: 使用Claude Code CLI
claude

# 方式2: 在Claude Code中直接使用
# 輸入你的指令，agent會自動按照agent.md中定義的規範工作
```

### 3. 開始規劃
```bash
# 建議的第一個任務
"讀取 ../../framework-design.md 和所有 Deep Research 文件，創建完整的content strategy"
```

---

## Agent工作流程

### Phase 0: 理解研究核心
Agent會：
1. 讀取 `framework-design.md`
2. 提取研究問題、核心創新、關鍵技術、對比對象
3. 輸出 `content-strategy/research-core-analysis.md`

### Phase 1: 分析文獻
Agent會：
1. 讀取所有 `deep_research_*.md` 文件
2. 篩選與創新相關的技術和方案
3. 提取關鍵信息

### Phase 2: 創建策略
Agent會：
1. 創建內容分配矩陣
2. 標記潛在重複並提供區分策略
3. 輸出 `content-strategy/strategy-YYYYMMDD.md`

---

## 輸出文件

### 1. research-core-analysis.md
位置：`../../content-strategy/research-core-analysis.md`

內容：
- 研究問題
- 核心創新（排序）
- 關鍵支撐技術
- 主要對比對象
- 三章目標

### 2. strategy-YYYYMMDD.md
位置：`../../content-strategy/strategy-YYYYMMDD.md`

內容：
- Research Core Summary
- Content Distribution Matrix（核心！）
- Potential Overlaps & Differentiation
- Chapter Resource Allocation
- Quality Metrics Target

---

## 常用指令範例

### 創建初始策略
```
讀取 framework-design.md 和所有 deep_research 文件，創建完整的content strategy
```

### 更新特定章節策略
```
更新 Chapter 2 的內容分配，增加 PBFT 的深度到 4 頁
```

### 檢查並解決重複
```
檢查三章中關於 Byzantine容錯 的內容是否有重複，並提供區分策略
```

### 版本更新
```
根據reviewer的反饋，更新strategy到v1.1：將Ch2的2.3節拆分為2.3和2.4
```

---

## 注意事項

### ✅ Do
- 先讀 framework-design.md 理解核心創新
- 嚴格過濾無關內容
- 為每個技術設定明確的Goal
- 標記潛在的章節間重複
- 使用狀態emoji追蹤進度

### ❌ Don't
- 不要規劃與論文創新無關的技術
- Ch1不要允許超過20字的技術描述
- Ch2不要規劃具體研究系統（留給Ch3）
- 不要忘記版本控制

---

## 與其他Agent的協作

### → Chapter Writer
完成策略後，Chapter Writer會根據strategy.md寫作：
```bash
cd ../chapter-writer
```

### → Review Agent
策略可以提交給Review Agent審核：
```bash
cd ../review-agent
# 輸入: "審核 content-strategy/strategy-20250129.md 的合理性"
```

---

## 故障排除

### Q: Agent沒有讀取framework-design.md？
**A**: 明確指示："請先讀取 ../../framework-design.md"

### Q: 輸出的矩陣不完整？
**A**: 要求："確保每個技術都有Ch1/Ch2/Ch3/Goal四個欄位"

### Q: 如何重新生成策略？
**A**: 刪除舊的strategy.md，重新運行agent，並更新版本號

---

## 檔案結構

```
master-thesis/
├── .claude/agents/content-strategist/
│   ├── agent.md                    # Agent prompt
│   └── README.md                   # 本文件
├── content-strategy/
│   ├── research-core-analysis.md   # Phase 0 輸出
│   └── strategy-YYYYMMDD.md        # Phase 2 輸出（SSOT）
├── framework-design.md             # 必讀輸入
└── deep_research_*.md              # 文獻輸入
```
