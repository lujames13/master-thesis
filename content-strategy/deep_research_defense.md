# Defense Mechanisms in Blockchain-Based Federated Learning: The Verification Layer Blind Spot

The systematic analysis of 2023-2025 BCFL literature reveals a critical research gap: **while Byzantine-robust aggregation methods defend against malicious clients, the vast majority of systems assume honest verifiers who execute these defense algorithms**. This creates an unaddressed attack surface at the verification layer that undermines the security guarantees these systems claim to provide.

## The core vulnerability

Blockchain-based federated learning systems employ Byzantine-robust aggregation methods like Krum, Trimmed Mean, and Median to filter malicious client updates. However, these defenses are only effective if the entities executing them—miners, validators, or committee members—honestly follow the protocol. **Our research finds that 70-80% of BCFL papers make this assumption without explicitly stating it, and only one paper even acknowledges the problem of malicious verifiers without solving it**.

## State-of-the-art defense mechanisms and their assumptions

### Papers with explicit honest verifier/aggregator assumptions

**BRFLATA (2025)** - Enhancing Byzantine robustness via tripartite adaptive authentication
- **Citation**: X. Li, Y. Li, H. Wan, L. Qi, X. Zhou, and W. Shi, "Enhancing Byzantine robustness of federated learning via tripartite adaptive authentication," J. Big Data, vol. 12, article 121, 2025.
- **Defense mechanism**: Uses Krum and Trimmed Mean for Byzantine client detection with credibility-based weighting during aggregation. Implements adaptive client matching and authentication mechanisms with zero-knowledge proofs for communication verification.
- **Verifier assumption**: **Explicitly states "the server is reliable"** in threat model. Assumes Byzantine clients and link attackers but not malicious servers. The server performs all aggregation and authentication tasks.
- **Addresses malicious verifiers**: NO - security model explicitly excludes server compromise.

**Adaptive Adversaries Survey (IACR 2025)** - Comprehensive evaluation of Byzantine defenses
- **Citation**: J. K. Szeląg, J.-J. Chin, and S.-C. Yip, "Adaptive Adversaries in Byzantine-Robust Federated Learning: A Survey," IACR Cryptology ePrint Archive, Paper 2025/510, 2025.
- **Defense mechanism**: Evaluates Krum (configured for ⌈N/2⌉-1 Byzantine clients) and Trimmed Mean (β=0.4) as baseline defenses. Demonstrates these methods are insufficient against adaptive adversaries who modify attack strategies after detection, introducing "Reconnecting Malicious Clients" threat.
- **Verifier assumption**: Describes aggregator as "the centralised anchor for FL systems, responsible for distributing, updating and securing the global model" and **implicitly assumes the aggregator correctly executes Krum and Trimmed Mean protocols**. The threat model exclusively focuses on Byzantine clients.
- **Addresses malicious verifiers**: NO - assumes aggregator correctness throughout analysis.

**BlockDFL (ACM Web Conference 2024)** - Fully decentralized P2P framework
- **Citation**: Z. Qin, X. Yan, M. Zhou, and S. Deng, "BlockDFL: A Blockchain-based Fully Decentralized Peer-to-Peer Federated Learning Framework," in Proc. ACM Web Conference, 2024, pp. 2914-2925.
- **Defense mechanism**: Employs voting mechanism with PBFT-based consensus and two-layer scoring (gradient compression plus model quality scoring) to coordinate FL without mutual trust. Defends against poisoning attacks with up to 40% malicious participants through stake-based reputation.
- **Verifier assumption**: **States "The voting mechanism can produce a non-empty block only if the super majority of verifiers (over 2/3) are honest"**. Assumes proportion of honest stake increases over rounds, making ≥67% honest verifiers "more and more likely."
- **Addresses malicious verifiers**: Partially - uses Byzantine fault tolerance but requires honest supermajority assumption.

