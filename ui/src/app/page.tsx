"use client";

import { Header } from "@/components/layout/Header";
import { MetricCard } from "@/components/dashboard/MetricCard";
import { usePlatformStatus, useEventHistory } from "@/hooks/use-platform";
import { 
  useExecutiveIntelligence, 
  useRiskIntelligence, 
  useGovernanceCognition,
  useForecastIntelligence 
} from "@/hooks/use-intelligence";
import { 
  Activity, 
  ShieldAlert, 
  TrendingUp, 
  Zap, 
  Globe, 
  Cpu, 
  BarChart3,
  Terminal
} from "lucide-react";
import { format } from "date-fns";

export default function ExecutiveDashboard() {
  const { data: statusData, isLoading: statusLoading } = usePlatformStatus();
  const { data: historyData, isLoading: historyLoading } = useEventHistory();
  const { data: execIntel, isLoading: execLoading } = useExecutiveIntelligence();
  const { data: riskIntel, isLoading: riskLoading } = useRiskIntelligence();
  const { data: govIntel, isLoading: govLoading } = useGovernanceCognition();
  const { data: forecastIntel, isLoading: forecastLoading } = useForecastIntelligence();

  const events = historyData?.data?.events || [];
  const status = statusData?.data;

  return (
    <div className="flex flex-col h-full bg-background overflow-hidden">
      <Header title="EXECUTIVE_OVERVIEW" />
      
      <main className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* Top KPI Layer */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <MetricCard 
            label="Platform Resilience"
            value={status?.status || "SYNC..."}
            subValue={`Uptime: ${status?.uptime || '99.99%'}`}
            icon={Activity}
            color={status?.status === 'OPERATIONAL' ? 'success' : 'warning'}
            loading={statusLoading}
            trend="neutral"
          />
          <MetricCard 
            label="Risk Intelligence"
            value={riskIntel?.data?.risk_score || "NOMINAL"}
            subValue="Institutional Exposure"
            icon={ShieldAlert}
            color="gold"
            loading={riskLoading}
            trend="down"
          />
          <MetricCard 
            label="Compute Efficiency"
            value="84.2%"
            subValue="L_4 Orchestration"
            icon={Cpu}
            color="primary"
            loading={execLoading}
            trend="up"
          />
          <MetricCard 
            label="Market Projection"
            value="+1.24%"
            subValue="24h Forecast Delta"
            icon={TrendingUp}
            color="accent"
            loading={forecastLoading}
            trend="up"
          />
        </div>

        {/* Secondary Metric Layer */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            {/* Intelligence Summary Panel */}
            <div className="panel-glass p-6">
              <div className="flex justify-between items-center mb-6">
                <div className="flex items-center space-x-2">
                  <BarChart3 className="w-4 h-4 text-primary" />
                  <h2 className="text-sm font-space font-bold tracking-widest text-gray-300 uppercase">Executive_Intelligence_Summary</h2>
                </div>
                <span className="text-[10px] font-mono text-gray-500 uppercase">Source: Cognitive_Engine_V4</span>
              </div>
              
              <div className="prose prose-invert max-w-none">
                <p className="text-xs text-gray-400 leading-relaxed font-mono">
                  {execIntel?.data?.summary || "Analyzing institutional data streams... Generating executive summary based on real-time telemetry and governance events."}
                </p>
                <div className="grid grid-cols-2 gap-4 mt-6">
                  <div className="bg-black/40 border border-white/5 p-3 rounded-lg">
                    <span className="text-[10px] text-primary font-bold block mb-1 tracking-tighter uppercase">Governance_Health</span>
                    <div className="h-1.5 w-full bg-white/5 rounded-full mt-2 overflow-hidden">
                      <div className="h-full bg-primary w-4/5" />
                    </div>
                  </div>
                  <div className="bg-black/40 border border-white/5 p-3 rounded-lg">
                    <span className="text-[10px] text-success font-bold block mb-1 tracking-tighter uppercase">Operational_Liquidity</span>
                    <div className="h-1.5 w-full bg-white/5 rounded-full mt-2 overflow-hidden">
                      <div className="h-full bg-success w-3/4" />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Event Stream Panel */}
            <div className="panel-glass p-6 min-h-[300px]">
              <div className="flex justify-between items-center mb-6">
                <div className="flex items-center space-x-2">
                  <Terminal className="w-4 h-4 text-primary" />
                  <h2 className="text-sm font-space font-bold tracking-widest text-gray-300 uppercase">Real-Time_Intelligence_Stream</h2>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 rounded-full bg-success animate-pulse" />
                  <span className="text-[10px] font-mono text-gray-500 uppercase">Live_Telemetry</span>
                </div>
              </div>
              
              <div className="space-y-2 max-h-[400px] overflow-y-auto custom-scrollbar pr-2">
                {historyLoading ? (
                  <div className="flex items-center space-x-2 text-xs text-gray-500 font-mono animate-pulse">
                    <span>{'>'}</span>
                    <span>Synchronizing institutional event history...</span>
                  </div>
                ) : events.length > 0 ? (
                  events.map((event: any, i: number) => (
                    <div key={i} className="flex items-start space-x-4 text-[11px] border-l border-white/5 pl-4 py-2 hover:bg-white/[0.02] transition-colors group">
                      <span className="text-gray-500 font-mono w-20 shrink-0">{format(new Date(event.timestamp), "HH:mm:ss")}</span>
                      <span className="text-primary font-bold shrink-0 min-w-[80px]">[{event.domain || 'SYSTEM'}]</span>
                      <span className="text-gray-400 group-hover:text-gray-200 transition-colors leading-relaxed">{event.message}</span>
                    </div>
                  ))
                ) : (
                  <p className="text-xs font-mono text-gray-600 italic">No recent institutional events detected.</p>
                )}
              </div>
            </div>
          </div>

          {/* Right Sidebar - System Integrity & Nodes */}
          <div className="space-y-6">
            <div className="panel-glass p-6">
              <h3 className="text-[10px] font-space font-bold tracking-widest text-gray-400 uppercase mb-4">Institutional_Nodes</h3>
              <div className="space-y-4">
                {[
                  { name: "NY_CORE_01", status: "online", load: 12 },
                  { name: "LDN_EDGE_04", status: "online", load: 24 },
                  { name: "SGP_CORE_02", status: "online", load: 18 },
                  { name: "HKG_REPL_09", status: "maintenance", load: 0 },
                ].map((node) => (
                  <div key={node.name} className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Globe className={cn("w-3 h-3", node.status === 'online' ? 'text-success' : 'text-warning')} />
                      <span className="text-xs font-mono text-gray-300">{node.name}</span>
                    </div>
                    <span className={cn(
                      "text-[9px] font-bold px-1.5 py-0.5 rounded border uppercase",
                      node.status === 'online' 
                        ? 'text-success border-success/20 bg-success/5' 
                        : 'text-warning border-warning/20 bg-warning/5'
                    )}>
                      {node.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="panel-glass p-6">
              <h3 className="text-[10px] font-space font-bold tracking-widest text-gray-400 uppercase mb-4">Governance_Snapshots</h3>
              <div className="space-y-4">
                {govIntel?.data?.snapshots?.slice(0, 3).map((snap: any, i: number) => (
                  <div key={i} className="p-3 bg-black/40 border border-white/5 rounded-lg space-y-1 hover:border-primary/30 transition-colors cursor-pointer group">
                    <div className="flex justify-between items-center">
                      <span className="text-[10px] text-primary font-bold uppercase">{snap.type || 'RECONCILIATION'}</span>
                      <span className="text-[9px] text-gray-500 font-mono">{format(new Date(snap.timestamp), "MMM dd")}</span>
                    </div>
                    <p className="text-[11px] text-gray-400 group-hover:text-gray-300 line-clamp-2">{snap.description}</p>
                  </div>
                )) || (
                  <p className="text-[10px] text-gray-600 italic">No governance snapshots available.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
