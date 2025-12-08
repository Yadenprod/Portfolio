
'use client';

import { useEffect, useState } from 'react';

// Define the type for the Telegram Web App object for better type safety
declare global {
  interface Window {
    Telegram: {
      WebApp: any;
    };
  }
}

export function useTelegram() {
  const [webApp, setWebApp] = useState<any>(null);

  useEffect(() => {
    if (typeof window !== 'undefined' && window.Telegram && window.Telegram.WebApp) {
      const app = window.Telegram.WebApp;
      app.ready(); // Important to call this to signal the app is ready
      setWebApp(app);
    }
  }, []);

  return {
    webApp,
    user: webApp?.initDataUnsafe?.user,
  };
}
