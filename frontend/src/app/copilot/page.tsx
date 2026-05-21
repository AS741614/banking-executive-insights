"use client";

import { useState, useRef, useEffect } from "react";
import { useCognitionQuery } from "@/lib/queries";
import { Card, CardContent, CardHeader } from "@/components/shared/ui";
import { BrainCircuit, Send, Shield, Info, Loader2, User, Bot } from "lucide-react";
import { cn } from "@/lib/utils";
import { ClientOnly } from "@/components/shared/client-only";

interface Message {
  role: "user" | "assistant";
  content: string;
  confidence?: number;
  sources?: string[];
  timestamp: string;
}

export default function CopilotPage() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const { mutate: sendQuery, isPending } = useCognitionQuery();
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isPending]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isPending) return;

    const userMessage: Message = {
      role: "user",
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    sendQuery(
      { prompt: input, governance_level: "STRICT" },
      {
        onSuccess: (data) => {
          const botMessage: Message = {
            role: "assistant",
            content: data.intelligence_payload,
            confidence: data.confidence_score,
            sources: data.sources,
            timestamp: new Date().toISOString(),
          };
          setMessages((prev) => [...prev, botMessage]);
        },
        onError: () => {
          const errorMessage: Message = {
            role: "assistant",
            content: "CRITICAL_ERROR: UNABLE_TO_ACCESS_COGNITION_KERNEL. Please verify institutional connectivity.",
            timestamp: new Date().toISOString(),
          };
          setMessages((prev) => [...prev, errorMessage]);
        },
      }
    );
  };

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)] max-w-5xl mx-auto animate-in fade-in duration-500">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-heading font-bold text-white tracking-tight">AI Copilot Console</h1>
          <p className="text-muted-foreground text-sm">Institutional intelligence and predictive banking queries.</p>
        </div>
        <div className="flex items-center gap-2 px-3 py-1 rounded bg-primary/10 border border-primary/20">
          <Shield className="w-3 h-3 text-primary" />
          <span className="text-[10px] font-bold text-primary uppercase tracking-widest">GOVERNANCE_MODE: STRICT</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 flex-1 overflow-hidden">
        <Card className="lg:col-span-3 flex flex-col overflow-hidden">
          <CardHeader className="flex flex-row items-center justify-between py-3">
            <div className="flex items-center gap-2">
              <BrainCircuit className="w-4 h-4 text-primary" />
              <span className="text-xs font-bold text-white uppercase tracking-wider">Cognition Feed</span>
            </div>
            <ClientOnly fallback={<div className="text-[10px] font-mono text-white/20">--:--:--</div>}>
              <div className="text-[10px] font-mono text-white/40">KERNEL_SYNC_READY</div>
            </ClientOnly>
          </CardHeader>
          <CardContent className="flex-1 overflow-y-auto p-0" ref={scrollRef}>
            <div className="p-6 space-y-6">
              {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center h-full text-center space-y-4 pt-20">
                  <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center">
                    <BrainCircuit className="w-8 h-8 text-white/20" />
                  </div>
                  <div className="max-w-xs space-y-2">
                    <p className="text-sm font-medium text-white/60">Initialize Banking Intelligence Query</p>
                    <p className="text-xs text-muted-foreground">Ask about treasury positions, risk exposure, or institutional forecasting.</p>
                  </div>
                </div>
              )}
              {messages.map((m, i) => (
                <div key={i} className={cn("flex gap-4", m.role === "assistant" ? "justify-start" : "justify-end")}>
                  {m.role === "assistant" && (
                    <div className="w-8 h-8 rounded bg-primary/10 flex items-center justify-center shrink-0">
                      <Bot className="w-4 h-4 text-primary" />
                    </div>
                  )}
                  <div className={cn(
                    "max-w-[80%] rounded-lg p-4 text-sm leading-relaxed",
                    m.role === "assistant" 
                      ? "bg-white/5 text-white/90 border border-white/5" 
                      : "bg-primary text-background font-medium shadow-lg"
                  )}>
                    {m.content}
                    {m.confidence !== undefined && (
                      <div className="mt-4 pt-3 border-t border-white/10 flex items-center justify-between gap-4">
                        <div className="flex items-center gap-2">
                          <span className="text-[10px] font-bold text-white/40 uppercase">Confidence</span>
                          <div className="h-1.5 w-20 bg-white/10 rounded-full overflow-hidden">
                            <div className="h-full bg-success" style={{ width: `${m.confidence * 100}%` }} />
                          </div>
                          <span className="text-[10px] font-bold text-success">{(m.confidence * 100).toFixed(1)}%</span>
                        </div>
                        {m.sources && m.sources.length > 0 && (
                          <div className="text-[10px] text-primary hover:underline cursor-pointer font-bold uppercase">
                            View {m.sources.length} Sources
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                  {m.role === "user" && (
                    <div className="w-8 h-8 rounded bg-white/5 flex items-center justify-center shrink-0">
                      <User className="w-4 h-4 text-white/60" />
                    </div>
                  )}
                </div>
              ))}
              {isPending && (
                <div className="flex gap-4 animate-in fade-in duration-300">
                  <div className="w-8 h-8 rounded bg-primary/10 flex items-center justify-center shrink-0">
                    <Bot className="w-4 h-4 text-primary animate-pulse" />
                  </div>
                  <div className="bg-white/5 rounded-lg p-4 border border-white/5 flex items-center gap-3">
                    <Loader2 className="w-3 h-3 text-primary animate-spin" />
                    <span className="text-[10px] font-mono text-primary uppercase tracking-widest animate-pulse">Processing_Cognitive_Trace...</span>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
          <div className="p-4 border-t border-white/5 bg-background/50">
            <form onSubmit={handleSubmit} className="relative">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Query institutional intelligence..."
                className="w-full bg-[#050816] border border-white/10 rounded-lg py-3 px-4 pr-12 text-sm text-white focus:outline-none focus:border-primary/50 transition-colors"
                disabled={isPending}
              />
              <button
                type="submit"
                disabled={!input.trim() || isPending}
                className="absolute right-2 top-1/2 -translate-y-1/2 w-8 h-8 rounded bg-primary text-background flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed transition-all hover:scale-105 active:scale-95"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <div className="text-[10px] font-bold text-white uppercase tracking-widest">Audit Trace Panel</div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="p-3 rounded bg-white/5 border border-white/5 space-y-2">
                <div className="flex items-center gap-2 text-[10px] font-bold text-primary uppercase">
                  <Info className="w-3 h-3" />
                  Institutional Guardrails
                </div>
                <p className="text-[10px] text-muted-foreground leading-relaxed">
                  Queries are filtered through the Governance Reconciliation engine. Sensitive data anonymization is active.
                </p>
              </div>
              
              <div className="space-y-3">
                <TraceItem label="Kernel Version" value="v1.0.4-LOCKED" />
                <TraceItem label="Data Freshness" value="REAL_TIME" />
                <TraceItem label="Latency (ms)" value="124" />
                <TraceItem label="Security Tier" value="TIER_4" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="text-[10px] font-bold text-white uppercase tracking-widest">Suggested Queries</div>
            </CardHeader>
            <CardContent className="space-y-2">
              <SuggestedQuery text="Project treasury liquidity for Q3" />
              <SuggestedQuery text="Identify high-risk AML concentrations" />
              <SuggestedQuery text="Analyze capital adequacy sensitivity" />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

function TraceItem({ label, value }: { label: string, value: string }) {
  return (
    <div className="flex justify-between items-center text-[10px] font-mono">
      <span className="text-white/40">{label}</span>
      <span className="text-white/80">{value}</span>
    </div>
  );
}

function SuggestedQuery({ text }: { text: string }) {
  return (
    <div className="p-2 rounded border border-white/5 hover:border-primary/30 hover:bg-primary/5 transition-all cursor-pointer text-[10px] text-white/60 hover:text-primary">
      {text}
    </div>
  );
}
