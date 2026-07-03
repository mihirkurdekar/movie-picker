import React from 'react';

const CATEGORIES = [
  { value: 'bollywood', label: 'Bollywood', accent: 'from-rose-500 to-pink-500' },
  { value: 'hollywood', label: 'Hollywood', accent: 'from-sky-500 to-cyan-500' },
  { value: 'tollywood', label: 'Tollywood', accent: 'from-emerald-500 to-lime-500' },
  { value: 'kollywood', label: 'Kollywood', accent: 'from-amber-500 to-orange-500' },
  { value: 'punjabi', label: 'Punjabi', accent: 'from-fuchsia-500 to-violet-500' },
  { value: 'mixed_indian', label: 'Mixed-Indian', accent: 'from-indigo-500 to-purple-500' },
  { value: 'random', label: 'Random', accent: 'from-slate-500 to-slate-600' },
];

function CategorySelector({ value, onChange }) {
  const toggleCategory = (category) => {
    const selected = value.includes(category)
      ? value.filter((item) => item !== category)
      : [...value, category];

    onChange(selected);
  };

  return (
    <div>
      <label className="mb-2 block text-sm font-semibold text-slate-200">
        Categories <span className="text-xs font-normal text-slate-400">(pick one or more)</span>
      </label>
      <div className="flex flex-wrap gap-2">
        {CATEGORIES.map((category) => {
          const selected = value.includes(category.value);
          return (
            <button
              key={category.value}
              type="button"
              onClick={() => toggleCategory(category.value)}
              className={`rounded-full border px-3 py-2 text-sm font-medium transition duration-200 ease-out hover:-translate-y-0.5 hover:shadow-lg ${
                selected
                  ? `border-transparent bg-gradient-to-r ${category.accent} text-white shadow-lg shadow-black/20 scale-[1.02]`
                  : 'border-white/10 bg-slate-800/70 text-slate-200 hover:bg-slate-700/80'
              }`}
            >
              {category.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}

export default CategorySelector;
