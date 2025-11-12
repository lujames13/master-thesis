# zkML in Blockchain-Based Federated Learning: A Technical Analysis of Applications, Viability, and Critical Limitations

## 1. Executive Summary

This report provides a technical investigation into the application of Zero-Knowledge Machine Learning (zkML) within blockchain-based Federated Learning (FL) systems. zkML is an emerging cryptographic technique that enables a party to generate a succinct, verifiable proof of a machine learning computation's integrity.

In the context of blockchain-based FL, its primary application is to provide a "trustless" mechanism for on-chain verification. This allows a central aggregator to perform computationally expensive model aggregation off-chain and then prove to an on-chain smart contract that the aggregation was performed correctly, without revealing any private client data.

### Key Finding

While zkML provides the strongest possible cryptographic guarantee of computational integrity ("math-based trust"), its practical application in FL is severely constrained by fundamental limitations in scalability, generality, and efficiency. Current zkML technology is viable only for small, specialized models—with a practical upper bound in the range of 18 million parameters—and simple, linear aggregation algorithms such as Federated Averaging (FedAvg).

### Four Critical Limitations

This report quantifies four critical limitations that currently render zkML non-viable for large-scale, general-purpose FL systems:

#### 1. Memory and Model Size Constraints

There is a significant disconnect between the scale of modern ML and the capabilities of zkML. Proving computations for large-scale models is described by researchers as "totally impractical". Proving a 7B-parameter LLaMA model aggregation, for example, is estimated to require memory on the order of "TB or even PB levels," compared to a <32GB requirement for native execution. More extreme estimates for a 138M-parameter VGG16 model suggest a proof generation time of "10 years" with key sizes exceeding "1,000 TB".

#### 2. Computational Generality

zkML's reliance on arithmetic circuits makes it unsuitable for the complex, non-linear, and iterative logic required by Byzantine-robust aggregation algorithms. This creates a "catch-22": the algorithms that are verifiable (like FedAvg) are not robust to the attacks that on-chain verification is meant to prevent, while the algorithms that are robust (like Krum) are not practically verifiable.

#### 3. Proof Generation Efficiency

Generating a ZK proof is "orders of magnitude slower" than the native computation itself. Benchmarks for FL aggregation demonstrate this bottleneck, with proof times ranging from over 170 seconds for a simple MLP aggregation to approximately 55 minutes for a ResNet50 aggregation.

#### 4. Precision and Determinism

ZKPs cannot natively handle floating-point arithmetic, mandating that all ML models be "quantized" to fixed-point arithmetic. While modern techniques have minimized the accuracy impact of this conversion to as low as 0.01%, it adds a mandatory, complex pre-processing step to the MLOps pipeline and forces a sub-optimal, deterministic execution path.

### Conclusion

This report concludes that for large-scale, general-purpose FL, zkML is not a viable solution at present. Alternative approaches, such as optimistic verification (opML) for scalability and Trusted Execution Environments (TEEs) for performance, offer more practical, albeit different, trust trade-offs.

---

## 2. Technical Background: Verifiable Computation in FL

### 2.1. Defining Zero-Knowledge Machine Learning (zkML)

Zero-Knowledge Machine Learning (zkML) is a technology stack that integrates Zero-Knowledge Proofs (ZKPs) with machine learning algorithms. A ZKP is a cryptographic protocol where one party (the prover) can prove to another party (the verifier) that a statement is true, without revealing any information beyond the validity of the statement itself.

In the context of machine learning, zkML's primary function is to prove computational integrity. It provides a verifiable, mathematical guarantee that a specific computation (e.g., a model's inference or, in this report's focus, an aggregation of models) was executed correctly. This ability to verify computation without re-execution or access to private data solves a fundamental "trust gap" in decentralized systems.

#### Distinguishing zkML from Other Privacy-Preserving Techniques

It is critical to distinguish zkML from other privacy-preserving ML techniques. zkML is not typically used for training on encrypted data; that is the domain of Fully Homomorphic Encryption (FHE). Instead, zkML is used to prove that a known (or private) ML model was executed correctly on known (or private) inputs to produce a given output. In the FL context, this allows an untrusted aggregator to prove it faithfully executed the Aggregate() function without deviation or manipulation.

### 2.2. The Role of zkML in Blockchain Systems

Blockchains, such as Ethereum, are secure and decentralized but are also computationally weak and prohibitively expensive environments. Executing complex computations, like aggregating a neural network's parameters, directly on-chain via a smart contract is not feasible due to gas limits and cost.

zkML provides a solution via the "off-chain compute, on-chain verify" paradigm. This workflow unfolds as follows:

