export interface EnterpriseMetadata {
  status: "success" | "error";
  timestamp: string;
  trace_id?: string;
  version?: string;
}

export interface EnterpriseResponse<T> {
  meta: EnterpriseMetadata;
  data: T;
}

export interface ExecutiveIntelligence {
  domain: string;
  institutional_health_score: number;
  capital_adequacy_ratio: number;
  liquidity_coverage_ratio: number;
  net_stable_funding_ratio: number;
  aum_trend: number[];
  risk_posture: "CONSERVATIVE" | "BALANCED" | "AGGRESSIVE";
  active_escalations: number;
}

export interface PlatformStatus {
  status: "online" | "degraded" | "offline";
  subsystem: string;
  uptime?: string;
  cpu_usage?: number;
  memory_usage?: number;
  latency_ms?: number;
}

export interface CognitiveEvent {
  event_id: string;
  timestamp: string;
  domain: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  message: string;
  source: string;
  metadata?: Record<string, any>;
}

export interface GovernanceState {
  domain: string;
  governance_status: "SYNCHRONIZED" | "DESYNCHRONIZED" | "CRITICAL";
  active_policies: number;
  compliance_score: number;
  last_audit_timestamp: string;
}

export interface IntelligenceQuery {
  prompt: string;
  context?: Record<string, any>;
  governance_level?: string;
}

export interface IntelligenceResponse {
  query: string;
  intelligence_payload: string;
  confidence_score: number;
  sources?: string[];
}
