"use client";

import React, { useState, useEffect, useRef } from "react";
import { ResponsiveContainer } from "recharts";
import { cn } from "@/lib/utils";

interface InstitutionalChartContainerProps {
  children: React.ReactElement;
  height?: number | string;
  minHeight?: number;
  className?: string;
  fallback?: React.ReactNode;
}

/**
 * InstitutionalChartContainer v2 (Hardened)
 * 
 * Forensic-grade wrapper for Recharts components to achieve ZERO runtime warnings.
 * 
 * Root Cause Fix:
 * Recharts ResponsiveContainer triggers width(-1) warnings when it attempts to measure 
 * parent DOM dimensions during hydration or before paint. 
 * 
 * Strategy:
 * 1. Use ResizeObserver to detect stable, strictly positive parent dimensions.
 * 2. Delay rendering until dimensions > 0 are confirmed.
 * 3. Use requestAnimationFrame to ensure the browser has finished layout paint.
 * 4. Pass explicit numeric dimensions to ResponsiveContainer to bypass its internal DOM measurement logic.
 */
export function InstitutionalChartContainer({
  children,
  height = 320,
  minHeight = 320,
  className,
  fallback
}: InstitutionalChartContainerProps) {
  const [isMounted, setIsMounted] = useState(false);
  const [dimensions, setDimensions] = useState<{ width: number; height: number } | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setIsMounted(true);
    
    if (!containerRef.current) return;

    const observer = new ResizeObserver((entries) => {
      const entry = entries[0];
      if (entry) {
        const { width, height } = entry.contentRect;
        
        // Institutional Guard: strictly positive dimensions only
        if (width > 0 && height > 0) {
          // ensure paint is complete
          window.requestAnimationFrame(() => {
            setDimensions({ width, height });
          });
        }
      }
    });

    observer.observe(containerRef.current);
    
    return () => {
      observer.disconnect();
    };
  }, []);

  const defaultFallback = (
    <div 
      className={cn(
        "w-full bg-white/[0.01] animate-pulse rounded-lg flex items-center justify-center border border-white/5",
        className
      )}
      style={{ height, minHeight }}
    >
      <div className="text-[10px] font-mono text-white/10 uppercase tracking-widest text-center px-4">
        Synchronising_Institutional_Dimensions...
      </div>
    </div>
  );

  // We only render children if we are mounted AND have positive dimensions measured.
  // We pass these dimensions EXPLICITLY to ResponsiveContainer to prevent it from failing.
  const shouldRender = isMounted && dimensions && dimensions.width > 0 && dimensions.height > 0;

  return (
    <div 
      ref={containerRef}
      className={cn("w-full h-full relative overflow-hidden", className)}
      style={{ height, minHeight }}
    >
      {shouldRender ? (
        <div className="absolute inset-0 w-full h-full">
          <ResponsiveContainer width={dimensions.width} height={dimensions.height}>
            {children}
          </ResponsiveContainer>
        </div>
      ) : (
        fallback || defaultFallback
      )}
    </div>
  );
}
