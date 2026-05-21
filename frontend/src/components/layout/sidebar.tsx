"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  ShieldCheck, 
  Activity, 
  Database, 
  BrainCircuit,
  Settings,
  Lock
} from "lucide-react";
import { cn } from "@/lib/utils";

const navigation = [
  { name: "Executive Overview", href: "/executive", icon: LayoutDashboard },
  { name: "Treasury Cockpit", href: "/treasury", icon: Database },
  { name: "Governance Center", href: "/governance", icon: ShieldCheck },
  { name: "Observability Center", href: "/observability", icon: Activity },
  { name: "AI Copilot", href: "/copilot", icon: BrainCircuit },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex flex-col w-64 border-r border-white/5 bg-[#0B1120] h-full">
      <div className="flex items-center h-16 px-6 border-b border-white/5">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded bg-primary flex items-center justify-center">
            <Lock className="w-5 h-5 text-background" />
          </div>
          <span className="text-lg font-bold tracking-tight text-white">ESOTERIC BANK</span>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto py-6 px-4 space-y-1">
        <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest px-2 mb-2">
          Command Domains
        </div>
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-md transition-all duration-200 group",
                isActive 
                  ? "bg-primary/10 text-primary border border-primary/20" 
                  : "text-muted-foreground hover:text-white hover:bg-white/5"
              )}
            >
              <item.icon className={cn(
                "w-4 h-4",
                isActive ? "text-primary" : "text-muted-foreground group-hover:text-white"
              )} />
              <span className="text-sm font-medium">{item.name}</span>
              {isActive && (
                <div className="ml-auto w-1 h-4 bg-primary rounded-full" />
              )}
            </Link>
          );
        })}
      </div>

      <div className="p-4 border-t border-white/5">
        <div className="bg-white/5 rounded-lg p-3">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-8 h-8 rounded-full bg-accent flex items-center justify-center text-[10px] font-bold text-background">
              AS
            </div>
            <div>
              <div className="text-xs font-bold text-white uppercase">Akash Sharma</div>
              <div className="text-[10px] text-accent font-medium">TIER_4_BOARD</div>
            </div>
          </div>
          <div className="text-[10px] text-muted-foreground text-center">
            INSTITUTIONAL_RESILIENCE_V2.0
          </div>
        </div>
      </div>
    </div>
  );
}
