'use client';
import { motion } from 'framer-motion';
import { User, ChevronRight } from 'lucide-react';
import StepGrid from './StepGrid';
import LogicTable from './LogicTable';

interface TestCardProps {
  test: any;
}

export default function TestCard({ test }: TestCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -40, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="mb-10 w-full border border-zinc-200 dark:border-zinc-800 rounded-3xl bg-white dark:bg-zinc-900 shadow-sm overflow-hidden"
    >
      {/* Repo Header */}
      <div className="px-8 py-6 border-b border-zinc-100 dark:border-zinc-800 bg-zinc-50/30 dark:bg-zinc-800/20 flex justify-between items-center text-black dark:text-white">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-white dark:bg-zinc-800 rounded-2xl shadow-sm border border-zinc-100 dark:border-zinc-700 flex items-center justify-center">
            <User className="text-blue-500" size={24} />
          </div>
          <div>
            <div className="flex items-center gap-2 text-zinc-400 text-xs font-semibold uppercase tracking-wider mb-1">
              <span>{test.owner}</span>
              <ChevronRight size={12} />
              <span>{test.name}</span>
            </div>
            <h2 className="text-xl font-black leading-none tracking-tight">ID: {test.id}</h2>
          </div>
        </div>
        <div className={`px-5 py-2 rounded-xl text-xs font-black tracking-[2px] text-white ${test.status === 'SUCCESS' ? 'bg-green-600 shadow-lg shadow-green-500/20' : 'bg-red-600 shadow-lg shadow-red-500/20'}`}>
          {test.status}
        </div>
      </div>

      <StepGrid steps={test.standardChecks} />
      <LogicTable logicTests={test.logicTests} />
    </motion.div>
  );
}