**Off-Chain Computation**: An FL aggregator (or any prover) performs the resource-intensive ML computation (e.g., model aggregation) on a powerful, off-chain machine where computation is cheap and fast.

**Off-Chain Proof Generation**: Concurrently, the prover feeds this computation into a ZK proving system to generate a succinct cryptographic proof (e.g., a zk-SNARK) that attests to the computation's correctness.

**On-Chain Verification**: The prover submits this small, succinct proof to a verifier smart contract on the blockchain.

**On-Chain State Change**: The smart contract executes a verify() function on the proof. This verification step is computationally trivial and extremely cheap (low gas cost). If the proof is valid, the smart contract accepts the result of the off-chain computation as truth and can trigger a state change, such as updating the on-chain hash of the new global model.

This mechanism effectively "amplifies" the capabilities of smart contracts, allowing them to exercise judgment and act on the results of complex computations performed in the off-chain world.

### 2.3. Underlying ZK Proof Systems: A Brief Comparison

The trade-offs of zkML are directly inherited from the underlying ZKP systems. The choice of system dictates the performance, security, and cost of the entire verification workflow.

#### zk-SNARKs (Zero-Knowledge Succinct Non-Interactive Argument of Knowledge)

**Description**: This is a class of ZKPs, with Groth16 being a popular implementation. Their defining features are succinctness (very small proof sizes, often a few hundred bytes) and extremely fast, constant-time verification ($O(1)$).

**FL Context**: The fast, constant-time verification is ideal for on-chain smart contracts, as it translates to minimal and predictable gas costs.

**Limitation**: Most classic zk-SNARKs, like Groth16, require a trusted setup for each new circuit. This is a cryptographic ceremony that generates a proving key and a verification key. If the secret parameters (often called "toxic waste") used in this ceremony are not destroyed, an attacker could forge invalid proofs. This presents a significant security and operational burden, as a new ceremony is required every time the model architecture (and thus the circuit) changes.

#### zk-STARKs (Zero-Knowledge Scalable Transparent Argument of Knowledge)

**Description**: STARKs are defined by their transparency—they require no trusted setup. They are also quantum-resistant, a significant long-term security advantage.

**FL Context**: The lack of a trusted setup makes them operationally superior for rapidly iterating on FL models.

**Limitation**: STARKs are not as "succinct" as SNARKs. Proof sizes are larger (quasilinear, $O(\log^2 n)$) and, critically, on-chain verification time is also quasilinear ($O(\log^2 n)$). This translates to "larger proofs" and "more computing power" for verification, making them "more costly" in on-chain gas fees compared to SNARKs.

#### Modern Systems (e.g., PLONK, Halo2, Plonky2)

**Description**: These systems, often called "modern SNARKs" or "SNARK-like" constructions, seek to achieve a practical balance. Systems like PLONK and Halo2 (which is used by the EZKL framework) often use a universal and updateable setup. This "setup" is performed once and can be re-used for any circuit up to a certain size, eliminating the per-circuit setup burden of Groth16.

**FL Context**: This "setup once, use for any model" (or "transparent") approach, combined with efficient proof generation and relatively fast verification, has made these systems the de facto standard for current zkML development.

---

## 3. Implementation in Blockchain-Based Federated Learning

### 3.1. Verifiable Aggregation: The Computational Workflow

In a typical blockchain-based FL system, the goal of zkML is not to verify the local client training—which is a far more complex problem involving privacy and intractable proof costs. Instead, the primary use case is to verify the aggregator. This ensures that the entity responsible for combining client models does so faithfully.

A single round of zkML-verified aggregation follows a precise workflow:

**Local Training (Off-Chain)**: A cohort of clients (e.g., 100 participants) independently trains their local models on their private data. This step is not proven with ZK.

**Model Submission (Off-Chain)**: Clients encrypt and submit their local model updates (e.g., $w_i$) to a single, off-chain aggregator node.

**Aggregation and Proof Generation (Off-Chain)**: The aggregator node performs two tasks in parallel:

- **Computation**: It decrypts the client updates and executes the aggregation algorithm (e.g., FedAvg) to compute the new global model, $w_{global} = \sum_{i=1}^{n} \frac{1}{n} w_i$.
- **Proof Generation**: It feeds the inputs (client models) and the computation logic into a ZK proving system to generate a cryptographic proof, $\pi$, which attests: "I correctly computed $w_{global}$ from these inputs using the publicly agreed-upon FedAvg algorithm".

**Verification and State Update (On-Chain)**: The aggregator submits the new global model $w_{global}$ (or its hash) and the proof $\pi$ to a verifier smart contract on the blockchain.

**Finality (On-Chain)**: The smart contract executes the verify(w_{global}, \pi) function. This function is extremely cheap. If it returns true, the contract updates its internal state to recognize the new global model as canonical and can autonomously trigger incentive payments to the clients and the aggregator.

