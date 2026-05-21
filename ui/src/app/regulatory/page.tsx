"use client";

import { Header } from "@/components/layout/Header";
import { MetricCard } from "@/components/dashboard/MetricCard";
import { 
  ShieldCheck, 
  AlertTriangle, 
  Search, 
  FileText, 
  Users, 
  BarChart2,
  Lock,
  Eye,
  CheckCircle2
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useState } from "react";

const AML_ALERTS = [
  { id: "SAR-2026-001", entity: "Institutional Client #8821", severity: "CRITICAL", trigger: "Cross-border Layering", status: "PENDING" },
  { id: "SAR-2026-002", entity: "HNWI Portfolio #4412", severity: "HIGH", trigger: "Structuring Pattern", status: "REVIEW" },
  { id: "SAR-2026-003", entity: "Global Trade Corp", severity: "MEDIUM", trigger: "Sanction Linkage (L3)", status: "MONITOR" },
  { id: "SAR-2026-004", entity: "Retail Segment #9901", severity: "LOW", trigger: "Velocity Anomaly", status: "RESOLVED" },
];

export default function RegulatoryCockpit() {
  const [activeTab, setActiveTab] = useState("AML_SURVEILLANCE");

  return (
    <div className="flex flex-col h-full bg-background overflow-hidden">
      <Header title="REGULATORY_COCKPIT" />
      
      <main className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* Top KPI Layer */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <MetricCard 
            label="Compliance Score"
            value="98.2%"
            subValue="Institutional Grade"
            icon={ShieldCheck}
            color="success"
            trend="up"
          />
          <MetricCard 
            label="Pending SARs"
            value="14"
            subValue="Suspicious Activity Reports"
            icon={FileText}
            color="warning"
            trend="down"
          />
          <MetricCard 
            label="High Risk Entities"
            value="2.4%"
            subValue="Total Portfolio Conc."
            icon={Users}
            color="gold"
            trend="neutral"
          />
          <MetricCard 
            label="Blocked Volume"
            value="$4.2M"
            subValue="Past 24 Hours"
            icon={Lock}
            color="critical"
            trend="up"
          />
        </div>

        {/* Command Tabs */}
        <div className="flex border-b border-white/5 space-x-8">
            {["AML_SURVEILLANCE", "KYC_INTELLIGENCE", "FRAUD_PATTERNS"].map((tab) => (
                <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={cn(
                        "pb-4 text-[10px] font-space font-bold tracking-[0.2em] transition-all relative uppercase",
                        activeTab === tab ? "text-primary" : "text-gray-500 hover:text-gray-300"
                    )}
                >
                    {tab}
                    {activeTab === tab && (
                        <div className="absolute bottom-0 left-0 w-full h-0.5 bg-primary shadow-[0_0_10px_rgba(0,209,255,0.5)]" />
                    )}
                </button>
            ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
                {activeTab === "AML_SURVEILLANCE" && (
                    <div className="panel-glass overflow-hidden">
                        <div className="p-4 border-b border-white/5 bg-white/[0.02] flex justify-between items-center">
                            <h3 className="text-[10px] font-space font-bold tracking-widest text-gray-400 uppercase">Alert_Matrix_Surveillance</h3>
                            <div className="flex items-center space-x-2">
                                <Search className="w-3 h-3 text-gray-500" />
                                <span className="text-[9px] text-gray-500 font-mono">Filter_Active_Alerts</span>
                            </div>
                        </div>
                        <div className="divide-y divide-white/5">
                            {AML_ALERTS.map((alert) => (
                                <div key={alert.id} className="p-4 hover:bg-white/[0.01] transition-colors group flex items-center justify-between">
                                    <div className="flex items-center space-x-4">
                                        <div className={cn(
                                            "w-2 h-2 rounded-full",
                                            alert.severity === 'CRITICAL' ? 'bg-critical animate-pulse' : alert.severity === 'HIGH' ? 'bg-warning' : 'bg-primary'
                                        )} />
                                        <div className="space-y-0.5">
                                            <div className="flex items-center space-x-2">
                                                <span className="text-[11px] font-bold text-white font-mono">{alert.id}</span>
                                                <span className={cn(
                                                    "text-[8px] font-bold px-1.5 py-0.5 rounded uppercase tracking-tighter",
                                                    alert.severity === 'CRITICAL' ? 'text-critical border border-critical/20 bg-critical/5' : 'text-gray-400 border border-white/10 bg-white/5'
                                                )}>
                                                    {alert.severity}
                                                </span>
                                            </div>
                                            <div className="flex items-center space-x-2 text-[10px] text-gray-500 font-mono">
                                                <span>{alert.entity}</span>
                                                <span className="opacity-30">|</span>
                                                <span className="text-gray-400">{alert.trigger}</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex items-center space-x-3">
                                        <button className="p-2 text-gray-500 hover:text-white transition-colors">
                                            <Eye className="w-4 h-4" />
                                        </button>
                                        <button className="px-3 py-1.5 bg-white/5 border border-white/10 text-[9px] font-space font-bold text-gray-400 uppercase tracking-widest hover:bg-white/10 hover:text-white transition-all rounded">
                                            Authorize_SAR
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {activeTab === "KYC_INTELLIGENCE" && (
                    <div className="panel-glass p-6 min-h-[400px]">
                        <div className="flex justify-between items-center mb-8">
                            <div className="flex items-center space-x-2">
                                <Users className="w-4 h-4 text-primary" />
                                <h2 className="text-sm font-space font-bold tracking-widest text-gray-300 uppercase">Risk_Concentration_Analytics</h2>
                            </div>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <div className="space-y-6">
                                {[
                                    { label: "HNWI Segment", risk: 12, color: "text-success" },
                                    { label: "Institutional Hub", risk: 8, color: "text-primary" },
                                    { label: "Retail Network", risk: 45, color: "text-warning" },
                                    { label: "FinTech Partners", risk: 88, color: "text-critical" },
                                ].map((item) => (
                                    <div key={item.label} className="space-y-2">
                                        <div className="flex justify-between text-[10px] font-mono">
                                            <span className="text-gray-400">{item.label}</span>
                                            <span className={item.color}>{item.risk}% RISK</span>
                                        </div>
                                        <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                                            <div 
                                                className={cn("h-full rounded-full", item.color.replace('text', 'bg'))} 
                                                style={{ width: `${item.risk}%` }} 
                                            />
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <div className="bg-black/40 border border-white/5 rounded-xl p-6 flex flex-col items-center justify-center text-center space-y-4">
                                <div className="w-16 h-16 rounded-full border-2 border-primary/20 border-t-primary animate-spin" />
                                <div className="space-y-1">
                                    <h4 className="text-xs font-space font-bold text-white uppercase tracking-widest">Cognitive_KYC_Sync</h4>
                                    <p className="text-[10px] text-gray-500 font-mono">Evaluating 12.4k customer profiles across 14 jurisdictions...</p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === "FRAUD_PATTERNS" && (
                     <div className="panel-glass p-6 min-h-[400px] flex flex-col">
                        <div className="flex justify-between items-center mb-8">
                            <div className="flex items-center space-x-2">
                                <AlertTriangle className="w-4 h-4 text-critical" />
                                <h2 className="text-sm font-space font-bold tracking-widest text-gray-300 uppercase">Fraud_Pattern_Discovery</h2>
                            </div>
                            <span className="text-[10px] text-gray-500 font-mono">Confidence: 0.942</span>
                        </div>
                        
                        <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-6">
                            {[
                                { title: "Synthetic ID", count: 124, trend: "+12%", desc: "New pattern detected in AMER onboarding" },
                                { title: "Deepfake Audio", count: 42, trend: "+84%", desc: "Escalation in TIER_4 authorization" },
                                { title: "Layering Rings", count: 8, trend: "-2%", desc: "L3 cross-border sequence identified" },
                            ].map((pattern) => (
                                <div key={pattern.title} className="bg-white/[0.02] border border-white/5 rounded-xl p-4 flex flex-col justify-between hover:border-primary/20 transition-all group">
                                    <div className="space-y-1">
                                        <span className="text-[10px] text-gray-500 font-mono uppercase tracking-widest">{pattern.title}</span>
                                        <div className="flex items-baseline space-x-2">
                                            <span className="text-2xl font-bold text-white">{pattern.count}</span>
                                            <span className="text-[9px] text-critical font-bold">{pattern.trend}</span>
                                        </div>
                                    </div>
                                    <p className="text-[10px] text-gray-500 italic mt-4 group-hover:text-gray-400 transition-colors">"{pattern.desc}"</p>
                                </div>
                            ))}
                        </div>

                        <div className="mt-8 p-4 bg-critical/5 border border-critical/20 rounded-xl flex items-center justify-between">
                            <div className="flex items-center space-x-4">
                                <div className="p-2 bg-critical/10 rounded-lg">
                                    <Activity className="w-5 h-5 text-critical" />
                                </div>
                                <div>
                                    <h4 className="text-[10px] font-space font-bold text-white uppercase tracking-widest">Threat_Replay_Engine</h4>
                                    <p className="text-[10px] text-gray-500 font-mono">Simulate multi-vector attacks against current perimeter.</p>
                                </div>
                            </div>
                            <button className="px-4 py-2 bg-critical text-white font-space font-bold text-[9px] tracking-widest uppercase hover:bg-critical/80 transition-all rounded">
                                TRIGGER_SIMULATION
                            </button>
                        </div>
                     </div>
                )}
            </div>

            {/* Regulatory Intelligence & Oversight */}
            <div className="space-y-6">
                <div className="panel-glass p-6">
                    <h3 className="text-[10px] font-space font-bold tracking-widest text-gray-400 uppercase mb-4">Regulatory_Environment</h3>
                    <div className="space-y-4">
                        {[
                            { name: "FinCEN_AML_V4", status: "compliant", date: "2026-05-18" },
                            { name: "EU_MICA_ADAPT", status: "compliant", date: "2026-05-12" },
                            { name: "HKMA_KYC_DIR", status: "review", date: "2026-05-20" },
                        ].map((reg) => (
                            <div key={reg.name} className="flex flex-col space-y-1 border-l border-white/5 pl-4 py-1">
                                <span className="text-xs font-mono text-gray-300">{reg.name}</span>
                                <div className="flex justify-between items-center">
                                    <span className={cn(
                                        "text-[9px] font-bold uppercase",
                                        reg.status === 'compliant' ? 'text-success' : 'text-warning'
                                    )}>
                                        {reg.status}
                                    </span>
                                    <span className="text-[9px] text-gray-600 font-mono">{reg.date}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="panel-glass p-6 bg-gold/5 border-gold/20">
                    <div className="flex items-center space-x-2 mb-4">
                        <CheckCircle2 className="w-4 h-4 text-gold" />
                        <h3 className="text-[10px] font-space font-bold tracking-widest text-gold uppercase">Audit_Readiness</h3>
                    </div>
                    <div className="space-y-4">
                        <div className="flex justify-between items-end">
                            <span className="text-[10px] text-gray-500 uppercase font-space font-bold">Traceability_Index</span>
                            <span className="text-xl font-bold text-gold">0.998</span>
                        </div>
                        <div className="h-1 w-full bg-gold/10 rounded-full overflow-hidden">
                            <div className="h-full bg-gold w-[99.8%]" />
                        </div>
                        <p className="text-[10px] text-gray-500 font-mono leading-relaxed">
                            Institutional memory is fully synchronized. All executive decisions carry a cryptographic governance signature.
                        </p>
                    </div>
                </div>

                <div className="panel-glass p-6">
                    <h3 className="text-[10px] font-space font-bold tracking-widest text-gray-400 uppercase mb-4">Oversight_Log</h3>
                    <div className="space-y-3">
                        {[
                            "System initialized TIER_4 governance sweep",
                            "SAR-2026-004 resolved by automated engine",
                            "New regulation FinCEN_AML_V4 integrated",
                            "Compliance score adjusted: +0.2% delta"
                        ].map((log, i) => (
                            <div key={i} className="text-[10px] text-gray-600 font-mono flex items-start space-x-2">
                                <span className="text-primary mt-0.5">{'>'}</span>
                                <span>{log}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
      </main>
    </div>
  );
}
ort { Activity } from "lucide-react";
