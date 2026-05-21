import logging
from prometheus_client import Gauge, Counter, Histogram, Summary

logger = logging.getLogger("esoteric_bank.observability.prometheus")

class PrometheusMetrics:
    """
    Centralized Prometheus Metrics for Esoteric Bank.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PrometheusMetrics, cls).__new__(cls)
            cls._instance._init_metrics()
        return cls._instance

    def _init_metrics(self):
        # Platform Health
        self.system_health = Gauge(
            "esoteric_system_health",
            "Overall system health score (0.0 - 1.0)",
            ["component_id"]
        )
        self.risk_exposure = Gauge(
            "esoteric_risk_exposure",
            "Current risk exposure index (0.0 - 1.0)",
            ["component_id"]
        )
        self.active_incidents = Gauge(
            "esoteric_active_incidents",
            "Number of active governance incidents",
            ["component_id"]
        )

        # Domain Specific Metrics
        self.aml_severity = Gauge(
            "esoteric_aml_severity_avg",
            "Average AML severity score"
        )
        self.kyc_approval_rate = Gauge(
            "esoteric_kyc_approval_rate",
            "KYC approval rate"
        )
        self.fraud_prevention_efficiency = Gauge(
            "esoteric_fraud_prevention_efficiency",
            "Fraud prevention efficiency"
        )
        
        # Adaptive Cognition Metrics
        self.governance_drift = Gauge(
            "esoteric_governance_drift_index",
            "Institutional governance drift index"
        )
        self.liquidity_risk = Gauge(
            "esoteric_liquidity_risk_score",
            "Real-time liquidity risk score"
        )
        self.anomalies_detected = Gauge(
            "esoteric_anomalies_total",
            "Total anomalies detected by cognitive agents"
        )
        
        # Performance
        self.cognition_latency = Histogram(
            "esoteric_cognition_latency_seconds",
            "Latency of cognitive cycles",
            buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0)
        )
        
        # Transactional
        self.transaction_count = Counter(
            "esoteric_transaction_total",
            "Total number of transactions processed",
            ["region", "segment"]
        )
        self.liquidity_flow = Gauge(
            "esoteric_liquidity_net_flow",
            "Net liquidity flow",
            ["region", "segment"]
        )

    def update_governance_telemetry(self, telemetry):
        """Updates metrics from a GovernanceTelemetry object."""
        self.system_health.labels(component_id=telemetry.component_id).set(telemetry.system_health)
        self.risk_exposure.labels(component_id=telemetry.component_id).set(telemetry.risk_exposure)
        self.active_incidents.labels(component_id=telemetry.component_id).set(telemetry.active_incidents)

metrics = PrometheusMetrics()
