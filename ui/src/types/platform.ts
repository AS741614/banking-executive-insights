export interface EnterpriseMetadata {
  status: string;
  timestamp: string;
  trace_id?: string | null;
  latency_ms?: number | null;
  version: string;
}

export interface EnterpriseResponse<T> {
  meta: EnterpriseMetadata;
  data: T | null;
  error?: Record<string, any> | null;
}

export interface PlatformStatus {
  status: string;
  environment: string;
  version: string;
  uptime: number;
  services: Record<string, string>;
}
