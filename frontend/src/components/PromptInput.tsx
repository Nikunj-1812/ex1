/**
 * Prompt Input Component
 * Large textarea for entering prompts
 */

'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';

interface PromptInputProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

const EXAMPLE_PROMPTS = [
  'Explain quantum computing in simple terms',
  'Write a Python function to calculate fibonacci numbers',
  'What are the main symptoms of diabetes?',
  'Create a business plan for a coffee shop',
];

export default function PromptInput({ value, onChange, disabled }: PromptInputProps) {
  const [isFocused, setIsFocused] = useState(false);
  const charCount = value.length;
  const maxChars = 5000;

  const insertExample = (example: string) => {
    onChange(example);
  };

  return (
    <div className="space-y-3">
      {/* Label */}
      <div className="flex items-center justify-between">
        <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
          Enter Your Prompt
        </label>
        <span
          className={`text-xs ${
            charCount > maxChars * 0.9
              ? 'text-red-600 dark:text-red-400 font-medium'
              : 'text-gray-500 dark:text-gray-400'
          }`}
        >
          {charCount} / {maxChars}
        </span>
      </div>

      {/* Textarea */}
      <motion.div
        animate={{
          boxShadow: isFocused
            ? '0 0 0 3px rgba(59, 130, 246, 0.1)'
            : '0 0 0 0px rgba(59, 130, 246, 0)',
        }}
        className="relative rounded-lg"
      >
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          disabled={disabled}
          placeholder="Ask anything... Try questions about science, coding, business, health, or creative tasks."
          maxLength={maxChars}
          className={`
            w-full min-h-[200px] p-4 rounded-lg resize-none
            bg-white dark:bg-gray-800
            border-2 border-gray-200 dark:border-gray-700
            focus:border-blue-500 dark:focus:border-blue-400
            text-gray-900 dark:text-gray-100
            placeholder:text-gray-400 dark:placeholder:text-gray-500
            transition-colors duration-200
            disabled:opacity-50 disabled:cursor-not-allowed
            font-mono text-sm leading-relaxed
          `}
        />

        {/* Character warning */}
        {charCount > maxChars * 0.9 && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="absolute bottom-2 right-2 px-2 py-1 bg-red-100 dark:bg-red-900 rounded text-xs text-red-600 dark:text-red-400"
          >
            Approaching character limit
          </motion.div>
        )}
      </motion.div>

      {/* Example prompts */}
      {!value && !disabled && (
        <div className="space-y-2">
          <p className="text-xs text-gray-500 dark:text-gray-400">Try an example:</p>
          <div className="flex flex-wrap gap-2">
            {EXAMPLE_PROMPTS.map((example, idx) => (
              <button
                key={idx}
                onClick={() => insertExample(example)}
                className="text-xs px-3 py-1.5 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-blue-900/30 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Tips */}
      {isFocused && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="flex items-start gap-2 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800"
        >
          <span className="text-blue-600 dark:text-blue-400 text-lg">💡</span>
          <div className="text-xs text-blue-700 dark:text-blue-300">
            <p className="font-medium mb-1">Tips for better results:</p>
            <ul className="space-y-0.5 list-disc list-inside">
              <li>Be specific and clear about what you want</li>
              <li>Provide context when needed</li>
              <li>Ask one question at a time for best comparison</li>
            </ul>
          </div>
        </motion.div>
      )}
    </div>
  );
}
