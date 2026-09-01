type ApiBase =
  | { ok: true; base: string }
  | { ok: false; reason: string };

function isLocalHost(hostname: string): boolean {
  return hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '::1' || hostname === 'backend';
}

export function getApiBase(): ApiBase {
  const raw = (process.env.NEXT_PUBLIC_API_URL || '').trim().replace(/\/$/, '');
  const deployed = process.env.NODE_ENV === 'production';

  if (!raw) {
    if (deployed) {
      return {
        ok: false,
        reason: 'NEXT_PUBLIC_API_URL is not set. This deployment will not call localhost.',
      };
    }
    return { ok: true, base: 'http://localhost:8000' };
  }

  try {
    const url = new URL(raw);
    if (deployed && isLocalHost(url.hostname)) {
      return {
        ok: false,
        reason: 'NEXT_PUBLIC_API_URL points at a local or Compose host. Set a reachable HTTPS API URL in Vercel.',
      };
    }
    return { ok: true, base: raw };
  } catch {
    return { ok: false, reason: 'NEXT_PUBLIC_API_URL is not a valid URL.' };
  }
}
