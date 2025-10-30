# Chapter 2: ⚠️ Ch2 Writing Forbidden Zone (NEW - R1)

**絕對禁止出現的關鍵詞**:
- FLCoin, opML, BlockDFL, BMA-FL, MCFLM-CB
- EPP-BCFL, FLB2, FLock, BAFFLE, BFLC

**檢測方法**:
```bash
# Writer完成section後，先自行掃描再提交Review
grep -E "FLCoin|opML|BlockDFL|BMA-FL|MCFLM-CB|EPP-BCFL|FLB2|FLock|BAFFLE|BFLC" chapter2-section-X.md
```

**允許的例外**（僅限以下格式）:
- ✅ "某些研究將PBFT應用於FL多聚合器場景[TODO]"
- ✅ "相關系統[7][8]採用委員會機制優化PBFT"
- ❌ "例如FLCoin使用PBFT委員會機制..."
- ❌ "如opML所示，樂觀執行可..."

**警告**:
即使作為「範例」或「案例」也不可提及具體系統名稱。Ch2講通用原理，Ch3講具體系統。違反此規則將導致section返工（預估損失3-5天）。

---
