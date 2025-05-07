# IV. Framework Design

## A. System Architecture

Our Blockchain-based Federated Learning (BFL) framework extends the traditional federated learning architecture by incorporating multiple aggregators with a challenge-based security mechanism inspired by Optimistic Rollup. The system operates on the principle that a single honest validator can ensure the security of the entire federated learning process, enabling a more efficient aggregation workflow compared to traditional Byzantine Fault Tolerance (BFT) approaches.

```
Architecture Overview:
1. Requester: Initiates federated learning tasks and defines parameters
2. Clients: Perform local model training on private datasets
3. Aggregator Pool: Multiple aggregators that process client updates
4. Challenge Mechanism: Verification system to detect malicious behavior
5. Blockchain Layer: Provides immutability, coordination, and security guarantees
6. IPFS Layer: Handles model and update storage
```

Figure 1 illustrates the high-level architecture of our BFL system, showing the interactions between components and the data flow during the federated learning process.

## B. Multi-Aggregator Model

Unlike traditional federated learning systems with a single aggregator, our framework employs multiple aggregators operating in a round-robin fashion. This design enhances system efficiency by distributing computational load while maintaining security through our challenge mechanism.

```
Multi-Aggregator Selection:
1. For each round r:
   a. Select aggregator A_i where i = (r-1) mod N
   b. A_i collects client updates U = {u_1, u_2, ..., u_m}
   c. A_i performs aggregation to produce new global model G_r
   d. A_i submits G_r to the system
2. Enter challenge period for round r
3. If no successful challenges, G_r becomes the official model for round r+1
```

The round-robin selection ensures fair distribution of aggregation tasks among all available aggregators, while the challenge period provides a window for validators to identify and report malicious behavior before the model update is finalized.

## C. Challenge Mechanism

We incorporate a challenge mechanism based on established methods in the literature to detect potentially malicious aggregations. Rather than focusing on developing new validation techniques, we leverage these proven approaches as triggers for our novel Optimistic Rollup-inspired recovery system. The challenge mechanism serves as a detection layer that activates the security guarantees provided by our rollback protocol.

```
Challenge Process Overview:
1. After aggregator A_i submits aggregated model G_r
2. System enters challenge period of T blocks/time
3. Any validator can submit challenge if suspicious behavior detected
4. System evaluates challenge validity using predefined metrics
5. If challenge successful, trigger rollback procedure
```

The challenge period provides a crucial security window during which validators can verify aggregations and submit proofs if malicious behavior is detected, similar to the fraud proof submission in Optimistic Rollup systems.

## D. Optimistic Rollup Integration

The core innovation of our framework lies in the application of Optimistic Rollup principles to federated learning. In blockchain systems, Optimistic Rollup allows for high throughput by assuming transactions are valid by default, with a challenge period where anyone can submit fraud proofs. Similarly, our BFL framework assumes aggregations are honest by default but provides a challenge window where validators can contest malicious results.

```
Optimistic Security Model:
1. Assume aggregations are valid by default
2. Allow system to proceed without expensive consensus for each aggregation
3. Provide challenge period where validators can submit proofs of incorrect aggregation
4. Require only one honest validator to maintain system security
5. Enforce penalties (stake slashing) for proven malicious behavior
```

This approach significantly improves system efficiency compared to traditional Byzantine Fault Tolerance protocols that require consensus from a majority of honest nodes for each update. By adopting the Optimistic Rollup paradigm, we can achieve higher throughput while maintaining strong security guarantees with minimal honest participation.

## E. Exclusion and Recovery Mechanism

When malicious behavior is detected through a successful challenge, our system employs a comprehensive recovery mechanism. This includes rolling back to a secure state, excluding the malicious aggregator, and redistributing tasks to honest aggregators.

```
Recovery Protocol:
1. Upon successful challenge against aggregator A_m:
   a. Revert to last verified state (round r-1)
   b. Add A_m to exclusion list E
   c. Slash stake of A_m as penalty
   d. Reassign round r to next eligible aggregator A_j where j ∉ E
   e. Resume federation from round r with A_j
2. Update security metrics and system state
```

The exclusion mechanism ensures that once identified, malicious aggregators cannot participate in future rounds, gradually improving system security over time. The recovery mechanism enables the system to restore a secure state without losing significant progress in the federated learning process.

## F. Security Model and Assumptions

Our security model requires at least one honest validator to ensure system integrity, similar to Optimistic Rollup's security guarantees. We assume that malicious aggregators cannot prevent honest validators from accessing the system or submitting challenges.

```
Security Assumptions:
1. At least one honest validator exists in the system
2. Validators have access to sufficient computational resources to verify aggregations
3. Challenge submission cannot be censored by malicious actors
4. Challenge period T is sufficiently long for validation but short enough for system efficiency
5. Stake amounts are significant enough to deter malicious behavior
```

These assumptions establish the security boundaries of our system and highlight the advantages of our approach over traditional Byzantine Fault Tolerance methods that typically require a two-thirds majority of honest participants. Our framework can maintain security with just a single honest validator, significantly reducing the trust requirements for secure federated learning.