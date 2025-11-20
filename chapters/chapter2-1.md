# 第二章 背景知識

## 2.1 聯邦學習基礎

### 2.1.1 聯邦學習定義與數學模型

聯邦學習（Federated Learning, FL）是一種分散式機器學習範式，允許多個參與者在不共享原始數據的情況下協同訓練模型。相較於傳統的集中式學習，聯邦學習將訓練過程分散到各個客戶端，每個客戶端在本地私有數據集上執行訓練，僅將模型更新（如梯度或參數）上傳至聚合器，從而實現數據隱私保護與分散式訓練的結合[1]。

**數學框架**

聯邦學習的核心目標是最小化全局損失函數。假設系統中有 K 個客戶端，每個客戶端 k 擁有本地數據集 $\mathcal{D}_k$，數據量為 $n_k$，總數據量為 $n = \sum_{k=1}^{K} n_k$。聯邦學習的優化目標可表示為：

$$\min_{w} F(w) = \sum_{k=1}^{K} \frac{n_k}{n} F_k(w)$$

其中 $w$ 為全局模型參數，$F_k(w)$ 為客戶端 k 的本地損失函數：

$$F_k(w) = \frac{1}{n_k} \sum_{i \in \mathcal{D}_k} \ell(w; x_i, y_i)$$

其中 $\ell(\cdot)$ 為損失函數，$(x_i, y_i)$ 為訓練樣本。此框架將全局目標分解為各客戶端的局部目標，並以數據量作為加權係數，確保訓練過程反映整體數據分布。

**聯邦學習訓練流程**

如圖 2.1 所示，聯邦學習的基本流程包括四個主要階段：(1) 聚合器初始化全局模型並廣播給所有客戶端；(2) 各客戶端在本地數據上並行訓練模型，計算模型更新（梯度或參數差異）；(3) 客戶端將本地更新上傳至聚合器（可選擇性上傳至去中心化儲存如 IPFS）；(4) 聚合器收集所有更新後執行聚合算法，計算新的全局模型並開始下一輪訓練。此循環過程持續 R 輪直至模型收斂。

[圖 2.1：聯邦學習訓練流程圖]
<!-- 圖示應包含：
- K 個客戶端節點
- 聚合器節點
- 可選的 IPFS 儲存層
- 模型分發與更新收集的雙向箭頭
- 訓練循環的流程指示 -->

**FedAvg 聚合算法**

McMahan 等人於 2017 年提出的聯邦平均（Federated Averaging, FedAvg）算法[1]是聯邦學習領域的基礎算法。該算法在每個訓練輪次中，由聚合器協調各客戶端執行本地訓練，隨後收集並聚合模型更新以生成新的全局模型。FedAvg 的工作流程如下：

```
演算法 1: 聯邦平均算法 (FedAvg)
輸入: 全局模型參數 w_0, 訓練輪數 R, 客戶端數 K, 本地訓練輪次 E, 學習率 η
輸出: 全局模型參數 w_R

1: 伺服器初始化: w_0
2: for 每個訓練輪次 r = 1, 2, ..., R do
3:     伺服器將當前全局模型 w_{r-1} 分發給所有客戶端
4:     for 每個客戶端 k = 1, 2, ..., K (並行執行) do
5:         w_k^{r,0} ← w_{r-1}  // 初始化本地模型
6:         for 本地訓練輪次 e = 1, 2, ..., E do
7:             w_k^{r,e} ← w_k^{r,e-1} - η ∇F_k(w_k^{r,e-1})  // 本地梯度下降
8:         end for
9:         將本地更新 Δw_k = w_k^{r,E} - w_{r-1} 上傳至伺服器
10:    end for
11:    伺服器執行加權聚合:
12:        w_r ← w_{r-1} + \sum_{k=1}^{K} \frac{n_k}{n} Δw_k
13: end for
14: return w_R
```

該算法的計算複雜度主要由本地訓練和聚合兩部分構成。客戶端的本地訓練複雜度為 $O(E \cdot n_k \cdot d)$，其中 d 為模型維度；聚合器的聚合複雜度為 $O(K \cdot d)$。FedAvg 通過在客戶端執行多輪本地訓練（E > 1），顯著減少了通訊輪數，從而降低了整體通訊成本。

**聚合算法的多樣性**

雖然 FedAvg 是最基礎的聚合算法，但實際應用中存在多種聚合算法，以應對不同的場景需求與挑戰。這些算法在計算複雜度、記憶體需求和魯棒性方面存在顯著差異：

1. **FedProx**[2]：在 FedAvg 基礎上添加近端項（proximal term），通過正則化約束本地更新偏離全局模型的程度，適用於非獨立同分布（Non-IID）場景。其優化目標為 $\min_{w} F_k(w) + \frac{\mu}{2} \|w - w_{r-1}\|^2$，其中 μ 為近端項係數。

2. **Krum**[3]：一種拜占庭魯棒聚合算法，通過計算各客戶端更新之間的歐幾里得距離，選擇與其他更新最接近的模型。計算複雜度為 $O(K^2 \cdot d)$，其中需要計算所有更新對之間的距離，對於大規模系統而言計算開銷較高。

3. **Median**：對模型參數的每個維度取中位數，具有天然的魯棒性，可抵禦離群值攻擊。計算複雜度為 $O(K \cdot d \log K)$，主要開銷來自於對每個維度進行排序操作。

4. **Trimmed Mean**：對模型參數的每個維度移除最大和最小的 β 比例值後取平均，平衡了計算效率與魯棒性。計算複雜度為 $O(K \cdot d \log K)$。

