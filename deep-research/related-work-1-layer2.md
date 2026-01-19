# 區塊鏈聯邦學習中的 Layer-2 擴展與零知識證明驗證文獻綜述

零知識機器學習（zkML）與 Layer-2 擴展方案為區塊鏈聯邦學習（BCFL）提供了密碼學驗證的可能性，但其**極高的計算開銷**已成為實際部署的主要瓶頸。本綜述分析 2022-2025 年間的代表性研究，揭示現有方法在處理大規模模型即時驗證時的根本性限制，為 Optimistic-PBFT 混合框架的研究動機提供理論支撐。

## zkML 驗證方法的最新進展與計算代價

Chen 等人於 EuroSys 2024 發表的 ZKML 系統 [1] 代表了 zkSNARK 應用於機器學習驗證的重要突破。該系統採用 halo2 proving system 搭配 KZG commitment scheme，透過優化編譯器將 TensorFlow 模型轉換為零知識電路。實驗數據顯示，對於 **ResNet-18（280.9K 參數）**，proof generation time 為 52.9 秒，verification time 僅需 11.84 毫秒；然而當模型擴展至 **GPT-2（81.3M 參數）**時，proving time 激增至 **3,651 秒（約 61 分鐘）**，且需要配備 1TB RAM 的高階伺服器（AWS r6i.32xlarge）。此一數量級的計算開銷意味著，若每輪聯邦學習更新都需生成 ZK proof，訓練效率將大幅降低。

針對大型語言模型的驗證需求，Sun 等人提出的 zkLLM [2] 於 ACM CCS 2024 發表，首次實現對 **13B 參數模型（LLaMA-2-13B）**的零知識證明。該系統創新性地設計了 tlookup（平行化 lookup argument）與 zkAttn（Transformer attention 專用證明協議），並採用 GPU-parallelized CUDA 實現。儘管如此，proof generation time 仍需 **15 分鐘以下**，且作者明確指出「extending to training LLMs may pose insurmountable challenges」——驗證訓練過程而非推論的複雜度將更高數個數量級。

在聯邦學習專用場景中，Zhu 等人的 RiseFL [3]（VLDB 2024）採取不同策略。該研究指出「zkSNARK protocols are not additively homomorphic, thus they cannot support the secure aggregation required in federated learning」，因此改用 **Pedersen commitment 與 Bulletproofs** 進行梯度 L2-norm 驗證。相較於 baseline 方法 EIFFeL，RiseFL 在 100K 參數規模下達到 **165 倍加速**（從 1,536 秒降至 9.3 秒），但其驗證為機率性檢查而非嚴格密碼學證明，安全性有所折衷。

## Layer-2 與 Off-chain 計算方法

Heiss 等人 [4] 於 IEEE Blockchain 2022 提出基於 Verifiable Off-Chain Computations（VOC）的框架，使用 ZoKrates 工具實現 zkSNARK（Groth16 scheme）。該方法將訓練節點作為 off-chain prover，證明運算正確性後由智能合約進行 on-chain 驗證。實驗顯示，對於 batch size 40 的模型，**proof time 約 167.6 秒，記憶體消耗達 17.45 GB**，而 one-time setup phase 更需 **45 分鐘**。此 setup phase 的 blocking 特性對高頻更新的聯邦學習系統極為不利。

Wang 等人的 zkFL [5] 將區塊鏈礦工納入驗證流程，client 無需自行驗證 ZKP，改由區塊鏈共識機制承擔。然而對於 ResNet50 模型，**每輪聚合的 proof generation 仍需約 54.72 分鐘**，驗證時間約為生成時間的一半。這意味著若聯邦學習每小時進行一次全域更新，光是證明生成就可能佔用大部分時間窗口。

在 Optimistic rollup 方向，Conway 等人的 opML [6]（arXiv 2024）採用 fraud proof 機制，假設計算預設正確，僅在受到挑戰時才進行驗證。此方法的計算成本遠低於 zkML，可在標準 PC 上執行 7B 參數模型。然而其**挑戰期通常為 7-14 天**，對需要快速 finality 的聯邦學習場景並不適用，且目前尚無學術研究將其具體應用於 FL aggregation 驗證。

## 計算瓶頸的批判性分析

綜合上述文獻，zkML 方法存在三項根本性限制：

- **Proof generation overhead 與模型規模非線性相關**：從 MNIST（8.1K 參數，2.45 秒）到 GPT-2（81.3M 參數，3,651 秒），overhead ratio 高達 **1000 倍以上**
- **記憶體需求極端**：大型模型需 512GB-1TB RAM，EZKL benchmarks 顯示 RISC Zero 框架處理 Random Forest 需 **10,189 MB** 記憶體
- **Blocking 特性限制更新頻率**：zkFL 每輪需 55 分鐘 proof overhead，無法支援分鐘級或秒級的高頻參數同步

此外，現有 Layer-2 方案的研究空白值得注意：**Optimistic rollup 與聯邦學習的結合尚無系統性研究**。學術界傾向採用 validity proof（ZK-based）而非 fraud proof，主要因 FL 涉及多方分散式計算，經濟激勵機制較難設計。然而，當模型規模持續擴大，zkML 的計算代價可能使其在實務上不可行。

## 結論與研究缺口

現有密碼學驗證方法雖能保證正確性，但其計算開銷——特別是 **proof generation time 達數十分鐘至數小時級別**——嚴重限制了 BCFL 系統的實時性與可擴展性。RiseFL 等折衷方案雖大幅降低開銷，卻犧牲了嚴格的安全保證。Optimistic rollup 的低計算成本特性理論上適合 FL 場景，但其長挑戰期與 FL 高頻更新需求存在矛盾。此一研究缺口——**如何在多聚合器架構下實現低延遲、非阻塞式驗證**——正是 Optimistic-PBFT 混合框架所欲解決的核心問題。

---

**參考文獻**

[1] B.-J. Chen, S. Waiwitlikhit, I. Stoica, and D. Kang, "ZKML: An Optimizing System for ML Inference in Zero-Knowledge Proofs," in *Proc. EuroSys*, Athens, Greece, Apr. 2024, pp. 560-574.

[2] H. Sun, J. Li, and H. Zhang, "zkLLM: Zero Knowledge Proofs for Large Language Models," in *Proc. ACM CCS*, Salt Lake City, USA, Oct. 2024.

[3] Y. Zhu, Y. Wu, Z. Luo, B. C. Ooi, and X. Xiao, "RiseFL: Secure and Verifiable Data Collaboration with Low-Cost Zero-Knowledge Proofs," *Proc. VLDB Endow.*, vol. 17, no. 9, pp. 2321-2334, 2024.

[4] J. Heiss, E. Grünewald, S. Tai, N. Haimerl, and S. Schulte, "Advancing Blockchain-based Federated Learning through Verifiable Off-chain Computations," in *Proc. IEEE Int. Conf. Blockchain*, Espoo, Finland, Aug. 2022, pp. 194-201.

[5] Z. Wang *et al.*, "zkFL: Zero-Knowledge Proof-based Gradient Aggregation for Federated Learning," *IEEE Trans. Big Data*, 2024.

[6] K. Conway *et al.*, "opML: Optimistic Machine Learning on Blockchain," arXiv:2401.17555, Jan. 2024.