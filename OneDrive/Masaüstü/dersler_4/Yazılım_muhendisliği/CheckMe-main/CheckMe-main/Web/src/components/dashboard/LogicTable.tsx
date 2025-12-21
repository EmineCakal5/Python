'use client';

interface LogicTableProps {
  logicTests: any[];
}

export default function LogicTable({ logicTests }: LogicTableProps) {
  return (
    <div className="w-full overflow-x-auto text-black dark:text-white">
      <table className="w-full text-sm text-left border-collapse">
        <thead className="bg-zinc-50/50 dark:bg-zinc-800/50 text-zinc-400 font-bold border-b border-zinc-100 dark:border-zinc-800">
          <tr>
            <th className="px-8 py-4 uppercase text-[10px] tracking-widest">Input</th>
            <th className="px-8 py-4 uppercase text-[10px] tracking-widest">Expected</th>
            <th className="px-8 py-4 uppercase text-[10px] tracking-widest">Output</th>
            <th className="px-8 py-4 text-center uppercase text-[10px] tracking-widest">Result</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-zinc-50 dark:divide-zinc-800">
          {logicTests.map((lt, idx) => (
            <tr key={idx} className="hover:bg-zinc-50/30 dark:hover:bg-zinc-800/30 transition-colors">
              <td className="px-8 py-4 font-mono text-xs text-zinc-600 dark:text-zinc-400 truncate max-w-[200px]">{lt.input}</td>
              <td className="px-8 py-4 font-mono text-xs text-zinc-400 truncate max-w-[200px]">{lt.expected}</td>
              <td className="px-8 py-4 font-mono text-xs text-zinc-400 truncate max-w-[200px]">{lt.output}</td>
              <td className="px-8 py-4 text-center">
                <span className={`px-3 py-1 rounded-lg text-[10px] font-bold ${lt.status === 'OK' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                  {lt.status === 'OK' ? 'PASSED' : 'FAILED'}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}