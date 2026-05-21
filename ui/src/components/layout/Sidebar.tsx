"use client";

import { 
  LayoutDashboard, 
  ShieldCheck, 
  BarChart3, 
  Cpu, 
  Activity, 
  Search,
  Settings,
  Bell
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const navigation = [
  { name: "EXECUTIVE_OVERVIEW", href: "/", icon: LayoutDashboard },
  { name: "TREASURY_COCKPIT", href: "/treasury", icon: BarChart3 },
  { name: "GOVERNANCE_CENTER", href: "/governance", icon: ShieldCheck },
  { name: "OBSERVABILITY", href: "/observability", icon: Activity },
  { name: "INTELLIGENCE_API", href: "/api-explorer", icon: Cpu },
];


export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="w-64 bg-panels border-r border-border flex flex-col h-full">
      <div className="p-6 flex items-center space-x-3">
        <div className="w-8 h-8 bg-primary rounded-sm flex items-center justify-center">
            <ShieldCheck className="text-background w-5 h-5" />
        </div>
        <span className="font-space font-bold text-lg tracking-tighter">ESOTERIC_BANK</span>
      </div>

      <nav className="flex-1 px-4 py-4 space-y-1">
        {navigation.map((item) => (
          <Link
            key={item.name}
            href={item.href}
            className={cn(
              "flex items-center space-x-3 px-3 py-2 rounded-md text-sm transition-all duration-200",
              pathname === item.href
                ? "bg-primary/10 text-primary border-l-2 border-primary"
                : "text-gray-400 hover:text-white hover:bg-white/5"
            )}
          >
            <item.icon className="w-4 h-4" />
            <span className="font-space text-xs tracking-wider">{item.name}</span>
          </Link>
        ))}
      </nav>

      <div className="p-4 border-t border-border">
        <div className="panel-glass p-3 bg-white/5">
            <div className="flex items-center space-x-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-success animate-pulse" />
                <span className="text-[10px] text-gray-400 font-space uppercase">System Live</span>
            </div>
            <p className="text-[10px] text-gray-500 font-mono">OP_ID: AKASH_SHARMA</p>
            <p className="text-[10px] text-gray-500 font-mono">SEC_LEVEL: TIER_4</p>
        </div>
      </div>
    </div>
  );
}