This workflow successfully outsources the "heavy" computation off-chain while retaining the "high" trust and verifiability of the blockchain.

### 3.2. From ML to Circuits: The Arithmetization Challenge

The most significant technical hurdle is that ZK proving systems do not understand high-level programming languages like Python or ML frameworks like PyTorch. ZKPs operate on a low-level mathematical construct known as an arithmetic circuit. These circuits are composed solely of addition and multiplication gates over a finite field.

Therefore, to prove an FL aggregation, the entire aggregation algorithm must be "arithmetized"—that is, decomposed and re-written as a massive system of polynomial equations.

#### Simple Case (FedAvg)

For a simple algorithm like FedAvg, this process is straightforward. A weighted average, $W_{global} = (W_1 \times 0.5) + (W_2 \times 0.5)$, is already composed of additions and multiplications. This maps cleanly to a "degree-two arithmetic circuit" and is highly compatible with ZKP systems.

#### Complex Case (General ML)

For general machine learning models, this process is handled by a zkML compiler. These compilers take a standard model format (like ONNX, which can be exported from PyTorch or TensorFlow) and automatically translate its layers (e.g., convolutions, linear layers, ReLU activations) into a corresponding set of arithmetic constraints, or "gadgets".

### 3.3. Survey of Existing Projects and Frameworks

Several key projects have emerged to tackle the "arithmetization" and proving challenge, representing two distinct architectural philosophies.

#### EZKL

This is a leading model-to-circuit compiler. It provides a library and command-line tool that ingests ONNX files (exported from PyTorch or TensorFlow) and compiles them into ZK circuits using the Halo2 proving system. It is noted for its developer-friendliness, abstracting away most of the complex cryptography. It has been used in proof-of-concept blockchain-based FL systems, for example, to verify model aggregation on Hyperledger Fabric.

#### Risc Zero

This project represents a fundamentally different approach: the general-purpose zkVM (Zero-Knowledge Virtual Machine). Instead of compiling the ML model into a circuit, Risc Zero allows a developer to write their aggregation logic in a standard language like Rust or C++. The Risc Zero zkVM then executes this program and generates a ZK proof of the entire program's execution. One academic paper explicitly uses this architecture, building a ZKVM on all FL nodes and running the ML algorithm as a "guest program" within the ZKVM to generate proofs.

#### Modulus Labs

This is a research-focused organization that has pushed the state-of-the-art in verifiable model size. They are known for benchmarking various ZKP systems for on-chain inference and have demonstrated verification for models with up to 18 million parameters. Their work includes a "zkPredictor" built in collaboration with the Allora network.

#### Architectural Trade-offs

These projects highlight a core architectural trade-off. The circuit-compiler approach (EZKL) is highly optimized for specific ML operations, resulting in "blazing fast" performance for the tasks it supports. Benchmarks on simple linear regression, for example, show EZKL proof generation at 0.118 seconds. The general-purpose zkVM approach (Risc Zero) offers far greater generality and a superior developer experience, as any logic can be written in Rust. However, this generality comes at a staggering performance cost: the ZKVM must prove every single CPU instruction of the virtual machine, not just the core mathematical operations. The same linear regression benchmark on Risc Zero took 10.028 seconds—over 85 times slower than the specialized compiler.

This schism presents a difficult choice for FL architects: the compiler path (EZKL) is performant but too restrictive to support the robust, complex aggregation algorithms needed for a trustless setting. Conversely, the zkVM path (Risc Zero) is general enough to support such algorithms but is likely too slow to be practical for large-scale model aggregation.

---

## 4. Critical Limitations of zkML in Federated Learning

While zkML offers a powerful vision, its practical deployment in blockchain-based FL is severely hindered by four interconnected and critical limitations. This section provides a quantitative analysis of these constraints.

### 4.1. Memory and Model Size Constraints

The most significant blocker for zkML is its inability to scale with the size and complexity of modern machine learning models. The computational and memory resources required to generate a ZK proof for a large model are astronomical.

#### Impractical Upper Bounds (100M+ Parameters)

Research surveying the ZKP-VML (Verifiable Machine Learning) landscape provides a stark example. For a VGG16 neural network with 138 million parameters, generating a proof using the Groth16 zk-SNARK scheme is estimated to take a "staggering 10 years". Furthermore, the keys required to generate and verify this proof (the proving key and verification key) would exceed "1,000 TB" in size. While this estimate is for a specific (and perhaps non-optimized) setup, it illustrates the exponential nature of the problem.

#### Impractical LLM Scale (7B+ Parameters)

