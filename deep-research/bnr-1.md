# Section 2.1 聯邦式學習基礎 (Federated Learning Fundamentals)

聯邦學習是一種革命性的分散式機器學習典範，其核心創新在於實現「資料不動、模型動」的訓練機制。本節從聯邦學習的起源出發，建立完整的數學框架，深入分析 FedAvg 演算法，並探討其面臨的安全挑戰，為後續章節的區塊鏈整合研究奠定理論基礎。

## 2.1.1 聯邦學習的起源與動機

聯邦學習的概念最早由 Google 於 2017 年正式提出，其動機源於一個關鍵矛盾：現代行動裝置擁有豐富的訓練資料，但這些資料往往具有高度隱私敏感性或資料量龐大，傳統集中式訓練方法不適用 [1]。McMahan 等人在原始論文中明確指出，聯邦學習的設計目標是「將模型訓練與直接存取原始訓練資料的需求解耦」，這體現了**資料最小化原則**（Data Minimization Principle）的核心精神。

**Google Gboard 鍵盤預測**是聯邦學習最具代表性的應用案例。在此應用中，使用者的打字習慣、輸入內容等高度敏感資料完全保留在本地裝置，僅有模型更新以加密形式上傳至雲端進行聚合。Google 報告指出，此系統已部署超過**二十種語言模型**，服務數百萬活躍用戶，實現了下一詞預測、表情符號推薦等功能的持續優化 [1]。值得注意的是，本地訓練僅在裝置閒置、充電中且連接免費 Wi-Fi 時執行，確保對使用者體驗零影響。

聯邦學習與傳統分散式機器學習（如 Parameter Server 架構）存在本質差異。Parameter Server 假設資料為**獨立同分布（IID）**且集中存儲於資料中心，主要目標是透過平行化加速計算。相比之下，聯邦學習面對的是本質上**非獨立同分布（Non-IID）**的資料分布，且資料永遠不離開終端裝置 [1]。McMahan 等人歸納了聯邦優化問題的四大特性：(1) Non-IID：每個使用者的本地資料不代表整體分布；(2) Unbalanced：不同使用者的資料量差異懸殊；(3) Massively Distributed：客戶端數量遠超每個客戶端的樣本數；(4) Limited Communication：裝置經常離線或處於低頻寬環境。這些特性使聯邦學習成為一個獨特的優化問題類別，需要專門的演算法設計 [2]。

從產業背景來看，**資料孤島（Data Silos）**問題日益嚴峻——醫療產業產生全球超過 30% 的資料，但多數資訊仍被鎖在組織邊界內。聯邦學習的出現恰逢歐盟《一般資料保護規則》（GDPR）於 2018 年生效，該法規對違規處理個人資料的企業處以最高全球年營業額 4% 或兩千萬歐元的罰款。聯邦學習「訓練資料不離開裝置」的架構設計，天然符合 GDPR 的同意機制、被遺忘權及資料最小化等要求 [2]。

## 2.1.2 數學框架與優化目標

聯邦學習的優化問題可形式化為一個加權有限和目標函數。設系統中共有 $K$ 個客戶端，第 $k$ 個客戶端擁有 $n_k$ 個訓練樣本，總樣本數為 $n = \sum_{k=1}^{K} n_k$。全域優化目標定義為：

$$\min_{w \in \mathbb{R}^d} F(w) = \sum_{k=1}^{K} \frac{n_k}{n} F_k(w)$$

其中 $w \in \mathbb{R}^d$ 為 $d$ 維模型參數，$F_k(w)$ 為第 $k$ 個客戶端的本地目標函數 [1]。本地目標函數定義為該客戶端資料上的經驗風險：

$$F_k(w) = \frac{1}{n_k} \sum_{i \in \mathcal{P}_k} \ell(w; x_i, y_i)$$

其中 $\mathcal{P}_k$ 為客戶端 $k$ 持有的資料索引集合，$\ell(w; x_i, y_i)$ 為模型在樣本 $(x_i, y_i)$ 上的損失函數。

**加權係數 $p_k = n_k/n$ 的理論依據**在於確保每個訓練樣本對全域目標的貢獻相等，無論該樣本位於哪個客戶端。若資料分布滿足 IID 假設（即 $\mathcal{P}_k$ 為從總體資料隨機均勻抽樣形成），則有 $\mathbb{E}_{\mathcal{P}_k}[F_k(w)] = F(w)$，此時本地優化等價於全域優化 [3]。

