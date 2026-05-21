"use client";

import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { useObservabilityStore } from "@/hooks/use-observability";
import { Activity, Server, Activity as TraceIcon, AlertTriangle } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { InstitutionalChartContainer } from "@/components/charts/InstitutionalChartContainer";

export default function ObservabilityPage() {
  const { apiLatency, sseStatus, errors } = useObservabilityStore();

  const latencyData = apiLatency.map((val, i) => ({ name: i, ms: val }));

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <Header title="PLATFORM_OBSERVABILITY" />
        <main className="flex-1 overflow-y-auto p-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <div className="panel-glass p-6">
                <div className="flex items-center space-x-3 mb-4">
                    <Server className="w-5 h-5 text-primary" />
                    <h2 className="text-sm font-space font-bold uppercase tracking-widest">Runtime Health</h2>
                </div>
                <div className="space-y-4">
                    <div className="flex justify-between items-center">
                        <span className="text-xs text-gray-400">SSE_STREAM_STATUS</span>
                        <span className={`text-xs font-bold px-2 py-0.5 rounded ${
                            sseStatus === 'connected' ? 'bg-success/10 text-success' : 
                            sseStatus === 'connecting' ? 'bg-warning/10 text-warning' : 'bg-critical/10 text-critical'
                        }`}>
                            {sseStatus.toUpperCase()}
                        </span>
                    </div>
                    <div className="flex justify-between items-center">
                        <span className="text-xs text-gray-400">PROMETHEUS_SCRAPE</span>
                        <span className="text-xs font-bold text-success uppercase">Active</span>
                    </div>
                    <div className="flex justify-between items-center">
                        <span className="text-xs text-gray-400">OTEL_TRACING</span>
                        <span className="text-xs font-bold text-primary uppercase">Provisioned</span>
                    </div>
                </div>
            </div>

            <div className="panel-glass p-6 lg:col-span-2">
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                        <TraceIcon className="w-5 h-5 text-primary" />
                        <h2 className="text-sm font-space font-bold uppercase tracking-widest">API_LATENCY_TRACING (MS)</h2>
                    </div>
                    <span className="text-[10px] font-mono text-gray-500">N=20 SAMPLES</span>
                </div>
                <div className="w-full">
                    <InstitutionalChartContainer height={120} minHeight={120}>
                        <LineChart data={latencyData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#ffffff05" />
                            <Line 
                                type="monotone" 
                                dataKey="ms" 
                                stroke="#00D1FF" 
                                strokeWidth={2} 
                                dot={false}
                                isAnimationActive={false}
                            />
                            <YAxis hide domain={[0, 'auto']} />
                            <Tooltip 
                                contentStyle={{ backgroundColor: '#0B1120', border: '1px solid rgba(255,255,255,0.08)', fontSize: '10px' }}
                                itemStyle={{ color: '#00D1FF' }}
                            />
                        </LineChart>
                    </InstitutionalChartContainer>
                </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="panel-glass p-6 min-h-[300px]">
                <div className="flex items-center space-x-3 mb-6">
                    <AlertTriangle className="w-5 h-5 text-warning" />
                    <h2 className="text-sm font-space font-bold uppercase tracking-widest">RUNTIME_ANOMALIES</h2>
                </div>
                <div className="space-y-3">
                    {errors.length > 0 ? (
                        errors.map((err, i) => (
                            <div key={i} className="flex items-start space-x-3 text-xs bg-critical/5 border-l-2 border-critical p-3">
                                <span className="text-critical font-bold">ERROR:</span>
                                <span className="text-gray-300 font-mono">{err}</span>
                            </div>
                        ))
                    ) : (
                        <div className="text-center py-12">
                            <Activity className="w-8 h-8 text-success/20 mx-auto mb-2" />
                            <p className="text-xs text-gray-500">No active runtime anomalies detected.</p>
                        </div>
                    )}
                </div>
            </div>

            <div className="panel-glass p-6">
                <h2 className="text-sm font-space font-bold uppercase tracking-widest mb-6">External Observability</h2>
                <div className="grid grid-cols-2 gap-4">
                    <a 
                        href="http://localhost:3001" 
                        target="_blank"
                        className="panel-glass bg-white/[0.02] p-4 flex flex-col items-center justify-center space-y-2 hover:bg-white/[0.05] transition-all group"
                    >
                        <span className="text-[10px] font-space text-gray-400 group-hover:text-primary transition-colors">GRAFANA_CORE</span>
                        <div className="text-primary font-bold text-xs">PORT 3001</div>
                    </a>
                    <a 
                        href="http://localhost:9090" 
                        target="_blank"
                        className="panel-glass bg-white/[0.02] p-4 flex flex-col items-center justify-center space-y-2 hover:bg-white/[0.05] transition-all group"
                    >
                        <span className="text-[10px] font-space text-gray-400 group-hover:text-primary transition-colors">PROMETHEUS_NODE</span>
                        <div className="text-primary font-bold text-xs">PORT 9090</div>
                    </a>
                </div>
                <div className="mt-6 p-4 bg-primary/5 border border-primary/20 rounded-md">
                    <p className="text-[10px] text-gray-400 leading-relaxed">
                        Institutional observability is enforced via OTLP collector. Metrics are synchronized every 15s. 
                        Executive oversight dashboards are auto-provisioned on startup.
                    </p>
                </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
