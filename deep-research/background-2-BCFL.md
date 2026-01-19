# BCFL 架構與共識機制文獻調查

區塊鏈式聯邦學習（BCFL）透過去中心化帳本取代傳統中央聚合器，解決單點故障與信任問題。本調查涵蓋 **2018-2024 年六篇核心論文**，展示 BCFL 從 PoW 到委員會共識的演進脈絡。

---

## 1. BlockFL：首個 BCFL 架構

**H. Kim, J. Park, M. Bennis, and S.-L. Kim, "Blockchained on-device federated learning," IEEE Commun. Lett., vol. 24, no. 6, pp. 1279-1283, Jun. 2020.**

**系統架構**：BlockFL 完全移除中央參數伺服器，礦工節點同時擔任驗證者與聚合器。本地模型更新被打包進區塊，透過挖礦達成全域模型共識。採用自建的 **permissionless 區塊鏈**。

**共識機制**：採用 **Proof of Work (PoW)**。選擇理由為 PoW 在開放網路中提供完全去中心化與抗操控能力，適合無需許可的 FL 場景。然而，作者指出 **端到端延遲** 是主要瓶頸——區塊生成率過高會導致分叉，降低 FL 效能。

**驗證方式**：全節點驗證，所有礦工在出塊前驗證本地更新的合法性。模型更新 **完全儲存於鏈上**。

---

## 2. PoQ：將共識運算與訓練結合

**Y. Lu, X. Huang, Y. Dai, S. Maharjan, and Y. Zhang, "Blockchain and federated learning for privacy-preserved data sharing in industrial IoT," IEEE Trans. Ind. Informat., vol. 16, no. 6, pp. 4177-4186, Jun. 2020.**

**系統架構**：針對工業物聯網設計的 **聯盟鏈架構**，將 FL 直接整合至共識流程，使共識運算同時服務於聯邦訓練。

**共識機制**：提出 **Proof of Training Quality (PoQ)**。選擇理由為傳統 PoW 的哈希運算無實際意義，PoQ 將共識挑戰替換為 **模型參數準確性驗證**，結合差分隱私保護，使運算資源不再浪費於無意義的數學難題。

**驗證方式**：兩階段驗證——本地訓練在鏈下執行，模型參數（非原始資料）在鏈上經 PoQ 驗證後整合為全域模型。

---

## 3. BFLC：委員會共識降低開銷

**Y. Li, C. Chen, N. Liu, H. Huang, Z. Zheng, and Q. Yan, "A blockchain-based decentralized federated learning framework with committee consensus," IEEE Netw., vol. 35, no. 1, pp. 234-241, Jan. 2021.**

**系統架構**：基於 FISCO BCOS 聯盟鏈，採用 **動態選舉的委員會** 取代中央伺服器進行模型聚合。區塊鏈儲存兩種區塊類型：全域模型區塊與本地更新區塊。

**共識機制**：採用 **委員會式 BFT 共識**。選擇理由為傳統 PBFT 需要所有節點參與，產生 O(n²) 通訊複雜度；委員會機制將參與者限縮至 **約 40% 活躍節點**，大幅降低共識運算開銷，同時透過 BFT 協議偵測惡意模型投毒。

**驗證方式**：委員會驗證——委員會成員使用自身資料集驗證本地更新並計算驗證分數。全域模型與本地更新皆 **儲存於鏈上**。

---

## 4. VBFL：PoS 啟發的貢獻權重機制

**H. Chen, S. A. Asif, J. Park, C.-C. Shen, and M. Bennis, "Robust blockchained federated learning with model validation and proof-of-stake inspired consensus," arXiv:2101.03300, 2021.**

**系統架構**：完全去中心化架構，節點在每輪扮演三種角色：Worker（訓練）、Validator（驗證）、Miner（出塊）。