This problem persists for modern Large Language Models (LLMs). In a direct comparison between zkML and optimistic verification (opML), researchers concluded that applying zkML to a 7B LLaMA model is "totally impractical". The memory consumption for generating the ZK circuit for a model of this scale is estimated to be on the order of "TB or even PB levels". In contrast, an optimistic system can execute the same model in a native environment with less than 32GB of RAM.

#### Practical State-of-the-Art (10M+ Parameters)

The current, practical (i.e., demonstrated, not theoretical) upper bound for zkML verification is orders of magnitude smaller. Work by Modulus Labs, a leader in the field, has presented benchmarks for verifying models with up to 18 million parameters.

This reveals a gap of over 1,000x between the largest practical zkML models (~18M) and the desired large-scale models (~7B-175B) common in today's ML landscape.

#### Differentiating Inference from Aggregation

It is crucial to differentiate the FL aggregation use case from the more commonly cited inference use case. Recent, highly publicized zkML projects (e.g., zkLLM) have demonstrated proof generation for 13B-parameter model inference in under 15 minutes. This apparent contradiction arises from a fundamental technical difference.

**Proving Inference** (Output = Model(Input)) involves proving the execution of the model architecture, where the model's parameters (weights) are often treated as a public, pre-committed input. The circuit size scales with the architecture and input size.

**Proving FL Aggregation** ($w_{global} = \sum w_i$) involves a computation over the parameters themselves. The entire set of model parameters from all clients is a variable input to the aggregation circuit.

Consequently, the circuit for FL aggregation scales directly with the number of parameters being aggregated, making it a fundamentally larger and more complex computation. The "impractical" TB-scale memory estimates are therefore more relevant to the FL aggregation use case than the more optimistic "zkLLM-for-inference" benchmarks.

### 4.2. Computational Generality

The second critical limitation is zkML's lack of generality. Because all computations must be "arithmetized" into add/multiply gates, zkML is only practical for a very narrow subset of algorithms.

#### Supported Algorithms (Simple Arithmetic)

zkML is well-suited for computations that are inherently arithmetic. The standard FedAvg algorithm (a weighted average of client models) is the canonical example. Its logic is nothing more than a large set of multiplications and additions, which maps perfectly to a "degree-two arithmetic circuit".

#### Unsupported Algorithms (Complex Logic)

The primary motivation for using a blockchain to verify FL is to provide robustness against attacks, particularly from Byzantine (malicious) clients. However, FedAvg is not Byzantine-robust; a single malicious client submitting a poisoned model can completely corrupt the global model.

This creates a "catch-22":

To secure the FL process, Byzantine-robust aggregation algorithms (e.g., Krum, FedProx, q-FedAvg, Median) are required. These robust algorithms are, by definition, not simple arithmetic. Krum, for example, requires the aggregator to calculate all pairwise Euclidean distances between client updates, sort them, and select the n-f-2 updates that are "closest" to each other.

These operations—such as calculating distances, sorting, finding medians, or (in other algorithms) performing iterative clustering—are complex, iterative, and non-arithmetic. Translating them into a ZK circuit is prohibitively expensive and, in most cases, considered computationally infeasible with current technology.

Even the most advanced zkML compilers, like EZKL or zkPyTorch, do not support this arbitrary logic. They are designed to compile a limited subset of ML operations (e.g., linear layers, convolutions, and specific activation functions like ReLU). They cannot compile the arbitrary programmatic logic of an algorithm like Krum.

#### The Fundamental Problem

Therefore, zkML can only be used to verify the FL algorithms (like FedAvg) that are already vulnerable to the very attacks that on-chain verification is intended to prevent. It cannot currently be used to verify the robust algorithms that are most needed in a trustless environment.

### 4.3. Proof Generation Efficiency

Even for the simple, arithmetic-friendly models that zkML can support, the performance overhead of proof generation is a major bottleneck. Generating the proof is computationally "many times more" intensive than running the original computation. One paper describes the zkML pipeline as "orders of magnitude slower" than native execution.

This is not a theoretical concern. Benchmarks from FL-specific research show debilitating proof times:

**MLP Aggregation**: In a paper proposing a verifiable FL system, the proof time for "model detection and aggregation" for even a simple Multi-Layer Perceptron (MLP) model was reported to be more than 170 seconds.

**ResNet50 Aggregation**: A more complex (but still small) model, ResNet50, was benchmarked in a blockchain-based zkFL system using the Halo2 prover. The proof generation time for a single aggregation round was approximately 54.72 minutes.

A 55-minute delay for a single aggregation round is untenable for any practical FL system. While highly optimized compilers like EZKL can achieve sub-second proof times for extremely simple models (e.g., 0.118s for a linear regression), the data clearly shows that proof times scale rapidly with model complexity, becoming a critical bottleneck.

