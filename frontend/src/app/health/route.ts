import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json(
    {
      status: "healthy",
      layer: "experience",
      timestamp: new Date().toISOString(),
    },
    {
      status: 200,
    }
  );
}
