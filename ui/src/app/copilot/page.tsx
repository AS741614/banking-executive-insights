"use client";

import { Header } from "@/components/layout/Header";
import { CopilotInterface } from "@/components/copilot/CopilotInterface";
import { Sparkles, History, Settings2, ShieldAlert } from "lucide-react";

export default function CopilotPage() {
  return (
    <div className="flex flex-col h-full bg-background overflow-hidden">
      <Header title="AI_COPILOT_CONSOLE" />
      
      <main className="flex-1 overflow-hidden p-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-full">
          {/* Main Chat Area */}
          <div className="lg:col-span-3 h-full">
            <CopilotInterface />
          </div>

          {/* Right Sidebar - Cognitive Context */}
          <div className="space-y-6 overflow-y-auto pr-2 custom-scrollbar">
            <div className="panel-glass p-6">
              <div className="flex items-center space-x-2 mb-4">
                <Sparkles className="w-4 h-4 text-primary" />
                <h3 className="text-[10px] font-space font-bold tracking-widest text-gray-400 uppercase">Cognitive_Capabilities</h3>
              </div>
              <ul className="space-y-3">
                {[
                  "Risk_Exposure_Analysis",
                  "Market_Sentiment_Mapping",
                  "Governance_Traceability",
                  "Strategic_Forecasting",
                  "Anomaly_Detection"
                ].map((cap) => (
                  <li key={cap} className="flex items-center space-x-2 text-[10px] text-gray-500 font-mono hover:text-primary transition-colors cursor-pointer group">
                    <div className="w-1 h-1 rounded-full bg-gray-700 group-hover:bg-primary" />
                    <span>{cap}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="panel-glass p-6">
              <div className="flex items-center space-x-2 mb-4">
                <History className="w-4 h-4 text-gray-400" />
                <h3 className="text-[10px] font-space font-bold tracking-widest text-gray-400 uppercase">Recent_Queries</h3>
              </div>
              <div className="space-y-3">
                {[
                  "Assess liquidity impact of node NY_01 failure",
                  "Generate AML risk report for TIER_4",
                  "Forecast Q3 institutional exposure"
                ].map((q, i) => (
                  <div key={i} className="text-[10px] text-gray-600 font-mono italic border-l border-white/5 pl-3 py-1 hover:border-primary/30 transition-colors cursor-pointer">
                    "{q}"
                  </div>
                ))}
              </div>
            </div>

            <div className="panel-glass p-6 border-gold/20 bg-gold/5">
                <div className="flex items-center space-x-2 mb-4">
                    <ShieldAlert className="w-4 h-4 text-gold" />
                    <h3 className="text-[10px] font-space font-bold tracking-widest text-gold uppercase">Governance_Notice</h3>
                </div>
                <p className="text-[10px] text-gold/70 font-mono leading-relaxed">
                    All cognitive queries are logged and audited in accordance with TIER_4 institutional governance protocols.
                </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
