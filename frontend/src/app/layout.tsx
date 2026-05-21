import type { Metadata } from "next";
import { Inter, Space_Grotesk } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/layout/sidebar";
import { Providers } from "./providers";
import { ClientOnly } from "@/components/shared/client-only";

// Remove Google Fonts to prevent build-time network failures
// const inter = Inter({
//   variable: "--font-sans",
//   subsets: ["latin"],
// });

// const spaceGrotesk = Space_Grotesk({
//   variable: "--font-heading",
//   subsets: ["latin"],
// });

export const metadata: Metadata = {
  title: "ESOTERIC BANK | Experience Layer",
  description: "Institutional Banking Intelligence Command Center",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased dark">
      <body className="h-full bg-background text-foreground flex overflow-hidden font-sans">
        <style dangerouslySetInnerHTML={{ __html: `
          :root {
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --font-heading: 'Space Grotesk', sans-serif;
          }
        `}} />
        <Providers>
          <Sidebar />
          <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
            <header className="h-16 border-b border-white/5 flex items-center justify-between px-8 bg-[#0B1120]/50 backdrop-blur-sm z-10">
              <div className="flex items-center gap-4">
                <div className="px-2 py-1 rounded bg-success/10 border border-success/20 text-[10px] font-bold text-success uppercase tracking-wider">
                  System: Online
                </div>
                <div className="px-2 py-1 rounded bg-primary/10 border border-primary/20 text-[10px] font-bold text-primary uppercase tracking-wider">
                  Env: Production
                </div>
              </div>
              <div className="flex items-center gap-6">
                <ClientOnly fallback={<div className="w-32 h-8 bg-white/5 animate-pulse rounded" />}>
                  <div className="text-right">
                    <div className="text-[10px] text-muted-foreground uppercase font-bold tracking-widest">Global Latency</div>
                    <div className="text-xs font-mono text-success">14ms</div>
                  </div>
                  <div className="text-right">
                    <div className="text-[10px] text-muted-foreground uppercase font-bold tracking-widest">Session ID</div>
                    <div className="text-xs font-mono text-white/40">EB-772-XQ-9</div>
                  </div>
                </ClientOnly>
              </div>
            </header>
            <div className="flex-1 overflow-y-auto p-8">
              {children}
            </div>
          </main>
        </Providers>
      </body>
    </html>
  );
}