**共識機制**：採用 **PoS 啟發的協議**。選擇理由為將 stake 定義為 **累積的 FL 貢獻獎勵**，誠實節點透過成功驗證累積更多 stake，提高成為出塊者的機率。此設計使共識權重與訓練貢獻對齊，避免 PoW 的無謂運算。

**Stake 機制**：獎勵依角色分配——Worker 因更新被驗證獲獎、Validator 因準確驗證獲獎、Miner 因出塊獲獎。累積 stake 最高者成為 winning-miner。連續 k 輪被識別為惡意的節點將被 **黑名單排除**。

**驗證方式**：Validator 以自身資料集測試本地更新的準確度，投票結果記錄於鏈上。

---

## 5. VFChain：可驗證與可審計的聚合

**Z. Peng et al., "VFChain: Enabling verifiable and auditable federated learning via blockchain systems," IEEE Trans. Netw. Sci. Eng., vol. 9, no. 1, pp. 173-186, Jan. 2022.**

**系統架構**：基於 **Hyperledger Fabric** 私有鏈，委員會節點集體執行模型聚合，區塊鏈記錄可驗證證明。

**共識機制**：委員會透過區塊鏈共識選出，採用新穎的 **Dual Skip Chain (DSC)** 資料結構支援安全的委員會輪換與高效的證明檢索。

**驗證方式**：聚合的 **可驗證證明記錄於鏈上**，支援多模型學習任務的審計追溯。DSC 結構實現 O(log n) 的證明搜尋效率。

---

## 6. FLCoin：滑動視窗委員會選舉

**S. Ren, E. Kim, and C. Lee, "A scalable blockchain-enabled federated learning architecture for edge computing," PLOS ONE, vol. 19, no. 8, e0308991, Aug. 2024.**

**系統架構**：**雙層區塊鏈架構**——更新區塊儲存本地模型資訊，模型區塊儲存聚合後的全域參數。另有身份鏈管理節點。

**共識機制**：採用 **優化的委員會式 BFT**，具備 fast 與 backup 兩種協議。選擇理由為固定大小的滑動視窗（s=50-100）決定委員會，無論網路總規模，通訊複雜度維持 **線性 O(n)**，相較 PBFT 的 O(n²) 減少 90% 開銷。共識延遲在 500 節點時仍 **低於 3 秒**。

**Stake 機制**：節點透過提交有效更新區塊獲得委員會「份額」，滑動視窗內持有份額的節點組成當輪委員會。**貢獻值 C_k = α × |D_k|**（依訓練資料集大小加權），貢獻值最高者擔任委員會領導者。獎勵依貢獻值比例分配。

**驗證方式**：**兩步驗證**——(1) 誠實訓練檢查：比對資料集大小與訓練時間是否合理；(2) 準確度檢查：委員會成員以自身資料測試更新。區塊標頭與 2/3 委員會簽名 **儲存於鏈上**，模型區塊本體 **儲存於鏈下**（分散式儲存）。

---

## 演進脈絡總結

| 年份 | 系統 | 共識機制 | 驗證方式 | 關鍵演進 |
|------|------|----------|----------|----------|
| 2020 | BlockFL | PoW | 全節點/鏈上 | 首創 BCFL 架構 |
| 2020 | Lu et al. | PoQ | 兩階段/鏈上 | 共識即訓練驗證 |
| 2021 | BFLC | 委員會 BFT | 委員會/鏈上 | 降低共識開銷 |
| 2021 | VBFL | PoS 啟發 | 投票/鏈上 | 貢獻對齊權重 |
| 2022 | VFChain | 委員會+DSC | 證明/鏈上 | 可審計性 |
| 2024 | FLCoin | 優化 BFT | 兩步/混合 | 線性擴展性 |

BCFL 領域從早期 PoW 的高能耗全節點驗證，演進至委員會共識與混合儲存架構，逐步解決 **擴展性瓶頸**。Stake-based participation 將參與權重與獎勵分配綁定 FL 貢獻，建立正向激勵循環。此技術基礎為後續章節討論 Layer-2 方案與經濟漏洞提供脈絡。