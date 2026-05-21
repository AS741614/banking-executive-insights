"use client";

import { useState, useEffect } from "react";
import { create } from "zustand";

interface ObservabilityState {
  apiLatency: number[];
  sseStatus: "connected" | "disconnected" | "connecting";
  errors: string[];
  addLatency: (ms: number) => void;
  setSseStatus: (status: "connected" | "disconnected" | "connecting") => void;
  addError: (error: string) => void;
}

export const useObservabilityStore = create<ObservabilityState>((set) => ({
  apiLatency: [],
  sseStatus: "disconnected",
  errors: [],
  addLatency: (ms) => set((state) => ({ 
    apiLatency: [...state.apiLatency.slice(-19), ms] 
  })),
  setSseStatus: (status) => set({ sseStatus: status }),
  addError: (error) => set((state) => ({ 
    errors: [...state.errors.slice(-9), error] 
  })),
}));

export function useSseRuntime() {
  const { setSseStatus, addError } = useObservabilityStore();

  useEffect(() => {
    let eventSource: EventSource | null = null;

    const connect = () => {
      setSseStatus("connecting");
      eventSource = new EventSource("/api/v1/platform/stream");

      eventSource.onopen = () => {
        setSseStatus("connected");
      };

      eventSource.onerror = (e) => {
        setSseStatus("disconnected");
        addError("SSE_CONNECTION_LOST");
        eventSource?.close();
        // Reconnect after 5s
        setTimeout(connect, 5000);
      };

      eventSource.onmessage = (event) => {
        // Handle incoming institutional events
      };
    };

    connect();

    return () => {
      eventSource?.close();
    };
  }, [setSseStatus, addError]);
}
