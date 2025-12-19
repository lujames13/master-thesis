# 聯邦學習與拜占庭容錯文獻綜述

## II.A 聯邦學習基礎架構與拜占庭威脅

**聯邦學習（Federated Learning）** 由 McMahan 等人於 2017 年正式提出，其核心目標為在保持訓練資料分散於各用戶端設備的前提下，協同訓練高品質的全域模型。此架構定義的優化問題為：

$$\min_{w} F(w) = \sum_{k=1}^{K} \frac{n_k}{n} F_k(w)$$

其中 $K$ 為參與客戶端總數，$n_k$ 為第 $k$ 個客戶端的本地樣本數，$F_k(w)$ 為其本地損失函數。**FederatedAveraging (FedAvg)** 演算法透過週期性聚合各客戶端的本地模型更新 $w_{t+1} \leftarrow \sum_k \frac{n_k}{n} w_{t+1}^k$，相較於同步 SGD 可減少 **10-100 倍**通訊開銷。

---

### 文獻 1：FedAvg 聯邦學習基礎

**[1]** H. B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, "Communication-Efficient Learning of Deep Networks from Decentralized Data," in *Proc. AISTATS*, 2017, pp. 1273-1282.

**核心貢獻：** 首次提出聯邦學習框架，建立客戶端-伺服器架構的數學定義與 FedAvg 聚合演算法，成為後續所有聯邦學習研究的基礎。

**關鍵假設：** 假設中央聚合器（aggregator）誠實執行加權平均聚合；未討論惡意客戶端或拜占庭容錯機制。

**相關性標籤：** [FOUNDATIONAL]

---

## 拜占庭容錯於分散式機器學習之定義

在分散式機器學習語境中，**拜占庭故障（Byzantine fault）** 指參與者可發送任意、潛在惡意的梯度向量，並可能與其他拜占庭節點協同攻擊。Blanchard 等人定義：*「拜占庭故障包含軟體錯誤、網路非同步、本地資料偏差，以及試圖破壞整體系統的攻擊者。」* 相較於傳統分散式系統僅考慮節點崩潰或訊息遺失，ML 領域的拜占庭威脅更為複雜，因攻擊者可針對模型收斂方向進行精準操控。

---

### 文獻 2：Krum 拜占庭容錯梯度下降

**[2]** P. Blanchard, E. M. El Mhamdi, R. Guerraoui, and J. Stainer, "Machine Learning with Adversaries: Byzantine Tolerant Gradient Descent," in *Advances in NeurIPS*, 2017, pp. 118-128.

**核心貢獻：** 首個可證明拜占庭容錯的分散式 SGD 演算法。證明**線性聚合規則（包括平均）無法容忍任何拜占庭故障**，並提出 Krum 選擇機制。

**數學定義 - Krum 分數函數：**
$$s(V_i) = \sum_{i \rightarrow j} ||V_i - V_j||^2$$

其中 $i \rightarrow j$ 表示 $V_j$ 為距離 $V_i$ 最近的 $n-f-2$ 個向量之一。Krum 輸出為分數最低之梯度向量。

**關鍵假設：** (1) **誠實聚合器假設**：參數伺服器必須正確實作 Krum 規則；(2) 需 $n \geq 2f+3$ 個工作節點以容忍 $f$ 個拜占庭節點；(3) **IID 資料分布假設**。

**相關性標籤：** [DEFENSE]

---

### 文獻 3：統計最優拜占庭容錯分散式學習

**[3]** D. Yin, Y. Chen, R. Kannan, and P. Bartlett, "Byzantine-Robust Distributed Learning: Towards Optimal Statistical Rates," in *Proc. ICML*, 2018, pp. 5650-5659.

**核心貢獻：** 首個針對拜占庭容錯分散式學習的精確統計分析，證明座標中位數與裁剪平均達到**階數最優統計誤差率**。

**數學定義 - 座標裁剪平均：**
$$G[j] = \frac{1}{n-2\lfloor\beta n\rfloor} \sum_{i=\lfloor\beta n\rfloor+1}^{n-\lfloor\beta n\rfloor} g_{(i)}[j]$$

其中 $\beta$ 為裁剪比例，去除最大與最小 $\beta$ 比例的座標值後取平均。

**關鍵假設：** (1) **誠實中央伺服器**執行座標運算；(2) 裁剪平均容忍 $f < \beta n$ 個拜占庭節點；(3) **IID 資料分布與亞高斯梯度假設**。

**相關性標籤：** [DEFENSE]

---

## 聯邦學習中的拜占庭攻擊類型

聯邦學習面臨的拜占庭威脅主要分為三類：**模型投毒攻擊**（直接操控模型權重）、**梯度攻擊**（符號翻轉、縮放攻擊）、以及**後門攻擊**（注入特定觸發器的惡意行為）。

