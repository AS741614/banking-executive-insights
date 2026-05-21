"use client";

import { useState } from "react";
import { 
  useSimulateKYC, 
  useSimulateDrift, 
  useSimulateOperationalRisk 
} from "@/lib/governance-queries";
import { Card, CardContent, CardHeader } from "@/components/shared/ui";
import { 
  Play, 
  AlertTriangle, 
  Users, 
  Zap, 
  ShieldAlert, 
  Activity,
  Loader2,
  CheckCircle2
} from "lucide-react";
import { cn } from "@/lib/utils";

export function ScenarioControlPanel() {
  const kycMutation = useSimulateKYC();
  const driftMutation = useSimulateDrift();
  const riskMutation = useSimulateOperationalRisk();

  const [activeScenario, setActiveScenario] = useState<string | null>(null);

  const handleTrigger = async (type: string, fn: () => Promise<any>) => {
    setActiveScenario(type);
    try {
      await fn();
      setTimeout(() => setActiveScenario(null), 2000);
    } catch (err) {
      setActiveScenario(null);
    }
  };

  return (
    <Card className="flex flex-col h-full border-primary/10">
      <CardHeader className="flex flex-row items-center justify-between">
        <div className="flex items-center gap-2">
          <Zap className="w-4 h-4 text-primary" />
          <div className="text-xs font-bold text-white uppercase tracking-wider">Executive Scenario Console</div>
        </div>
        <div className="text-[10px] font-mono text-primary/60 animate-pulse">SYSTEM_READY</div>
      </CardHeader>
      <CardContent className="space-y-4 p-6">
        <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-2">Institutional Stress Triggers</div>
        
        <ScenarioButton 
          title="High-Risk KYC Injection" 
          description="Simulate REJECTED customer evaluation"
          icon={Users}
          isLoading={kycMutation.isPending}
          isSuccess={activeScenario === 'KYC'}
          onClick={() => handleTrigger('KYC', () => kycMutation.mutateAsync({ status: 'REJECTED', severity: 'CRITICAL' }))}
        />

        <ScenarioButton 
          title="Governance Drift Spike" 
          description="Inject 45% variance in Treasury domain"
          icon={ShieldAlert}
          isLoading={driftMutation.isPending}
          isSuccess={activeScenario === 'DRIFT'}
          onClick={() => handleTrigger('DRIFT', () => driftMutation.mutateAsync({ domain: 'treasury', variance: 0.48 }))}
        />

        <ScenarioButton 
          title="Operational Risk Surge" 
          description="Simulate ECOS Kernel resource anomaly"
          icon={Activity}
          isLoading={riskMutation.isPending}
          isSuccess={activeScenario === 'RISK'}
          onClick={() => handleTrigger('RISK', () => riskMutation.mutateAsync({ 
            subsystem: 'ECOS_KERNEL', 
            severity: 'CRITICAL', 
            message: 'INSTITUTIONAL_MEMORY_SATURATION_DETECTED' 
          }))}
        />

        <div className="mt-6 pt-6 border-t border-white/5">
          <div className="p-4 bg-primary/5 border border-primary/20 rounded-lg">
            <div className="flex items-start gap-3">
              <AlertTriangle className="w-4 h-4 text-primary shrink-0 mt-0.5" />
              <div className="space-y-1">
                <p className="text-[10px] font-bold text-primary uppercase">Safe Simulation Protocol</p>
                <p className="text-[9px] text-primary/70 leading-relaxed">
                  Triggering scenarios will emit REAL institutional events. All governance workflows and audit logs will be active.
                </p>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function ScenarioButton({ title, description, icon: Icon, onClick, isLoading, isSuccess }: any) {
  return (
    <button 
      onClick={onClick}
      disabled={isLoading}
      className={cn(
        "w-full flex items-center gap-4 p-3 rounded-lg border transition-all text-left group",
        isSuccess 
          ? "bg-success/10 border-success/30" 
          : "bg-white/[0.02] border-white/5 hover:border-primary/30 hover:bg-white/[0.04]"
      )}
    >
      <div className={cn(
        "w-10 h-10 rounded bg-white/5 flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform",
        isSuccess && "bg-success/20"
      )}>
        {isLoading ? <Loader2 className="w-5 h-5 text-primary animate-spin" /> : 
         isSuccess ? <CheckCircle2 className="w-5 h-5 text-success" /> :
         <Icon className="w-5 h-5 text-white/40 group-hover:text-primary transition-colors" />}
      </div>
      <div className="flex-1 min-w-0">
        <div className="text-xs font-bold text-white group-hover:text-primary transition-colors">{title}</div>
        <div className="text-[9px] text-muted-foreground truncate">{description}</div>
      </div>
      <Play className={cn(
        "w-3 h-3 text-white/20 group-hover:text-primary transition-all",
        isSuccess && "opacity-0"
      )} />
    </button>
  );
}
