# ESOTERIC BANK Dashboard Cognition & Semantic BI Intelligence

Institutional-grade reasoning infrastructure for executive visualization and semantic BI.

## Architecture
- **Framework**: Modular Python-based BI Cognition Services.
- **Semantic Layer**: KPI classification based on institutional domains (Liquidity, Compliance, Fraud).
- **Recommendation Engine**: Intelligent mapping of KPIs to optimal visualization types (e.g., Time Series for Liquidity, Heatmaps for Compliance).
- **Specification System**: Generation of machine-readable `DashboardSpecification` profiles for downstream BI orchestration.

## Core Subsystems

### 1. KPI Semantic Classification (`ai/tableau/semantic/`)
Defines the institutional meaning of data metrics.
- **Models**: `KPIMetadata`, `KPISemanticCategory`.
- **Logic**: Maps raw warehouse fields to semantic groups like `GOVERNANCE_DRIFT` or `REGULATORY_COMPLIANCE`.

### 2. Visualization Recommendation (`ai/tableau/cognition/engines/`)
Reasons through metric characteristics to suggest the most effective executive-level visualizations.
- **Viz Selection**: Automatically chooses between Time Series, Heatmaps, Sankey diagrams, etc., based on the institutional context.
- **Layout Intelligence**: Proposes high-density grid layouts optimized for executive command centers.

### 3. Cognition Orchestration (`ai/tableau/cognition/services/`)
The centralized `DashboardCognitionService` that synthesizes institutional personas and KPI registries into full dashboard specifications.

## BI Cognition Workflow
1. **Define Persona**: Select target executive role (e.g., CHIEF_RISK_OFFICER).
2. **Select KPIs**: Identify relevant metrics from the institutional registry.
3. **Reason**: The Cognition Engine selects visualization types and calculates an optimal layout.
4. **Specify**: A formal `DashboardSpecification` is generated.
5. **Orchestrate**: The specification is passed to the Tableau/UI layer for rendering.

## Integration
This domain is designed to be ontology-aware, ensuring that dashboard logic evolves alongside the platform's adaptive cognition layer.
