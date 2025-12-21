'use client';
import { motion } from 'framer-motion';
import { CheckCircle2, XCircle } from 'lucide-react';

const STEP_LABELS: Record<number, string> = {
  1: "Clone", 2: "Makefile", 3: "Rules", 4: "Flags", 5: "Build", 6: "Relink"
};

interface StepGridProps {
  steps: { id: number; status: 'OK' | 'KO' }[];
}

export default function StepGrid({ steps }: StepGridProps) {
  return (
    <div className="px-8 py-8 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 bg-white dark:bg-zinc-900 border-b border-zinc-50 dark:border-zinc-800 text-black dark:text-white">
      {steps.map((step, sIdx) => (
        <motion.div
          key={step.id}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 * sIdx + 0.3 }}
          className="flex flex-col gap-3 bg-zinc-50/50 dark:bg-zinc-800/30 p-4 rounded-2xl border border-zinc-100 dark:border-zinc-800 hover:border-blue-500/30 transition-colors"
        >
          <div className="flex justify-between items-center">
            <span className="text-[10px] font-bold text-zinc-400 uppercase tracking-tighter">STEP {step.id}</span>
            {step.status === 'OK' ? <CheckCircle2 size={16} className="text-green-500" /> : <XCircle size={16} className="text-red-500" />}
          </div>
          <span className="text-sm font-bold">{STEP_LABELS[step.id]}</span>
        </motion.div>
      ))}
    </div>
  );
}