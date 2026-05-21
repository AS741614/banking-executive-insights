"use client";

import { useExecutiveIntelligence } from "@/lib/queries";
import { Card, CardContent, CardHeader, Stat } from "@/components/shared/ui";
import { InstitutionalChartContainer } from "@/components/charts/institutional-chart-container";
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Cell
} from "recharts";
import { Coins, Landmark, ArrowUpRight, ArrowDownRight } from "lucide-react";
import { cn } from "@/lib/utils";

export default function TreasuryPage() {
  const { data, isLoading } = useExecutiveIntelligence();

  if (isLoading) return <div className="text-primary font-mono animate-pulse">CALCULATING_TREASURY_POSITIONS...</div>;

  const liquidityData = [
    { name: "Cash", value: 420 },
    { name: "Sovereign", value: 380 },
    { name: "Corporate", value: 240 },
    { name: "Equities", value: 120 },
    { name: "Others", value: 45 },
  ];

  const COLORS = ["#00D1FF", "#7B61FF", "#00FFAE", "#F4B942", "#FF4D6D"];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-heading font-bold text-white tracking-tight">Treasury & Liquidity Cockpit</h1>
          <p className="text-muted-foreground text-sm">Asset-liability management and funding optimization.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="flex items-center gap-6">
            <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
              <Landmark className="w-6 h-6 text-primary" />
            </div>
            <Stat label="Total Assets (AUM)" value={`$${data?.aum_trend?.[11] || 0}B`} trend="up" trendValue="0.4%" />
          </CardContent>
        </Card>
        <Card>
          <CardContent className="flex items-center gap-6">
            <div className="w-12 h-12 rounded-xl bg-success/10 flex items-center justify-center">
              <Coins className="w-6 h-6 text-success" />
            </div>
            <Stat label="Liquidity Buffer" value="$42.8B" subvalue="COVERAGE_RATIO: 142%" />
          </CardContent>
        </Card>
        <Card>
          <CardContent className="flex items-center gap-6">
            <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center">
              <ArrowUpRight className="w-6 h-6 text-accent" />
            </div>
            <Stat label="Net Funding Cost" value="3.12%" subvalue="WACC_OPTIMIZED" />
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <div className="text-xs font-bold text-white uppercase tracking-wider">Liquidity Composition by Asset Class</div>
          </CardHeader>
          <CardContent className="p-0">
            <InstitutionalChartContainer height={320}>
              <BarChart data={liquidityData} layout="vertical" margin={{ top: 20, right: 30, left: 10, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
                <XAxis type="number" stroke="rgba(255,255,255,0.3)" fontSize={10} tickLine={false} axisLine={false} />
                <YAxis dataKey="name" type="category" stroke="rgba(255,255,255,0.3)" fontSize={10} tickLine={false} axisLine={false} />
                <Tooltip 
                  cursor={{ fill: "rgba(255,255,255,0.05)" }}
                  contentStyle={{ backgroundColor: "#0B1120", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "8px" }}
                  itemStyle={{ color: "#00D1FF", fontSize: "12px" }}
                />
                <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                  {liquidityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </InstitutionalChartContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="text-xs font-bold text-white uppercase tracking-wider">Treasury Advisory & Insights</div>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded bg-success/10 flex items-center justify-center shrink-0">
                <ArrowUpRight className="w-4 h-4 text-success" />
              </div>
              <div className="space-y-1">
                <div className="text-sm font-medium text-white">Positive Carry Detected</div>
                <p className="text-xs text-muted-foreground">Short-term rate differentials in Sector 4 provide a 12bps carry opportunity for institutional sweep.</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded bg-warning/10 flex items-center justify-center shrink-0">
                <ArrowDownRight className="w-4 h-4 text-warning" />
              </div>
              <div className="space-y-1">
                <div className="text-sm font-medium text-white">Hedging Variance Warning</div>
                <p className="text-xs text-muted-foreground">Derivative counterparty exposure in Region B approaching internal limit. Recommend balancing through Region C.</p>
              </div>
            </div>

            <div className="pt-4 border-t border-white/5">
              <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-4">Funding Source Stability</div>
              <div className="space-y-3">
                <StabilityIndicator label="Core Deposits" value={82} color="bg-success" />
                <StabilityIndicator label="Commercial Paper" value={45} color="bg-warning" />
                <StabilityIndicator label="Interbank Funding" value={28} color="bg-primary" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function StabilityIndicator({ label, value, color }: { label: string, value: number, color: string }) {
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-[10px] text-white/60">
        <span>{label}</span>
        <span>{value}%</span>
      </div>
      <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
        <div className={cn("h-full rounded-full", color)} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}
