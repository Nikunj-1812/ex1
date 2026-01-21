/**
 * Navigation Bar Component
 * Top navigation with logo, theme toggle, and actions
 */

'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

interface NavBarProps {
  onHistoryClick?: () => void;
}

export default function NavBar({ onHistoryClick }: NavBarProps) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    // Check system preference on mount
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setTheme(isDark ? 'dark' : 'light');
    document.documentElement.classList.toggle('dark', isDark);
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };

  return (
    <nav className="sticky top-0 z-40 w-full border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg">
      <div className="flex h-16 items-center justify-between px-6">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <motion.div
            className="text-3xl"
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
          >
            🤖
          </motion.div>
          <div>
            <h1 className="text-xl font-bold gradient-text">MAI-PAEP</h1>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Multi-AI Prompt Intelligence
            </p>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-4">
          {/* History Button */}
          {onHistoryClick && (
            <button
              onClick={onHistoryClick}
              className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            >
              <span className="text-lg">📚</span>
              History
            </button>
          )}

          {/* Theme Toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            aria-label="Toggle theme"
          >
            <motion.span
              className="block text-2xl"
              key={theme}
              initial={{ rotate: 180, scale: 0 }}
              animate={{ rotate: 0, scale: 1 }}
              transition={{ type: 'spring', stiffness: 200, damping: 10 }}
            >
              {theme === 'light' ? '🌙' : '☀️'}
            </motion.span>
          </button>

          {/* Settings */}
          <button
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            aria-label="Settings"
          >
            <span className="block text-2xl">⚙️</span>
          </button>
        </div>
      </div>
    </nav>
  );
}
