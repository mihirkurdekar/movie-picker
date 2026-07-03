import React from 'react';

// Difficulty options per spec
const DIFFICULTIES = [
  { value: 'easy', label: 'Easy – well known' },
  { value: 'hard', label: 'Hard – lesser known' },
];

function DifficultySelector({ value, onChange }) {
  return (
    <div>
      <label className="mb-2 block text-sm font-semibold text-slate-200">Difficulty</label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full rounded-xl border border-white/10 bg-slate-800/70 px-3 py-3 text-sm text-slate-100 outline-none transition focus:border-purple-400"
      >
        {DIFFICULTIES.map((d) => (
          <option key={d.value} value={d.value} className="bg-slate-800 text-slate-100">
            {d.label}
          </option>
        ))}
      </select>
    </div>
  );
}

export default DifficultySelector;