#### Hardware Requirements

This poor performance necessitates the use of high-performance hardware. ZK proofs are bottlenecked by specific cryptographic operations, primarily Multi-Scalar Multiplication (MSM) and Number-Theoretic Transforms (NTT). To make proof generation practical, hardware acceleration (GPUs/FPGAs) is mandatory, not optional.

Recent developments, such as the Icicle library for GPU acceleration, have shown a 98% reduction in MSM time and a 35% reduction in total proof time. While promising, this reliance on specialized, high-end hardware for the aggregator node adds significant cost and centralization pressure, undermining some of the decentralized ethos.

### 4.4. Precision and Determinism

The final critical limitation stems from a fundamental mismatch between the mathematics of ML and the mathematics of ZKPs.

#### The Floating-Point Problem

Modern ML models are built on floating-point arithmetic (e.g., FP32, BF16) to handle continuous values. ZK proof systems, however, operate over finite fields—mathematical structures based on large integers modulo a prime number. These two domains are mathematically incompatible.

#### The Solution: Quantization

The only practical solution is to quantize the ML model. This is a mandatory pre-processing step for all current zkML frameworks. It involves converting all floating-point numbers (model weights, gradients, activations) into fixed-point integers that can be represented in the finite field.

#### Impact on Accuracy

This conversion inherently causes a loss of precision. This creates a direct trade-off for the system designer: using lower precision (e.g., 8-bit integers) makes the ZK circuits dramatically smaller and faster but can lead to "slight accuracy degradation".

However, this problem is being actively and successfully researched. Quantization-Aware Training (QAT) can be used to train models that are robust to this precision loss. One paper demonstrated that a VGG16 model converted for ZK-SNARKs had an accuracy difference of only 0.01% compared to its floating-point original. Furthermore, new frameworks like the 'ZEN' system are being designed to convert PyTorch models into ZK-friendly circuits without "causing additional accuracy loss" relative to standard quantization techniques.

#### The Determinism Problem

A more subtle issue is that ZKPs require perfect, bitwise determinism. A computation, when proven, must produce the exact same result every time. However, native ML execution, especially on parallel hardware like GPUs, is "inherently nondeterministic" due to variations in floating-point operation order. This forces zkML frameworks to use a specific, non-native execution schedule, sacrificing the performance and optimizations of native ML frameworks.

While the accuracy-loss problem is largely manageable, the requirement to quantize and enforce determinism adds a significant layer of MLOps complexity and fragility to the entire system.

---

## 5. Comparison Table: zkML vs. Alternative Verification Methods

The critical limitations of zkML do not exist in a vacuum. Architects of decentralized AI systems must evaluate these trade-offs against the primary alternatives: Optimistic Machine Learning (opML) and Trusted Execution Environments (TEEs).

### Alternative Approaches

**opML (Optimistic Verification)**: This approach (e.g., opML, Truebit) uses a "fraud-proof" system, similar to Optimistic Rollups in blockchain scaling. The aggregator "optimistically" posts their result on-chain, and a "challenge period" opens. Any off-chain "watcher" can re-compute the result and challenge it if it's fraudulent. A challenge triggers an on-chain "verification game" (bisection protocol) to identify the single, specific-erroneous step, which is then re-executed on-chain.

**TEEs (Hardware Attestation)**: This approach (e.g., Intel SGX, NVIDIA H100 Confidential Computing) uses a secure "black box" in the hardware. The aggregator performs the computation inside this secure enclave. The TEE then produces a cryptographic attestation (a signature) proving that the correct code was executed on the correct data within the secure, untampered hardware. This attestation is submitted on-chain for verification.

### Comprehensive Comparison

