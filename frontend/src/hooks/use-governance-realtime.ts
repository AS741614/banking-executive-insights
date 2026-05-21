"use client";

import { useEventStream } from "@/hooks/use-event-stream";
import { useEffect, useState, useMemo } from "react";
import { CognitiveEvent } from "@/types/api";

export function useGovernanceRealtime() {
  const { events, status, isConnected } = useEventStream();
  const [governanceEvents, setGovernanceEvents] = useState<CognitiveEvent[]>([]);

  useEffect(() => {
    // Filter for Governance and Compliance categories
    const latestGov = events.filter(e => 
      e.domain === "GOVERNANCE" || e.domain === "COMPLIANCE"
    );
    setGovernanceEvents(latestGov);
  }, [events]);

  const escalations = useMemo(() => 
    governanceEvents.filter(e => e.message.includes("REGULATORY_ESCALATION")),
  [governanceEvents]);

  const kycUpdates = useMemo(() => 
    governanceEvents.filter(e => e.message.includes("KYC_EVALUATION_COMPLETED")),
  [governanceEvents]);

  return {
    allEvents: governanceEvents,
    escalations,
    kycUpdates,
    status,
    isConnected
  };
}
