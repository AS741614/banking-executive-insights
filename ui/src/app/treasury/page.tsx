"use client";

import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { useRiskIntelligence, useForecastIntelligence } from "@/hooks/use-treasury";
import { 
  TrendingUp, 
  TrendingDown, 
  AlertCircle, 
  BarChart3, 
  Globe2,
  PieChart,
  ArrowUpRight,
  ArrowDownRight
} from "lucide-react";
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Cell,
  LineChart,
  Line
} from 'recharts';
import { InstitutionalChartContainer } from "@/components/charts/InstitutionalChartContainer";

export default function TreasuryCockpit() {
  const { data: riskData, isLoading: riskLoading } = useRiskIntelligence();
  const { data: forecastData, isLoading: forecastLoading } = useForecastIntelligence();

  const risk = riskData?.data;
  const forecast = forecastData?.data;

  const regionalData = risk?.regional_breakdown?.map(r => ({
    name: r.region,
    value: r.net_flow
  })) || [];

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <Header title="TREASURY_COCKPIT" />
        <main className="flex-1 overflow-y-auto p-6">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
            <div className="panel-glass p-4 flex flex-col justify-between">
                <div className="flex justify-between items-start">
                    <span className="text-[10px] text-gray-400 font-space tracking-widest uppercase">Net Projection</span>
                    <TrendingUp className="w-4 h-4 text-success" />
                </div>
                <div className="mt-2">
                    <span className="text-2xl font-bold text-white">
                        {forecastLoading ? "..." : `$${((forecast?.projected_next_month_flow || 0) / 1000000).toFixed(2)}M`}
                    </span>
                    <div className="flex items-center space-x-1 mt-1">
                        <ArrowUpRight className="w-3 h-3 text-success" />
                        <span className="text-[10px] text-success font-bold uppercase">{forecast?.trend}</span>
                    </div>
                </div>
            </div>

            <div className="panel-glass p-4 flex flex-col justify-between">
                <div className="flex justify-between items-start">
                    <span className="text-[10px] text-gray-400 font-space tracking-widest uppercase">Risk Exposure</span>
                    <AlertCircle className="w-4 h-4 text-gold" />
                </div>
                <div className="mt-2">
                    <span className={`text-2xl font-bold uppercase ${risk?.risk_level === 'ELEVATED' ? 'text-critical' : 'text-gold'}`}>
                        {riskLoading ? "..." : risk?.risk_level}
                    </span>
                    <p className="text-[10px] text-gray-500 mt-1 uppercase">
                        {risk?.anomalies_detected} Anomalies detected
                    </p>
                </div>
            </div>

            <div className="panel-glass p-4 flex flex-col justify-between">
                <div className="flex justify-between items-start">
                    <span className="text-[10px] text-gray-400 font-space tracking-widest uppercase">Confidence Score</span>
                    <BarChart3 className="w-4 h-4 text-primary" />
                </div>
                <div className="mt-2">
                    <span className="text-2xl font-bold text-primary">
                        {forecastLoading ? "..." : `${((forecast?.confidence_score || 0) * 100).toFixed(1)}%`}
                    </span>
                    <p className="text-[10px] text-gray-500 mt-1 uppercase">Model: {forecast?.prediction_model}</p>
                </div>
            </div>

            <div className="panel-glass p-4 flex flex-col justify-between border-l-4 border-primary-accent">
                <div className="flex justify-between items-start">
                    <span className="text-[10px] text-primary-accent font-space tracking-widest uppercase">Institutional Pulse</span>
                    <Globe2 className="w-4 h-4 text-primary-accent" />
                </div>
                <div className="mt-2">
                    <span className="text-2xl font-bold text-white uppercase">Stable</span>
                    <p className="text-[10px] text-gray-500 mt-1 uppercase">Global Liquidity Pool</p>
                </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="panel-glass p-6 min-h-[400px]">
                <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center space-x-3">
                        <PieChart className="w-5 h-5 text-primary" />
                        <h2 className="text-sm font-space font-bold uppercase tracking-widest">Regional_Liquidity_Distribution</h2>
                    </div>
                </div>
                <div className="w-full">
                    <InstitutionalChartContainer height={280} minHeight={280}>
                        <BarChart data={regionalData} layout="vertical">
                            <CartesianGrid strokeDasharray="3 3" stroke="#ffffff05" horizontal={false} />
                            <XAxis type="number" hide />
                            <YAxis 
                                dataKey="name" 
                                type="category" 
                                stroke="#8B949E" 
                                fontSize={10} 
                                axisLine={false}
                                tickLine={false}
                                width={80}
                            />
                            <Tooltip 
                                cursor={{ fill: 'rgba(255,255,255,0.02)' }}
                                contentStyle={{ backgroundColor: '#0B1120', border: '1px solid rgba(255,255,255,0.08)', fontSize: '10px' }}
                            />
                            <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                                {regionalData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={entry.value < 0 ? '#FF4D6D' : '#00D1FF'} fillOpacity={0.8} />
                                ))}
                            </Bar>
                        </BarChart>
                    </InstitutionalChartContainer>
                </div>
            </div>

            <div className="panel-glass p-6 min-h-[400px]">
                <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center space-x-3">
                        <BarChart3 className="w-5 h-5 text-success" />
                        <h2 className="text-sm font-space font-bold uppercase tracking-widest">Predictive_Flow_Analysis</h2>
                    </div>
                </div>
                <div className="flex-1 flex flex-col justify-center">
                    <div className="space-y-6">
                        <div className="p-4 bg-white/[0.02] border border-border rounded-lg">
                            <span className="text-[10px] text-gray-500 uppercase font-space block mb-2">Primary Trend Vector</span>
                            <div className="flex items-center space-x-4">
                                <div className={`p-2 rounded ${forecast?.trend === 'UPWARD' ? 'bg-success/10' : 'bg-critical/10'}`}>
                                    {forecast?.trend === 'UPWARD' ? <ArrowUpRight className="text-success" /> : <ArrowDownRight className="text-critical" />}
                                </div>
                                <div>
                                    <p className="text-sm font-bold">{forecast?.trend === 'UPWARD' ? 'Positive Accretion' : 'Potential Outflow'}</p>
                                    <p className="text-[10px] text-gray-500 uppercase">Institutional Velocity Metric</p>
                                </div>
                            </div>
                        </div>

                        <div className="p-4 bg-white/[0.02] border border-border rounded-lg">
                            <span className="text-[10px] text-gray-500 uppercase font-space block mb-2">Model Confidence Analysis</span>
                            <div className="w-full bg-white/5 h-2 rounded-full overflow-hidden">
                                <div 
                                    className="bg-primary h-full transition-all duration-1000" 
                                    style={{ width: `${(forecast?.confidence_score || 0) * 100}%` }}
                                />
                            </div>
                            <div className="flex justify-between mt-2">
                                <span className="text-[10px] text-gray-500 uppercase">Variance: Minimal</span>
                                <span className="text-[10px] text-primary font-bold">{((forecast?.confidence_score || 0) * 100).toFixed(1)}% Accuracy</span>
                            </div>
                        </div>

                        <div className="p-4 border border-primary/20 bg-primary/5 rounded-lg">
                            <p className="text-[10px] text-primary leading-relaxed uppercase">
                                <span className="font-bold mr-2">[INSIGHT]</span>
                                {forecast?.trend === 'UPWARD' 
                                    ? "Liquidity vectors indicate strong institutional resilience. No immediate capital buffer adjustments recommended."
                                    : "Predictive drift suggests regional liquidity compression. Monitor APAC flows for early warning signals."}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
