/**
 * AI Response Card Component
 * Displays individual AI model response with scores
 */

'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { AIResponseData } from '@/types';
import { AI_MODELS, formatCost, formatTime } from '@/lib/utils';
import ScoreCard from './ScoreCard';

interface ResponseCardProps {
  response: AIResponseData;
  index: number;
}

export default function ResponseCard({ response, index }: ResponseCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const modelInfo = AI_MODELS[response.model];
  const scores = response.evaluation_scores;

  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className={`
        relative bg-white dark:bg-gray-800 rounded-xl p-6 border-2
        ${response.is_best
          ? 'border-yellow-400 dark:border-yellow-500 shadow-xl shadow-yellow-500/20'
          : 'border-gray-200 dark:border-gray-700'
        }
        transition-all duration-300 hover:shadow-lg
      `}
    >
      {/* Best AI Badge */}
      {response.is_best && (
        <motion.div
          initial={{ scale: 0, rotate: -180 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ delay: 0.5, type: 'spring', stiffness: 200 }}
          className="absolute -top-3 -right-3 bg-gradient-to-r from-yellow-400 to-orange-500 text-white px-4 py-2 rounded-full shadow-lg flex items-center gap-2 badge-bounce"
        >
          <span className="text-lg">🏆</span>
          <span className="font-bold text-sm">Best AI</span>
        </motion.div>
      )}

      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${modelInfo.color} flex items-center justify-center text-2xl shadow-md`}>
            {modelInfo.icon}
          </div>
          <div>
            <h3 className="font-bold text-lg text-gray-900 dark:text-white">
              {modelInfo.name}
            </h3>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              by {modelInfo.provider}
            </p>
          </div>
        </div>
        <div className="text-right">
          <div className="inline-flex items-center gap-1 px-3 py-1 bg-blue-50 dark:bg-blue-900/30 rounded-full">
            <span className="text-lg">🏅</span>
            <span className="text-sm font-bold text-blue-600 dark:text-blue-400">
              #{response.ranking}
            </span>
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
            {formatTime(response.response_time)}
          </p>
        </div>
      </div>

      {/* Response Text */}
      <div className="mb-4">
        <div
          className={`
            text-sm text-gray-700 dark:text-gray-300 leading-relaxed
            ${!isExpanded ? 'line-clamp-4' : ''}
          `}
        >
          {response.response_text}
        </div>
        {response.response_text.length > 200 && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-xs text-blue-600 dark:text-blue-400 hover:underline mt-2"
          >
            {isExpanded ? 'Show less ▲' : 'Show more ▼'}
          </button>
        )}
      </div>

      {/* Scores Grid */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <ScoreCard
          label="Accuracy"
          score={scores.accuracy}
          icon="🎯"
          delay={index * 0.1 + 0.2}
        />
        <ScoreCard
          label="Relevance"
          score={scores.relevance}
          icon="🔍"
          delay={index * 0.1 + 0.3}
        />
        <ScoreCard
          label="Clarity"
          score={scores.clarity}
          icon="💡"
          delay={index * 0.1 + 0.4}
        />
        <ScoreCard
          label="Trust Score"
          score={scores.trust_score}
          icon="✓"
          delay={index * 0.1 + 0.5}
        />
      </div>

      {/* Risk Indicator */}
      <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
        <div className="flex items-center gap-2">
          <span className="text-lg">
            {scores.hallucination_risk < 30 ? '🟢' : scores.hallucination_risk < 60 ? '🟡' : '🔴'}
          </span>
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Hallucination Risk
          </span>
        </div>
        <span className="text-lg font-bold text-gray-900 dark:text-white">
          {Math.round(scores.hallucination_risk)}%
        </span>
      </div>

      {/* Metadata */}
      <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400">
          <span>📝 {response.token_count} tokens</span>
          <span>💰 {formatCost(response.cost)}</span>
        </div>
        <button
          className="text-xs text-blue-600 dark:text-blue-400 hover:underline"
          onClick={() => {
            navigator.clipboard.writeText(response.response_text);
          }}
        >
          Copy response
        </button>
      </div>
    </motion.div>
  );
}
