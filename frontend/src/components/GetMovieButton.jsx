import React from 'react';

function GetMovieButton({ onClick, disabled, loading }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      className="flex-1 rounded-2xl bg-gradient-to-r from-fuchsia-600 via-purple-600 to-cyan-500 px-4 py-3 font-semibold text-white shadow-lg shadow-fuchsia-600/20 transition duration-200 hover:scale-[1.01] hover:shadow-fuchsia-500/30 disabled:cursor-not-allowed disabled:opacity-60"
    >
      {loading ? 'Generating…' : 'Get Movie'}
    </button>
  );
}

export default GetMovieButton;
