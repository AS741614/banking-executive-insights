"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, ShieldCheck, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import api from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export function CopilotInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Institutional Intelligence System online. How can I assist with your executive queries today?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const { data } = await api.post("/cognition/query", {
        prompt: input,
        governance_level: "STRICT",
      });

      const assistantMessage: Message = {
        role: "assistant",
        content: data.data?.intelligence_payload || "Cognitive query completed with nominal results.",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "ERROR: Failed to establish cognitive link with intelligence backend. Please verify system connectivity.",
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-160px)] panel-glass overflow-hidden">
      <div className="p-4 border-b border-white/5 bg-white/5 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center border border-primary/30">
            <Bot className="w-5 h-5 text-primary" />
          </div>
          <div>
            <h3 className="text-xs font-space font-bold text-white tracking-widest uppercase">Institutional_Cognition_Node</h3>
            <div className="flex items-center space-x-1">
              <div className="w-1.5 h-1.5 rounded-full bg-success animate-pulse" />
              <span className="text-[9px] text-success font-mono uppercase">Operational_Ready</span>
            </div>
          </div>
        </div>
        <div className="flex items-center space-x-2">
            <ShieldCheck className="w-4 h-4 text-gold" />
            <span className="text-[9px] text-gold font-mono uppercase">Governance_STRICT</span>
        </div>
      </div>

      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar"
      >
        {messages.map((msg, i) => (
          <div 
            key={i} 
            className={cn(
              "flex items-start space-x-4",
              msg.role === "user" ? "flex-row-reverse space-x-reverse" : ""
            )}
          >
            <div className={cn(
              "w-8 h-8 rounded-full flex items-center justify-center shrink-0 border",
              msg.role === "assistant" 
                ? "bg-primary/10 border-primary/20 text-primary" 
                : "bg-white/5 border-white/10 text-gray-400"
            )}>
              {msg.role === "assistant" ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
            </div>
            <div className={cn(
              "max-w-[80%] p-4 rounded-2xl text-xs font-mono leading-relaxed",
              msg.role === "assistant" 
                ? "bg-white/5 border border-white/5 text-gray-300 rounded-tl-none" 
                : "bg-primary/10 border border-primary/20 text-white rounded-tr-none"
            )}>
              {msg.content}
              <div className="mt-2 text-[8px] opacity-40 text-right">
                {msg.timestamp.toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex items-start space-x-4">
            <div className="w-8 h-8 rounded-full bg-primary/10 border border-primary/20 text-primary flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4" />
            </div>
            <div className="bg-white/5 border border-white/5 p-4 rounded-2xl rounded-tl-none">
              <div className="flex space-x-1">
                <div className="w-1.5 h-1.5 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-1.5 h-1.5 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-1.5 h-1.5 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="p-4 bg-black/40 border-t border-white/5">
        <div className="relative">
          <input 
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Query Institutional Intelligence..."
            className="w-full bg-white/5 border border-white/10 rounded-xl pl-4 pr-12 py-3 text-xs font-mono focus:outline-none focus:border-primary/50 transition-colors"
          />
          <button 
            onClick={handleSend}
            disabled={isLoading}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-primary hover:text-white transition-colors disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
        <div className="flex items-center justify-between mt-3 px-1">
            <div className="flex items-center space-x-4">
                <button className="text-[9px] text-gray-500 hover:text-primary transition-colors flex items-center space-x-1 uppercase font-bold">
                    <Sparkles className="w-3 h-3" />
                    <span>Generate_Analysis</span>
                </button>
                <button className="text-[9px] text-gray-500 hover:text-primary transition-colors flex items-center space-x-1 uppercase font-bold">
                    <BarChart3 className="w-3 h-3" />
                    <span>Visualize_Impact</span>
                </button>
            </div>
            <span className="text-[9px] text-gray-600 font-mono italic">Context: Institutional_Executive_View</span>
        </div>
      </div>
    </div>
  );
}
iv>
  );
}

import { BarChart3 } from "lucide-react";
