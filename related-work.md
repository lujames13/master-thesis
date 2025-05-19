## 現有研究的問題
### 只是把區塊鏈當不變帳本，本質上還是中心化聯邦學習的
### 提出多聚合器協作，使用PBFT的
Che等人[1]提出基於委員會機制的聯邦學習框架(CMFL)，以無服務器架構實現聯邦學習中的拜占庭容錯，但其僅依賴歐氏距離的單一評分度量標準在異質數據環境下易於失效，且全域模型聚合使用PBFT共識。
Wang等人[2]提出了FL-MFC框架能處理異質聯邦學習，但其模型校準過程缺乏有效的驗證機制，任何能提交工作量證明的礦工都可操縱更新過程，無法確保聚合安全性。
### 證明使用optimistic rollup可以增加效能的
### 使用zk的->zk計算很耗費資源
### 貢獻：提出基於 Optimistic rollup 的 Hybrid PBFT 安全聚合機制，在樂觀情況下擁有中心化聯邦學習效率的同時也能有 BFT 程度的防禦性能，還不需要計算 zkp

[1]: A Decentralized Federated Learning Framework via Committee Mechanism with Convergence Guarantee
