# V. Implementation

## A. Technology Stack and Development Environment

Our implementation extends the Flower federated learning framework to support multiple aggregators and challenge-based security mechanisms. The system is built using Python with PyTorch for model training and evaluation.

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

The strategy handles the selection of aggregators for each round, the creation of malicious aggregations for simulation purposes, and the scheduling of delayed detection to mimic the challenge period in Optimistic Rollup systems.

## C. Challenge Mechanism Implementation

We implement a simplified challenge mechanism that triggers our rollback protocol upon detection of malicious behavior. While the actual validation logic follows established methods in the literature, our focus is on the system's response to successful challenges.

```
Algorithm 2: Challenge Detection and Processing
Input: challenge_round r, malicious_round m, aggregator_id a
Output: challenge_result (success/failure)

1: if IsPendingDetection(r, m, a) then
2:     honest_parameters ← safe_parameters_history[m-1]
3:     challenge_success ← ValidateChallenge(m, a, honest_parameters)
4:     if challenge_success then
5:         Add m to detected_attacks
6:         Add a to excluded_aggregators
7:         Increment total_rollbacks
8:         Set recovery_mode ← true
9:         Set recovery_from_round ← m-1
10:        Log challenge metrics
11:    end if
12:    Remove from pending_detections
13: end if
14: return challenge_success
```

The challenge detection process uses delayed verification to simulate the time window in which validators can submit challenges in an Optimistic Rollup system. This implementation allows us to study the effectiveness of the challenge mechanism and its impact on system performance.

## D. Delayed Detection and Rollback Implementation

The enhanced version of our implementation includes a delayed detection mechanism to reflect the challenge period in Optimistic Rollup systems. When malicious behavior is detected, the system triggers a rollback to restore the last secure state.

```
Algorithm 3: Recovery Mode Execution
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

## E. Malicious Behavior Simulation

For research purposes, we implemented a noise attack simulation to study the effectiveness of our challenge mechanism. The noise attack adds random perturbations to the aggregated model parameters.

```
Algorithm 4: Malicious Aggregation with Noise Attack
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

## F. Experimental Configuration

The system can be configured with various parameters to simulate different research scenarios, including varying numbers of clients, aggregators, malicious entities, and enabling/disabling the challenge mechanism.

```
Algorithm 5: Experiment Configuration
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
10: end if
11: strategy ← MultiAggregatorStrategy(
12:     num_aggregators=num_aggregators,
13:     malicious_aggregator_ids=malicious_ids,
14:     enable_challenges=enable_challenges,
15:     detection_delay=2  // Default challenge period
16: )
17: return strategy
```

These configuration options allow researchers to explore the performance and security characteristics of the system under various conditions, facilitating comprehensive evaluation of the proposed approach.

## G. Implementation Challenges and Solutions

During the implementation of our BFL framework, we encountered several challenges that required creative solutions:

1. **Simulating Delayed Detection**: We implemented a pending detection mechanism that schedules validation for future rounds, mimicking the challenge period in Optimistic Rollup.

2. **Maintaining Safe Parameters**: We created a history of safe parameters to enable recovery when malicious behavior is detected, ensuring the system can revert to a secure state.

3. **Handling Excluded Aggregators**: We developed a mechanism to track excluded aggregators and adjust the round-robin selection to skip them, ensuring that known malicious aggregators cannot participate in future rounds.

4. **Recovery Mode Logic**: We implemented a special recovery mode that allows the system to resume from a secure state after detecting malicious behavior, minimizing the impact on the learning process.

These solutions demonstrate the practical feasibility of applying Optimistic Rollup principles to federated learning systems, providing both security guarantees and performance benefits compared to traditional approaches.