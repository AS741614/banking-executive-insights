"use client";

import { Sidebar } from "./Sidebar";
import { Search, Bell, Settings } from "lucide-react";

export function DashboardShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-background overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <header className="h-16 border-b border-border bg-card/50 backdrop-blur-md flex items-center justify-between px-8">
          <div className="flex items-center flex-1">
            <div className="relative w-96">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input 
                type="text" 
                placeholder="Search institutional intelligence..."
                className="w-full bg-background/50 border border-border rounded-sm py-1.5 pl-10 pr-4 text-xs focus:outline-none focus:ring-1 focus:ring-primary/50 transition-all"
              />
            </div>
          </div>
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2">
               <div className="w-2 h-2 rounded-full bg-success animate-pulse" />
               <span className="text-[10px] font-bold text-muted-foreground tracking-widest uppercase">System Operational</span>
            </div>
            <div className="h-4 w-[1px] bg-border" />
            <div className="flex items-center gap-4">
              <button className="p-2 text-muted-foreground hover:text-foreground transition-colors relative">
                <Bell className="w-4 h-4" />
                <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-destructive rounded-full" />
              </button>
              <button className="p-2 text-muted-foreground hover:text-foreground transition-colors">
                <Settings className="w-4 h-4" />
              </button>
            </div>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto bg-[#050816] p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
