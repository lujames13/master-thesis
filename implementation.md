# V. Implementation

## A. Technology Stack and Development Environment

Our implementation extends the Flower federated learning framework to support multiple aggregators and our hybrid Optimistic-PBFT security mechanism. The system is built using Python with PyTorch for model training and evaluation.

```
Key Components:
1. Flower Framework: Extended for multi-aggregator support
2. Python 3.8+: Primary implementation language
3. PyTorch: Model definition and training
4. CIFAR-10: Benchmark dataset for experimentation
```

We chose Flower due to its modular design, which allowed us to extend the core components while maintaining compatibility with the existing federated learning ecosystem. The implementation is designed to be framework-agnostic, with the core concepts applicable to other federated learning frameworks as well.

## B. Core Component Implementation

The core of our implementation is the MultiAggregatorStrategy class, which extends Flower's FedAvg strategy to support multiple aggregators and malicious behavior detection.

```
Algorithm 1: MultiAggregatorStrategy Aggregation Process
Input: server_round r, client_updates U, num_aggregators N
Output: aggregated_parameters G_r, metrics M

1: current_aggregator_id ← (r-1) mod N
2: if current_aggregator_id ∈ excluded_aggregators then
3:     Find next non-excluded aggregator
4: end if
5: honest_parameters ← FedAvg(U)  // For validation purposes
6: if current_aggregator_id ∈ malicious_aggregator_ids then
7:     aggregated_parameters ← CreateMaliciousAggregation(honest_parameters)
8:     Schedule delayed detection for round r + detection_delay
9: else
10:    aggregated_parameters ← honest_parameters
11: end if
12: Store honest_parameters in safe_parameters_history
13: return aggregated_parameters, metrics
```

The strategy handles the selection of aggregators for each round, the creation of malicious aggregations for simulation purposes, and the scheduling of delayed detection to mimic the challenge period in our Optimistic-PBFT system.

## C. Hybrid Challenge Mechanism Implementation

Our implementation includes a hybrid challenge mechanism that combines the efficiency of optimistic assumptions with the security guarantees of Byzantine Fault Tolerance when needed.

```
Algorithm 2: Hybrid Challenge Processing with PBFT
Input: challenge_round r, challenged_aggregator_id a, challenged_result R
Output: challenge_result (success/failure)

1: if ValidChallenge(r, a, R) then
2:     Activate PBFT validation mode
3:     Broadcast validation request to all validators
4:     Wait for at least 2f+1 validator responses V = {v_1, v_2, ..., v_m}
5:     consensus_result ← PBFT_Consensus(V)
6:     if DifferSignificantly(R, consensus_result) then
7:         Add a to excluded_aggregators
8:         Set recovery_mode ← true
9:         Set recovery_from_round ← r-1
10:        Apply penalties to aggregator a
11:        return success
12:    else
13:        Apply penalties to challenger
14:        return failure
15:    end if
16: end if
```

The challenge mechanism activates PBFT consensus only when a challenge is submitted, maintaining system efficiency during normal operation while providing strong security guarantees when needed.

## D. PBFT Consensus Implementation

We implemented a simplified PBFT consensus algorithm for challenge validation, which collects aggregation results from validators and determines the consensus based on Byzantine quorum.

```
Algorithm 3: PBFT Consensus for Challenge Validation
Input: validator_results V = {v_1, v_2, ..., v_m}
Output: consensus_result C

1: for each validator result v_i in V do
2:     Verify digital signature of v_i
3: end for
4: Group results by similarity
5: if Largest group size ≥ 2f+1 (Byzantine quorum) then
6:     C ← Median result from largest group
7:     return C
8: else
9:     return inconclusive
10: end if
```

This implementation ensures that the system can achieve Byzantine consensus when validating challenges, providing strong security guarantees with 2f+1 honest validators.

## E. Delayed Detection and Rollback Implementation

Our implementation includes a delayed detection mechanism to reflect the challenge period in Optimistic Rollup systems. When malicious behavior is detected and validated through PBFT, the system triggers a rollback to restore the last secure state.

```
Algorithm 4: Recovery Mode Execution
Input: server_round r, client_updates U
Output: recovered_parameters G_r, metrics M

1: if recovery_mode = true then
2:     safe_parameters ← safe_parameters_history[recovery_from_round]
3:     Select non-excluded aggregator based on round number
4:     aggregated_parameters ← FedAvg(U) starting from safe_parameters
5:     Mark metrics as recovery_round
6:     recovery_mode ← false
7:     Store aggregated_parameters in safe_parameters_history
8:     return aggregated_parameters, metrics
9: end if
```

