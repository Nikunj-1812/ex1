/**
 * Main Application Page
 * MAI-PAEP - Multi-AI Prompt Intelligence & Accuracy Evaluation Platform
 */

'use client';

import { useState } from 'react';
import { AIModel, PromptSubmitResponse, ToastMessage, LoadingState } from '@/types';
import { apiClient } from '@/lib/api';
import { generateId } from '@/lib/utils';
import NavBar from '@/components/NavBar';
import PromptInput from '@/components/PromptInput';
import ModelCard from '@/components/ModelCard';
import LoadingSkeleton from '@/components/LoadingSkeleton';
import ResultsDashboard from '@/components/ResultsDashboard';
import { ToastContainer } from '@/components/Toast';
import { motion } from 'framer-motion';
import Sidebar from '@/components/Sidebar';
import { useAppStore } from '@/lib/store';

export default function Home() {
  const promptText = useAppStore((s) => s.promptText);
  const setPromptText = useAppStore((s) => s.setPrompt);
  const selectedModels = useAppStore((s) => s.selectedModels);
  const toggleModel = useAppStore((s) => s.toggleModel);
  const setModels = useAppStore((s) => s.setModels);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingState, setLoadingState] = useState<LoadingState>({
    isLoading: false,
    message: 'Initializing...',
  });
  const results = useAppStore((s) => s.results);
  const setResults = useAppStore((s) => s.setResults);
  const toasts = useAppStore((s) => s.toasts);
  const addToast = useAppStore((s) => s.addToast);
  const removeToast = useAppStore((s) => s.removeToast);

  // Visible models per user preference (hide Opus and Mistral for now)
  const availableModels = [
    AIModel.GPT_4,
    AIModel.GPT_35_TURBO,
    AIModel.CLAUDE_3_SONNET,
    AIModel.GEMINI_PRO,
    AIModel.LLAMA_3_70B,
  ];

  

  const handleSubmit = async () => {
    // Validation
    if (!promptText.trim()) {
      addToast('error', 'Please enter a prompt');
      return;
    }

    if (selectedModels.length === 0) {
      addToast('error', 'Please select at least one AI model');
      return;
    }

    if (selectedModels.length < 2) {
      addToast('warning', 'Select at least 2 models for meaningful comparison');
      return;
    }

    // Start loading
    setIsLoading(true);
    setResults(null);
    setLoadingState({
      isLoading: true,
      message: 'Querying AI models...',
      progress: 10,
    });

    try {
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setLoadingState((prev) => ({
          ...prev,
          progress: Math.min((prev.progress || 10) + 15, 90),
        }));
      }, 1000);

      // Submit prompt
      const response = await apiClient.submitPrompt({
        prompt_text: promptText,
        selected_models: selectedModels,
      });

      clearInterval(progressInterval);

      setLoadingState({
        isLoading: true,
        message: 'Analysis complete!',
        progress: 100,
      });

      // Show results after brief delay
      setTimeout(() => {
        setResults(response);
        setIsLoading(false);
        addToast('success', `Successfully compared ${response.ai_responses.length} AI models!`);
      }, 500);
    } catch (error) {
      setIsLoading(false);
      const errorMessage = error instanceof Error ? error.message : 'Failed to process request';
      addToast('error', errorMessage);
      console.error('Submission error:', error);
    }
  };

  const handleNewPrompt = () => {
    setResults(null);
    setPromptText('');
    // Keep selected models for convenience
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-cyan-50 dark:from-gray-900 dark:via-blue-950 dark:to-slate-950">
      <NavBar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex gap-6">
        <Sidebar selectedModels={selectedModels} onToggleModel={toggleModel} />
        <div className="flex-1">
        {!isLoading && !results && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-8"
          >
            {/* Hero Section */}
            <div className="text-center space-y-4 py-8">
              <motion.h1
                initial={{ y: -20 }}
                animate={{ y: 0 }}
                className="text-4xl md:text-5xl font-bold gradient-text"
              >
                Compare AI models. Find the best response. Make smarter decisions.
              </motion.h1>
              <motion.p
                initial={{ y: -10 }}
                animate={{ y: 0 }}
                transition={{ delay: 0.1 }}
                className="text-lg text-gray-600 dark:text-gray-400 max-w-3xl mx-auto"
              >
                Compare responses from multiple AI models simultaneously. Get detailed accuracy,
                relevance, and trust scores powered by advanced ML evaluation.
              </motion.p>
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2, type: 'spring' }}
                className="flex items-center justify-center gap-4 text-sm text-gray-600 dark:text-gray-400"
              >
                <span className="flex items-center gap-1">
                  <span className="text-lg">🤖</span>
                  7 AI Models
                </span>
                <span>•</span>
                <span className="flex items-center gap-1">
                  <span className="text-lg">🎯</span>
                  Real-time Analysis
                </span>
                <span>•</span>
                <span className="flex items-center gap-1">
                  <span className="text-lg">📊</span>
                  ML-Powered Scoring
                </span>
              </motion.div>
            </div>

            {/* Prompt Input Section */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700"
            >
              <PromptInput
                value={promptText}
                onChange={setPromptText}
                disabled={isLoading}
              />
            </motion.div>

            {/* Model Selection Section */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="space-y-4"
            >
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  Select AI Models to Compare
                </h2>
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  {selectedModels.length} of {availableModels.length} selected
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {availableModels.map((model) => (
                  <ModelCard
                    key={model}
                    model={model}
                    selected={selectedModels.includes(model)}
                    onToggle={toggleModel}
                  />
                ))}
              </div>

              {/* Quick select buttons */}
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-sm text-gray-600 dark:text-gray-400">Quick select:</span>
                <button
                  onClick={() => setModels(availableModels)}
                  className="text-sm px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/50 transition-colors"
                >
                  All models
                </button>
                <button
                  onClick={() => setModels([AIModel.GPT_4, AIModel.CLAUDE_3_OPUS, AIModel.GEMINI_PRO])}
                  className="text-sm px-3 py-1 rounded-full bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-400 hover:bg-green-100 dark:hover:bg-green-900/50 transition-colors"
                >
                  Top 3 models
                </button>
                <button
                  onClick={() => setModels([])}
                  className="text-sm px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                >
                  Clear all
                </button>
              </div>
            </motion.div>

            {/* Submit Button */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="flex justify-center"
            >
              <motion.button
                onClick={handleSubmit}
                disabled={isLoading}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={`
                  px-8 py-4 rounded-xl font-bold text-lg shadow-xl
                  ${
                    isLoading
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 pulse-glow'
                  }
                  text-white transition-all duration-300
                  flex items-center gap-3
                `}
              >
                <span className="text-2xl">🚀</span>
                {isLoading ? 'Processing...' : 'Compare AI Models'}
              </motion.button>
            </motion.div>

            {/* Info cards */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8"
            >
              <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
                <div className="text-3xl mb-2">🎯</div>
                <h3 className="font-bold text-gray-900 dark:text-white mb-1">
                  Accuracy Analysis
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  ML-powered semantic analysis measures response accuracy and relevance
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
                <div className="text-3xl mb-2">🛡️</div>
                <h3 className="font-bold text-gray-900 dark:text-white mb-1">
                  Hallucination Detection
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Advanced algorithms detect unsourced claims and contradictions
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
                <div className="text-3xl mb-2">📊</div>
                <h3 className="font-bold text-gray-900 dark:text-white mb-1">
                  Visual Comparison
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Interactive charts show performance metrics across all models
                </p>
              </div>
            </motion.div>
          </motion.div>
        )}

        {/* Loading State */}
        {isLoading && !results && <LoadingSkeleton state={loadingState} />}

        {/* Results */}
        {results && <ResultsDashboard results={results} onNewPrompt={handleNewPrompt} />}
        </div>
      </main>

      {/* Toast Notifications */}
      <ToastContainer toasts={toasts} onClose={removeToast} />
    </div>
  );
}
