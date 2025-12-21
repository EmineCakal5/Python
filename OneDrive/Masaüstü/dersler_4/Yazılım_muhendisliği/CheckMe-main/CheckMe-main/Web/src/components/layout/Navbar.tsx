'use client';
import { LayoutDashboard, Box } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navbar() {
  const pathname = usePathname();

  // Aktif dil kontrolü için yardımcı fonksiyon
  const isActive = (locale: string) => pathname.includes(`/${locale}`);

  return (
    <header className="w-full h-16 border-b bg-white dark:bg-zinc-900 flex items-center px-8 justify-between shrink-0 shadow-sm z-50">
      <div className="flex gap-12 items-center h-full">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-black italic">C</div>
          <span className="font-black text-xl tracking-tighter text-zinc-800 dark:text-white">CHECKME.</span>
        </div>
        
        <nav className="flex gap-8 h-full">
          <button className="flex items-center gap-2 px-1 border-b-2 border-blue-600 text-blue-600 font-bold text-sm h-full transition-all">
            <LayoutDashboard size={18} /> Dashboard
          </button>
          <button className="flex items-center gap-2 px-1 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 text-sm font-medium h-full transition-all">
            <Box size={18} /> Virtualizator
            <span className="text-[9px] bg-zinc-100 dark:bg-zinc-800 px-1.5 py-0.5 rounded text-zinc-500 uppercase ml-2">Soon</span>
          </button>
        </nav>
      </div>

      {/* Dil Seçici - Düzeltilmiş Hali */}
      <div className="flex bg-zinc-100 dark:bg-zinc-800 p-1 rounded-xl text-[11px] font-bold shadow-inner border border-zinc-200/50 dark:border-zinc-700/50">
        <Link 
          href="/tr" 
          className={`px-3 py-1.5 rounded-lg transition-all duration-200 ${
            isActive('tr') 
              ? 'bg-white dark:bg-zinc-700 text-blue-600 dark:text-blue-400 shadow-sm' 
              : 'text-zinc-500 hover:text-zinc-800 dark:text-zinc-400 dark:hover:text-zinc-200'
          }`}
        >
          TR
        </Link>
        <Link 
          href="/en" 
          className={`px-3 py-1.5 rounded-lg transition-all duration-200 ${
            isActive('en') 
              ? 'bg-white dark:bg-zinc-700 text-blue-600 dark:text-blue-400 shadow-sm' 
              : 'text-zinc-500 hover:text-zinc-800 dark:text-zinc-400 dark:hover:text-zinc-200'
          }`}
        >
          EN
        </Link>
      </div>
    </header>
  );
}