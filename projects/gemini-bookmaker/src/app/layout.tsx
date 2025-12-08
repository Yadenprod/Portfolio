
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { BetSlipProvider } from "@/context/BetSlipContext";
import Sidebar from "@/components/Sidebar";
import { BetSlip } from "@/components/BetSlip";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Gemini Bet",
  description: "A bookmaker app built with Gemini",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
      </head>
      <body className={`${inter.className} antialiased`}>
        <BetSlipProvider>
          <div className="flex h-screen bg-gray-900 text-gray-100">
            <Sidebar />
            <main className="flex-1 p-6 overflow-y-auto">
              {children}
            </main>
            <div className="w-80 bg-gray-800 p-4 overflow-y-auto">
              <BetSlip />
            </div>
          </div>
        </BetSlipProvider>
      </body>
    </html>
  );
}
