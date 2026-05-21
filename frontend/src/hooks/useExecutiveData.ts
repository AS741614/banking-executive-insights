import { useQuery } from "@tanstack/react-query";
import { api, endpoints } from "@/lib/api";

export function useExecutiveIntelligence() {
  return useQuery({
    queryKey: ["executive-intelligence"],
    queryFn: async () => {
      const response = await api.get(endpoints.executive.intelligence);
      return response.data.data;
    },
  });
}

export function useRiskIntelligence() {
  return useQuery({
    queryKey: ["risk-intelligence"],
    queryFn: async () => {
      const response = await api.get(endpoints.executive.risk);
      return response.data.data;
    },
  });
}

export function useInstitutionalEvents() {
  return useQuery({
    queryKey: ["institutional-events"],
    queryFn: async () => {
      const response = await api.get(endpoints.executive.events);
      return response.data.data;
    },
  });
}