The recovery mode ensures that the system can restore a secure state after detecting malicious behavior. By rolling back to the last verified state and excluding the malicious aggregator, the system can continue operating without compromising security.

## F. Malicious Behavior Simulation

For research purposes, we implemented a noise attack simulation to study the effectiveness of our challenge mechanism. The noise attack adds random perturbations to the aggregated model parameters.

```
Algorithm 5: Malicious Aggregation with Noise Attack
Input: honest_parameters H
Output: malicious_parameters M

1: noise_level ← 0.1  // Configurable parameter
2: M ← []
3: for each parameter tensor p in H do
4:     noise ← RandomNormal(shape=p.shape, mean=0, std=noise_level)
5:     p_malicious ← p + noise
6:     Append p_malicious to M
7: end for
8: return M
```

This implementation allows us to simulate malicious behavior in a controlled environment and evaluate the effectiveness of our challenge and recovery mechanisms in detecting and mitigating such attacks.

## G. Mode Switching Implementation

A key aspect of our hybrid approach is the ability to switch between efficient optimistic mode and secure PBFT mode when needed. We implemented a mode switching mechanism that activates PBFT consensus only during challenge resolution.

```
Algorithm 6: Mode Switching Mechanism
Input: system_state S, event E
Output: updated_system_state S'

1: if E is normal_round_start then
2:     S.mode ← OPTIMISTIC
3:     S.current_aggregator_id ← (S.round - 1) mod N
4:     if S.current_aggregator_id ∈ S.excluded_aggregators then
5:         Find next non-excluded aggregator
6:     end if
7: else if E is challenge_submitted then
8:     S.mode ← PBFT
9:     S.challenge_round ← S.round
10:    S.validators_required ← 2 * S.max_faulty + 1
11:    Broadcast validation request to all validators
12: else if E is challenge_resolved then
13:    S.mode ← OPTIMISTIC
14:    if S.challenge_result = successful then
15:        S.recovery_mode ← true
16:        S.recovery_from_round ← S.challenge_target_round - 1
17:    end if
18: end if
19: return S
```

This mode switching mechanism ensures that the system operates efficiently under normal conditions (O(n) complexity) while activating more expensive but secure Byzantine consensus (O(n²) complexity) only when necessary.

## H. Experimental Configuration

The system can be configured with various parameters to simulate different research scenarios, including varying numbers of clients, aggregators, malicious entities, and enabling/disabling the challenge mechanism.

```
Algorithm 7: Experiment Configuration
Input: scenario_type, num_clients, num_rounds, num_aggregators, malicious_ids, enable_challenges
Output: Configured simulation environment

1: if scenario_type = "baseline" then
2:     malicious_ids ← []
3:     enable_challenges ← false
4: else if scenario_type = "malicious_no_challenges" then
5:     malicious_ids ← [predefined IDs]
6:     enable_challenges ← false
7: else if scenario_type = "malicious_with_challenges" then
8:     malicious_ids ← [predefined IDs]
9:     enable_challenges ← true
10:    consensus_mode ← "hybrid_optimistic_pbft"
11: end if
12: strategy ← MultiAggregatorStrategy(
13:     num_aggregators=num_aggregators,
14:     malicious_aggregator_ids=malicious_ids,
15:     enable_challenges=enable_challenges,
16:     detection_delay=2,  // Default challenge period
17:     consensus_mode=consensus_mode
18: )
19: return strategy
```

These configuration options allow researchers to explore the performance and security characteristics of the system under various conditions, facilitating comprehensive evaluation of the proposed hybrid Optimistic-PBFT approach.

## I. Implementation Challenges and Solutions

During the implementation of our hybrid Optimistic-PBFT framework, we encountered several challenges that required creative solutions:

1. **Balancing Modes**: We implemented a dynamic mode switching mechanism that activates PBFT only when challenges occur, maintaining efficiency under normal operation.

2. **Byzantine Quorum Collection**: We developed a validator response collection system that waits for at least 2f+1 responses to form a Byzantine quorum.

3. **Similarity Grouping**: We implemented a parameter similarity grouping algorithm to identify the largest consensus group among validator responses.

4. **Secure Parameter Storage**: We created a history of safe parameters to enable recovery when malicious behavior is detected, ensuring the system can revert to a secure state.

5. **Validator Coordination**: We developed a broadcast mechanism to coordinate validator participation during PBFT mode, ensuring sufficient responses for Byzantine consensus.

These solutions demonstrate the practical feasibility of our hybrid Optimistic-PBFT approach, combining the efficiency of optimistic operation with the security guarantees of Byzantine consensus when needed.