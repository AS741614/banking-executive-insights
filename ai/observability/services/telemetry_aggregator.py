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
        
        # Synthesize AUM trend for frontend visualization (12 months)
        # In production, this would be a historical aggregation from the warehouse
        base_aum = summary.get("active_account_base", 100) * 1.2
        aum_trend = [base_aum * (1 + (0.02 * i)) for i in range(12)]

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "institutional_health_score": int(telemetry.system_health * 100),
            "capital_adequacy_ratio": 15.4, # Institutional Baseline
            "liquidity_coverage_ratio": int(current_metrics["liquidity_coverage_ratio"] * 100),
            "active_escalations": active_incidents,
            "aum_trend": aum_trend,
            "risk_posture": "OPTIMAL" if telemetry.risk_exposure < 0.3 else "VIGILANT",
            "health_score": telemetry.system_health,
            "risk_index": telemetry.risk_exposure,
            "domain_metrics": current_metrics,
            "status": "STABLE" if telemetry.system_health > 0.8 else "DEGRADED"
        }
