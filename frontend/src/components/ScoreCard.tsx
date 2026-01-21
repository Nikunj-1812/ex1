/**
 * Score Card Component
 * Displays individual score with visual indicator
 */

'use client';

import { motion } from 'framer-motion';
import { getScoreColor, getScoreGradient, getScoreLabel } from '@/lib/utils';

interface ScoreCardProps {
  label: string;
  score: number;
  icon?: string;
  delay?: number;
}

export default function ScoreCard({ label, score, icon, delay = 0 }: ScoreCardProps) {
  const percentage = Math.round(score);
  const circumference = 2 * Math.PI * 40;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay, type: 'spring', stiffness: 200 }}
      className={`
        relative p-4 rounded-xl border-2
        ${getScoreColor(percentage)}
        transition-all duration-300 hover:shadow-md
      `}
    >
      <div className="flex items-center justify-between">
        {/* Label and icon */}
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1 has-tooltip relative">
            {icon && <span className="text-lg">{icon}</span>}
            <p className="text-xs font-medium uppercase tracking-wide opacity-80">
              {label}
            </p>
            <span className="text-xs text-gray-500 dark:text-gray-400">ⓘ</span>
            <div className="tooltip left-0 top-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md p-2 shadow-md w-48 text-[11px] text-gray-700 dark:text-gray-300">
              {label === 'Accuracy' && 'Estimated factual and semantic correctness of the response.'}
              {label === 'Relevance' && 'How closely the response matches the prompt intent.'}
              {label === 'Clarity' && 'Readability and structure of the response.'}
              {label === 'Trust Score' && 'Composite score balancing all metrics and risk.'}
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <motion.p
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: delay + 0.2, type: 'spring', stiffness: 300 }}
              className="text-3xl font-bold"
            >
              {percentage}
            </motion.p>
            <span className="text-sm opacity-70">/ 100</span>
          </div>
          <p className="text-xs mt-1 opacity-70 font-medium">
            {getScoreLabel(percentage)}
          </p>
        </div>

        {/* Circular progress */}
        <div className="relative w-20 h-20">
          <svg className="transform -rotate-90 w-20 h-20">
            {/* Background circle */}
            <circle
              cx="40"
              cy="40"
              r="36"
              stroke="currentColor"
              strokeWidth="6"
              fill="none"
              className="opacity-20"
            />
            {/* Progress circle */}
            <motion.circle
              cx="40"
              cy="40"
              r="36"
              stroke="currentColor"
              strokeWidth="6"
              fill="none"
              strokeLinecap="round"
              initial={{ strokeDashoffset: circumference }}
              animate={{ strokeDashoffset: offset }}
              transition={{ delay: delay + 0.3, duration: 1, ease: 'easeOut' }}
              strokeDasharray={circumference}
              className="opacity-100"
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-xs font-bold">{percentage}%</span>
          </div>
        </div>
      </div>

      {/* Progress bar */}
      <div className="mt-3 h-2 bg-black/10 dark:bg-white/10 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ delay: delay + 0.4, duration: 1, ease: 'easeOut' }}
          className={`h-full bg-gradient-to-r ${getScoreGradient(percentage)}`}
        />
      </div>
    </motion.div>
  );
}