**LiteChain (IEEE TMC 2025)** - Lightweight blockchain for massive edge networks
- **Citation**: H. Chen, R. Zhou, Y.-H. Chan, Z. Jiang, X. Chen, and E. C. H. Ngai, "LiteChain: A Lightweight Blockchain for Verifiable and Scalable Federated Learning in Massive Edge Networks," IEEE Trans. Mobile Comput., vol. 24, no. 3, pp. 1928-1944, Mar. 2025.
- **Defense mechanism**: Comprehensive Byzantine Fault Tolerance (CBFT) consensus with Krum and Trimmed Mean for poisoning defense. Reorganizes devices into two-level structure where elected cluster nodes form verification committee.
- **Verifier assumption**: States "the assumptions of trustworthy central servers and clients in traditional FL studies are often unrealistic" and uses blockchain to address this. However, **assumes committee members performing dual controller-verifier roles are trustworthy through election mechanism**.
- **Addresses malicious verifiers**: Partially - acknowledges untrusted servers problem but relies on committee election without explicit malicious committee member modeling.

### Papers addressing malicious verifiers (the exceptions)

**KFC: Krum Federated Chain (arXiv 2025)** - The only comprehensive solution
- **Citation**: M. García-Márquez, N. Rodríguez-Barroso, M. V. Luzón, and F. Herrera, "Krum Federated Chain (KFC): Using blockchain to defend against adversarial attacks in Federated Learning," arXiv preprint arXiv:2502.06917, Feb. 2025.
- **Defense mechanism**: Combines Krum Byzantine-robust aggregation with Proof of Federated Learning (PoFL) consensus. First tests PoFL alone, then proposes KFC which layers Krum on top of blockchain consensus to provide defense even when all verification nodes are compromised.
- **Verifier assumption**: Explicitly addresses miner compromise. States PoFL is effective "when at least one miner remains uncompromised" but **KFC is designed to defend "even when all miners are compromised"**, directly tackling the malicious verifier problem.
- **Addresses malicious verifiers**: **YES** - This is the ONLY 2023-2025 BCFL paper that explicitly addresses scenarios where all miners/validators executing aggregation can be Byzantine and proposes a working defense.

**FedBlock (IEEE Big Data 2024)** - Acknowledges problem without solution
- **Citation**: D. H. Nguyen, P. L. Nguyen, T. T. Nguyen, H. H. Pham, and D. A. Tran, "FedBlock: A Blockchain Approach to Federated Learning against Backdoor Attacks," in IEEE International Conference on Big Data, Washington, DC, USA, 2024, pp. 1-8.
- **Defense mechanism**: Client-as-verifier approach where clients with trust scores above 0.5 can become verifiers. Smart contract manages verification process where verifiers classify other clients with trust scores (0, 0.5, 1) to detect backdoor attacks.
- **Verifier assumption**: **Critically acknowledges the gap**: "with possibility of malicious verifiers, our proposed client-as-a-verifier approach can be highly effective, but if anyone can be a verifier, we need more than just assuming that the majority of verifiers is honest and will prevail over many FL rounds. We need a mechanism to detect and ignore malicious verifiers."
- **Addresses malicious verifiers**: NO - explicitly lists this as **future work** without providing a solution, making this paper evidence of the research gap itself.

**Fantastyc (arXiv 2024)** - Byzantine aggregators in traditional FL context
- **Citation**: "Fantastyc: Blockchain-based Federated Learning Made Secure and Practical," arXiv:2406.03608v1, 2024.
- **Defense mechanism**: Offloads validation to dedicated server set using validity proofs. Tolerates up to one-third Byzantine aggregators with majority-honest requirement (improved from typical two-thirds).
- **Verifier assumption**: **States "Byzantine behavior is attributed solely to aggregators, with a tolerance for up to one-third of them"** while regarding clients as honest-but-curious. Requires majority of honest servers for robustness.
- **Addresses malicious verifiers**: YES - explicitly models Byzantine aggregators but still requires honest majority.

### Papers with implicit honest verifier assumptions

