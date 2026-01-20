# 區塊鏈聯邦學習驗證機制的相關研究

現有區塊鏈聯邦學習(BCFL)驗證方法可分為兩大類:基於密碼學證明的驗證方法與基於委員會的共識方法。前者追求數學上可證明的正確性但面臨嚴重的效能瓶頸,後者透過經濟激勵達成共識但依賴誠實多數假設。本節系統性分析這些方法的技術原理、效能數據與固有局限,以定位本研究的貢獻。

## 基於驗證的方法:zkML 的計算瓶頸

零知識機器學習(zkML)透過將 ML 計算轉換為算術電路,使驗證者無需重新執行即可確認計算正確性 [1]。其技術堆疊包括 Groth16(證明大小最小,約 **200 bytes**)、PLONK(通用可更新設置)與 zk-STARK(無需信任設置,具量子抗性)[2]。轉換過程需經歷三階段:首先將浮點數量化為有限域整數,接著將每個運算分解為多項式約束,最後生成密碼學證明。

然而,約束數量隨模型複雜度急劇膨脹。根據 ZEN 編譯器的基準測試 [3],ShallowNet-MNIST 需要 **4.31M** 個約束,而 LeNet-Face-large-ORL 則暴增至 **263M** 個約束。Chen 等人在 EuroSys 2024 的實驗顯示 [1],ResNet-18 的證明生成需 **52.9 秒**,VGG16 需 **637 秒**,DistillGPT-2 更高達 **3,651 秒**(約一小時),且需要 **1TB RAM** 的高規格硬體。框架效能差異顯著:ezkl 比 RISC Zero 快 **65.88 倍**,記憶體使用減少 **98.13%** [4]。

zkML 的核心局限在於難以支援拜占庭容錯聚合演算法。Krum 與 Multi-Krum 需計算所有客戶端更新間的成對距離,產生 O(n²·d) 的約束爆炸;排序與中位數運算在零知識電路中極度昂貴。現有 zkFL 方案如 RiseFL [5] 僅支援 L2-norm 有效性檢查,將密碼學成本從 O(d) 降至 O(d/log d),但仍無法實現完整的距離計算。與本研究相比,zkML 提供密碼學安全性但犧牲了聚合演算法的通用性,而本研究透過委員會機制在保持演算法靈活性的同時達成可驗證性。

## 基於驗證的方法:opML 的架構限制

樂觀機器學習(opML)採用「預設正確」的執行模式,僅在爭議發生時才啟動驗證 [6]。其運作流程為:服務提供者於鏈下執行 ML 推論並提交結果,驗證者在挑戰期內可發起欺詐證明,透過二分協議(Bisection Protocol)逐步縮小爭議範圍至單一計算步驟,最終由 FPVM(欺詐證明虛擬機)在鏈上仲裁。ORA Protocol 是首個開源 opML 實現,支援 LLaMA 2 等 **7B+ 參數**模型直接於以太坊運行 [7]。

挑戰期設計反映安全性與效率的權衡。Optimism 採用 **7 天**、Arbitrum 採用 **6.4 天**的挑戰期 [8],以確保驗證者有充足時間偵測並提交欺詐證明,同時容納網路延遲、時區差異與潛在的共識失效。然而,這種設計與 FL 訓練動態根本衝突——聯邦學習需要快速迭代更新與聚合,每輪等待 7 天驗證將使訓練完全不可行。

opML 的 AnyTrust 假設(「至少一個誠實驗證者」)與 BCFL 的需求存在本質差異。opML 設計為單一提交者與單一挑戰者間的兩方爭議,而非多方參與者間的共識達成。FPVM 的記憶體限制需採用延遲載入設計,當 FL 模型涉及大量參與者更新時可能超出實際限制。此外,opML 假設「數據與模型非敏感」,與 FL 的隱私保護需求相悖。雖然 opp/ai 透過整合 zkML 元件增強隱私,但仍維持單一證明者架構,無法滿足多驗證者場景需求。

## 基於委員會的方法:FLCoin 的滑動窗口機制

FLCoin 提出基於滑動窗口的動態委員會選舉機制 [9],將聯邦學習過程本身作為委員會成員資格的依據。每個有效更新區塊代表一個委員會成員份額,窗口大小固定為 s,隨新區塊附加而滑動更新。節點的貢獻值計算為 C_k = α × |D_k|,其中 α 為預定義係數,|D_k| 為訓練數據規模;貢獻值最高者成為委員會領導者。