然而實際應用中，**Non-IID 資料分布**才是常態。Kairouz 等人 [2] 系統性地歸納了五種 Non-IID 類型：(1) 標籤分布偏斜 $P(y)$：不同客戶端的類別比例不同；(2) 特徵分布偏斜 $P(x)$：相同標籤下的特徵分布差異；(3) 相同標籤不同特徵 $P(x|y)$：如不同地區的手寫風格差異；(4) 相同特徵不同標籤 $P(y|x)$：標註偏好差異；(5) 數量偏斜：各客戶端 $n_k$ 差異懸殊。

為量化資料異質性程度，Li 等人 [3] 引入**異質性度量 $\Gamma$**：

$$\Gamma = F^* - \sum_{k=1}^{K} p_k F_k^*$$

其中 $F^*$ 和 $F_k^*$ 分別為全域和本地目標函數的最小值。當資料為 IID 時，$\Gamma \to 0$；Non-IID 程度越高，$\Gamma$ 越大，此參數直接影響收斂速度。另一常用度量為**有界散度假設**（Bounded Dissimilarity）：$\mathbb{E}_k[\|\nabla F_k(w)\|^2] \leq B^2 \|\nabla F(w)\|^2$，參數 $B$ 反映本地梯度與全域梯度的偏離程度 [3]。

## 2.1.3 FedAvg 演算法詳解

**FederatedAveraging（FedAvg）**演算法是聯邦學習最基礎且應用最廣泛的優化方法 [1]。其核心思想是讓選定的客戶端在本地執行多步隨機梯度下降（SGD），再由伺服器聚合各客戶端的模型更新。完整演算法如下：

---
**Algorithm 1: FederatedAveraging (FedAvg)**

**伺服器端執行：**
1. 初始化全域模型 $w_0$
2. **for** 每一輪 $t = 1, 2, \ldots$ **do**
3. 　　$m \leftarrow \max(C \cdot K, 1)$ 　　　// 選取比例 $C$ 的客戶端
4. 　　$S_t \leftarrow$ 隨機選取 $m$ 個客戶端
5. 　　**for each** 客戶端 $k \in S_t$ 平行執行 **do**
6. 　　　　$w_k^{t+1} \leftarrow$ ClientUpdate$(k, w_t)$
7. 　　$w_{t+1} \leftarrow \sum_{k \in S_t} \frac{n_k}{n} w_k^{t+1}$ 　// 加權平均聚合

**客戶端更新 ClientUpdate$(k, w)$：**
1. $\mathcal{B} \leftarrow$ 將本地資料 $\mathcal{P}_k$ 分成大小為 $B$ 的批次
2. **for** 每一本地週期 $i = 1, \ldots, E$ **do**
3. 　　**for each** 批次 $b \in \mathcal{B}$ **do**
4. 　　　　$w \leftarrow w - \eta \nabla \ell(w; b)$
5. **return** $w$ 傳回伺服器

---

關鍵超參數包括：客戶端選取比例 $C$、本地訓練週期數 $E$、批次大小 $B$、學習率 $\eta$。McMahan 等人 [1] 的實驗表明，**較小的 $B$ 配合較大的 $E$ 能顯著減少通訊輪數**：在 MNIST 資料集上，設定 $B=10, E=20$ 達到 99% 準確率僅需 **18 輪通訊**，相比基準 FedSGD 的 626 輪實現了 **34.8 倍加速**。在 CIFAR-10 實驗中，FedAvg 以 2,000 輪達到 85% 準確率，而標準 SGD 需要 99,000 步，通訊成本降低約 **50 倍** [1]。

**收斂性保證**需要以下標準假設 [3]：(1) $L$-Lipschitz 平滑性：$F_k(v) \leq F_k(w) + \nabla F_k(w)^T(v-w) + \frac{L}{2}\|v-w\|^2$；(2) $\mu$-強凸性；(3) 有界變異數：$\mathbb{E}[\|\nabla F_k(w, \xi) - \nabla F_k(w)\|^2] \leq \sigma_k^2$；(4) 有界梯度：$\mathbb{E}[\|\nabla F_k(w, \xi)\|^2] \leq G^2$。在這些假設下，FedAvg 的收斂速率為 $O(1/T)$，但收斂上界包含異質性項 $\Gamma$ 和本地訓練相關項 $(E-1)^2 G^2$ [3]。

