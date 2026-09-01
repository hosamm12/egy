type ApiBase =
  | { ok: true; base: string }
  | { ok: false; reason: string };

function isBlockedHost(hostname: string): boolean {
  return (
    hostname === 'localhost' ||
    hostname === '127.0.0.1' ||
    hostname === '::1' ||
    hostname === 'backend' ||
    hostname === 'postgres' ||
    hostname === 'redis'
  );
}

export function getApiBase(): ApiBase {
  const raw = (process.env.NEXT_PUBLIC_API_URL || '').trim().replace(/\/$/, '');

  if (!raw) {
    return { ok: true, base: '' };
  }

  try {
    const url = new URL(raw);
    if (isBlockedHost(url.hostname)) {
      return {
        ok: false,
        reason: 'API URL cannot be localhost or a Docker service name. Set NEXT_PUBLIC_API_URL to an HTTPS origin.',
      };
    }
    if (url.protocol !== 'https:') {
      return {
        ok: false,
        reason: 'API URL must use HTTPS.',
      };
    }
    return { ok: true, base: raw };
  } catch {
    return { ok: false, reason: 'NEXT_PUBLIC_API_URL is not a valid URL.' };
  }
}