| Dimension | zkML (Validity Proofs) | opML (Fraud Proofs) | TEEs (e.g., Intel SGX, NVIDIA H100 CC) |
|-----------|------------------------|---------------------|----------------------------------------|
| **Verification Method** | On-chain verification of a cryptographic validity proof (succinct). | Off-chain "watchers" challenge invalid state. On-chain arbitration via fraud proof (bisection protocol) if challenged. | Off-chain hardware attestation. On-chain check of the attestation signature. |
| **Security Model** | Cryptographic ("Trustless"). Relies only on mathematics and cryptographic assumptions. | Crypto-economic ("1-of-N Honest"). Relies on at least one honest validator being online to challenge fraud. | Hardware-based ("Trust in Vendor"). Relies on trusting the hardware manufacturer (Intel, NVIDIA) and its supply chain. |
| **Computational Universality** | Very Low. Restricted to operations that can be efficiently arithmetized (e.g., FedAvg). Cannot support arbitrary logic or complex algorithms (e.g., Krum). | High. Supports native execution in any environment (PyTorch, TensorFlow). Arbitrary computation is possible. | High. Supports native execution of arbitrary code inside the secure enclave. |
| **Model Scale Support** | Very Low. "Impractical" for 7B+ models (TBs/PBs of RAM). Practical limit ~18M params. | High. Can handle 7B LLaMA models with <32GB RAM. | High. Near-native performance on 13B+ LLMs (e.g., <7% overhead on H100 CC). |
| **Proof/Execution Cost** | Extremely High. "Orders of magnitude slower". Proof generation takes seconds to minutes or hours (e.g., 55 mins for ResNet50). | Low. Native execution speed. No overhead unless challenged. | Very Low. Near-native execution speed (e.g., <7% latency overhead on H100 CC). |
| **Verification Cost (On-Chain)** | Low. Succinct proof verification is computationally cheap (e.g., Groth16). | Very Low (in aggregate). No cost if unchallenged. Gas cost is high during a dispute, but this is designed to be rare. | Very Low. Verifying a hardware attestation signature on-chain is a cheap and standard operation. |
| **Finality** | Slow. Time-to-Proof. Finality is achieved only once the (slow) proof is generated and verified on-chain. | Very Slow. Time-to-Challenge-Period. Finality is achieved only after a long (e.g., 1-7 day) challenge window closes. | Fast. Finality is achieved as soon as the (fast) computation and attestation are complete and verified on-chain. |
| **Hardware Requirements** | Requires high-performance GPUs/FPGAs for the prover to be practical. | Can run on standard CPU/GPU. | Requires specialized, trusted hardware (SGX, H100 CC) for all compute nodes. |

### Key Insights

This comparison reveals a clear "trilemma" for verifiable computation: architects must choose between Trust, Scale, and Performance.

- **zkML** optimizes only for Trust (cryptographic), at the severe expense of Scale and Performance.
- **opML** optimizes only for Scale (it is the only one that supports 7B+ models), at the expense of Trust (a weaker 1-of-N model) and Performance (very slow finality).
- **TEEs** optimize only for Performance (near-native speed), at the expense of Trust (a centralized, hardware-based model).

For the specified use case of blockchain-based Federated Learning, zkML is not a practical, general-purpose solution today. A project needing to support large-scale models must choose opML. A project needing high-speed, private computation must choose TEEs. zkML is currently viable only for niche applications with very small models where "math-based trust" is the single, non-negotiable priority that outweighs all other practical considerations.

---

## 6. Conclusion

This report has conducted a technical analysis of the application, viability, and limitations of Zero-Knowledge Machine Learning (zkML) in the context of blockchain-based Federated Learning (FL). The analysis confirms that zkML provides the "gold standard" of computational integrity, offering a path to on-chain verification of off-chain computation that relies purely on cryptographic assumptions.

However, a sober assessment of the current state-of-the-art reveals that zkML is not a practical or viable solution for large-scale, general-purpose FL systems. The technology is constrained by four critical limitations that, in combination, present insurmountable hurdles for most real-world applications:

### Four Critical Limitations

**Prohibitive Scale**: The memory and computational costs to prove large models (e.g., 7B+ parameters) are "totally impractical," estimated in Terabytes or Petabytes of RAM. The practical limit (sub-18M parameters) is misaligned with the direction of modern machine learning.

**Paralyzing Generality**: A "catch-22" exists where zkML can only verify simple, arithmetic-friendly aggregation algorithms like FedAvg, which are known to be vulnerable to the Byzantine attacks that on-chain verification is intended to solve. Robust algorithms like Krum remain computationally infeasible to prove.

**Intolerable Inefficiency**: Proof generation is "orders of magnitude slower" than native computation. Benchmarks showing proof times of 170 seconds to 55 minutes for a single aggregation round are operationally non-viable.

**Inherent Complexity**: The mandatory requirement for fixed-point quantization and enforcement of determinism adds significant fragility and engineering complexity to the entire system, even if accuracy loss can be managed.

### Final Assessment

The comparison with alternatives (Table 5) solidifies this conclusion. Optimistic verification (opML) is the only current decentralized solution that can support large-scale models, while TEEs are the only solution that offers near-native performance.

The future of zkML in this domain depends on fundamental breakthroughs in ZK proof systems, widespread adoption of specialized hardware acceleration (GPUs/FPGAs), and the development of novel, "ZK-friendly" robust aggregation algorithms. Until such breakthroughs occur, this report concludes that for practical, large-scale deployment, architects of decentralized FL systems must look to opML (for scale) or TEEs (for performance), treating zkML as a long-term, but not-yet-practical, research-oriented goal.

---

## 7. References

