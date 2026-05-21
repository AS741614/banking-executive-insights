import uuid
from datetime import datetime, timedelta
from typing import List
from models.core import GovernanceEvent, TreasurySignal
import random

class GovernanceTreasuryEngine:
    """
    Generates high-level institutional signals: Governance Drift and Treasury Liquidity constraints.
    These events are driven directly by the macroscopic TemporalEngine state.
    """
    def __init__(self, seed: int = 42):
        random.seed(seed)

    def generate_daily_signals(self, current_date: datetime.date, macro_state: dict) -> tuple[List[GovernanceEvent], List[TreasurySignal]]:
        events = []
        signals = []
        
        timestamp = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=12)
        
        # 1. Treasury Signals
        liquidity_pressure = macro_state.get("liquidity_pressure", 1.0)
        
        # Generate Core Liquidity Coverage Ratio (LCR) proxy
        base_lcr = 120.0 # 120% is healthy
        simulated_lcr = base_lcr / liquidity_pressure
        
        lcr_status = "HEALTHY"
        if simulated_lcr < 100.0:
            lcr_status = "DEGRADED"
        elif simulated_lcr < 80.0:
            lcr_status = "CRITICAL"
            
        signal = TreasurySignal(
            signal_id=f"TS-{uuid.uuid4().hex[:8]}",
            metric_name="LCR_PROXY",
            value=round(simulated_lcr, 2),
            timestamp=timestamp,
            drift_status=lcr_status
        )
        signals.append(signal)
        
        # 2. Governance Events
        # Triggered by operational degradation or high fraud multipliers
        operational_efficiency = macro_state.get("operational_efficiency", 100.0)
        fraud_multiplier = macro_state.get("fraud_multiplier", 1.0)
        
        if operational_efficiency < 85.0 and random.random() < 0.2:
            events.append(GovernanceEvent(
                event_id=f"GOV-{uuid.uuid4().hex[:10]}",
                event_type="OPERATIONAL_DEGRADATION",
                severity="MEDIUM" if operational_efficiency > 75.0 else "HIGH",
                entity_id="ESOTERIC_CORE",
                entity_type="SYSTEM",
                description=f"Core operational efficiency fell to {round(operational_efficiency, 1)}%. Processing backlogs expanding.",
                timestamp=timestamp
            ))
            
        if fraud_multiplier > 1.3 and random.random() < 0.15:
            events.append(GovernanceEvent(
                event_id=f"GOV-{uuid.uuid4().hex[:10]}",
                event_type="AML_POLICY_BREACH",
                severity="HIGH",
                entity_id="COMPLIANCE_ENGINE",
                entity_type="SYSTEM",
                description="Elevated fraud velocity detected. Automatic policy escalation triggered.",
                timestamp=timestamp
            ))

        return events, signals