拜占庭安全機率透過超幾何分佈計算:P[X ≤ s/3] 表示窗口內惡意節點數不超過容錯閾值的機率。在網路規模 n=500、惡意節點比例 ≤25%、窗口大小 s=100 的條件下,安全機率達 **98.4%**;s=150 時提升至 99.8%,s=50 時降至 91.3% [9]。驗證採用兩步驟:誠實訓練檢查(驗證訓練時間與算力的一致性)與準確度檢查(委員會成員使用本地數據驗證模型品質)。

效能方面,FLCoin 相較 PBFT 實現通訊開銷降低 **90%**、訓練時間縮短 **35%**。在 100 節點配置下,共識延遲僅 **3.05 秒**(PBFT 為 25.11 秒),且隨網路規模擴大保持穩定 [9]。然而,FLCoin 未明確處理長期權益累積風險——惡意節點可透過持續參與逐步增加委員會影響力。身份鏈依賴「預定義的可信管理者群組」,引入中心化風險。論文亦承認實驗假設無惡意節點,未驗證對抗性累積策略的防禦效果。

## 基於委員會的方法:BlockDFL 的權益加權選舉

BlockDFL 採用完全去中心化的點對點架構 [10],透過最新區塊雜湊值與權益加權實現委員會選舉的隨機性與可驗證性。系統定義三種角色:更新提供者(UP)負責本地訓練、聚合者負責收集與篩選更新、驗證者透過 PBFT 投票達成共識。其核心假設為「持有大量權益的參與者傾向誠實行為,因為他們能從貨幣獎勵中獲益更多」。

BlockDFL 採用兩層評分機制:第一層由聚合者透過本地推論評估更新品質並篩選;第二層由驗證者使用 **Krum 演算法**過濾異常值。這使系統能容忍 **40% 惡意參與者**,優於多數現有框架的 30% 閾值 [10]。獎勵連鎖機制將權益均等分配給被選中全局更新的聚合者、更新提供者與支持驗證者,區塊內容完整記錄所有獲獎身份。

與 FLCoin 的關鍵差異在於選舉基礎:BlockDFL 依賴經濟權益,FLCoin 依賴 FL 貢獻歷史。這產生不同的安全特性——BlockDFL 在對手取得 >50% 權益、協調 >40% 惡意節點、或願意犧牲權益發動攻擊時失效。後者尤其值得關注:國家級攻擊者或競爭對手可能接受經濟損失以達成外部目標。此外,Sybil 攻擊者可跨多重身份逐步累積權益,最終達成多數影響力。

## 基於委員會的方法:BFLC 與其他方案

BFLC 開創性地將委員會共識引入 BCFL [11],採用雙區塊儲存設計:模型區塊儲存聚合後的全局模型,更新區塊儲存經驗證的本地梯度。每輪約 **40% 活躍節點**被選為下輪委員會成員,透過 K-fold 交叉驗證評估提交更新的品質。實驗於 FISCO 區塊鏈系統上進行,使用 FEMNIST 數據集與 AlexNet 模型,證明在正常與對抗場景下均維持較高準確度。

然而,BFLC 的聲譽機制存在冷啟動問題——新節點缺乏歷史數據建立信任,使惡意節點易於滲透委員會。當惡意節點佔據 50% 委員會席位時攻擊即可成功。後續研究指出 BFLC「易受惡意節點混入委員會的影響」[10],且委員會共識機制可能導致節點間大量通訊開銷。

VBFL 提出 PoS 啟發的去中心化驗證機制 [12],個別驗證者使用準確度差異(VAD)指標評估更新品質,連續多輪被識別為惡意的裝置將被列入黑名單。實驗顯示在 15% 惡意裝置下達 **87% 準確度**,比 Vanilla FL 高 **7.4 倍**。VFChain 則首創結合可驗證性與可審計性的框架 [13],其雙跳鏈(DSC)數據結構支援高效的委員會輪換搜尋與歷史追溯。這些方案共同面臨 50% 拜占庭閾值限制與資源受限裝置的驗證計算負擔。

## 現有方法的系統性局限分析

綜合分析揭示現有方法在「安全性-效率-通用性」三維度上的 Pareto 前沿權衡。zkML 提供最強的密碼學安全性(無需信任假設),但證明生成時間與模型規模呈超線性增長,且無法支援 Krum 等複雜聚合;opML 透過經濟激勵大幅降低計算成本,但 7 天挑戰期與單一證明者架構使其不適用於多驗證者 FL 場景。委員會方法在效率與實用性間取得平衡,但均依賴某種形式的誠實多數假設——無論是 FLCoin 的 25% 資源閾值、BlockDFL 的 50% 權益閾值,或 BFLC 的 50% 委員會閾值。

