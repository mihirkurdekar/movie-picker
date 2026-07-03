import React from 'react';

function MovieCard({ title, revealed, onReveal }) {
  return (
    <div className="mx-auto w-full max-w-xl rounded-3xl border border-fuchsia-400/20 bg-gradient-to-br from-slate-900/90 to-purple-950/90 p-6 text-center shadow-[0_20px_60px_rgba(168,85,247,0.18)]">
      <p className="mb-3 text-sm font-semibold uppercase tracking-[0.3em] text-fuchsia-300">
        Current pick
      </p>
      <h2 className={`mb-5 text-3xl font-bold text-white sm:text-4xl transition-all duration-300 ${revealed ? 'scale-100' : 'scale-95 opacity-80'}`}>
        {revealed ? title : '???'}
      </h2>
      <button
        onClick={onReveal}
        className={`rounded-full border px-4 py-2 text-sm font-semibold transition duration-200 ${revealed ? 'border-emerald-400/30 bg-emerald-500/15 text-emerald-100 shadow-lg shadow-emerald-500/10' : 'border-cyan-400/20 bg-cyan-500/10 text-cyan-100 hover:bg-cyan-500/20'}`}
      >
        {revealed ? 'Title revealed' : 'Reveal Title'}
      </button>
    </div>
  );
}
export default MovieCard;