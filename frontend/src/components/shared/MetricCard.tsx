"use client";

import { cn } from "@/lib/utils";
import { ArrowUpRight, ArrowDownRight } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  change?: number;
  status?: "success" | "warning" | "destructive" | "neutral";
  label?: string;
  className?: string;
}

export function MetricCard({ title, value, change, status = "neutral", label, className }: MetricCardProps) {
  return (
    <div className={cn("glass-panel p-5 rounded-sm flex flex-col justify-between h-32", className)}>
      <div className="flex justify-between items-start">
        <span className="text-[10px] font-bold text-muted-foreground tracking-widest uppercase">{title}</span>
        {status !== "neutral" && (
           <div className={cn("w-2 h-2 rounded-full shadow-[0_0_8px]", {
             "bg-success shadow-success/50": status === "success",
             "bg-warning shadow-warning/50": status === "warning",
             "bg-destructive shadow-destructive/50": status === "destructive",
           })} />
        )}
      </div>
      <div className="flex items-end justify-between">
        <div>
          <div className="text-2xl font-heading font-bold tracking-tight">{value}</div>
          {label && <div className="text-[10px] text-muted-foreground mt-1 uppercase tracking-wider">{label}</div>}
        </div>
        {change !== undefined && (
          <div className={cn("flex items-center text-[10px] font-bold", change >= 0 ? "text-success" : "text-destructive")}>
            {change >= 0 ? <ArrowUpRight className="w-3 h-3 mr-0.5" /> : <ArrowDownRight className="w-3 h-3 mr-0.5" />}
            {Math.abs(change)}%
          </div>
        )}
      </div>
    </div>
  );
}
