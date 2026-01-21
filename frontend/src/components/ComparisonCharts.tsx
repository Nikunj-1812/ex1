/**
 * Comparison Charts Component
 * Visual charts comparing AI model performance
 */

'use client';

import { motion } from 'framer-motion';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from 'recharts';
import { AIResponseData } from '@/types';
import { AI_MODELS } from '@/lib/utils';

interface ComparisonChartsProps {
  responses: AIResponseData[];
}

export default function ComparisonCharts({ responses }: ComparisonChartsProps) {
  // Prepare data for bar chart
  const barData = responses.map((r) => ({
    name: AI_MODELS[r.model].name,
    'Trust Score': Math.round(r.evaluation_scores.trust_score),
    'Accuracy': Math.round(r.evaluation_scores.accuracy),
    'Relevance': Math.round(r.evaluation_scores.relevance),
  }));

  // Prepare data for radar chart
  const radarData = [
    {
      metric: 'Accuracy',
      ...Object.fromEntries(
        responses.map((r) => [
          AI_MODELS[r.model].name,
          Math.round(r.evaluation_scores.accuracy),
        ])
      ),
    },
    {
      metric: 'Relevance',
      ...Object.fromEntries(
        responses.map((r) => [
          AI_MODELS[r.model].name,
          Math.round(r.evaluation_scores.relevance),
        ])
      ),
    },
    {
      metric: 'Clarity',
      ...Object.fromEntries(
        responses.map((r) => [
          AI_MODELS[r.model].name,
          Math.round(r.evaluation_scores.clarity),
        ])
      ),
    },
    {
      metric: 'Trust',
      ...Object.fromEntries(
        responses.map((r) => [
          AI_MODELS[r.model].name,
          Math.round(r.evaluation_scores.trust_score),
        ])
      ),
    },
  ];

  const colors = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#ef4444', '#06b6d4'];

  return (
    <div className="space-y-6">
      {/* Bar Chart */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700"
      >
        <div className="mb-4">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <span className="text-2xl">📊</span>
            Performance Comparison
          </h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Compare trust score, accuracy, and relevance across models
          </p>
        </div>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={barData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.1} />
            <XAxis
              dataKey="name"
              tick={{ fill: '#6b7280', fontSize: 12 }}
              angle={-15}
              textAnchor="end"
              height={80}
            />
            <YAxis tick={{ fill: '#6b7280', fontSize: 12 }} />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(17, 24, 39, 0.9)',
                border: 'none',
                borderRadius: '8px',
                color: '#fff',
              }}
            />
            <Legend wrapperStyle={{ fontSize: '12px' }} />
            <Bar dataKey="Trust Score" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            <Bar dataKey="Accuracy" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
            <Bar dataKey="Relevance" fill="#ec4899" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Radar Chart */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700"
      >
        <div className="mb-4">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <span className="text-2xl">🎯</span>
            Multi-Dimensional Analysis
          </h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Comprehensive evaluation across all metrics
          </p>
        </div>
        <ResponsiveContainer width="100%" height={400}>
          <RadarChart data={radarData}>
            <PolarGrid stroke="#374151" opacity={0.2} />
            <PolarAngleAxis
              dataKey="metric"
              tick={{ fill: '#6b7280', fontSize: 12 }}
            />
            <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: '#6b7280', fontSize: 10 }} />
            {responses.map((r, idx) => (
              <Radar
                key={r.model}
                name={AI_MODELS[r.model].name}
                dataKey={AI_MODELS[r.model].name}
                stroke={colors[idx]}
                fill={colors[idx]}
                fillOpacity={0.3}
                strokeWidth={2}
              />
            ))}
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(17, 24, 39, 0.9)',
                border: 'none',
                borderRadius: '8px',
                color: '#fff',
              }}
            />
            <Legend wrapperStyle={{ fontSize: '12px' }} />
          </RadarChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Speed Comparison */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700"
      >
        <div className="mb-4">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <span className="text-2xl">⚡</span>
            Response Time & Cost
          </h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Efficiency metrics for each model
          </p>
        </div>
        <div className="space-y-3">
          {responses
            .sort((a, b) => a.response_time - b.response_time)
            .map((r, idx) => {
              const maxTime = Math.max(...responses.map((r) => r.response_time));
              const percentage = (r.response_time / maxTime) * 100;
              const modelInfo = AI_MODELS[r.model];

              return (
                <div key={r.model} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{modelInfo.icon}</span>
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        {modelInfo.name}
                      </span>
                    </div>
                    <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400">
                      <span>⏱️ {r.response_time.toFixed(2)}s</span>
                      <span>💰 ${r.cost.toFixed(4)}</span>
                    </div>
                  </div>
                  <div className="relative h-6 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${percentage}%` }}
                      transition={{ delay: idx * 0.1, duration: 0.8 }}
                      className={`h-full bg-gradient-to-r ${modelInfo.color} flex items-center justify-end pr-2`}
                    >
                      {idx === 0 && (
                        <span className="text-xs font-bold text-white">Fastest</span>
                      )}
                    </motion.div>
                  </div>
                </div>
              );
            })}
        </div>
      </motion.div>
    </div>
  );
}
