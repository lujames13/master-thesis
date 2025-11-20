# 第二章 背景知識

## 2.2 區塊鏈與智能合約

### 2.2.1 區塊鏈基礎架構

區塊鏈（Blockchain）是一種分散式帳本技術（Distributed Ledger Technology, DLT），通過密碼學鏈接和共識機制確保數據的不可篡改性與透明性。區塊鏈由一系列按時間順序連接的區塊組成，每個區塊包含一組交易記錄、時間戳、前一區塊的密碼學雜湊值（cryptographic hash）以及其他元數據。這種鏈式結構使得任何對歷史數據的篡改都會導致後續所有區塊的雜湊值失效，從而保證了數據的完整性[1]。

**區塊鏈的核心特性**

區塊鏈技術為分散式系統提供了以下核心特性，這些特性使其成為多聚合器聯邦學習架構的理想信任基礎層：

1. **去中心化（Decentralization）**：區塊鏈網絡中不存在單一的控制節點，所有參與者共同維護系統狀態。這種去中心化架構消除了單點故障風險，避免了對中央權威的完全信任依賴。

2. **不可篡改性（Immutability）**：一旦數據被記錄在區塊鏈上並經過足夠的確認，修改歷史記錄在計算上是不可行的。這一特性依賴於密碼學雜湊函數（如 SHA-256）的抗碰撞性和工作量證明或權益證明等共識機制的安全保證[2]。

3. **透明性（Transparency）**：區塊鏈上的所有交易記錄對所有參與者可見，任何節點都可以驗證交易的合法性。這種透明性確保了系統操作的可審計性，使得惡意行為難以隱藏。

4. **持久性（Persistence）**：區塊鏈的分散式副本機制確保數據在多個節點上存儲，即使部分節點故障或離線，系統仍能維持運作並保證數據的持久存取。

**許可鏈與公有鏈**

根據訪問控制機制的不同，區塊鏈可分為公有鏈（Public Blockchain）和許可鏈（Permissioned Blockchain）兩大類。本研究聚焦於許可鏈場景，原因如下：

- **公有鏈**：任何節點都可自由加入網絡，參與共識過程（如比特幣、以太坊）。公有鏈提供最高程度的去中心化和抗審查性，但共識效率較低（如比特幣每秒約 7 筆交易，以太坊約 15-30 筆交易[3]），且缺乏對參與者身份的控制。

- **許可鏈**：僅允許經過授權的節點加入網絡（如 Hyperledger Fabric、Quorum）。許可鏈適合聯盟場景，參與者之間存在一定程度的信任基礎，可採用更高效的共識機制（如 PBFT），實現更高的交易吞吐量（可達數千 TPS[4]）和更低的確認延遲。

在聯邦學習應用中，參與者通常是特定領域的機構（如醫療機構、金融機構），它們願意在聯盟框架下合作訓練模型，但需要保護各自的數據隱私和計算利益。因此，許可鏈的受控訪問與高效共識機制更符合實際需求。

**區塊鏈結構**

一個典型的區塊包含以下組成部分：

- **區塊頭（Block Header）**：包含前一區塊的雜湊值、Merkle 根雜湊值、時間戳和隨機數（nonce）
- **交易列表（Transaction List）**：該區塊中包含的所有交易記錄
- **Merkle 樹（Merkle Tree）**：用於高效驗證交易完整性的數據結構

在聯邦學習應用中，區塊鏈記錄的「交易」包括客戶端提交的模型更新雜湊值、聚合器發布的全局模型雜湊值、驗證者提出的挑戰記錄，以及智能合約觸發的獎勵與懲罰分配。通過將這些關鍵操作記錄在區塊鏈上，系統實現了可驗證的訓練歷史追溯與不可篡改的審計軌跡。

### 2.2.2 智能合約與自動執行

智能合約（Smart Contract）是部署在區塊鏈上的自動執行程式，當預設條件滿足時，合約代碼自動執行相應的操作，無需人工干預或可信第三方參與[5]。智能合約的執行結果會被記錄在區塊鏈上，具有與區塊鏈相同的不可篡改性和透明性保證。以太坊平台上的 Solidity 語言是目前最廣泛使用的智能合約開發語言。

**智能合約在聯邦學習中的應用**

在多聚合器聯邦學習框架中，智能合約扮演著自動化協調者的角色，負責執行以下關鍵功能：

1. **自動觸發挑戰機制**：當驗證者檢測到可疑的聚合結果時，可以調用智能合約提交挑戰。合約會自動啟動挑戰驗證流程，通知其他驗證者參與共識驗證，並記錄挑戰時間以開始挑戰期間倒計時。