| 方案 | 安全性保證 | 效率 (典型延遲) | 聚合通用性 |
|------|-----------|----------------|-----------|
| zkML | 密碼學證明 | 分鐘至小時 | 僅 FedAvg |
| opML | 經濟安全 (AnyTrust) | 7 天挑戰期 | 受 FPVM 限制 |
| FLCoin | 98.4% 機率 (s=100) | 3.05 秒共識 | 支援 |
| BlockDFL | 40% 容錯 | &lt;3 秒驗證 | 支援 Krum |
| BFLC | 50% 委員會閾值 | 中等 | 支援 |

更關鍵的是,所有委員會方案均未充分處理**長期權益累積**導致的委員會滲透風險。FLCoin 的滑動窗口基於即時貢獻而非累積權益,但未建立權益衰減機制;BlockDFL 的權益直接影響選舉機率,惡意方可透過長期參與逐步控制系統。這揭示了現有研究的核心缺口:靜態的安全性分析假設對手資源固定,忽略了對手策略性累積影響力的動態過程。

## 研究缺口與本研究定位

本節分析揭示三個核心研究缺口:首先,**缺乏動態安全性分析**——現有方案採用靜態機率模型(如超幾何分佈)假設對手比例固定,未考慮對手透過持續參與累積委員會影響力的攻擊向量。其次,**驗證效率與通用性的矛盾**——zkML 犧牲演算法通用性換取密碼學安全,委員會方法犧牲強安全性換取效率,尚無方案同時達成兩者。第三,**缺乏抗累積攻擊機制**——無論基於貢獻(FLCoin)或權益(BlockDFL)的選舉,均未內建防止長期滲透的設計。

本研究透過引入時間衰減權益函數與動態委員會輪換策略,旨在填補上述缺口。相較於 FLCoin 的靜態滑動窗口,本研究的機制考量歷史權益的時間加權衰減,降低早期參與者的長期優勢;相較於 BlockDFL 的純權益加權,本研究結合即時貢獻與衰減權益,平衡經濟激勵與抗累積需求。這使本研究能在維持 >98% 拜占庭安全機率的同時,將長期滲透攻擊的成功機率降低至可接受範圍。

---

**參考文獻**

[1] B.-J. Chen, S. Waiwitlikhit, I. Stoica, and D. Kang, "ZKML: An optimizing system for ML inference in zero-knowledge proofs," in *Proc. EuroSys*, 2024, pp. 1-16.

[2] A. Gabizon et al., "PLONK: Permutations over lagrange-bases for oecumenical noninteractive arguments of knowledge," *Cryptology ePrint Archive*, 2019.

[3] B. Feng et al., "ZEN: An optimizing compiler for verifiable, zero-knowledge neural network inferences," *Cryptology ePrint Archive*, 2021.

[4] EZKL, "Benchmarking ZKML frameworks," EZKL Blog, Jan. 2024.

[5] H. Xiao et al., "Secure and verifiable data collaboration with low-cost zero-knowledge proofs," in *Proc. VLDB*, 2024.

[6] K. D. Conway et al., "opML: Optimistic machine learning on blockchain," arXiv:2401.17555, 2024.

[7] ORA Protocol, "opML documentation," docs.ora.io, 2024.

[8] Optimism Foundation, "Rollup protocol overview," docs.optimism.io, 2024.

[9] S. Ren, E. Kim, and C. Lee, "A scalable blockchain-enabled federated learning architecture for edge computing," *PLOS ONE*, vol. 19, no. 8, e0308991, 2024.

[10] Z. Qin et al., "BlockDFL: A blockchain-based fully decentralized peer-to-peer federated learning framework," in *Proc. WWW*, 2024.

[11] Y. Li et al., "A blockchain-based decentralized federated learning framework with committee consensus," *IEEE Network*, vol. 35, no. 1, pp. 234-241, 2021.

[12] H. Chen et al., "Robust blockchained federated learning with model validation and proof-of-stake inspired consensus," arXiv:2101.03300, 2021.

[13] Z. Peng et al., "VFChain: Enabling verifiable and auditable federated learning via blockchain systems," *IEEE Trans. Netw. Sci. Eng.*, vol. 9, no. 1, pp. 173-186, 2022.