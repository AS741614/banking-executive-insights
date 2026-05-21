"use client";

import { useExecutiveIntelligence } from "@/lib/queries";
import { Card, CardContent, CardHeader, Stat } from "@/components/shared/ui";
import { ClientOnly } from "@/components/shared/client-only";
import { InstitutionalChartContainer } from "@/components/charts/institutional-chart-container";
import { 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  AreaChart,
  Area
} from "recharts";
import { TrendingUp, Shield, Zap } from "lucide-react";

export default function ExecutivePage() {
  const { data, isLoading, error } = useExecutiveIntelligence();

  if (isLoading) return <div className="text-primary font-mono animate-pulse">BOOTING_INTELLIGENCE_KERNEL...</div>;
  if (error) return <div className="text-destructive font-mono">CRITICAL_SYSTEM_ERROR: UNABLE_TO_RETRIEVE_INTELLIGENCE</div>;

  const chartData = (data?.aum_trend || []).map((val, i) => ({ name: `T-${12-i}`, value: val }));

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-heading font-bold text-white tracking-tight">Executive Command Overview</h1>
          <p className="text-muted-foreground text-sm">Institutional health and risk posture analysis.</p>
        </div>
        <div className="text-right">
          <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">Last Update</div>
          <ClientOnly fallback={<div className="text-xs font-mono text-white/20">--:--:--</div>}>
            <div className="text-xs font-mono text-white/60">{new Date().toLocaleTimeString()}</div>
          </ClientOnly>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="accent-glow border-primary/20">
          <CardContent>
            <Stat 
              label="Institutional Health" 
              value={`${data?.institutional_health_score}%`} 
              trend="up" 
              trendValue="1.2%"
              subvalue="KERNEL_STABILITY: OPTIMAL"
            />
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <Stat 
              label="Capital Adequacy (CAR)" 
              value={`${data?.capital_adequacy_ratio}%`} 
              subvalue="REGULATORY_MIN: 12.5%"
            />
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <Stat 
              label="Liquidity (LCR)" 
              value={`${data?.liquidity_coverage_ratio}%`} 
              subvalue="STRESS_TEST: PASSED"
            />
          </CardContent>
        </Card>
        <Card className={data?.active_escalations ? "border-destructive/50" : ""}>
          <CardContent>
            <Stat 
              label="Active Escalations" 
              value={data?.active_escalations || 0} 
              trend={data?.active_escalations ? "down" : "neutral"}
              trendValue={data?.active_escalations ? "CRITICAL" : "CLEAR"}
              subvalue="GOVERNANCE_QUEUE"
            />
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="text-xs font-bold text-white uppercase tracking-wider">AUM Growth Projection</div>
              <TrendingUp className="w-4 h-4 text-primary" />
            </div>
          </CardHeader>
          <CardContent className="p-0">
            <InstitutionalChartContainer height={320}>
              <AreaChart data={chartData} margin={{ top: 20, right: 30, left: 10, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#00D1FF" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#00D1FF" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis 
                  dataKey="name" 
                  stroke="rgba(255,255,255,0.3)" 
                  fontSize={10} 
                  tickLine={false} 
                  axisLine={false}
                />
                <YAxis 
                  stroke="rgba(255,255,255,0.3)" 
                  fontSize={10} 
                  tickLine={false} 
                  axisLine={false}
                  tickFormatter={(val) => `$${val}B`}
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: "#0B1120", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "8px" }}
                  itemStyle={{ color: "#00D1FF", fontSize: "12px" }}
                />
                <Area 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#00D1FF" 
                  strokeWidth={2}
                  fillOpacity={1} 
                  fill="url(#colorValue)" 
                />
              </AreaChart>
            </InstitutionalChartContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="text-xs font-bold text-white uppercase tracking-wider">Risk Intelligence</div>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <Shield className="w-5 h-5 text-primary" />
              </div>
              <div>
                <div className="text-sm font-bold text-white">Posture: {data?.risk_posture}</div>
                <div className="text-[10px] text-muted-foreground uppercase tracking-widest">ECOS_STATE_SYNCED</div>
              </div>
            </div>
            
            <div className="space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between text-[10px] font-bold text-muted-foreground uppercase">
                  <span>Exposure Concentration</span>
                  <span className="text-white">Low</span>
                </div>
                <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-success w-[24%]" />
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex justify-between text-[10px] font-bold text-muted-foreground uppercase">
                  <span>Volatility Sensitivity</span>
                  <span className="text-white">Moderate</span>
                </div>
                <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-warning w-[45%]" />
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-[10px] font-bold text-muted-foreground uppercase">
                  <span>Anomaly Propagation</span>
                  <span className="text-white">Minimal</span>
                </div>
                <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-primary w-[12%]" />
                </div>
              </div>
            </div>

            <div className="p-4 rounded-lg bg-success/5 border border-success/10 flex items-start gap-3">
              <Zap className="w-4 h-4 text-success shrink-0 mt-0.5" />
              <div className="text-[10px] text-success leading-normal font-medium">
                AI_COPILOT_ADVISORY: Institutional liquidity buffers are currently 18% above target. Opportunity for treasury optimization detected.
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