2. **分配獎勵與懲罰**：智能合約根據參與者的行為自動分配經濟激勵。若挑戰成功，挑戰者獲得獎勵，惡意聚合器的質押被罰沒（slashing）；若挑戰失敗，挑戰者損失質押，被挑戰的聚合器獲得補償。這種自動化的經濟激勵機制確保了系統的博弈論均衡。

3. **維護排除清單**：智能合約維護一個動態的排除清單（Exclusion List），記錄被檢測到惡意行為的聚合器。輪替選擇演算法在選擇下一個聚合器時會自動跳過清單中的節點，從而實現惡意節點的自動隔離。

4. **協調訓練流程**：智能合約記錄當前訓練輪次、選定的聚合器、挑戰狀態等系統狀態信息，所有參與者可以通過查詢合約狀態了解系統進度，確保訓練流程的透明與可追溯。

**智能合約範例**

以下 Solidity 偽代碼展示了一個簡化的挑戰提交函數：

```solidity
// 智能合約範例：挑戰機制
contract FederatedLearningChallenge {

    // 狀態變量
    mapping(uint256 => bytes32) public globalModelHashes;  // 輪次 -> 全局模型雜湊值
    mapping(address => uint256) public stakes;             // 參與者 -> 質押金額
    mapping(uint256 => Challenge) public challenges;       // 挑戰記錄
    address[] public excludedAggregators;                  // 排除清單

    struct Challenge {
        uint256 round;           // 被挑戰的輪次
        address challenger;      // 挑戰者
        address aggregator;      // 被挑戰的聚合器
        uint256 timestamp;       // 挑戰時間
        bool resolved;           // 是否已解決
        bool successful;         // 挑戰是否成功
    }

    // 提交挑戰函數
    function submitChallenge(uint256 _round, address _aggregator) public {
        require(stakes[msg.sender] >= MIN_STAKE, "Insufficient stake");
        require(block.timestamp <= challengeDeadline[_round], "Challenge period expired");

        // 創建挑戰記錄
        uint256 challengeId = nextChallengeId++;
        challenges[challengeId] = Challenge({
            round: _round,
            challenger: msg.sender,
            aggregator: _aggregator,
            timestamp: block.timestamp,
            resolved: false,
            successful: false
        });

        // 觸發 PBFT 驗證事件
        emit ChallengeSubmitted(challengeId, _round, msg.sender, _aggregator);

        // 啟動驗證流程（通過鏈下共識機制）
        initiatePBFTVerification(challengeId);
    }

    // 解決挑戰函數（由共識機制調用）
    function resolveChallenge(uint256 _challengeId, bool _successful) public onlyValidator {
        Challenge storage c = challenges[_challengeId];
        require(!c.resolved, "Challenge already resolved");

        c.resolved = true;
        c.successful = _successful;

        if (_successful) {
            // 懲罰惡意聚合器
            uint256 slashedAmount = stakes[c.aggregator];
            stakes[c.aggregator] = 0;
            stakes[c.challenger] += slashedAmount / 2;  // 獎勵挑戰者

            // 添加到排除清單
            excludedAggregators.push(c.aggregator);

            emit ChallengeSuccessful(_challengeId, c.aggregator);
        } else {
            // 懲罰錯誤挑戰者
            stakes[c.challenger] -= CHALLENGE_PENALTY;
            stakes[c.aggregator] += CHALLENGE_PENALTY;

            emit ChallengeFailed(_challengeId, c.challenger);
        }
    }
}
```

上述合約展示了智能合約如何自動化處理挑戰流程。當驗證者調用 `submitChallenge` 函數時，合約會檢查質押金額和挑戰期限，創建挑戰記錄並觸發事件通知驗證者網絡。當共識驗證完成後，`resolveChallenge` 函數根據驗證結果自動分配獎懲並更新排除清單。這種自動化機制消除了對可信第三方的依賴，確保了規則的公正執行。

### 2.2.3 IPFS 與鏈下存儲

雖然區塊鏈提供了不可篡改的記錄能力，但直接在鏈上存儲大量數據存在顯著的成本與效率問題。深度學習模型的參數規模通常非常龐大，例如一個 ResNet-50 模型約有 25.5 百萬個參數（以 32 位浮點數存儲約 102 MB），大型語言模型（如 LLaMA-7B）則高達 7 十億參數（約 28 GB）。將如此大量的數據直接存儲在區塊鏈上會導致以下問題[6]：

1. **存儲成本高昂**：以太坊網絡上每存儲 1 KB 數據的 Gas 成本約為 20,000 Gas，按當前 Gas 價格計算，存儲 1 MB 數據的成本可達數百美元，對於 GB 級別的模型而言完全不可行。

2. **吞吐量受限**：區塊鏈的區塊大小和出塊速度限制了數據寫入速度。以太坊的區塊大小限制約為 30 MB，比特幣僅為 1-4 MB，遠無法滿足大型模型的存儲需求。