5. **FedAdam/FedYogi**[4]：將自適應優化器（如 Adam、Yogi）應用於聯邦學習，在伺服器端維護動量和自適應學習率，提升非獨立同分布（Non-IID）數據場景下的收斂速度，但需要額外的記憶體存儲優化器狀態。

不同聚合算法的選擇對系統設計有重要影響。簡單的加權平均（如 FedAvg）計算效率高但缺乏魯棒性；拜占庭魯棒算法（如 Krum、Median）能抵禦惡意更新但計算複雜度顯著增加；自適應算法（如 FedAdam）提升收斂性能但需要更多記憶體資源。這種多樣性在系統設計與安全性分析中具有重要意義。

### 2.1.2 聚合器的角色與責任

在聯邦學習系統中，聚合器（Aggregator）扮演著協調者與計算者的雙重角色。其主要職責包括：(1) 收集各客戶端上傳的本地模型更新；(2) 執行聚合算法計算新的全局模型；(3) 將更新後的全局模型分發給各客戶端。聚合器的設計直接影響系統的效率、安全性與可擴展性[5]。

**聚合器的核心責任**

聚合器的工作流程可分為三個階段：

1. **模型更新收集**：在每個訓練輪次開始時，聚合器等待各客戶端完成本地訓練並上傳模型更新。此階段的通訊複雜度為 $O(K)$，其中 K 為參與客戶端數量。

2. **聚合算法執行**：聚合器根據選定的聚合算法（如 FedAvg、Krum 等）計算新的全局模型。如前所述，不同算法的計算複雜度差異顯著，從 $O(K \cdot d)$ 到 $O(K^2 \cdot d)$ 不等。這一階段強調了聚合器必須具備足夠的計算能力以執行選定的聚合算法。

3. **模型分發**：聚合器將新的全局模型廣播給所有客戶端，啟動下一輪訓練。此階段的通訊複雜度同樣為 $O(K)$。

需要特別指出的是，聚合器不僅是模型參數的「傳遞者」，更是聚合算法的「執行者」。不同的聚合算法對聚合器的計算能力、記憶體容量和執行環境有不同的要求。例如，執行 Krum 算法需要計算並存儲 $O(K^2)$ 個距離值；執行帶有正則化的 FedProx 需要支援優化求解器；執行需要排序的 Median 或 Trimmed Mean 需要支援高效的排序操作。因此，聚合器的「計算通用性」（即支援任意聚合算法的能力）是系統設計的關鍵考量。

**單聚合器架構的問題**

傳統聯邦學習系統採用單一聚合器架構，存在單點故障（SPOF）、計算瓶頸、安全風險和可擴展性受限等根本性缺陷[5][6]。單一聚合器的故障會導致整個訓練中斷，且隨著參與節點數量增加，聚合器的計算壓力與通訊開銷呈線性增長，成為系統性能瓶頸。此外，單聚合器模式缺乏拜占庭容錯能力，無法檢測和防禦惡意聚合結果。

**多聚合器的設計動機**

為解決單聚合器架構的根本性缺陷，研究者提出多聚合器（Multi-Aggregator）設計，其核心動機包括：

1. **負載分散**：將聚合任務分散到 N 個聚合器上，每個聚合器僅需負責 $R/N$ 次聚合運算，計算負擔降低 N 倍。這種負載分散機制不僅減輕了單個節點的壓力，也提升了系統的整體計算效率。

2. **容錯能力增強**：多聚合器架構中，單一聚合器的故障不會導致系統完全停止。系統可以通過輪替機制繞過故障節點，或通過冗餘設計確保訓練過程的持續性。

3. **去信任化**：在多聚合器環境下，不再需要完全信任單一中央伺服器。通過引入驗證機制和共識協議，系統可以檢測並排除惡意聚合器，實現去中心化的安全保障。

**引出共識機制的需求**

然而，多聚合器架構需要一種協調機制來驗證聚合結果的正確性並在分散式環境下達成一致性。這正是區塊鏈技術中的拜占庭容錯共識協議（如 PBFT）和樂觀執行機制（如 Optimistic Rollup）被引入聯邦學習領域的根本原因。本章後續章節將詳細介紹這些共識機制的技術原理。

---

## 參考文獻

[1] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, "Communication-efficient learning of deep networks from decentralized data," in *Proc. Int. Conf. Artificial Intelligence and Statistics (AISTATS)*, Fort Lauderdale, FL, USA, 2017, pp. 1273-1282.

[2] T. Li, A. K. Sahu, M. Zaheer, M. Sanjabi, A. Talwalkar, and V. Smith, "Federated optimization in heterogeneous networks," in *Proc. Machine Learning and Systems (MLSys)*, 2020, pp. 429-450.

[3] P. Blanchard, E. M. El Mhamdi, R. Guerraoui, and J. Stainer, "Machine learning with adversaries: Byzantine tolerant gradient descent," in *Proc. Advances in Neural Information Processing Systems (NeurIPS)*, 2017, pp. 119-129.

[4] S. J. Reddi, Z. Charles, M. Zaheer, Z. Garrett, K. Rush, J. Konečný, S. Kumar, and H. B. McMahan, "Adaptive federated optimization," in *Proc. Int. Conf. Learning Representations (ICLR)*, 2021.

[5] T. Li, A. K. Sahu, A. Talwalkar, and V. Smith, "Federated learning: Challenges, methods, and future directions," *IEEE Signal Process. Mag.*, vol. 37, no. 3, pp. 50-60, May 2020.

[6] Y. Zhou, Y. Chen, and S. Guo, "A blockchain-empowered multiaggregator federated learning architecture in edge computing," *IEEE Trans. Comput. Soc. Syst.*, early access, 2024.
