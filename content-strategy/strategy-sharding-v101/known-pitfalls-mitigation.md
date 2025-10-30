# Known Pitfalls & Mitigation

## Pitfall 1: Ch1深度失控

**常見錯誤**:
- 技術描述超過20字
- 引入算法流程
- 討論具體系統設計

**檢測方法**:
```python
# 偽代碼檢查工具
def check_ch1_depth(sentence):
    if contains_algorithm_flow(sentence):
        return "FAIL: 包含算法流程"
    if contains_formula(sentence):
        return "FAIL: 包含數學公式"
    if mentions_specific_system_detail(sentence):
        return "FAIL: 討論具體系統"
    if word_count(sentence) > 20 and is_technical_term(sentence):
        return "FAIL: 技術描述超過20字"
    return "PASS"
```

**Mitigation**:
- Writer完成後自行檢查字數
- Review Agent使用深度檢查清單
- 超過20字的句子必須拆分或刪除

---

## Pitfall 2: Ch2與Ch3邊界模糊 ⚠️ CRITICAL (Enhanced - R1)

**常見錯誤**:
- Ch2討論FLCoin等具體系統
- Ch3重複解釋PBFT原理

**檢測方法**:
- **Ch2關鍵詞黑名單** (NEW - R1): ["FLCoin", "opML", "BlockDFL", "BMA-FL", "MCFLM-CB", "EPP-BCFL", "FLB2", "FLock", "BAFFLE", "BFLC"]
- **自動掃描工具** (NEW - R1):
  ```bash
  grep -E "FLCoin|opML|BlockDFL|BMA-FL|MCFLM-CB|EPP-BCFL|FLB2|FLock|BAFFLE|BFLC" chapter2-section-X.md
  ```
- Ch3應引用Ch2而非重新解釋: "如2.3節所述，PBFT三階段協議..."

**Mitigation** (Enhanced - R1):
1. **Writer自行掃描** (NEW): 完成section後先執行黑名單掃描，再提交Review
2. **明確警告** (NEW): Ch2 Writing Forbidden Zone已在Ch2章節開頭標注
3. **允許例外格式** (NEW): 僅允許"相關系統[7][8]"等匿名引用格式
4. Writer嚴格遵守「Ch2講原理，Ch3講系統」
5. Review Agent檢查是否出現黑名單關鍵詞
6. Ch3必須用「引用+批判」模式，禁止「重新解釋+批判」

**預估影響** (NEW - R1): 防止最高風險的邊界違規，節省3-5天返工時間

---

## Pitfall 3: Related Work缺乏批判性

**常見錯誤**:
- 純描述性內容（"FLCoin採用委員會機制，性能良好"）
- 缺乏與本研究對比
- 主觀評價（"很好但..."）

**檢測方法**:
```
每個方案必須回答4個問題:
1. 他們做了什麼？(貢獻)
2. 效果如何？(數據)
3. 缺少什麼？(局限，與本研究特性對比)
4. 我們如何解決？(本研究優勢)
```

**Mitigation**:
- 使用批判性分析模板（見3.1.1 FLCoin和3.2.1 opML完整範例）(R4 Implemented)
- Review Agent檢查是否包含四要素
- 局限必須是技術差異，非主觀評價

---

## Pitfall 4: 術語不一致

**常見錯誤**:
- 混用「聚合器」與「聚合者」
- 混用「回合」與「輪次」
- "PBFT"、"pbft"、"Pbft"大小寫不一致

**檢測方法**:
- 全文搜索同義詞對（aggregator: 聚合器vs聚合者）
- 檢查首字母大小寫一致性

**Mitigation**:
- 提供Terminology Consistency Table
- Citation Manager最後統一檢查
- 使用查找-替換批量修正

---

## Pitfall 5: 引用缺失或格式錯誤

**常見錯誤**:
- Background章節缺乏引用
- 引用格式不符IEEE標準
- [TODO]標記未處理

**檢測方法**:
```
Ch2每段應至少有1個引用（技術陳述需引用）
IEEE格式: [數字] 作者縮寫, "標題", 期刊/會議縮寫, vol. X, no. Y, pp. Z, 月 年份
```

**Mitigation**:
- Writer完成Ch2後立即補充引用
- Citation Manager專門審查引用完整性
- 建立references.bib統一管理

---

## Boundary Cases FAQ (NEW - 部分實現R9)

### Q1: 技術描述恰好20字，是否通過？
**A**: ✅ PASS。"≤20字"包含20字本身。

### Q2: "PBFT因O(n²)瓶頸需委員會機制優化"（22字），是否失敗？
**A**: ❌ FAIL。有兩個問題：
1. 超過20字（22字）
2. "委員會機制"屬於具體優化方案（FLCoin等），應留給Ch3

**修正**: "PBFT因O(n²)瓶頸限制可擴展性"（16字）

### Q3: Ch2可否用FLCoin作為範例解釋PBFT？
**A**: ❌ 絕對禁止。即使作為"範例"也不可。(R1 Enhanced)
- ✅ 正確做法: "某些研究將PBFT應用於FL多聚合器場景[TODO]"
- ❌ 錯誤做法: "例如FLCoin使用PBFT委員會機制..."

### Q4: Ch3引用Ch2技術時，可重新解釋嗎？
**A**: ❌ 不可重新解釋，僅能引用。
- ✅ 正確: "如2.3節所述，PBFT三階段協議複雜度為O(n²)"
- ❌ 錯誤: "PBFT包含Pre-prepare、Prepare、Commit三階段，複雜度為O(n²)"

### Q5: 術語首次出現在Ch2，Ch3還需完整定義嗎？
**A**: ⚠️ 部分需要。規則：
- 若Ch2與Ch3相鄰閱讀: 簡化提醒即可（"PBFT共識協議"）
- 若Ch3可能獨立閱讀: 完整定義（"實用拜占庭容錯（PBFT）"）
- 建議: 跨章首次使用完整定義，保險起見

### Q6: Ch3批判"局限性"時，可以主觀評價嗎？
**A**: ❌ 不可主觀評價，必須基於技術差異。
- ✅ 正確: "FLCoin固定委員會規模無法根據威脅等級動態調整"（具體技術差異）
- ❌ 錯誤: "FLCoin設計不夠靈活"（主觀評價）

---
