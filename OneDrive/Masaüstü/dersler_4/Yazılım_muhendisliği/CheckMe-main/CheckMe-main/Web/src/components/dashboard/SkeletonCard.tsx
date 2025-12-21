export default function SkeletonCard() {
  return (
    <div className="mb-10 w-full border border-zinc-200 dark:border-zinc-800 rounded-3xl bg-white dark:bg-zinc-900 overflow-hidden animate-pulse">
      <div className="px-8 py-6 border-b border-zinc-100 dark:border-zinc-800 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-zinc-200 dark:bg-zinc-800 rounded-2xl" />
          <div className="space-y-2">
            <div className="h-3 w-32 bg-zinc-100 dark:bg-zinc-800 rounded" />
            <div className="h-5 w-48 bg-zinc-200 dark:bg-zinc-800 rounded" />
          </div>
        </div>
      </div>
      <div className="px-8 py-8 grid grid-cols-6 gap-4 border-b border-zinc-50 dark:border-zinc-800">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} className="h-20 bg-zinc-100 dark:bg-zinc-800 rounded-2xl" />
        ))}
      </div>
    </div>
  );
}