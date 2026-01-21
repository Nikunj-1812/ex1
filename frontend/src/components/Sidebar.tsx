/**
 * Sidebar Component
 * Left navigation with sections: AI Models, History, Analytics
 */

'use client';

import Link from 'next/link';
import { AIModel } from '@/types';
import { AI_MODELS } from '@/lib/utils';

interface SidebarProps {
  selectedModels: AIModel[];
  onToggleModel: (model: AIModel) => void;
}

export default function Sidebar({ selectedModels, onToggleModel }: SidebarProps) {
  const sections = [
    { title: 'AI Models', icon: '🤖' },
    { title: 'History', icon: '📚', href: '/history' },
    { title: 'Analytics', icon: '📈', href: '/analytics' },
  ];

  return (
    <aside className="hidden lg:block w-64 flex-shrink-0">
      <div className="sticky top-20 space-y-4">
        {/* Sections */}
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
          <h2 className="text-sm font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
            <span className="text-lg">{sections[0].icon}</span>
            {sections[0].title}
          </h2>
          <div className="space-y-2">
            {Object.values(AIModel).map((model) => {
              const info = AI_MODELS[model as AIModel];
              const selected = selectedModels.includes(model as AIModel);
              return (
                <button
                  key={model}
                  onClick={() => onToggleModel(model as AIModel)}
                  className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors border-2 ${
                    selected
                      ? 'bg-gradient-to-r ' + info.color + ' text-white border-transparent'
                      : 'bg-gray-50 dark:bg-gray-900 text-gray-700 dark:text-gray-300 border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800'
                  }`}
                >
                  <span className="text-lg">{info.icon}</span>
                  <span className="flex-1 text-left">{info.name}</span>
                  {selected && <span className="text-xs px-2 py-0.5 rounded-full bg-white/20">Selected</span>}
                </button>
              );
            })}
          </div>
          <div className="mt-3 text-xs text-gray-600 dark:text-gray-400">
            Selected: <span className="font-bold">{selectedModels.length}</span>/
            {Object.values(AIModel).length}
          </div>
        </div>

        {/* Links */}
        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700 space-y-2">
          {sections.slice(1).map((s) => (
            <Link key={s.title} href={s.href!} className="block">
              <div className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                <span className="text-lg">{s.icon}</span>
                <span className="text-sm text-gray-800 dark:text-gray-200">{s.title}</span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </aside>
  );
}