值得注意的是，當 $E > 1$ 時，**學習率必須衰減**才能保證收斂至最優解。Li 等人 [3] 證明若使用固定學習率 $\eta$，最終解與最優解的距離為 $\Omega(\eta(E-1))$。此外，Non-IID 環境下 FedAvg 無法實現與客戶端數量成正比的線性加速，這是其主要理論限制。

## 2.1.4 安全與隱私挑戰

儘管聯邦學習的設計理念是保護資料隱私，但其分散式架構引入了新的安全威脅面。這些威脅可分為**完整性攻擊**（破壞模型效能）和**隱私攻擊**（竊取訓練資料）兩大類 [2]。

**拜占庭攻擊（Byzantine Attacks）**是完整性攻擊的核心威脅。Blanchard 等人 [4] 首次形式化此問題：在 $n$ 個參與者中，最多有 $f$ 個惡意參與者可發送任意更新值。典型攻擊包括**標籤翻轉攻擊**（Label Flipping）：惡意客戶端將本地資料標籤從源類別修改為目標類別；以及**模型投毒攻擊**（Model Poisoning）：直接操縱本地模型參數或梯度。後者的威力顯著更強——Bagdasaryan 等人證明單一惡意參與者可在**一輪內達到 100% 後門任務準確率**，且此攻擊無法被安全聚合機制偵測。

**梯度洩漏攻擊**揭示了聯邦學習中「僅分享梯度」並不能完全保證隱私。Zhu 等人 [5] 提出的 Deep Leakage from Gradients（DLG）攻擊展示了驚人的隱私風險：透過優化隨機初始化的虛擬資料，使其產生的梯度逼近真實梯度，即可**像素級精確還原原始訓練影像**，甚至可逐字元還原文本資料。攻擊僅需約 300 次 L-BFGS 迭代，當批次大小為 1 且影像解析度較低時效果最佳。後續研究進一步提升了攻擊效能，在 64×64 影像上可達 **PSNR > 30 dB** 的高保真還原 [5]。

**Non-IID 資料分布加劇了拜占庭防禦的困難**。傳統防禦方法（如 Krum [4]、Trimmed Mean、Coordinate-wise Median）假設誠實客戶端的更新會聚集在一起，而惡意更新為離群值。然而在 Non-IID 環境下，由於各客戶端本地資料分布差異大，誠實更新本身就呈現高度發散，使得離群值檢測方法失效。研究表明，現有拜占庭容錯方法在極端 Non-IID 情境下可能被完全突破，導致全域模型崩潰。這一觀察直接連結至本研究第三章將探討的威脅模型與防禦機制設計。

---

## References

[1] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, "Communication-efficient learning of deep networks from decentralized data," in *Proc. 20th Int. Conf. Artificial Intelligence and Statistics (AISTATS)*, Fort Lauderdale, FL, USA, Apr. 2017, pp. 1273–1282.

[2] P. Kairouz *et al.*, "Advances and open problems in federated learning," *Foundations and Trends in Machine Learning*, vol. 14, no. 1–2, pp. 1–210, 2021.

[3] T. Li, A. K. Sahu, M. Zaheer, M. Sanjabi, A. Talwalkar, and V. Smith, "Federated optimization in heterogeneous networks," in *Proc. Machine Learning and Systems (MLSys)*, Austin, TX, USA, Mar. 2020, pp. 429–450.

[4] P. Blanchard, E. M. El Mhamdi, R. Guerraoui, and J. Stainer, "Machine learning with adversaries: Byzantine tolerant gradient descent," in *Advances in Neural Information Processing Systems (NeurIPS)*, Long Beach, CA, USA, Dec. 2017, pp. 119–129.

[5] L. Zhu, Z. Liu, and S. Han, "Deep leakage from gradients," in *Advances in Neural Information Processing Systems (NeurIPS)*, Vancouver, BC, Canada, Dec. 2019, pp. 14747–14756.