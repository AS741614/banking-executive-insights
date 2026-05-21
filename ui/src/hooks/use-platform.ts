import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { EnterpriseResponse, PlatformStatus } from "@/types/platform";

export function usePlatformStatus() {
  return useQuery({
    queryKey: ["platform-status"],
    queryFn: async () => {
      const { data } = await api.get<EnterpriseResponse<PlatformStatus>>("/platform/status");
      return data;
    },
    refetchInterval: 10000, // Refetch every 10 seconds
  });
}

export function useEventHistory() {
  return useQuery({
    queryKey: ["platform-history"],
    queryFn: async () => {
      const { data } = await api.get<EnterpriseResponse<any>>("/platform/history");
      return data;
    },
  });
}