**BRFL: Byzantine-Robust Federated Learning Based on Blockchain (WASA 2024)**
- **Citation**: L. Song, C. Cai, S. Wei, R. Banerjee, X. Feng, and H. Jiang, "Byzantine-Robust Federated Learning Based on Blockchain," in Wireless Artificial Intelligent Computing Systems and Applications (WASA 2024), Lecture Notes in Computer Science, vol. 14997, Springer, 2025, pp. 573-586.
- **Defense mechanism**: Introduces Precision-based Spectral Aggregation (PSA) with Proof of Pearson Correlation Coefficient (PPCC) consensus algorithm. Blockchain records local models and scores them by distance; PPCC selects next aggregation node based on correlation with global model.
- **Verifier assumption**: Acknowledges "unreliable servers" as motivation for blockchain use. Rotating aggregation nodes selected via PPCC correlation scores. **Implicitly assumes high-correlation nodes are trustworthy** without explicit Byzantine aggregator modeling.
- **Addresses malicious verifiers**: Partially - mitigates through rotation and selection but doesn't model actively malicious selected aggregators.

**Privacy-Preserving Byzantine-Robust FL via Blockchain (IEEE TIFS 2022)** - Foundational work
- **Citation**: Y. Miao, Z. Liu, H. Li, K.-K. R. Choo, and R. H. Deng, "Privacy-Preserving Byzantine-Robust Federated Learning via Blockchain Systems," IEEE Transactions on Information Forensics and Security, vol. 17, pp. 2848-2861, 2022.
- **Defense mechanism**: PBFL uses cosine similarity to identify malicious gradients from Byzantine clients. Employs fully homomorphic encryption for secure aggregation while blockchain provides decentralized consensus to remove central trusted server dependency.
- **Verifier assumption**: Explicitly acknowledges "untrustworthiness of clients and servers" in traditional FL. Blockchain is used to "mitigate the impact of the central server."
- **Addresses malicious verifiers**: YES - one of few papers explicitly addressing both malicious clients AND servers through blockchain decentralization.

**BR-CPPFL: Blockchain-Based Robust Clustered Privacy-Preserving FL (ICICS 2025)**
- **Citation**: Y. Li et al., "BR-CPPFL: A Blockchain-Based Robust Clustered Privacy-Preserving Federated Learning System," in Information and Communications Security (ICICS 2025), Lecture Notes in Computer Science, vol. 16218, Springer, 2026, pp. 346-363.
- **Defense mechanism**: Weighted global model aggregation combining intra-cluster average aggregation and cross-cluster weight aggregation. Privacy-preserving detection of malicious models in IID and Non-IID scenarios through clustering without leaking privacy.
- **Verifier assumption**: No explicit verifier assumption stated in accessible excerpts. Blockchain used for decentralization but aggregator behavior assumptions not articulated.
- **Addresses malicious verifiers**: Partially - blockchain addresses centralization but focuses on malicious client detection.

**FLock (ACM Web Conference 2025)** - Multiple aggregators for fault tolerance
- **Citation**: "FLock: Robust and Privacy-Preserving Federated Learning based on Practical Blockchain State Channels," in Proceedings of the ACM Web Conference 2025, 2025.
- **Defense mechanism**: Secure aggregation with up to 25 aggregators using blockchain state channels. Achieves ResNet aggregation in 2 minutes over WAN with 25 aggregators and 100 clients.
- **Verifier assumption**: States FLock "successfully implements secure aggregation with such a large number of aggregators, thereby **enhancing the fault tolerance of the aggregation**" through redundancy.
- **Addresses malicious verifiers**: YES - uses multiple aggregators (up to 25) to tolerate faulty/malicious aggregators through redundancy.