3. **讀取效率低下**：所有區塊鏈節點都需要存儲完整的歷史數據，隨著模型版本累積，存儲負擔會持續增長，降低節點的同步效率。

**IPFS 的設計原理**

星際文件系統（InterPlanetary File System, IPFS）是一種分散式的內容定址存儲網絡，為區塊鏈應用提供了高效的鏈下存儲方案[7]。IPFS 的核心特點包括：

- **內容定址（Content Addressing）**：IPFS 使用文件內容的密碼學雜湊值（Content Identifier, CID）作為文件地址，而非傳統的位置定址。相同內容的文件必然產生相同的 CID，這確保了數據的完整性驗證。

- **分散式存儲**：文件被分割成多個區塊（Block），分散存儲在多個 IPFS 節點上。當節點請求文件時，IPFS 協議會自動從最近的存儲節點獲取區塊並重組文件。

- **去重與版本控制**：由於使用內容定址，IPFS 自動實現文件去重。相同的模型參數只需存儲一次，不同版本的模型可通過 Merkle DAG（有向無環圖）高效追蹤變更。

**IPFS 在聯邦學習中的工作流程**

在多聚合器聯邦學習框架中，IPFS 與區塊鏈的結合方式如下：

```
演算法 1: IPFS 與區塊鏈結合的存儲流程
// 客戶端上傳本地模型
1: 客戶端完成本地訓練，得到本地模型參數 w_k
2: 將 w_k 上傳至 IPFS 節點
3: IPFS 返回內容標識符 CID_k = Hash(w_k)
4: 客戶端將 CID_k 提交至區塊鏈智能合約
5: 智能合約記錄：(客戶端地址, 訓練輪次, CID_k, 時間戳)

// 聚合器獲取客戶端模型
6: 聚合器從區塊鏈讀取所有客戶端提交的 CID 列表
7: for 每個 CID_k in CID 列表 do
8:     從 IPFS 網絡獲取對應的模型參數 w_k
9:     驗證：Hash(w_k) == CID_k  // 確保數據完整性
10: end for
11: 執行聚合算法得到全局模型 w_global
12: 將 w_global 上傳至 IPFS，獲得 CID_global
13: 將 CID_global 提交至區塊鏈，開始挑戰期間

// 驗證者檢查聚合結果
14: 驗證者從區塊鏈讀取 CID_global 和所有 CID_k
15: 從 IPFS 獲取 w_global 和所有 w_k
16: 獨立執行聚合算法，得到 w_verify
17: if Hash(w_verify) != CID_global then
18:     提交挑戰至智能合約
19: end if
```

這種設計實現了「鏈上記錄雜湊值，鏈下存儲完整數據」的架構，兼顧了區塊鏈的不可篡改性與 IPFS 的高效存儲能力。區塊鏈上僅存儲約 32-64 字節的 CID 雜湊值，而完整的模型參數（可能數 GB）存儲在 IPFS 上。任何參與者都可以通過區塊鏈上的 CID 從 IPFS 獲取完整數據並驗證其完整性，確保了系統的透明性與可驗證性。

此外，IPFS 的分散式特性確保了即使部分存儲節點離線，數據仍可從其他節點獲取，提供了與區塊鏈去中心化理念一致的存儲可靠性保證。

---

## 參考文獻

[1] S. Nakamoto, "Bitcoin: A peer-to-peer electronic cash system," 2008. [Online]. Available: https://bitcoin.org/bitcoin.pdf

[2] M. Castro and B. Liskov, "Practical Byzantine fault tolerance," in *Proc. 3rd Symp. Operating Systems Design Implementation (OSDI)*, New Orleans, LA, USA, Feb. 1999, pp. 173-186.

[3] C. Decker and R. Wattenhofer, "Information propagation in the Bitcoin network," in *Proc. IEEE Int. Conf. Peer-to-Peer Computing (P2P)*, Trento, Italy, Sep. 2013, pp. 1-10.

[4] E. Androulaki et al., "Hyperledger Fabric: A distributed operating system for permissioned blockchains," in *Proc. 13th EuroSys Conf.*, Porto, Portugal, Apr. 2018, pp. 1-15.

[5] V. Buterin, "A next-generation smart contract and decentralized application platform," Ethereum White Paper, 2014. [Online]. Available: https://ethereum.org/en/whitepaper/

[6] K. Zhang, J. Jacobsen, and H. Zhu, "FLB2: Federated learning on blockchain with layer-2 implementation," in *Proc. IEEE Int. Conf. Blockchain*, Rhodes, Greece, Nov. 2022, pp. 456-463.

[7] J. Benet, "IPFS - Content addressed, versioned, P2P file system," arXiv:1407.3561, Jul. 2014.
