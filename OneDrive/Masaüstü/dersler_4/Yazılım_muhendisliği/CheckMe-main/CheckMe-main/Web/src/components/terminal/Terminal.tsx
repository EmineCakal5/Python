'use client';
import { Terminal as TerminalIcon } from 'lucide-react';

interface TerminalProps {
  logs: string[];
  endRef: React.RefObject<HTMLDivElement | null>;
}

export default function Terminal({ logs, endRef }: TerminalProps) {
  return (
    <div className="mt-8 flex-1 flex flex-col min-h-0 bg-[#0D1117] rounded-2xl border border-zinc-800 overflow-hidden shadow-2xl">
      <div className="bg-zinc-800/50 px-4 py-2 flex items-center gap-2 border-b border-zinc-800">
        <div className="flex gap-1.5">
          <div className="w-2.5 h-2.5 rounded-full bg-[#FF5F56]" />
          <div className="w-2.5 h-2.5 rounded-full bg-[#FFBD2E]" />
          <div className="w-2.5 h-2.5 rounded-full bg-[#27C93F]" />
        </div>
        <TerminalIcon size={12} className="text-zinc-500 ml-2" />
        <span className="text-[10px] text-zinc-400 font-mono italic">zsh — 80x24</span>
      </div>
      <div className="flex-1 p-4 font-mono text-[11px] overflow-y-auto leading-relaxed">
        {logs.map((log, i) => (
          <div key={i} className="mb-1 animate-in fade-in duration-300">
            {log.startsWith('➜') ? (
              <>
                <span className="text-[#27C93F]">➜</span>
                <span className="text-[#3391CC] ml-2">~</span>
                <span className="text-white ml-2">{log.substring(4)}</span>
              </>
            ) : (
              <span className="text-zinc-400">{log}</span>
            )}
          </div>
        ))}
        <div ref={endRef} />
      </div>
    </div>
  );
}