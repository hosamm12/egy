import { NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

export async function GET() {
  let deployedHash = process.env.DEPLOYED_HASH || 'unknown';
  try {
    const file = await fs.readFile(path.join(process.cwd(), '.security_hash'), 'utf8');
    deployedHash = file.trim();
  } catch {
    // ignore if file missing
  }
  return NextResponse.json({
    status: 'ok',
    deployedHash,
    time: new Date().toISOString(),
  });
}
