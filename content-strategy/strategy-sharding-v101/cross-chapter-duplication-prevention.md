# Cross-Chapter Duplication Prevention

## Duplication Risk Matrix

| Content | Ch1 | Ch2 | Ch3 | Differentiation Strategy |
|---------|-----|-----|-----|--------------------------|
| **PBFT複雜度** | "O(n²)導致瓶頸"(≤20字) | n×n×3階段推導(0.5頁) | "FLCoin降至O(3c)"(引用) | Ch1問題→Ch2原理→Ch3方案 |
| **Optimistic執行** | "樂觀假設節點誠實"(≤20字) | 樂觀假設公式+挑戰期(1頁) | "opML 7天挑戰期"(具體) | Ch1概念→Ch2原理→Ch3實作 |
| **多聚合器** | "分散負載提升容錯"(≤20字) | 算法1偽代碼(0.7頁) | "FLCoin滑動窗口"(設計) | Ch1動機→Ch2算法→Ch3系統 |
| **f<n/3條件** | "需要容忍f<n/3惡意"(≤20字) | Quorum交集證明(0.5頁) | "BlockDFL 40%實驗"(數據) | Ch1需求→Ch2理論→Ch3實證 |
| **挑戰機制** | "允許質疑可疑結果"(≤20字) | 挑戰流程算法2(1.2頁) | "opML欺詐證明vs PBFT"(對比) | Ch1亮點→Ch2流程→Ch3差異 |

## Terminology Consistency Table

| 術語（中文） | 術語（英文） | 首次定義 | 後續使用 | 避免混用 |
|------------|------------|---------|---------|---------|
| 實用拜占庭容錯 | Practical Byzantine Fault Tolerance | Ch1.1 | PBFT | ❌ "實用拜占庭容錯協議" |
| 樂觀執行 | Optimistic Execution | Ch1.1 | 樂觀執行/Optimistic | ❌ "樂觀假設執行" |
| 挑戰機制 | Challenge Mechanism | Ch1.3 | 挑戰機制 | ❌ "挑戰驗證機制" |
| 聚合器 | Aggregator | Ch1.1 | 聚合器 | ❌ "聚合者"、"聚合節點" |
| 驗證者 | Validator | Ch1.1 | 驗證者 | ❌ "驗證器"、"驗證節點" |
| 欺詐證明 | Fraud Proof | Ch2.4 | 欺詐證明 | ❌ "詐騙證明"、"錯誤證明" |
| 拜占庭容錯 | Byzantine Fault Tolerance | Ch2.3 | BFT/拜占庭容錯 | ❌ "Byzantine容錯" |
| 聯邦學習 | Federated Learning | Ch1.1 | FL/聯邦學習 | ❌ "聯合學習" |
| 單點故障 | Single Point of Failure | Ch1.1 | SPOF/單點故障 | ❌ "單一故障點" |
| 質押 | Staking | Ch2.6 | 質押 | ❌ "抵押"、"鎖倉" |
| 回合/輪次 | Round | Ch1.1 | 回合/輪 | ❌ 不混用"回合"與"輪次" |
| 委員會 | Committee | Ch2.3 | 委員會 | ❌ "委員會節點" |
| 模型參數 | Model Parameters | Ch2.1 | 模型參數 | ❌ "模型權重"、"權重參數" |
| 梯度 | Gradient | Ch2.1 | 梯度 | ❌ "梯度更新"、"梯度參數" |
| 本地更新 | Local Update | Ch2.1 | 本地更新 | ❌ "本地模型"、"更新參數" |
| 全局模型 | Global Model | Ch2.1 | 全局模型 | ❌ "聚合模型"、"全局參數" |

**使用規則**:
1. 首次: "實用拜占庭容錯（Practical Byzantine Fault Tolerance, PBFT）"
2. 同段第二次: "PBFT協議"
3. 後續段落: "PBFT"
4. 跨章首次: "PBFT共識協議"（提醒讀者）

**模型參數相關規則** (NEW - 部分實現R8):
- "模型參數"指完整模型權重（w_t）
- "梯度"指訓練過程中的梯度（∇L）
- "本地更新"指客戶端訓練後的參數變化
- "全局模型"指聚合後的模型
- 避免混用"參數"和"權重"（統一用"參數"）

---
