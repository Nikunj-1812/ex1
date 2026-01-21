/**
 * AI Model Selection Card Component
 * Visual card for selecting AI models
 */

'use client';

import { motion } from 'framer-motion';
import { AIModel, AIModelInfo } from '@/types';
import { AI_MODELS } from '@/lib/utils';

interface ModelCardProps {
  model: AIModel;
  selected: boolean;
  onToggle: (model: AIModel) => void;
}

export default function ModelCard({ model, selected, onToggle }: ModelCardProps) {
  const modelInfo: AIModelInfo = AI_MODELS[model];

  return (
    <motion.button
      onClick={() => onToggle(model)}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={`
        relative overflow-hidden rounded-xl p-4 text-left transition-all duration-300
        ${
          selected
            ? 'bg-gradient-to-br ' + modelInfo.color + ' text-white shadow-lg ring-2 ring-offset-2 ring-blue-500 dark:ring-offset-gray-900'
            : 'bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
        }
      `}
    >
      {/* Selection indicator */}
      {selected && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="absolute top-2 right-2 w-6 h-6 bg-white rounded-full flex items-center justify-center shadow-lg"
        >
          <span className="text-green-600 font-bold text-sm">✓</span>
        </motion.div>
      )}

      {/* Icon */}
      <div className="text-4xl mb-3">{modelInfo.icon}</div>

      {/* Model name */}
      <h3 className={`font-bold text-lg mb-1 ${selected ? 'text-white' : 'text-gray-900 dark:text-white'}`}>
        {modelInfo.name}
      </h3>

      {/* Provider */}
      <p className={`text-xs mb-2 ${selected ? 'text-white/80' : 'text-gray-500 dark:text-gray-400'}`}>
        by {modelInfo.provider}
      </p>

      {/* Description */}
      <p className={`text-sm mb-3 ${selected ? 'text-white/90' : 'text-gray-600 dark:text-gray-300'}`}>
        {modelInfo.description}
      </p>

      {/* Strengths */}
      <div className="flex flex-wrap gap-1">
        {modelInfo.strengths.slice(0, 2).map((strength, idx) => (
          <span
            key={idx}
            className={`
              text-xs px-2 py-1 rounded-full
              ${
                selected
                  ? 'bg-white/20 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
              }
            `}
          >
            {strength}
          </span>
        ))}
      </div>

      {/* Shimmer effect when selected */}
      {selected && (
        <div className="absolute inset-0 shimmer opacity-30 pointer-events-none" />
      )}
    </motion.button>
  );
}
