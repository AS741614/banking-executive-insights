"use client";

import { Bell, Search, User } from "lucide-react";

interface HeaderProps {
  title: string;
}

export function Header({ title }: HeaderProps) {
  return (
    <header className="h-16 border-b border-border bg-panels/50 backdrop-blur-md flex items-center justify-between px-6">
      <div className="flex items-center space-x-4">
        <h1 className="font-space text-sm font-bold tracking-[0.2em] text-gray-300 uppercase">
          {title}
        </h1>
      </div>

      <div className="flex items-center space-x-6">
        <div className="relative">
            <Search className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
            <input 
                type="text" 
                placeholder="SEARCH_COMMANDS..." 
                className="bg-background/50 border border-border rounded-md pl-10 pr-4 py-1.5 text-xs font-space focus:outline-none focus:border-primary/50 w-64"
            />
        </div>
        
        <div className="flex items-center space-x-4">
            <button className="text-gray-400 hover:text-white transition-colors relative">
                <Bell className="w-4 h-4" />
                <span className="absolute -top-1 -right-1 w-2 h-2 bg-critical rounded-full border border-background" />
            </button>
            <div className="h-4 w-px bg-border" />
            <button className="flex items-center space-x-2 text-gray-400 hover:text-white transition-colors">
                <span className="text-[10px] font-space tracking-wider">A. SHARMA</span>
                <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center border border-primary/30">
                    <User className="w-4 h-4 text-primary" />
                </div>
            </button>
        </div>
      </div>
    </header>
  );
}
