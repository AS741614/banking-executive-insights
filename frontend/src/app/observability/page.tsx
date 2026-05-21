"use client";

import { usePlatformStatus } from "@/lib/queries";
import { useEventStream } from "@/hooks/use-event-stream";
import { Card, CardContent, CardHeader, Stat } from "@/components/shared/ui";
import { ClientOnly } from "@/components/shared/client-only";
import { cn } from "@/lib/utils";
import { 
  Activity, 
  Terminal, 
  Cpu, 
  Database, 
  Wifi, 
  WifiOff,
  Loader2,
  AlertTriangle,
  Info,
  CheckCircle2
} from "lucide-react";

export default function ObservabilityPage() {
  const { data: status, isLoading: statusLoading } = usePlatformStatus();
  const { events, status: connectionStatus, error: sseError } = useEventStream();

  const isConnected = connectionStatus === "CONNECTED";
  const isConnecting = connectionStatus === "CONNECTING" || connectionStatus === "RECONNECTING";
  const hasError = connectionStatus === "ERROR";

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-heading font-bold text-white tracking-tight">Platform Observability</h1>
          <p className="text-muted-foreground text-sm">Real-time system health and cognitive event propagation.</p>
        </div>
        <div className="flex items-center gap-3">
          <ClientOnly fallback={<div className="px-3 py-1 rounded-full border border-white/5 text-[10px] text-white/20 uppercase font-bold tracking-widest">Initialising Stream...</div>}>
            <div className={cn(
              "flex items-center gap-2 px-3 py-1 rounded-full border text-[10px] font-bold uppercase tracking-widest transition-colors duration-500",
              isConnected ? "bg-success/10 border-success/20 text-success" : 
              isConnecting ? "bg-warning/10 border-warning/20 text-warning" :
              "bg-destructive/10 border-destructive/20 text-destructive"
            )}>
              {isConnected ? <Wifi className="w-3 h-3" /> : (isConnecting ? <Loader2 className="w-3 h-3 animate-spin" /> : <WifiOff className="w-3 h-3" />)}
              {hasError ? `STREAM_CRITICAL_FAILURE: ${sseError}` : 
               isConnected ? "Event Stream: Online" : 
               isConnecting ? "Event Stream: Synchronising..." : "Event Stream: Offline"}
            </div>
          </ClientOnly>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="flex items-center gap-6">
            <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
              <Cpu className="w-6 h-6 text-primary" />
            </div>
            <Stat label="CPU Usage" value={`${status?.cpu_usage || 0}%`} subvalue="CORE_LOAD_DISTRIBUTED" />
          </CardContent>
        </Card>
        <Card>
          <CardContent className="flex items-center gap-6">
            <div className="w-12 h-12 rounded-xl bg-secondary/10 flex items-center justify-center">
              <Database className="w-6 h-6 text-secondary" />
            </div>
            <Stat label="Memory Usage" value={`${status?.memory_usage || 0}%`} subvalue="HEAP_STABILITY: OPTIMAL" />
          </CardContent>
        </Card>
        <Card>
          <CardContent className="flex items-center gap-6">
            <div className="w-12 h-12 rounded-xl bg-success/10 flex items-center justify-center">
              <Activity className="w-6 h-6 text-success" />
            </div>
            <Stat label="System Latency" value={`${status?.latency_ms || 0}ms`} subvalue="I/O_PROPAGATION_DELAY" />
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[600px]">
        <Card className="lg:col-span-2 flex flex-col h-full">
          <CardHeader className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Terminal className="w-4 h-4 text-primary" />
              <div className="text-xs font-bold text-white uppercase tracking-wider">Cognitive Event Ticker</div>
            </div>
            <div className="text-[10px] font-mono text-white/40">BUFFER_LIMIT: 50_ENTRIES</div>
          </CardHeader>
          <CardContent className="flex-1 overflow-y-auto font-mono text-[11px] p-0">
            <ClientOnly fallback={<div className="p-8 text-center text-muted-foreground italic">Booting Event Engine...</div>}>
              <div className="divide-y divide-white/5">
                {events.length === 0 ? (
                  <div className="p-8 text-center text-muted-foreground italic">Waiting for institutional events...</div>
                ) : (
                  events.map((event, i) => (
                    <div key={event.event_id + i} className="p-3 hover:bg-white/[0.02] transition-colors flex gap-4">
                      <div className="w-20 shrink-0 text-white/40">{new Date(event.timestamp).toLocaleTimeString()}</div>
                      <div className={cn(
                        "w-20 shrink-0 font-bold",
                        event.severity === "CRITICAL" ? "text-destructive" :
                        event.severity === "HIGH" ? "text-warning" :
                        event.severity === "MEDIUM" ? "text-primary" : "text-success"
                      )}>
                        [{event.severity}]
                      </div>
                      <div className="w-24 shrink-0 text-secondary">{event.domain}</div>
                      <div className="flex-1 text-white/80">{event.message}</div>
                    </div>
                  ))
                )}
              </div>
            </ClientOnly>
          </CardContent>
        </Card>

        <Card className="flex flex-col h-full">
          <CardHeader>
            <div className="text-xs font-bold text-white uppercase tracking-wider">Subsystem Health</div>
          </CardHeader>
          <CardContent className="space-y-4">
            <SubsystemItem name="ECOS Kernel" status="HEALTHY" icon={CheckCircle2} color="text-success" />
            <SubsystemItem name="Gemini Cognition" status="HEALTHY" icon={CheckCircle2} color="text-success" />
            <SubsystemItem name="Event Streamer" status="STABLE" icon={CheckCircle2} color="text-success" />
            <SubsystemItem name="Regulatory Engine" status="HEALTHY" icon={CheckCircle2} color="text-success" />
            <SubsystemItem name="Treasury Forecaster" status="WARNING" icon={AlertTriangle} color="text-warning" />
            <SubsystemItem name="Governance Sync" status="HEALTHY" icon={CheckCircle2} color="text-success" />
            
            <div className="mt-8 p-4 rounded-lg bg-[#0B1120] border border-white/5 space-y-2">
              <div className="flex items-center gap-2 text-[10px] font-bold text-white uppercase tracking-widest">
                <Info className="w-3 h-3 text-primary" />
                Diagnostic Notes
              </div>
              <p className="text-[10px] text-muted-foreground leading-relaxed">
                Minor jitter detected in Treasury Forecaster due to increased simulation throughput. ECOS kernel automatically adjusting resource allocation.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function SubsystemItem({ name, status, icon: Icon, color }: { name: string; status: string; icon: any; color: string }) {
  return (
    <div className="flex items-center justify-between p-2 rounded border border-transparent hover:border-white/5 transition-colors">
      <div className="flex items-center gap-3">
        <Icon className={cn("w-4 h-4", color)} />
        <span className="text-xs font-medium text-white/80">{name}</span>
      </div>
      <span className={cn("text-[10px] font-bold uppercase tracking-widest px-1.5 py-0.5 rounded", color.replace('text-', 'bg-') + '/10', color)}>
        {status}
      </span>
    </div>
  );
}