[1] Z. Xing et al., "Zero-Knowledge Proof-based Verifiable Decentralized Machine Learning in Communication Network: A Comprehensive Survey," *arXiv preprint arXiv:2310.14848*, 2023.

[2] K. Conway et al., "opML: Optimistic Machine Learning on Blockchain," *arXiv preprint arXiv:2401.17555*, 2024.

[3] J. Yao et al., "Nondeterminism-Aware Optimistic Verification for Floating-Point Neural Networks," *arXiv preprint*, Oct. 2025.

[4] A. Author, "Zero-Knowledge Proof-Based Gradient Aggregation for Federated Learning," *IEEE Trans. Big Data*, vol. XX, no. XX, pp. XX-XX, Feb. 2025.

[5] A. Author, "Advancing Federated Learning through Verifiable Computations and Homomorphic Encryption," *Entropy*, vol. 25, no. 11, p. 1550, 2023.

[6] Z. Peng et al., "A Survey of Zero-Knowledge Proof Based Verifiable Machine Learning," *arXiv preprint arXiv:2502.18535*, 2025.

[7] D. Kang, K. Gurkan, and A. Rose, "Scaling up Trustless DNN Inference with Zero-Knowledge Proofs," in *Proc. NeurIPS RegulateML Workshop*, 2023.

[8] P. Blanchard et al., "Machine Learning with Adversaries: Byzantine Tolerant Gradient Descent," in *Proc. Advances in Neural Information Processing Systems (NeurIPS)*, 2017.

[9] Kudelski Security, "zkML: Verifiable Machine Learning Using Zero-Knowledge Proof," *Modern CISO Blog*, 2024.

[10] EZKL, "Benchmarks," *EZKL Blog*, 2024.

[11] SOTA zk, "Zero-Knowledge Proofs in Machine Learning: A Comprehensive Guide," *SOTA zk Insights*, Oct. 22, 2024.

[12] K. Chen et al., "ZKML: A System for Machine Learning Inference in Zero-Knowledge Proofs," in *Proc. EuroSys*, 2024.

[13] J. McAfee, "zkML: Evolving the Intelligence of Smart Contracts Through Zero-Knowledge Cryptography," *1kxnetwork*, 2023.

[14] A. Author, "zkML 101: A Beginner's Guide to Zero-Knowledge Machine Learning," *Arpa Medium*, 2024.

[15] L. Franceschini, "A Guide to Zero-Knowledge Proofs," *Medium*, 2024.

[16] T. Author, "AI Meets Zero-Knowledge: What is zkML and Why Does It Matter?" *CoinMonks Medium*, 2024.

[17] A. Author, "ZKML: Bringing Verifiable and Trustless ML to the Masses," *dev.to*, 2024.

[18] Hacken, "ZK-SNARK vs ZK-STARK: A Detailed Comparison," *Hacken.io*, 2024.

[19] T. Author, "Zero-Knowledge Machine Learning (zkML)," *Ledger Academy*, Mar. 25, 2025.

[20] Vara Network, "ZKML," *Vara Wiki*, 2024.

[21] J. Morton, "We'll start with the why of ZKML," *Zkonduit*, 2023.

[22] CoinAPI, "zkML: Zero-Knowledge Machine Learning," *CoinAPI Learn*, 2024.

[23] M. Bahrami, "Decentralized Federated Learning on Blockchain using Zero Knowledge Proofs," *Tesi Luiss*, 2024.

[24] R. Garcia, "zkPoT: A Zero-Knowledge Proof of Training Protocol," *Utu Pub*, 2024.

[25] A. Author, "Veri-CS-FL: Verifiable Client Selection for Federated Learning with Zero-Knowledge Proof," *arXiv preprint arXiv:2503.15550*, 2025.

[26] S. Author et al., "A Secure and Efficient Federated Averaging based on Zero-Knowledge Proofs," *MDPI Electronics*, vol. 13, no. 1, p. 86, 2024.

[27] A. Author, "A Zero-Knowledge Proof-Based Aggregation Scheme for Federated Machine Learning," *IEEE Trans. Dependable Secure Comput.*, 2024.

[28] A. Author, "Trusted Aggregation for Decentralized Federated Learning in Healthcare Consumer Electronics Using Zero-Knowledge Proofs," *ResearchGate*, 2025.

[29] T. Author, "Decentralized AI Systems: Cryptographic Infrastructures, Verifiable Computation, and Federated Learning," *LightcapAI Medium*, 2024.

[30] NP-Hard-LLC, "zkML: Tradeoffs in accuracy vs. proving cost," *np.engineering*, Jul. 24, 2024.

[31] A. Author et al., "A Survey of Zero-Knowledge Machine Learning," *arXiv preprint arXiv:2505.20136*, 2025.

