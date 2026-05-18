import random
from datetime import date, timedelta, datetime
import math

class TemporalEngine:
    """
    Manages the advancement of time and macroeconomic state across the 24-month simulation.
    Handles seasonality, liquidity pressure cycles, and operational degradation triggers.
    """
    def __init__(self, start_date: date, end_date: date):
        self.start_date = start_date
        self.end_date = end_date
        self.current_date = start_date
        
        # Macro State
        self.base_liquidity_pressure = 1.0
        self.fraud_multiplier = 1.0
        self.operational_efficiency = 100.0

    @property
    def is_finished(self) -> bool:
        return self.current_date > self.end_date

    def advance_day(self):
        """Advances the simulation by one day and updates macroeconomic variables."""
        self.current_date += timedelta(days=1)
        self._update_macro_state()

    def _update_macro_state(self):
        """
        Injects realistic cyclicality and institutional drift.
        """
        days_passed = (self.current_date - self.start_date).days
        total_days = (self.end_date - self.start_date).days
        progress = days_passed / total_days

        # Seasonality: higher transaction volume and fraud pressure during end-of-year/holidays
        month = self.current_date.month
        is_holiday_season = month in [11, 12]
        
        # 1. Liquidity Pressure
        # Simulates a slow buildup of treasury stress halfway through the simulation
        if progress > 0.5 and progress < 0.7:
            # Macro shock scenario
            self.base_liquidity_pressure += random.uniform(0.01, 0.05)
        else:
            # Mean reversion
            self.base_liquidity_pressure += (1.0 - self.base_liquidity_pressure) * 0.05
        
        # 2. Fraud Multiplier
        # Spikes during holidays and slowly trends up as networks adapt
        base_fraud_trend = 1.0 + (progress * 0.5) # 50% increase in baseline fraud over 24m
        seasonality_spike = 1.5 if is_holiday_season else 1.0
        self.fraud_multiplier = base_fraud_trend * seasonality_spike * random.uniform(0.9, 1.1)

        # 3. Operational Efficiency
        # Deteriorates as liquidity pressure and fraud pressure increase
        stress_factor = (self.base_liquidity_pressure - 1.0) + (self.fraud_multiplier - 1.0)
        target_efficiency = max(60.0, 100.0 - (stress_factor * 15.0))
        # Slowly drift towards target
        self.operational_efficiency += (target_efficiency - self.operational_efficiency) * 0.1

    def get_current_state(self):
        return {
            "date": self.current_date,
            "liquidity_pressure": self.base_liquidity_pressure,
            "fraud_multiplier": self.fraud_multiplier,
            "operational_efficiency": self.operational_efficiency
        }