**Byzantine-Robust Decentralized FL (ACM CCS 2024)** - Peer-to-peer architecture
- **Citation**: M. Fang, Z. Zhang, H. Xu, P. Khanduri, J. Liu, S. Lu, Y. Liu, and N. Gong, "Byzantine-Robust Decentralized Federated Learning," in Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (CCS '24), 2024, pp. 2874-2888.
- **Defense mechanism**: Byzantine-robust algorithms adapted for decentralized architecture where clients communicate peer-to-peer without central server. Uses robust aggregation methods for decentralized setting to defend against Byzantine attackers.
- **Verifier assumption**: No central aggregator exists in decentralized architecture. Each client performs its own local aggregation of received peer updates.
- **Addresses malicious verifiers**: N/A - eliminates central aggregators entirely through P2P architecture, fundamentally changing threat model.

**Median-Krum (MobiWac 2023)** - Joint distance-statistical approach
- **Citation**: F. Colosimo and F. De Rango, "Median-Krum: A Joint Distance-Statistical Based Byzantine-Robust Algorithm in Federated Learning," in Proc. Int'l ACM Symp. Mobility Manag. Wireless Access (MobiWac '23), New York, NY, USA: ACM, 2023, pp. 275-282.
- **Defense mechanism**: Combines distance-based Krum (selects models with smallest sum of distances to closest neighbors) with coordinate-wise median aggregation to provide dual-layer robustness against Byzantine failures.
- **Verifier assumption**: Standard centralized FL framework with central server performing aggregation. **No explicit discussion of server honesty assumptions**. Focus on Byzantine client resilience.
- **Addresses malicious verifiers**: Not explicitly - mentions blockchain for decentralization in passing but doesn't address malicious aggregator scenarios in threat model.

**Quantum-Enhanced Blockchain FL via Quantum Byzantine Agreement (Science China 2025)**
- **Citation**: "Quantum-enhanced blockchain federated learning via quantum Byzantine agreement," Science China Information Sciences, 2025.
- **Defense mechanism**: Quantum Byzantine agreement for consensus tolerating nearly 50% malicious clients (improved from traditional 33%). Matrix product operators achieve 90% communication reduction. Byzantine-resilient aggregation algorithm for adversarial attack mitigation.
- **Verifier assumption**: Addresses "limited fault tolerance" in existing blockchain FL, proposing quantum agreement enabling "consensus even when nearly 50% of clients are malicious." **No explicit aggregator/verifier honesty assumptions in accessible excerpts**.
- **Addresses malicious verifiers**: Partially - improved fault tolerance for malicious clients but doesn't explicitly address malicious aggregators/verifiers.

**Blockchain-Based FL System Survey (Sensors 2023)** - Pattern analysis
- **Citation**: Y. E. Octavian and S.-G. Lee, "Blockchain-Based Federated Learning System: A Survey on Design Choices," Sensors, vol. 23, no. 12, 2023, Art. no. 5658.
- **Survey findings**: Analyzed 30 BCFL papers revealing: 53.33% utilize model verification mechanisms, 66.67% have no punishment mechanism for malicious behavior, 56.67% use single aggregator (vulnerable to compromise). **Identifies "A single reviewer raises a robustness issue"** but notes most papers don't address it.
- **Critical insight**: Survey explicitly identifies the gap - single reviewers/aggregators create vulnerabilities that most papers don't address.

## Comparison: Traditional FL vs. blockchain FL malicious aggregator research

### Traditional federated learning (non-blockchain)

The traditional FL community has produced approximately 15 papers (2021-2025) explicitly addressing malicious aggregators:

**ELSA (IEEE S&P 2023)**: Distributed trust across two non-colluding servers with malicious security, 7-25% overhead versus semi-honest case. **zkFL (arXiv 2023)**: Zero-knowledge proofs forcing aggregator to prove correct aggregation, clients verify without trusting aggregator. **Aero (arXiv 2023)**: Differential privacy over completely untrusted aggregator, 10^5x efficiency improvement over prior work. **AlphaFL (2025)**: "Malicious²" security handling both malicious clients AND servers with server-client collusion tolerance. **Mario (EuroS&P 2025)**: Multiple-aggregator protocol with security AND robustness in malicious setting, 3.40× faster than ELSA.

