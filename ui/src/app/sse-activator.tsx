"use client";

import { useSseRuntime } from "@/hooks/use-observability";

export function SseActivator() {
  useSseRuntime();
  return null;
}
