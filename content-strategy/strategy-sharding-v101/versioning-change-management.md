# Versioning & Change Management

## Version Control Rules

**Version Format**: vX.Y
- X: 主版本號（重大架構變更時+1）
- Y: 次版本號（section修改或增強時+1）

**Change Log必須記錄**:
1. 變更日期
2. 變更原因（Review發現問題、架構調整等）
3. 受影響sections
4. 狀態重置（受影響sections → ⏸️ Not Started或🔄 Needs Revision）

## 範例Change Log

```markdown
# Change Log

## v1.1 (2025-02-05)
**Reason**: Review Agent發現Ch1.2深度超標
**Changes**:
- Ch1.2精簡至≤20字/術語
- 刪除PBFT三階段描述（移至Ch2）
**Affected Sections**:
- 1.2 研究問題: 🔄 Needs Revision
**Status**: Ch1完成度 75% → 50%

## v1.2 (2025-02-10)
**Reason**: framework-design.md更新，新增安全性分析
**Changes**:
- Ch2.3新增安全性理論分析(0.3頁)
- Ch3.5更新研究缺口
**Affected Sections**:
- 2.3 PBFT: 🔄 Needs Revision (新增內容)
- 3.5 研究缺口: 🔄 Needs Revision (更新定位)
**Status**: 整體完成度 60% → 55%
```

---
