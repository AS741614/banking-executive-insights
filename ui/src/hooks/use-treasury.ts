import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { EnterpriseResponse } from "@/types/platform";

export interface RiskIntelligence {
  risk_level: string;
  anomalies_detected: number;
  regional_breakdown: Array<{
    region: string;
    net_flow: number;
  }>;
  live_risk_state?: any;
}

export interface ForecastIntelligence {
  prediction_model: string;
  trend: string;
  projected_next_month_flow: number;
  confidence_score: number;
}

export interface TreasuryData {
  risk: RiskIntelligence;
  forecast: ForecastIntelligence;
}

export function useRiskIntelligence() {
  return useQuery({
    queryKey: ["risk-intelligence"],
    queryFn: async () => {
      const { data } = await api.get<EnterpriseResponse<RiskIntelligence>>("/risk/intelligence");
      return data;
    },
    refetchInterval: 15000,
  });
}

export function useForecastIntelligence() {
  return useQuery({
    queryKey: ["forecast-intelligence"],
    queryFn: async () => {
      const { data } = await api.get<EnterpriseResponse<ForecastIntelligence>>("/forecast/intelligence");
      return data;
    },
    refetchInterval: 30000,
  });
}
