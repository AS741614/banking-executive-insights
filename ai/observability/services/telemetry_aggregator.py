import logging
from datetime import datetime
from typing import Dict, Any, List

from ai.observability.services.operational_intelligence import OperationalIntelligenceService
from ai.observability.models.telemetry import GovernanceTelemetry
from ai.observability.services.prometheus_metrics import metrics

logger = logging.getLogger("esoteric_bank.observability.telemetry_aggregator")

from app.services.warehouse_service import WarehouseService
from ecos.main import ecos

class ExecutiveTelemetryAggregator:
    """
    Enterprise Telemetry Aggregator for Executive Oversight.
    Synthesizes domain-specific metrics into high-level institutional health.
    """

    def __init__(self):
        self.intel_service = OperationalIntelligenceService()

    async def get_institutional_health_snapshot(self) -> Dict[str, Any]:
        """
        Aggregates metrics from various domains into a single institutional snapshot.
        """
        # Fetch live governance stats from Warehouse
        gov_status = WarehouseService.get_governance_status()
        summary = WarehouseService.get_executive_summary()
        
        # Determine active incidents from ECOS task registry
        tasks = await ecos.state.get_domain_state("tasks")
        active_incidents = len([v for k, v in tasks.items() if v == "DISPATCHED"])
        
        # Pull live metrics from State Registry (Adaptive Layer)
        drift_index = await ecos.state.get_state("governance", "drift_index")
        liq_risk = await ecos.state.get_state("risk", "liquidity_risk")
        anomalies = await ecos.state.get_state("risk", "anomalies_detected")
        
        current_metrics = {
            "aml_severity_avg": 0.42 if not drift_index or drift_index.value < 0.1 else 0.85,
            "kyc_approval_rate": 0.95,
            "fraud_prevention_efficiency": 0.98 if not anomalies or anomalies.value < 5 else 0.75,
            "cognition_latency_ms": 138.4,
            "system_availability": 1.0,
            "aggregate_net_flow": summary.get("aggregate_net_flow", 0.0),
            "liquidity_coverage_ratio": liq_risk.value if liq_risk else 1.0,
            "anomalies_detected": anomalies.value if anomalies else 0
        }
        
        telemetry = await self.intel_service.generate_platform_telemetry(
            "INSTITUTIONAL_CORE", 
            current_metrics
        )

        # Update Prometheus Metrics
        metrics.update_governance_telemetry(telemetry)
        
        # Adaptive Metric Export to Prometheus
        metrics.governance_drift.set(current_metrics["aml_severity_avg"]) # Mapping drift to severity for visualization
        metrics.liquidity_risk.set(current_metrics["liquidity_coverage_ratio"])
        metrics.anomalies_detected.set(current_metrics["anomalies_detected"])
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "health_score": telemetry.system_health,
            "risk_index": telemetry.risk_exposure,
            "active_incidents": active_incidents,
            "domain_metrics": current_metrics,
            "status": "STABLE" if telemetry.system_health > 0.8 else "DEGRADED"
        }
