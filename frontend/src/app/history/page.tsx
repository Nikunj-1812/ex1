export default function HistoryPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-10">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">Session History</h1>
      <p className="text-gray-600 dark:text-gray-400">
        Coming soon: Browse, search, and re-run past sessions. This page will list your previous prompts, best models, costs, and quick actions.
      </p>
      <div className="mt-6 p-4 rounded-lg border border-dashed border-gray-300 dark:border-gray-700 text-sm text-gray-500 dark:text-gray-400">
        Placeholder UI. Backend integration will pull data from PostgreSQL/MongoDB.
      </div>
    </div>
  );
}
