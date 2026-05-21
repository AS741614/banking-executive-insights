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
        if (width > 0 && height > 0) {
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
