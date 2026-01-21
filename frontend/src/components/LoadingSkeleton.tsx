/**
 * Loading Skeleton Component
 * Displays during AI response loading
 */

'use client';

import { motion } from 'framer-motion';
import { LoadingState } from '@/types';

interface LoadingSkeletonProps {
  state: LoadingState;
}

export default function LoadingSkeleton({ state }: LoadingSkeletonProps) {
  return (
    <div className="space-y-6">
      {/* Loading header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-3"
      >
        <motion.div
          animate={{
            rotate: 360,
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: 'linear',
          }}
          className="inline-block text-6xl"
        >
          🤖
        </motion.div>
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
          {state.message}
        </h3>
        {state.progress !== undefined && (
          <div className="max-w-md mx-auto">
            <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${state.progress}%` }}
                transition={{ duration: 0.5 }}
                className="h-full bg-gradient-to-r from-blue-500 to-purple-600"
              />
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
              {state.progress}% complete
            </p>
          </div>
        )}
      </motion.div>

      {/* Skeleton cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {[1, 2, 3, 4].map((i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.1 }}
            className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700"
          >
            {/* Header skeleton */}
            <div className="flex items-center gap-3 mb-4">
              <div className="skeleton w-12 h-12 rounded-lg" />
              <div className="flex-1 space-y-2">
                <div className="skeleton h-4 w-32 rounded" />
                <div className="skeleton h-3 w-24 rounded" />
              </div>
            </div>

            {/* Content skeleton */}
            <div className="space-y-2 mb-4">
              <div className="skeleton h-3 w-full rounded" />
              <div className="skeleton h-3 w-full rounded" />
              <div className="skeleton h-3 w-3/4 rounded" />
            </div>

            {/* Score skeleton */}
            <div className="grid grid-cols-2 gap-2">
              <div className="skeleton h-16 rounded-lg" />
              <div className="skeleton h-16 rounded-lg" />
            </div>
          </motion.div>
        ))}
      </div>

      {/* Loading tips */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        className="max-w-2xl mx-auto p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800"
      >
        <p className="text-sm text-blue-700 dark:text-blue-300 text-center">
          ⚡ Querying multiple AI models simultaneously for comprehensive analysis...
        </p>
      </motion.div>
    </div>
  );
}
