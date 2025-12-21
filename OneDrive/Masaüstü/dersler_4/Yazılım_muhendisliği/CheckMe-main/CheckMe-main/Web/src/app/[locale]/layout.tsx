import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';
import { Toaster } from 'sonner';
import "./globals.css";

export default async function LocaleLayout({
  children,
  params
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const messages = await getMessages();

  return (
    <html lang={locale}>
      <body className="bg-zinc-50 dark:bg-black antialiased">
        <NextIntlClientProvider messages={messages}>
          {
          }
          {children}
          
          <Toaster 
            position="bottom-right" 
            richColors 
            closeButton
            theme="inherit"
          />
        </NextIntlClientProvider>
      </body>
    </html>
  );
}