[32] A. Author, "VeriLLM: A Verifiable and Privacy-Preserving Large Language Model Inference System," *arXiv preprint arXiv:2509.24257*, 2025.

[33] G. Author et al., "Kinic's Use of ZK and LLMs for Privacy-Preserving Data on ICP," *Medium*, 2024.

[34] T. Sun et al., "zkLLM: Efficient Zero-Knowledge Proofs for Large Language Models," *arXiv preprint arXiv:2404.16109*, 2024.

[35] C. Weng et al., "Mystique: Efficient conversions for Zero-Knowledge Proofs with applications to Machine Learning," *arXiv preprint arXiv:2304.05590*, 2023.

[36] M. Author, "Exploring and Investigating Federated Learning Aggregation Algorithms," *MDPI Electronics*, vol. 12, no. 10, p. 2287, 2023.

[37] S. Author et al., "zkPyTorch: A Framework for Zero-Knowledge Proofs in PyTorch," *Polyhedra Network Blog*, 2024.

[38] D. Kang et al., "ZKML: An Optimizing Compiler for ML Inference in Zero-Knowledge Proofs," *arXiv preprint arXiv:2403.22573*, 2024.

[39] A. Author, "zkdl: Efficient zero-knowledge proofs of deep learning training," *arXiv preprint arXiv:2307.16273*, 2023.

[40] A. Author, "Trustworthy Reputation for Federated Learning in O-RAN Using Blockchain and Smart Contracts," *Unity-6G*, 2025.

[41] N. Luza, "Secure Data Sharing in the Internet of Vehicles Using Blockchain-based Federated Learning," *GitHub*, 2024.

[42] T. Author, "zkML: Evolving the intelligence of smart contracts through zero-knowledge cryptography," *Accelxr.eth Paragraph*, 2024.

[43] J. Author, "A review on floating points in zero-knowledge proof systems," *ICME Blog*, 2024.

[44] N. Author, "How Quantization-Aware Training Enables Low-Precision Accuracy Recovery," *NVIDIA Developer Blog*, 2024.

[45] D. Author, "opML vs. zkML: On-chain AI Verification Methods," *Oasis Network Blog*, 2024.

[46] G. Author, "To Trust or Not to Trust: ZKML as an Answer to Big Tech's Influence on AI," *Symbolic Capital*, 2024.

[47] M. Author, "Memory-Efficient Deep Learning Inference in Trusted Execution Environments," *ResearchGate*, 2021.

[48] R. Author, "Private Verifiable and Auditable AI Systems," *ResearchGate*, 2025.

[49] N. Gupta et al., "RESAM: A Unified Framework for Optimal Byzantine Resilience in Distributed Machine Learning," in *Proc. 39th International Conference on Machine Learning (ICML)*, 2022.

[50] A. Author, "Near-Optimal Aggregators for Byzantine Resilient Distributed ML," in *Proc. AAAI Conference on Artificial Intelligence*, 2025.

[51] R. Author, "zkCNN: Zero Knowledge Proofs for Convolutional Neural Network Predictions and Accuracy," *ResearchGate*, 2020.

[52] Zkonduit, "ezkl," *GitHub*, 2024.

[53] Risc Zero, "RISC Zero Secures $40M Series A," *Risc Zero Blog*, 2023.

[54] N. Author, "Introducing Allora: A Self-Improving Decentralized AI Network," *Business Wire*, Feb. 1, 2024.

[55] A. Author, "ZKProphet: A Performance Study of Zero-Knowledge Proofs on GPUs," *arXiv preprint arXiv:2509.22684*, 2025.

[56] Polyhedra Network, "The GPU Revolution: How We're Making Ethereum 1000x Faster with Zero-Knowledge Proofs," *Polyhedra Network Blog*, 2024.

[57] G. Konstantopoulos, "ZK Hardware," *Paradigm.xyz*, Apr. 2022.

[58] EZKL, "Hardware Acceleration: ICICLE," *EZKL Blog*, 2024.

[59] O. Shlomovits, "Revisiting Paradigm's Hardware Acceleration for Zero-Knowledge Proofs," *Ingonyama Medium*, 2023.

[60] X. Author, "Privacy-Preserving Federated Learning Based on Differential Privacy and Homomorphic Encryption," *PMC NCBI*, vol. 10, no. 11, p. 2504, 2022.

[61] A. Author, "A Survey of Zero-Knowledge Proofs," *arXiv preprint arXiv:2408.00243*, 2024.

[62] T. Author, "What's the Difference Between zkML and opML?" *HackerNoon*, 2024.

[63] A. Author, "Decentralized Training," *Paragraph*, 2024.

---

*Document converted to Markdown format*