export interface GovernanceState {
  governance_status: string;
  active_policies: number;
  compliance_score: number;
  last_audit_timestamp: string;
  drift_detected: boolean;
  pending_escalations: number;
}

export interface RegulatoryEscalation {
  escalation_id: string;
  timestamp: string;
  domain: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  trigger: string;
  description: string;
  status: "PENDING" | "REVIEW" | "RESOLVED" | "DISMISSED";
  metadata: Record<string, any>;
}

export interface KYCEventPayload {
  customer_id: string;
  compliance_status: "PENDING" | "EVALUATING" | "APPROVED" | "UNDER_REVIEW" | "REJECTED";
  governance_tier: string;
  edd_required: boolean;
  event_version: string;
  source_domain: string;
  cognition_context: Record<string, any>;
}

export interface EscalationEventPayload {
  domain: string;
  customer_id: string;
  trigger: string;
  description: string;
  compliance_payload: KYCEventPayload;
}