---

### 文獻 4：對抗視角分析聯邦學習

**[4]** A. N. Bhagoji, S. Chakraborty, P. Mittal, and S. Calo, "Analyzing Federated Learning through an Adversarial Lens," in *Proc. ICML*, 2019, pp. 634-643.

**核心貢獻：** 正式引入**模型投毒（model poisoning）** 概念，證明其比資料投毒更具威脅性。提出顯式增強（explicit boosting）與隱蔽攻擊策略。

**威脅模型：** 單一非共謀惡意代理，可存取自身本地資料與當前全域模型，透過縮放攻擊更新 $\delta_{malicious} = \gamma \times (w_{malicious} - w_{global})$ 以主導聚合結果。

**關鍵發現：** 拜占庭容錯聚合策略（Krum、座標中位數）**對目標模型投毒攻擊不具魯棒性**。

**相關性標籤：** [ATTACK]

---

### 文獻 5：針對拜占庭容錯聯邦學習的本地模型投毒攻擊

**[5]** M. Fang, X. Cao, J. Jia, and N. Z. Gong, "Local Model Poisoning Attacks to Byzantine-Robust Federated Learning," in *Proc. USENIX Security*, 2020, pp. 1623-1640.

**核心貢獻：** 首個系統性研究針對拜占庭容錯聯邦學習的本地模型投毒攻擊。將攻擊形式化為優化問題，針對 Krum、裁剪平均、中位數等防禦機制設計專屬攻擊。

**關鍵發現：** 攻擊可將 MNIST 錯誤率從 <10% 提升至 >75%，證明**拜占庭容錯聚合提供虛假的安全保障**。Non-IID 資料使攻擊更有效，因難以區分惡意與合法的異質更新。

**相關性標籤：** [ATTACK]

---

### 文獻 6：如何後門聯邦學習

**[6]** E. Bagdasaryan, A. Veit, Y. Hua, D. Estrin, and V. Shmatikov, "How To Backdoor Federated Learning," in *Proc. AISTATS*, 2020, pp. 2938-2948.

**核心貢獻：** 提出**模型替換攻擊（model replacement attack）**，單一惡意參與者可在一輪內完全替換全域模型為後門版本，達成 **100% 後門任務準確率**。

**關鍵發現：** **安全聚合為雙面刃**：保護隱私的同時阻止聚合器檢測異常貢獻，使後門注入更加隱蔽。

**相關性標籤：** [ATTACK]

---

## 誠實聚合器假設之關鍵限制

上述所有拜占庭容錯防禦方法均隱含**誠實中央聚合器假設**，即假設參數伺服器將正確實作魯棒聚合規則。此假設構成聯邦學習的**單點故障（single point of failure）**：若聚合器本身被惡意控制，則所有防禦機制失效。

---

### 文獻 7：Bulyan 高維拜占庭容錯

**[7]** E. M. El Mhamdi, R. Guerraoui, and S. Rouault, "The Hidden Vulnerability of Distributed Learning in Byzantium," in *Proc. ICML*, 2018, pp. 3521-3530.

**核心貢獻：** 揭露現有拜占庭容錯方案在高維度下存在 $\Omega(\sqrt{d})$ 的投毒邊界，並提出 Bulyan 將攻擊者餘地縮減至 $O(1/\sqrt{d})$。

**關鍵假設：** 明確採用「1 master + n workers」架構，**假設 master 誠實執行聚合**。需 $n \geq 4f+3$ 個工作節點。

**相關性標籤：** [THEORY]

---

### 文獻 8：拜占庭容錯去中心化聯邦學習

**[8]** M. Fang, Z. Zhang, H. , P. Khanduri, J. Liu, S. Lu, Y. Liu, and N. Gong, "Byzantine-Robust Decentralized Federated Learning," in *Proc. ACM CCS*, 2024.

**核心貢獻：** 明確指出傳統聯邦學習架構存在**「信任依賴問題（trust dependency issues）」** 與通訊瓶頸，提出完全去中心化架構消除單一信任點。

**對聚合器信任問題的處理：** 透過對等網路拓撲實現無伺服器協同訓練，在不依賴誠實聚合器的前提下達成拜占庭容錯。

**相關性標籤：** [DEFENSE]

---

## 總結：研究缺口

現有拜占庭容錯聯邦學習文獻主要關注**惡意客戶端攻擊**情境，而**聚合器本身為惡意**的威脅模型尚未獲得充分研究。當中央聚合器被攻陷時，Krum、裁剪平均等防禦機制將完全失效，此為本研究欲填補之關鍵缺口。