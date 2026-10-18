import React from 'react';
import { motion } from 'framer-motion';

const CATEGORIES = [
  { value: 'bollywood', label: 'Bollywood', accent: 'bg-rose-500 shadow-rose-500/30' },
  { value: 'hollywood', label: 'Hollywood', accent: 'bg-sky-500 shadow-sky-500/30' },
  { value: 'tollywood', label: 'Tollywood', accent: 'bg-emerald-500 shadow-emerald-500/30' },
  { value: 'kollywood', label: 'Kollywood', accent: 'bg-amber-500 shadow-amber-500/30' },
  { value: 'punjabi', label: 'Punjabi', accent: 'bg-fuchsia-500 shadow-fuchsia-500/30' },
  { value: 'mixed_indian', label: 'Mixed-Indian', accent: 'bg-indigo-500 shadow-indigo-500/30' },
  { value: 'random', label: 'Random', accent: 'bg-slate-500 shadow-slate-500/30' },
];

function CategorySelector({ value, onChange }) {
  const toggleCategory = (category) => {
    const selected = value.includes(category)
      ? value.filter((item) => item !== category)
      : [...value, category];
    onChange(selected);
  };

  return (
    <div className="flex flex-wrap gap-3 justify-center lg:justify-start">
      {CATEGORIES.map((category) => {
        const isSelected = value.includes(category.value);
        return (
          <motion.button
            key={category.value}
            whileHover={{ scale: 1.02, y: -1 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => toggleCategory(category.value)}
            className={`relative px-5 py-2.5 rounded-2xl text-xs font-bold uppercase tracking-wider transition-all duration-300 ${
              isSelected
                ? `${category.accent} text-white shadow-md scale-105 ring-1 ring-white/30`
                : 'bg-white/5 text-slate-400 border border-white/10 hover:bg-white/10 hover:text-slate-200'
            }`}
          >
            <span className="relative z-10">{category.label}</span>
            
            {isSelected && (
              <div 
                className="absolute inset-0 rounded-2xl blur-md opacity-30" 
                style={{ backgroundColor: 'currentColor' }}
              />
            )}
          </motion.button>
        );
      })}
    </div>
  );
}

export default CategorySelector;
