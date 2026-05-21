import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { EnterpriseResponse } from "@/types/platform";

export function useExecutiveIntelligence() {
  return useQuery({
    queryKey: ["executive-intelligence"],
    queryFn: async () => {
      const { data } = await api.get<EnterpriseResponse<any>>("/executive/intelligence");
      return data;
    },
    refetchInterval: 30000,
  });
}

export function useRiskIntelligence() {
  return useQuery({
    queryKey: ["risk-intelligence"],
    queryFn: async () => {
      const { data } = await api.get<EnterpriseResponse<any>>("/risk/intelligence");
      return data;
    },
    refetchInterval: 60000,
  });
}

export function useGovernanceCognition() {
  return useQuery({
    queryKey: ["governance-cognition"],
    queryFn: async () => {
      const { data } = await api.get<EnterpriseResponse<any>>("/governance/cognition");
      return data;
    },
    refetchInterval: 60000,
  });
}

export function useForecastIntelligence() {
  return useQuery({
    queryKey: ["forecast-intelligence"],
    queryFn: async () => {
      const { data } = await api.get<EnterpriseResponse<any>>("/forecast/intelligence");
      return data;
    },
    refetchInterval: 300000, // 5 minutes
  });
}
