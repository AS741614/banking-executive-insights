import { forwardRef } from "react";
import { cn } from "@/lib/utils";

export const Card = forwardRef<HTMLDivElement, { className?: string; children: React.ReactNode }>(
  ({ className, children }, ref) => (
    <div ref={ref} className={cn("glass-panel rounded-xl overflow-hidden shadow-2xl", className)}>
      {children}
    </div>
  )
);
Card.displayName = "Card";

export function CardHeader({ className, children }: { className?: string; children: React.ReactNode }) {
  return (
    <div className={cn("px-6 py-4 border-b border-white/5", className)}>
      {children}
    </div>
  );
}

export const CardContent = forwardRef<HTMLDivElement, { className?: string; children: React.ReactNode }>(
  ({ className, children }, ref) => (
    <div ref={ref} className={cn("p-6", className)}>
      {children}
    </div>
  )
);
CardContent.displayName = "CardContent";

export function Stat({ label, value, subvalue, trend, trendValue }: { 
  label: string; 
  value: string | number; 
  subvalue?: string;
  trend?: "up" | "down" | "neutral";
  trendValue?: string;
}) {
  return (
    <div className="space-y-1">
      <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">{label}</div>
      <div className="flex items-baseline gap-2">
        <div className="text-2xl font-heading font-bold text-white tracking-tight">{value}</div>
        {trend && (
          <div className={cn(
            "text-[10px] font-bold px-1.5 py-0.5 rounded",
            trend === "up" ? "bg-success/10 text-success" : 
            trend === "down" ? "bg-destructive/10 text-destructive" : 
            "bg-white/10 text-white/40"
          )}>
            {trend === "up" ? "↑" : trend === "down" ? "↓" : "•"} {trendValue}
          </div>
        )}
      </div>
      {subvalue && <div className="text-[10px] text-white/40 font-mono">{subvalue}</div>}
    </div>
  );
}
