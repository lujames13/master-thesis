## 現有研究的問題
### 只是把區塊鏈當不變帳本，本質上還是中心化聯邦學習的
### 提出多聚合器協作，使用PBFT的
Che等人[1]提出基於委員會機制的聯邦學習框架(CMFL)，以無服務器架構實現聯邦學習中的拜占庭容錯，但其僅依賴歐氏距離的單一評分度量標準在異質數據環境下易於失效，且全域模型聚合使用PBFT共識。

Wang等人[2]提出了FL-MFC框架能處理異質聯邦學習，但其模型校準過程缺乏有效的驗證機制，任何能提交工作量證明的礦工都可操縱更新過程，無法確保聚合安全性。

在區塊鏈聯邦學習的安全聚合研究中，Qi等人[4]提出了一種基於聲譽的安全聚合機制，通過賦予不同節點基於其模型質量的聲譽權重，有效減輕了惡意節點對全局模型的負面影響。實驗結果顯示，即使在50%節點為惡意節點的場景中，該聲譽加權聚合方法仍能維持較高的模型性能。


### 證明使用optimistic rollup可以增加效能的
Alief等人[3]提出了FLB2架構，成功將Layer 2區塊鏈（特別是Optimistic Rollup技術）應用於聯邦學習系統，實驗結果表明與傳統Layer 1方法相比，該架構能將訓練時間減少約50%，同時保持模型準確性並維持去中心化的安全保障。
### 使用zk的->zk計算很耗費資源
### 貢獻：提出基於 Optimistic rollup 的 Hybrid PBFT 安全聚合機制，在樂觀情況下擁有中心化聯邦學習效率的同時也能有 BFT 程度的防禦性能，還不需要計算 zkp

[1]: A Decentralized Federated Learning Framework via Committee Mechanism with Convergence Guarantee
[2]:  Blockchain-Empowered Federated Learning Through Model and Feature Calibration
[3]: FLB2: Layer 2 Blockchain Implementation Scheme on Federated Learning Technique
[4]: High-Quality Model Aggregation for Blockchain-Based Federated Learning via Reputation-Motivated Task Participation
