"use client";

import { Header } from "@/components/layout/Header";
import { MetricCard } from "@/components/dashboard/MetricCard";
import { useGovernanceCognition } from "@/hooks/use-intelligence";
import { 
  Gavel, 
  GitBranch, 
  ShieldCheck, 
  RefreshCw, 
  Network, 
  FileCheck,
  Zap,
  ChevronRight
} from "lucide-react";
import { cn } from "@/lib/utils";

const TOPOLOGY_NODES = [
  { name: "CORE_01", type: "MASTER", status: "ONLINE", region: "GLOBAL" },
  { name: "AMER_HUB", type: "REGIONAL", status: "ONLINE", region: "AMER" },
  { name: "EMEA_HUB", type: "REGIONAL", status: "ONLINE", region: "EMEA" },
  { name: "NY_NODE_01", type: "EDGE", status: "ONLINE", region: "AMER" },
  { name: "SF_NODE_02", type: "EDGE", status: "ONLINE", region: "AMER" },
  { name: "LDN_NODE_01", type: "EDGE", status: "ONLINE", region: "EMEA" },
  { name: "FRA_NODE_02", type: "EDGE", status: "ONLINE", region: "EMEA" },
];

export default function GovernanceCockpit() {
  const { data: govIntel, isLoading } = useGovernanceCognition();
  const intel = govIntel?.data || {};

  return (
    <div className="flex flex-col h-full bg-background overflow-hidden">
      <Header title="GOVERNANCE_COCKPIT" />
      
      <main className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* Top KPI Layer */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <MetricCard 
            label="Governance Alignment"
            value="98.4%"
            subValue="Institutional Compliance"
            icon={ShieldCheck}
            color="success"
            loading={isLoading}
            trend="up"
          />
          <MetricCard 
            label="Policy Drift"
            value="0.12%"
            subValue="System-wide Variance"
            icon={RefreshCw}
            color="primary"
            loading={isLoading}
            trend="down"
          />
          <MetricCard 
            label="Node Connectivity"
            value="100%"
            subValue="7/7 Nodes Synchronized"
            icon={Network}
            color="accent"
            loading={isLoading}
            trend="neutral"
          />
          <MetricCard 
            label="Evolution Cycle"
            value="V2.4"
            subValue="Current Framework"
            icon={GitBranch}
            color="gold"
            loading={isLoading}
            trend="neutral"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
                {/* Topology Map Placeholder */}
                <div className="panel-glass p-6">
                    <div className="flex justify-between items-center mb-8">
                        <div className="flex items-center space-x-2">
                            <Network className="w-4 h-4 text-primary" />
                            <h2 className="text-sm font-space font-bold tracking-widest text-gray-300 uppercase">Institutional_Topology_Map</h2>
                        </div>
                        <span className="text-[10px] font-mono text-gray-500 uppercase">Schema: Active_Deployment</span>
                    </div>
                    
                    <div className="relative min-h-[300px] flex items-center justify-center">
                        {/* Simple tree/topology visualization with CSS */}
                        <div className="relative w-full max-w-2xl flex flex-col items-center space-y-12">
                            {/* Master Node */}
                            <div className="w-32 h-16 bg-primary/10 border border-primary/30 rounded-lg flex flex-col items-center justify-center space-y-1 z-10 hover:border-primary transition-colors cursor-pointer group">
                                <span className="text-[10px] text-primary font-bold tracking-tighter uppercase">INSTITUTIONAL_CORE</span>
                                <span className="text-[8px] text-success font-mono">MASTER_NODE</span>
                            </div>

                            {/* Connection Lines (SVGs) */}
                            <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-20" preserveAspectRatio="none">
                                <line x1="50%" y1="64" x2="30%" y2="128" stroke="white" strokeWidth="1" />
                                <line x1="50%" y1="64" x2="70%" y2="128" stroke="white" strokeWidth="1" />
                            </svg>

                            {/* Regional Hubs */}
                            <div className="flex justify-around w-full">
                                <div className="w-28 h-14 bg-white/5 border border-white/10 rounded-lg flex flex-col items-center justify-center space-y-1 z-10 hover:border-primary/50 transition-colors cursor-pointer">
                                    <span className="text-[10px] text-gray-300 font-bold tracking-tighter uppercase">AMER_HUB</span>
                                    <span className="text-[8px] text-success font-mono">STABLE</span>
                                </div>
                                <div className="w-28 h-14 bg-white/5 border border-white/10 rounded-lg flex flex-col items-center justify-center space-y-1 z-10 hover:border-primary/50 transition-colors cursor-pointer">
                                    <span className="text-[10px] text-gray-300 font-bold tracking-tighter uppercase">EMEA_HUB</span>
                                    <span className="text-[8px] text-success font-mono">STABLE</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Policy Drift Matrix */}
                <div className="panel-glass overflow-hidden">
                    <div className="p-4 border-b border-white/5 bg-white/[0.02] flex justify-between items-center">
                        <h3 className="text-[10px] font-space font-bold tracking-widest text-gray-400 uppercase">Policy_Drift_Alignment_Matrix</h3>
                        <div className="flex items-center space-x-2">
                            <span className="text-[9px] text-gray-500 font-mono">Drift_Detected: </span>
                            <span className={cn("text-[9px] font-bold font-mono", intel.drift_detected ? "text-critical" : "text-success")}>
                                {intel.drift_detected ? "CRITICAL_DRIFT" : "NOMINAL"}
                            </span>
                        </div>
                    </div>
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="border-b border-white/5 bg-white/[0.01]">
                                <th className="p-4 text-[10px] font-space font-bold text-gray-500 uppercase tracking-tighter">Policy_Domain</th>
                                <th className="p-4 text-[10px] font-space font-bold text-gray-500 uppercase tracking-tighter">Alignment</th>
                                <th className="p-4 text-[10px] font-space font-bold text-gray-500 uppercase tracking-tighter">Status</th>
                                <th className="p-4 text-[10px] font-space font-bold text-gray-500 uppercase tracking-tighter">Last_Evolution</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/5">
                            {(intel.policy_drift_matrix || [
                                { domain: "AML_SYNC_V4", alignment: "98.2%", status: "OPTIMAL", last: "2026-05-10" },
                                { domain: "KYC_ENHANCED", alignment: "99.1%", status: "OPTIMAL", last: "2026-05-12" },
                                { domain: "TREASURY_L1_LIQUIDITY", alignment: "82.4%", status: "DRIFT", last: "2026-04-20" },
                                { domain: "FRAUD_PRO_SIGNATURES", alignment: "94.8%", status: "DEGRADED", last: "2026-05-15" },
                            ]).map((row: any) => (
                                <tr key={row.domain} className="hover:bg-white/[0.02] transition-colors group">
                                    <td className="p-4 text-[11px] font-mono text-gray-300 uppercase">{row.domain}</td>
                                    <td className="p-4 text-[11px] font-mono text-white font-bold">{row.alignment}</td>
                                    <td className="p-4">
                                        <span className={cn(
                                            "text-[9px] font-bold px-1.5 py-0.5 rounded border uppercase",
                                            row.status === 'OPTIMAL' ? 'text-success border-success/20 bg-success/5' : 
                                            row.status === 'DRIFT' ? 'text-critical border-critical/20 bg-critical/5' : 
                                            'text-warning border-warning/20 bg-warning/5'
                                        )}>
                                            {row.status}
                                        </span>
                                    </td>
                                    <td className="p-4 text-[10px] text-gray-500 font-mono">{row.last}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Governance Intelligence Sidepanel */}
            <div className="space-y-6">
                <div className="panel-glass p-6 border-primary/20 bg-primary/5">
                    <div className="flex items-center space-x-2 mb-4">
                        <Zap className="w-4 h-4 text-primary" />
                        <h3 className="text-[10px] font-space font-bold tracking-widest text-primary uppercase">Evolution_Insight</h3>
                    </div>
                    <p className="text-[11px] text-gray-300 font-mono leading-relaxed mb-6">
                        {intel.critical_drift_insight || "Institutional alignment within optimal thresholds. Evolutionary framework suggests prioritizing cross-border AML synchronization."}
                    </p>
                    <button className="w-full py-2.5 bg-primary text-background font-space font-bold text-[10px] tracking-widest uppercase hover:bg-primary-accent transition-colors rounded-md">
                        INITIATE_REALIGNMENT
                    </button>
                </div>

                <div className="panel-glass p-6">
                    <h3 className="text-[10px] font-space font-bold tracking-widest text-gray-400 uppercase mb-4">Evolutionary_Roadmap</h3>
                    <div className="space-y-4">
                        {[
                            { phase: "Q2_ACTIVATE", task: "Multi-agent AML synchronization across hubs" },
                            { phase: "Q3_PLANNING", task: "Cognitive Liquidity Engine for treasury" },
                            { phase: "Q4_TARGET", task: "Fully autonomous governance framework" },
                        ].map((item, i) => (
                            <div key={i} className="space-y-1">
                                <span className="text-[9px] text-primary font-bold uppercase">{item.phase}</span>
                                <p className="text-[11px] text-gray-400 leading-relaxed font-mono">{item.task}</p>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="panel-glass p-6">
                    <h3 className="text-[10px] font-space font-bold tracking-widest text-gray-400 uppercase mb-4">Audit_Continuity</h3>
                    <div className="space-y-4">
                        <div className="flex justify-between items-end">
                            <span className="text-[10px] text-gray-500 uppercase font-space font-bold">Continuous_Score</span>
                            <span className="text-xl font-bold text-white">98.4%</span>
                        </div>
                        <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                            <div className="h-full bg-success w-[98.4%]" />
                        </div>
                        <div className="space-y-2 mt-4">
                            <div className="flex items-center justify-between text-[9px] font-mono text-gray-500">
                                <span>Trace_ID_Coverage</span>
                                <span className="text-success">100%</span>
                            </div>
                            <div className="flex items-center justify-between text-[9px] font-mono text-gray-500">
                                <span>Auth_Signatures</span>
                                <span className="text-success">VALID</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      </main>
    </div>
  );
}