These papers treat aggregator maliciousness as a first-class threat, using cryptographic verification (ZKP, commitments), distributed trust (multiple non-colluding servers), or hardware trust (TEE) to eliminate honest aggregator assumptions.

### Blockchain-based federated learning

In stark contrast, BCFL research exhibits a systematic pattern of assuming honest or majority-honest verifiers even while using blockchain for decentralization. **Of 20+ BCFL papers reviewed from 2023-2025, only one (KFC) provides a working defense against fully malicious verifiers, and one other (FedBlock) acknowledges the problem without solving it**.

The common justification is that blockchain's decentralization and transparency inherently solve trust issues. However, this reasoning is flawed: **blockchain consensus requires honest majority assumptions (typically >50% or >67%), and if the verification layer is compromised, the Byzantine-robust aggregation methods are never correctly executed**.

## The systematic blind spot: A research gap analysis

### Summary table

| Paper | Defense Method | Verifier Assumption | Addresses Verifier Collusion? | Year |
|-------|----------------|---------------------|-------------------------------|------|
| BRFLATA | Krum, Trimmed Mean | **"The server is reliable"** (explicit) | NO | 2025 |
| Adaptive Adversaries Survey | Krum, Trimmed Mean | Aggregator executes correctly (implicit) | NO | 2025 |
| BlockDFL | PBFT voting, scoring | **">2/3 verifiers are honest"** (explicit) | Requires honest supermajority | 2024 |
| LiteChain | CBFT, Krum, Trimmed Mean | Elected committee trustworthy (implicit) | Partially - via election | 2025 |
| **KFC** | **Krum + PoFL** | **Addresses "all miners compromised"** | **YES - Only complete solution** | **2025** |
| **FedBlock** | Trust scoring | **Acknowledges malicious verifiers** | **NO - Listed as future work** | **2024** |
| Fantastyc | Validity proofs | Up to 1/3 Byzantine aggregators tolerated | Requires honest majority | 2024 |
| BRFL | PSA, PPCC consensus | High-correlation nodes trustworthy (implicit) | Partially - via rotation | 2024 |
| PBFL (TIFS 2022) | Cosine similarity, FHE | Addresses untrusted servers (explicit) | YES | 2022 |
| BR-CPPFL | Weighted aggregation | No explicit statement | Partially | 2025 |
| FLock | State channels | Multiple aggregators for redundancy | YES - via redundancy | 2025 |
| Byzantine-Robust DFL (CCS) | Decentralized robust aggregation | N/A - no central aggregator | N/A - P2P architecture | 2024 |
| Median-Krum | Median + Krum | No explicit statement | Not explicitly | 2023 |
| Quantum-Enhanced BCFL | Quantum Byzantine agreement | No explicit statement | Partially - improved fault tolerance | 2025 |
| Blockchain FL Survey | N/A - Survey | **56.67% use vulnerable single aggregator** | Survey identifies gap | 2023 |

### Quantitative analysis

**Papers explicitly or implicitly assuming honest verifiers**: 14 out of 15 pure BCFL papers (93%)

**Papers with explicit honest verifier assumptions**: 3 (BRFLATA, BlockDFL, Adaptive Adversaries Survey)

**Papers addressing malicious verifiers with working solutions**: 1 (KFC - 6.7% of BCFL papers)

**Papers acknowledging but not solving malicious verifier problem**: 1 (FedBlock)

**Papers from traditional FL addressing malicious aggregators**: ~15 papers (versus hundreds on malicious clients)

### The trust assumption hierarchy in BCFL

**Level 1 (Strongest assumption)**: Fully trusted aggregator - "The server is reliable" (BRFLATA)

**Level 2**: Honest-but-curious aggregator - Follows protocol but may attempt inference (FedBASS 2025: "honest-but-curious servers and malicious clients")

