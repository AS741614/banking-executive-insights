import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface MetricCardProps {
  label: string;
  value: string | number;
  subValue?: string;
  icon: LucideIcon;
  trend?: "up" | "down" | "neutral";
  color?: "primary" | "success" | "warning" | "critical" | "gold" | "accent";
  loading?: boolean;
}

export function MetricCard({
  label,
  value,
  subValue,
  icon: Icon,
  trend,
  color = "primary",
  loading
}: MetricCardProps) {
  const colorMap = {
    primary: "text-primary border-primary/20 hover:border-primary/40",
    success: "text-success border-success/20 hover:border-success/40",
    warning: "text-warning border-warning/20 hover:border-warning/40",
    critical: "text-critical border-critical/20 hover:border-critical/40",
    gold: "text-gold border-gold/20 hover:border-gold/40",
    accent: "text-primary-accent border-primary-accent/20 hover:border-primary-accent/40",
  };

  const iconColorMap = {
    primary: "text-primary",
    success: "text-success",
    warning: "text-warning",
    critical: "text-critical",
    gold: "text-gold",
    accent: "text-primary-accent",
  };

  return (
    <div className={cn(
      "panel-glass p-4 min-h-[120px] flex flex-col justify-between group transition-all duration-300",
      colorMap[color]
    )}>
      <div className="flex justify-between items-start">
        <span className="text-[10px] text-gray-400 font-space tracking-widest uppercase">{label}</span>
        <Icon className={cn("w-4 h-4", iconColorMap[color])} />
      </div>
      
      <div className="mt-2 flex flex-col">
        {loading ? (
          <div className="h-8 w-24 bg-white/5 animate-pulse rounded" />
        ) : (
          <span className={cn("text-2xl font-bold tracking-tight", iconColorMap[color])}>
            {value}
          </span>
        )}
        {subValue && (
          <span className="text-[10px] text-gray-500 font-mono mt-1">{subValue}</span>
        )}
      </div>

      {trend && !loading && (
        <div className="mt-2 flex items-center space-x-1">
          <div className={cn(
            "w-1 h-1 rounded-full",
            trend === "up" ? "bg-success" : trend === "down" ? "bg-critical" : "bg-gray-500"
          )} />
          <span className="text-[9px] text-gray-500 uppercase font-bold tracking-tighter">
            Trend: {trend}
          </span>
        </div>
      )}
    </div>
  );
}
