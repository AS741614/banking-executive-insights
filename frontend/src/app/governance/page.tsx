"use client";

import { useGovernanceCognition } from "@/lib/governance-queries";
import { useGovernanceRealtime } from "@/hooks/use-governance-realtime";
import { Card, CardContent, CardHeader, Stat } from "@/components/shared/ui";
import { InstitutionalChartContainer } from "@/components/charts/institutional-chart-container";
import { ClientOnly } from "@/components/shared/client-only";
import { ScenarioControlPanel } from "@/components/governance/scenario-control-panel";
import { motion, AnimatePresence } from "framer-motion";
import { 
  ShieldCheck, 
  ShieldAlert, 
  History, 
  Scale, 
  AlertTriangle, 
  Activity,
  Users,
  Wifi,
  WifiOff,
  Loader2,
  Clock,
  ChevronRight,
  TrendingUp,
  Zap
} from "lucide-react";
import { 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar,
  Cell,
  PieChart,
  Pie
} from "recharts";
import { cn } from "@/lib/utils";

export default function GovernancePage() {
  const { data: govState, isLoading: stateLoading } = useGovernanceCognition();
  const { kycUpdates, escalations, isConnected, status: sseStatus } = useGovernanceRealtime();

  if (stateLoading) return <div className="text-primary font-mono animate-pulse p-8">INITIALISING_GOVERNANCE_KERNEL...</div>;

  const kycDistributionData = [
    { name: 'Approved', value: 65, color: '#00FFAE' },
    { name: 'Under Review', value: 20, color: '#F4B942' },
    { name: 'Rejected', value: 10, color: '#FF4D6D' },
    { name: 'Pending', value: 5, color: '#00D1FF' },
  ];

  const isCritical = govState?.governance_status !== "SYNCHRONIZED" || escalations.some(e => e.severity === "CRITICAL");

  return (
    <div className="space-y-8 animate-in fade-in duration-700">
      <div className="flex items-end justify-between">
        <motion.div 
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-3xl font-heading font-bold text-white tracking-tight flex items-center gap-3">
            Governance Intelligence
            <div className="h-1.5 w-1.5 rounded-full bg-primary animate-pulse" />
          </h1>
          <p className="text-muted-foreground text-sm">Institutional oversight and regulatory escalation cockpit.</p>
        </motion.div>
        
        <motion.div 
          className="flex items-center gap-4"
          initial={{ x: 20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
           <div className={cn(
              "flex items-center gap-2 px-3 py-1 rounded-full border text-[10px] font-bold uppercase tracking-widest transition-all duration-1000",
              isConnected ? "bg-success/10 border-success/20 text-success" : "bg-warning/10 border-warning/20 text-warning"
            )}>
              {isConnected ? <Wifi className="w-3 h-3" /> : <Loader2 className="w-3 h-3 animate-spin" />}
              {isConnected ? "Kernel: Synced" : "Kernel: Connecting..."}
            </div>
          <div className="text-right border-l border-white/10 pl-4">
            <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">Oversight Version</div>
            <div className="text-xs font-mono text-white/60">v2.4.0-STABLE</div>
          </div>
        </motion.div>
      </div>

      {/* KPI Layer */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className={cn(
          "border-l-4 transition-all duration-1000 relative overflow-hidden group",
          govState?.governance_status === "SYNCHRONIZED" 
            ? "border-l-success cinematic-gradient-blue" 
            : "border-l-destructive animate-pulse-critical cinematic-gradient-red"
        )}>
          <div className="cinematic-overlay" />
          <CardContent className="relative z-10">
            <Stat 
              label="Governance Posture" 
              value={govState?.governance_status || "UNKNOWN"} 
              subvalue="ECOS_KERNEL_INTEGRITY"
              trend={govState?.governance_status === "SYNCHRONIZED" ? "up" : "down"}
              trendValue={govState?.governance_status === "SYNCHRONIZED" ? "NOMINAL" : "DRIFT"}
            />
          </CardContent>
        </Card>

        <Card className="hover:border-primary/30 transition-colors group">
          <CardContent>
            <Stat 
              label="Compliance Score" 
              value={`${govState?.compliance_score}%`} 
              subvalue="TARGET: 99.5%"
              trend="neutral"
              trendValue="STABLE"
            />
          </CardContent>
        </Card>

        <Card className={cn(
          "hover:border-primary/30 transition-all group",
          (govState?.pending_escalations ?? 0) > 0 && "border-warning/50 animate-pulse-warning"
        )}>
          <CardContent>
            <Stat 
              label="Active Escalations" 
              value={govState?.pending_escalations || 0} 
              subvalue="REGULATORY_QUEUE"
              trend={govState?.pending_escalations === 0 ? "neutral" : "down"}
              trendValue={govState?.pending_escalations === 0 ? "CLEAR" : "ACTION_REQ"}
            />
          </CardContent>
        </Card>

        <Card className="hover:border-primary/30 transition-colors group">
          <CardContent>
            <Stat 
              label="Policy Enforcement" 
              value={govState?.active_policies || 0} 
              subvalue="INSTITUTIONAL_GUARDRAILS"
            />
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Escalation Activity Feed */}
        <Card className="lg:col-span-2 flex flex-col min-h-[500px] scanning-effect">
          <CardHeader className="flex flex-row items-center justify-between border-b border-white/5 py-4">
            <div className="flex items-center gap-2">
              <AlertTriangle className={cn("w-4 h-4", isCritical ? "text-destructive animate-pulse" : "text-warning")} />
              <div className="text-xs font-bold text-white uppercase tracking-wider">Institutional Incident Timeline</div>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex gap-1">
                <div className="h-1 w-8 rounded-full bg-success/20" />
                <div className="h-1 w-8 rounded-full bg-primary" />
                <div className="h-1 w-8 rounded-full bg-success/20" />
              </div>
              <div className="text-[10px] font-mono text-primary/60">REALTIME_STREAM_LOCKED</div>
            </div>
          </CardHeader>
          <CardContent className="flex-1 overflow-y-auto p-0">
            <div className="divide-y divide-white/5">
              <AnimatePresence initial={false}>
                {escalations.length === 0 ? (
                  <motion.div 
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="p-20 text-center text-muted-foreground italic flex flex-col items-center gap-4"
                  >
                    <ShieldCheck className="w-12 h-12 text-white/5" />
                    <span className="text-sm font-medium tracking-tight">No active regulatory escalations detected.</span>
                  </motion.div>
                ) : (
                  escalations.map((event) => (
                    <motion.div 
                      key={event.event_id} 
                      layout
                      initial={{ opacity: 0, x: -20, height: 0 }}
                      animate={{ opacity: 1, x: 0, height: 'auto' }}
                      exit={{ opacity: 0, x: 20 }}
                      className={cn(
                        "p-5 hover:bg-white/[0.02] transition-all flex gap-5 group relative",
                        event.severity === "CRITICAL" && "bg-destructive/5"
                      )}
                    >
                      <div className="flex flex-col items-center gap-2">
                        <div className={cn(
                          "w-2 h-2 rounded-full mt-2",
                          event.severity === "CRITICAL" ? "bg-destructive shadow-[0_0_8px_#FF4D6D]" : 
                          event.severity === "HIGH" ? "bg-warning shadow-[0_0_8px_#FFB020]" : "bg-primary"
                        )} />
                        <div className="w-px flex-1 bg-white/5 group-last:bg-transparent" />
                      </div>

                      <div className="flex-1 space-y-2">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                             <span className={cn(
                              "text-[9px] font-bold px-2 py-0.5 rounded border uppercase tracking-tighter",
                              event.severity === "CRITICAL" ? "bg-destructive/10 text-destructive border-destructive/20" : "bg-warning/10 text-warning border-warning/20"
                            )}>
                              {event.severity}
                            </span>
                            <span className="text-xs font-bold text-white uppercase tracking-widest">{event.domain} INCIDENT</span>
                          </div>
                          <span className="text-[10px] font-mono text-white/20">{new Date(event.timestamp).toLocaleTimeString()}</span>
                        </div>
                        
                        <p className="text-sm text-white/80 leading-relaxed font-medium">
                          {event.message}
                        </p>
                        
                        <div className="flex items-center justify-between pt-1">
                          <div className="flex items-center gap-4">
                            <div className="text-[9px] text-primary/60 font-mono flex items-center gap-1.5">
                              <Zap className="w-3 h-3" />
                              TRACE: {event.event_id.substring(0, 8)}
                            </div>
                            <div className="text-[9px] text-muted-foreground font-mono flex items-center gap-1.5">
                              <Clock className="w-3 h-3" />
                              LATENCY: 124ms
                            </div>
                          </div>
                          <button className="flex items-center gap-1.5 px-3 py-1 bg-white/5 border border-white/10 rounded text-[9px] font-bold text-white hover:bg-primary hover:text-background transition-all group/btn">
                            ANALYSIS_KERNEL
                            <ChevronRight className="w-3 h-3 transition-transform group-hover/btn:translate-x-0.5" />
                          </button>
                        </div>
                      </div>
                    </motion.div>
                  ))
                )}
              </AnimatePresence>
            </div>
          </CardContent>
        </Card>

        {/* KYC Lifecycle Distribution */}
        <div className="space-y-6">
          <Card className="hover:border-primary/20 transition-all overflow-hidden relative group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <TrendingUp className="w-16 h-16 text-primary" />
            </div>
            <CardHeader className="border-b border-white/5 py-4">
              <div className="text-xs font-bold text-white uppercase tracking-wider">KYC Cognition Topology</div>
            </CardHeader>
            <CardContent className="p-0">
              <InstitutionalChartContainer height={220}>
                <PieChart>
                  <Pie
                    data={kycDistributionData}
                    innerRadius={55}
                    outerRadius={75}
                    paddingAngle={8}
                    dataKey="value"
                    stroke="none"
                    animationDuration={1500}
                    animationBegin={200}
                  >
                    {kycDistributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} fillOpacity={0.8} className="hover:opacity-100 transition-opacity" />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ backgroundColor: "#0B1120", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "8px", boxShadow: "0 10px 25px -5px rgba(0,0,0,0.5)" }}
                    itemStyle={{ fontSize: "11px", fontWeight: "bold" }}
                  />
                </PieChart>
              </InstitutionalChartContainer>
              <div className="p-6 pt-0 grid grid-cols-2 gap-3">
                {kycDistributionData.map(item => (
                  <div key={item.name} className="flex items-center gap-2 group/legend cursor-default">
                    <div className="w-1.5 h-1.5 rounded-full transition-transform group-hover/legend:scale-150" style={{ backgroundColor: item.color }} />
                    <div className="flex flex-col">
                       <span className="text-[9px] text-white/40 uppercase font-bold tracking-tighter leading-none">{item.name}</span>
                       <span className="text-xs text-white/80 font-mono font-bold leading-none mt-0.5">{item.value}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <ScenarioControlPanel />
          
          <Card className="bg-primary/5 border-primary/10">
            <CardContent className="p-4 space-y-3">
              <div className="flex items-center gap-2 text-[10px] font-bold text-primary uppercase">
                <Activity className="w-3 h-3" />
                Operational Realignment
              </div>
              <p className="text-[10px] text-white/60 leading-relaxed italic">
                Governance realignment active. ECOS kernel automatically adjusting policy weights based on {escalations.length} new incidents.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
