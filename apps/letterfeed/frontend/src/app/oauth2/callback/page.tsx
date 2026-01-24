'use client';

import { useEffect, useState } from 'react';
import { completeGmailOAuth2 } from '@/lib/api';
import { useRouter } from 'next/navigation';
import { Loader2 } from 'lucide-react';

export default function OAuth2CallbackPage() {
  const router = useRouter();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>(
    'loading',
  );
  const [message, setMessage] = useState<string>(
    'Completing Gmail authorization...',
  );

  useEffect(() => {
    const url = new URL(window.location.href);
    const code = url.searchParams.get('code');
    if (!code) {
      setStatus('error');
      setMessage('Missing authorization code.');
      return;
    }

    const redirectUri = `${window.location.origin}/oauth2/callback`;

    completeGmailOAuth2(code, redirectUri)
      .then(() => {
        setStatus('success');
        setMessage('Gmail connected! Redirecting to settings...');
        setTimeout(() => {
          router.push('/');
        }, 1500);
      })
      .catch((err: unknown) => {
        setStatus('error');
        setMessage(
          err instanceof Error ? err.message : 'Authorization failed.',
        );
      });
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="flex items-center space-x-3 text-sm">
        {status === 'loading' && <Loader2 className="w-4 h-4 animate-spin" />}
        <span>{message}</span>
      </div>
    </div>
  );
}
