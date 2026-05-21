# ESOTERIC BANK Distributed Cognitive Agents

Enterprise-grade distributed cognition and institutional multi-agent orchestration.

## Architecture
- **Framework**: Modular Python-based Multi-Agent System (MAS).
- **Orchestration**: `InstitutionalOrchestratorAgent` manages task routing and collective decision workflows.
- **Messaging**: `CognitiveMessage` protocol for secure, ontology-aware inter-agent communication.
- **Governance**: Every agent operates with a specific clearance tier and publishes coordination events to the platform's central `CognitiveEventBus`.

## Core Subsystems

### 1. Agent Core (`ai/agents/core/`)
Provides the foundational `CognitiveAgent` base class and the `AgentRegistry` (Agent Topology Management).
- **Topology**: Tracks active agents, their types, statuses, and capabilities.
- **Traceability**: All inter-agent communication is correlated via institutional `trace_id` and `correlation_id`.

### 2. Specialized Agents (`ai/agents/services/`)
Domain-specific cognitive units that execute institutional tasks.
- **Orchestrator Agent**: The brain of the collective intelligence, resolving task requests and assigning them to specialized agents.
- **Compliance Agent**: A regulatory-focused agent that performs governance-aware reasoning for KYC/AML operations.

### 3. Messaging Protocols (`ai/agents/models/`)
Structured data models for messages and tasks, ensuring semantic interoperability across the distributed cognitive cluster.

## Distributed Cognition Workflow
1. **Request**: A task request is sent to the `OrchestratorAgent`.
2. **Resolve**: The orchestrator resolves the task description to a specialized agent type (e.g., `REGULATORY`).
3. **Assign**: The task is assigned to an available agent via the `TASK_ASSIGNMENT` intent.
4. **Reason**: The specialized agent executes domain-specific reasoning, adhering to institutional ontology and governance.
5. **Coordinate**: The agent communicates the result back to the orchestrator.
6. **Publish**: All significant coordination milestones are emitted as `CognitiveEvent` objects for platform-wide observability.