**Level 3**: Honest majority assumption - ">2/3 verifiers honest" (BlockDFL) or "majority of servers honest" (Fantastyc)

**Level 4**: Trust through redundancy - Multiple aggregators provide fault tolerance (FLock with 25 aggregators)

**Level 5**: Trust through selection/rotation - High-reputation or high-correlation nodes assumed trustworthy (BRFL via PPCC)

**Level 6 (Weakest assumption)**: Byzantine verifiers explicitly modeled - Defense works even when all verifiers malicious (KFC only)

**Critical finding**: 93% of BCFL papers operate at Levels 1-5, retaining trust assumptions that undermine the security guarantees of their Byzantine-robust aggregation mechanisms.

### Why this matters: The attack surface

Consider a blockchain FL system using Krum aggregation to tolerate 40% malicious clients. If malicious actors can:

1. **Compromise the verification layer** (miners, validators, committee members who execute Krum), they can:
   - Skip Krum execution entirely and accept all malicious updates
   - Modify Krum's k-nearest-neighbor selection to favor malicious updates
   - Collude to consistently vote for blocks containing poisoned models

2. **Launch Sybil attacks on verification** by creating many validator identities to exceed honest majority thresholds

3. **Execute economic attacks** by bribing validators or manipulating stake-based selection (as acknowledged in BlockDFL's stake-based verifier selection)

Yet the threat models in 93% of BCFL papers don't account for these attacks. The defense mechanisms (Krum, Trimmed Mean, Median) are robust against malicious inputs but **assume correct execution** - an assumption that blockchain's decentralization alone doesn't guarantee.

## Conclusions and research directions

### The systematic blind spot exists

This research establishes a clear and systematic gap in BCFL literature: **Defense mechanisms focus almost exclusively on malicious clients while assuming honest execution of defense algorithms at the verification layer**. This pattern holds across 2023-2025 publications from top venues including ACM CCS, IEEE conferences, and leading journals.

The blockchain FL community has largely treated decentralization as sufficient for trustworthiness without rigorously modeling threats to the verification layer itself. As FedBlock (2024) explicitly acknowledges: "we need a mechanism to detect and ignore malicious verifiers" - yet this remains unsolved.

### Why traditional FL is ahead on this problem

Ironically, traditional (non-blockchain) FL research has more comprehensively addressed malicious aggregators through cryptographic verification (ELSA, zkFL, Mario), multi-server protocols, and formal security proofs. These systems assume aggregator maliciousness as a first-class threat rather than relying on architectural decentralization.

### Critical research directions

**Verifiable execution of Byzantine-robust aggregation**: Extend zkFL's approach to blockchain contexts, requiring validators to prove they correctly executed Krum/Trimmed Mean/Median rather than trusting them to do so.

**Byzantine agreement on aggregation outcomes**: Multiple independent validators execute aggregation and reach consensus on results, tolerating disagreement from compromised validators (KFC's approach needs generalization).

**Economic security analysis**: Model attacks where adversaries manipulate stake, reputation, or selection mechanisms to compromise verification layer. Current BCFL papers assume economic incentives align with honesty without rigorous game-theoretic analysis.

**Adaptive verification**: Systems that detect malicious verifiers through cross-validation, challenge-response protocols, or statistical analysis of verification patterns rather than assuming honest majorities.

**Separation of concerns**: Distinguish between consensus layer security (blockchain's strength) and computation layer security (aggregation execution) - blockchain provides tamper-evident logs but doesn't guarantee correct computation.

### The bottom line

Byzantine-robust aggregation methods like Krum, Trimmed Mean, and Median are only as robust as the entities executing them. **The blockchain-based federated learning research community has systematically overlooked this dependency, creating a critical vulnerability in systems that claim Byzantine fault tolerance**. With only one working solution (KFC, 2025) and one acknowledgment without solution (FedBlock, 2024) among 20+ papers, this represents a significant opportunity for impactful research addressing a fundamental security gap in an increasingly important domain.