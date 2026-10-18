import React from 'react';
import { motion } from 'framer-motion';

const DIFFICULTIES = [
  { value: 'easy', label: 'Easy', desc: 'Well known' },
  { value: 'hard', label: 'Hard', desc: 'Lesser known' },
];

function DifficultySelector({ value, onChange }) {
  return (
    <div className="relative p-1 rounded-2xl bg-white/5 border border-white/10 flex gap-1">
      {DIFFICULTIES.map((d) => {
        const isActive = value === d.value;
        return (
          <button
            key={d.value}
            onClick={() => onChange(d.value)}
            className="relative z-10 flex-1 flex flex-col items-center justify-center py-2 px-3 transition-colors duration-300"
          >
            <span className={`text-xs font-bold ${isActive ? 'text-white' : 'text-slate-500'}`}>
              {d.label}
            </span>
            <span className={`text-[10px] ${isActive ? 'text-white/60' : 'text-slate-600'}`}>
              {d.desc}
            </span>
            
            {isActive && (
              <motion.div 
                layoutId="difficulty-pill"
                className="absolute inset-0 z-[-1] bg-gradient-to-r from-fuchsia-600 to-purple-600 rounded-xl shadow-lg shadow-purple-500/30"
                transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
              />
            )}
          </button>
        );
      })}
    </div>
  );
}

export default DifficultySelector;
