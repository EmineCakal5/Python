'use client';
import { Github, RefreshCcw } from 'lucide-react';
import { useTranslations } from 'next-intl';
import Terminal from '../terminal/Terminal';

interface SidebarProps {
  url: string;
  setUrl: (url: string) => void;
  loading: boolean;
  onStart: () => void;
  terminalLogs: string[];
  terminalEndRef: React.RefObject<HTMLDivElement | null>;
}

export default function Sidebar({ 
  url, setUrl, loading, onStart, terminalLogs, terminalEndRef 
}: SidebarProps) {
  const t = useTranslations('Index');

  return (
    <aside className="w-96 border-r bg-white dark:bg-zinc-900 p-8 flex flex-col gap-6 shrink-0 shadow-sm overflow-hidden">
      <div className="flex-1 space-y-6 overflow-y-auto">
        <div className="space-y-2">
          <h3 className="text-[11px] font-bold text-zinc-400 uppercase tracking-[2px]">
            {t('new_evaluation')}
          </h3>
          <p className="text-xs text-zinc-500 leading-relaxed">
            Repo linkini girin ve süreci terminalden izleyin.
          </p>
        </div>
        
        <div className="space-y-4">
          <div className="relative group">
            <Github className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-400" size={18} />
            <input 
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="w-full pl-12 pr-4 py-4 text-sm rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-950 outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all shadow-inner text-black dark:text-white"
                placeholder="username/repo or github.com link..."
                disabled={loading}
            />
          </div>
          <button 
            onClick={onStart}
            disabled={loading}
            className="w-full bg-blue-600 text-white py-4 rounded-2xl font-bold hover:bg-blue-700 transition-all flex items-center justify-center gap-2 disabled:bg-zinc-200"
          >
            {loading ? <RefreshCcw className="animate-spin" size={18} /> : t('start_test')}
          </button>
        </div>

        {/* Terminal Bileşenini Burada Çağırıyoruz */}
        <Terminal logs={terminalLogs} endRef={terminalEndRef} />
      </div>
    </aside>
  );
}