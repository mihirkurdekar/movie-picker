import React from 'react';

function ResetButton({ onClick, disabled }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="rounded-2xl border border-white/15 bg-slate-800/90 px-4 py-3 font-semibold text-slate-100 transition duration-200 hover:bg-slate-700 hover:shadow-md hover:shadow-slate-900/40 disabled:cursor-not-allowed disabled:opacity-60"
    >
      Reset
    </button>
  );
}

export default ResetButton;
