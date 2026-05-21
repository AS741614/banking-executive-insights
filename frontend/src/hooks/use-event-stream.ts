import { useState, useEffect, useRef, useCallback } from "react";
import { CognitiveEvent } from "@/types/api";

const MAX_RECONNECT_ATTEMPTS = 10; // Increased for enterprise resilience
const INITIAL_RECONNECT_DELAY = 1000;
const HEARTBEAT_TIMEOUT = 30000; // 30 seconds

export type ConnectionStatus = "CONNECTING" | "CONNECTED" | "DISCONNECTED" | "ERROR" | "RECONNECTING";

export function useEventStream() {
  const [events, setEvents] = useState<CognitiveEvent[]>([]);
  const [status, setStatus] = useState<ConnectionStatus>("DISCONNECTED");
  const [error, setError] = useState<string | null>(null);
  
  const eventSourceRef = useRef<EventSource | null>(null);
  const reconnectAttemptsRef = useRef(0);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const heartbeatTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const cleanup = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    if (heartbeatTimeoutRef.current) {
      clearTimeout(heartbeatTimeoutRef.current);
    }
  }, []);

  const resetHeartbeat = useCallback(() => {
    if (heartbeatTimeoutRef.current) {
      clearTimeout(heartbeatTimeoutRef.current);
    }
    heartbeatTimeoutRef.current = setTimeout(() => {
      // SILENT HEARTBEAT RECOVERY
      if (process.env.NODE_ENV !== 'production') {
        console.warn("SSE Heartbeat timeout - Reconnecting...");
      }
      setStatus("RECONNECTING");
      connect();
    }, HEARTBEAT_TIMEOUT);
  }, []);

  const connect = useCallback(() => {
    cleanup();
    
    // CONSTRUCTION VALIDATION: Ensure we use the correct institutional endpoint
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
    const endpoint = `${apiUrl}/observability/stream`;
    
    // SILENT INITIALIZATION
    if (reconnectAttemptsRef.current === 0) {
      setStatus("CONNECTING");
    }

    try {
      const es = new EventSource(endpoint);
      eventSourceRef.current = es;

      es.onopen = () => {
        setStatus("CONNECTED");
        setError(null);
        reconnectAttemptsRef.current = 0;
        resetHeartbeat();
      };

      es.onmessage = (event) => {
        resetHeartbeat();
        try {
          const parsedEvent: CognitiveEvent = JSON.parse(event.data);
          setEvents((prev) => [parsedEvent, ...prev].slice(0, 50));
        } catch (err) {
          // Silent parse error handling
        }
      };

      es.onerror = (e) => {
        es.close();
        
        // DETAILED ERROR ANALYSIS
        let errorMessage = "STREAM_CONNECTION_FAILED";
        if (es.readyState === EventSource.CLOSED) {
          errorMessage = "STREAM_CLOSED_BY_SERVER";
        } else if (es.readyState === EventSource.CONNECTING) {
          errorMessage = "STREAM_HANDSHAKE_TIMEOUT";
        }

        // SILENT RETRY LOGIC
        if (reconnectAttemptsRef.current < MAX_RECONNECT_ATTEMPTS) {
          setStatus("RECONNECTING");
          const delay = INITIAL_RECONNECT_DELAY * Math.pow(1.5, reconnectAttemptsRef.current);
          
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectAttemptsRef.current += 1;
            connect();
          }, delay);
        } else {
          setStatus("ERROR");
          setError("MAX_RECONNECT_ATTEMPTS_REACHED");
          console.error(`Institutional SSE Failure: ${errorMessage}. Kernel access suspended.`);
        }
      };
    } catch (err) {
      setStatus("ERROR");
      setError("STREAM_INITIALIZATION_CRITICAL_FAILURE");
    }
  }, [cleanup, resetHeartbeat]);

  useEffect(() => {
    connect();
    return cleanup;
  }, [connect, cleanup]);

  return { events, status, isConnected: status === "CONNECTED", error };
}
