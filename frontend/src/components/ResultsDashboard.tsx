/**
 * Results Dashboard Component
 * Main dashboard displaying all AI responses and comparisons
 */

'use client';

import { motion } from 'framer-motion';
import { PromptSubmitResponse } from '@/types';
import { getDomainIcon, getSafetyColor, formatCost, formatDate } from '@/lib/utils';
import ResponseCard from './ResponseCard';
import ComparisonCharts from './ComparisonCharts';
import { AI_MODELS } from '@/lib/utils';

interface ResultsDashboardProps {
  results: PromptSubmitResponse;
  onNewPrompt: () => void;
}

export default function ResultsDashboard({ results, onNewPrompt }: ResultsDashboardProps) {
  const domain = results.domain_classification;
  const bestModel = AI_MODELS[results.best_model];

  return (
    <div className="space-y-6 slide-in-bottom">
      {/* Header with domain classification */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-blue-50 to-cyan-50 dark:from-blue-950 dark:to-slate-950 rounded-xl p-6 border border-blue-200 dark:border-blue-800"
      >
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-3xl">{getDomainIcon(domain.domain)}</span>
              <div>
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                  Analysis Complete
                </h2>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Domain: <span className="font-semibold capitalize">{domain.domain}</span>
                  {' • '}
                  Confidence: <span className="font-semibold">{Math.round(domain.confidence * 100)}%</span>
                </p>
              </div>
            </div>

            {/* Safety badge */}
            <div className="flex items-center gap-2 mt-3">
              <span
                className={`px-3 py-1 rounded-full text-xs font-medium ${getSafetyColor(
                  domain.safety_level
                )}`}
              >
                {domain.safety_level === 'safe' && '✓ Safe'}
                {domain.safety_level === 'caution' && '⚠ Caution'}
                {domain.safety_level === 'warning' && '⚠️ Warning'}
                {domain.safety_level === 'critical' && '🚨 Critical'}
              </span>

              {/* Warnings */}
              {domain.warnings.length > 0 && (
                <span className="text-xs text-gray-600 dark:text-gray-400">
                  {domain.warnings.length} warning(s)
                </span>
              )}
            </div>

            {/* Display warnings */}
            {domain.warnings.length > 0 && (
              <div className="mt-3 space-y-1">
                {domain.warnings.map((warning, idx) => (
                  <p key={idx} className="text-xs text-orange-600 dark:text-orange-400">
                    ⚠️ {warning}
                  </p>
                ))}
              </div>
            )}
          </div>

          {/* Best model recommendation */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.3, type: 'spring' }}
            className="bg-white dark:bg-gray-800 rounded-lg p-4 border-2 border-yellow-400 dark:border-yellow-500 shadow-lg"
          >
            <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">
              🏆 Best AI for this prompt
            </p>
            <div className="flex items-center gap-2">
              <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${bestModel.color} flex items-center justify-center text-xl`}>
                {bestModel.icon}
              </div>
              <div>
                <p className="font-bold text-gray-900 dark:text-white">{bestModel.name}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400">{bestModel.provider}</p>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Metadata */}
        <div className="mt-4 pt-4 border-t border-blue-200 dark:border-blue-800 flex items-center justify-between flex-wrap gap-2 text-xs text-gray-600 dark:text-gray-400">
          <span>📅 {formatDate(results.timestamp)}</span>
          <span>⏱️ {results.processing_time.toFixed(2)}s total</span>
          <span>💰 {formatCost(results.total_cost)} total cost</span>
          <span>🤖 {results.ai_responses.length} models compared</span>
        </div>
      </motion.div>

      {/* Comparison Charts */}
      <ComparisonCharts responses={results.ai_responses} />

      {/* Individual responses */}
      <div>
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
          <span className="text-2xl">🤖</span>
          Individual AI Responses
        </h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {results.ai_responses.map((response, idx) => (
            <ResponseCard key={response.model} response={response} index={idx} />
          ))}
        </div>
      </div>

      {/* Action buttons */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="flex items-center justify-center gap-4 pt-6"
      >
        <button
          onClick={onNewPrompt}
          className="px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-medium rounded-lg shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105"
        >
          🚀 Try Another Prompt
        </button>
        <button
          onClick={() => {
            const data = JSON.stringify(results, null, 2);
            const blob = new Blob([data], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `mai-paep-${results.session_id}.json`;
            a.click();
          }}
          className="px-6 py-3 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 font-medium rounded-lg border-2 border-gray-300 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-500 transition-all duration-300"
        >
          📥 Export Results
        </button>
      </motion.div>
    </div>
  );
}
