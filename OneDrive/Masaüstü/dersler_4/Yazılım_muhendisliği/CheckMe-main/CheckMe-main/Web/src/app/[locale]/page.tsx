'use client';

import { useTranslations } from 'next-intl';
import { useState, useEffect, useRef } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Github } from 'lucide-react';
import { toast } from 'sonner'; // Toast eklendi

// Bileşen Importları (Relatif yollarla en güvenli hali)
import Navbar from '../../components/layout/Navbar';
import Sidebar from '../../components/layout/Sidebar';
import TestCard from '../../components/dashboard/TestCard';
import SkeletonCard from '../../components/dashboard/SkeletonCard';

export default function HomePage() {
  const t = useTranslations('Index');
  
  const [url, setUrl] = useState('');
  const [tests, setTests] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [terminalLogs, setTerminalLogs] = useState<string[]>(["Waiting for command..."]);
  
  const terminalEndRef = useRef<null | HTMLDivElement>(null);

  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [terminalLogs]);

  const addLog = (msg: string) => {
    setTerminalLogs(prev => [...prev, msg]);
  };

  const handleStartTest = async () => {
    if (!url) {
      toast.error('Please enter a GitHub URL or username/repo');
      return;
    }
    
    // Girdiyi düzenle
    let finalUrl = url.trim();
    if (!finalUrl.startsWith('http')) {
      finalUrl = `https://github.com/${finalUrl}`;
    }

    setLoading(true);
    setTerminalLogs([]); 
    
    addLog(`➜  ~ git clone ${finalUrl}`);
    addLog("Cloning into 'push_swap'...");
    
    try {
      const response = await fetch('http://127.0.0.1:8000/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_url: finalUrl }),
      });

      if (!response.ok) throw new Error("Backend connection failed");

      addLog("➜  push_swap git:(main) make");
      addLog("cc -Wall -Wextra -Werror -c *.c");
      addLog("cc -o push_swap *.o");
      addLog("➜  push_swap git:(main) ./push_swap 3 2 1");

      const data = await response.json();
      
      const urlParts = finalUrl.replace("https://github.com/", "").split("/");
      const owner = urlParts[0] || "Unknown";
      const repoName = data.result.project || urlParts[1] || "Project";

      addLog("OK! Test cycle completed.");
      toast.success(`Evaluation complete: ${repoName}`); // Başarı bildirimi

      const newTest = {
        id: data.test_id,
        owner: owner.toUpperCase(),
        name: repoName.toUpperCase(),
        repoUrl: finalUrl,
        status: data.result.status,
        standardChecks: data.steps || [],
        logicTests: data.logicTests || []
      };

      setTests([newTest, ...tests]);
      setUrl('');
    } catch (error) {
      addLog("!! ERROR: Connection failed. Check Docker status.");
      toast.error('Connection error: Make sure the tester backend is running.'); // Hata bildirimi
      console.error("Test Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-[#F8F9FB] dark:bg-black overflow-hidden font-sans text-black dark:text-white">
      
      <Navbar />

      <div className="flex flex-1 w-full overflow-hidden">
        
        <Sidebar 
          url={url}
          setUrl={setUrl}
          loading={loading}
          onStart={handleStartTest}
          terminalLogs={terminalLogs}
          terminalEndRef={terminalEndRef}
        />

        <main className="flex-1 p-10 overflow-y-auto bg-[#F8F9FB] dark:bg-black custom-scrollbar">
          <AnimatePresence mode="popLayout">
            {/* Yükleme sırasında en üstte Skeleton gösterilir */}
            {loading && (
              <motion.div
                key="skeleton"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.2 }}
              >
                <SkeletonCard />
              </motion.div>
            )}

            {tests.length === 0 && !loading ? (
              <motion.div 
                key="empty"
                initial={{ opacity: 0 }} 
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="h-full flex flex-col items-center justify-center text-zinc-400 border-2 border-dashed border-zinc-200 dark:border-zinc-800 rounded-[40px] bg-white dark:bg-zinc-900/20"
              >
                <div className="w-20 h-20 bg-zinc-100 dark:bg-zinc-900 rounded-3xl flex items-center justify-center mb-6 shadow-inner text-zinc-300">
                  <Github size={40} className="opacity-20" />
                </div>
                <p className="font-medium text-lg italic tracking-tight text-zinc-400">
                  {t('waiting_repo')}
                </p>
              </motion.div>
            ) : (
              tests.map((test) => (
                <TestCard key={test.id} test={test} />
              ))
            )}
          </AnimatePresence>
        </main>

      </div>
    </div>
  );
}