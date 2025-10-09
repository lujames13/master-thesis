# Byzantine-Robust Optimistic Aggregation: A Multi-Aggregator Framework for Blockchain-based Federated Learning
# 具拜占庭容錯能力的樂觀聚合：多聚合器區塊鏈聯邦學習框架
# Abstract
## 中文摘要

聯邦學習作為一種保護隱私的分散式機器學習技術，已成為現代人工智慧發展的重要方向。然而，傳統聯邦學習架構依賴單一中央聚合器，面臨單點故障風險、信任假設問題及缺乏惡意聚合器檢測機制等挑戰。雖然區塊鏈技術的引入為聯邦學習提供了去中心化解決方案，但現有的區塊鏈聯邦學習方案多採用傳統拜占庭容錯（PBFT）共識機制，因其密集的多輪通信需求和高計算開銷導致嚴重的效能瓶頸。

本研究提出一個創新的混合Optimistic-PBFT安全聚合框架，成功將Optimistic Rollup的樂觀原理系統性地應用於區塊鏈聯邦學習。該框架在樂觀情況下採用輕量級輪詢選擇機制，每輪僅需單一聚合器執行聚合運算，相較於傳統PBFT方法中所有聚合器都必須參與每輪計算，大幅提升了系統效率；當檢測到可疑行為時，啟動多驗證者並行驗證機制，需要至少2f+1個驗證者參與共識，實現效能與安全性的動態平衡。

系統核心創新包括：（1）異步挑戰機制設計，實現挑戰處理與主要訓練流程的完全解耦，確保聯邦學習過程永不中斷；（2）多聚合器協作與動態排除機制，通過輪詢演算法公平分配聚合任務，並在檢測到惡意行為後自動回滾至安全狀態；（3）經濟激勵與技術安全機制的深度整合，通過質押與獎懲機制防止惡意行為並鼓勵誠實參與。

本研究基於Flower聯邦學習框架開發完整的原型系統，通過模擬各種攻擊場景驗證系統安全性。實驗結果顯示，在正常運作情況下，該框架的計算複雜度為O(R/N)每聚合器，相較於傳統PBFT的O(R×V)每驗證者實現了顯著的效能提升。在面對惡意聚合器攻擊時，系統能夠有效檢測並回滾至安全狀態，同時通過經濟懲罰機制維持系統的長期安全性。

本研究的混合Optimistic-PBFT機制首次實現了區塊鏈聯邦學習中效能與安全性的最佳平衡，為該領域的實際部署與應用奠定重要基礎，同時為未來的去中心化人工智慧基礎架構研究提供新的技術路徑。

關鍵詞： 聯邦學習、區塊鏈、Optimistic Rollup、拜占庭容錯、安全聚合、多聚合器

## 英文摘要 (Abstract)
Federated Learning (FL) has emerged as a crucial privacy-preserving distributed machine learning paradigm for modern artificial intelligence development. However, traditional FL architectures rely on a single central aggregator, facing challenges including single point of failure risks, trust assumption issues, and lack of malicious aggregator detection mechanisms. While blockchain technology offers decentralized solutions for FL, existing blockchain-based FL schemes predominantly adopt traditional Byzantine Fault Tolerance (PBFT) consensus mechanisms, resulting in severe performance bottlenecks due to intensive multi-round communication requirements and high computational overhead.

This research proposes an innovative Hybrid Optimistic-PBFT secure aggregation framework that systematically applies Optimistic Rollup principles to blockchain-based federated learning. Under optimistic conditions, the framework employs a lightweight round-robin selection mechanism requiring only one aggregator per round for aggregation computation, significantly improving efficiency compared to traditional PBFT approaches where all aggregators must participate in every round. When suspicious behavior is detected, it activates a multi-validator parallel verification mechanism requiring at least 2f+1 validators to participate in consensus, achieving dynamic balance between performance and security.

The core innovations include: (1) An asynchronous challenge mechanism design that completely decouples challenge processing from the main training workflow, ensuring uninterrupted federated learning processes; (2) Multi-aggregator collaboration with dynamic exclusion mechanisms that fairly distribute aggregation tasks through round-robin algorithms and automatically rollback to safe states upon detecting malicious behavior; (3) Deep integration of economic incentives with technical security mechanisms, preventing malicious behavior and encouraging honest participation through staking and reward-penalty mechanisms.

This research develops a complete prototype system based on the Flower federated learning framework and validates system security through simulations of various attack scenarios. Experimental results demonstrate that under normal operation, the framework achieves computational complexity of O(R/N) per aggregator, representing significant performance improvements compared to traditional PBFT's O(R×V) per validator. When facing malicious aggregator attacks, the system effectively detects and rolls back to safe states while maintaining long-term security through economic penalty mechanisms.

The Hybrid Optimistic-PBFT mechanism presented in this research represents the first achievement of optimal balance between performance and security in blockchain-based federated learning, establishing important foundations for practical deployment and applications in this field, while providing new technical pathways for future decentralized artificial intelligence infrastructure research.
Keywords: Federated Learning, Blockchain, Optimistic Rollup, Byzantine Fault Tolerance, Secure Aggregation, Multi-Aggregator

# I. Introduction
[introduction](introduction.md)
# II. Background
[background](background.md)
# III. Related work
[related-work](related-work.md)
# IV. Framework design
[framework-design](framework-design.md)
# V. Implementation
[implementation](implementation.md)
# VI. Evaluation
[evaluation](evaluation.md)
# VII. Conclutions and future work
[conclutions-and-future-work](conclutions-and-future-work.md)
# Reference
