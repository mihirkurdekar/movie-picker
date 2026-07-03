import React, { useState } from 'react';
import CategorySelector from './components/CategorySelector';
import DifficultySelector from './components/DifficultySelector';
import GetMovieButton from './components/GetMovieButton';
import ResetButton from './components/ResetButton';
import MovieCard from './components/MovieCard';

// Top‑level application component
function App() {
  // UI selections
  const [selectedCategories, setSelectedCategories] = useState(['bollywood']);
  const [difficulty, setDifficulty] = useState('easy');

  // Session state – movies already shown this session (max 40, oldest dropped)
  const [shownMovies, setShownMovies] = useState([]);
  const [currentMovie, setCurrentMovie] = useState(null);
  const [revealed, setRevealed] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const addMovie = (movie) => {
    const updated = [...shownMovies, movie];
    // Keep only the latest 40 movies
    if (updated.length > 40) updated.shift();
    setShownMovies(updated);
  };

  const handleGetMovie = async () => {
    setLoading(true);
    setError(null);
    setRevealed(false);

    const categories = selectedCategories.length ? selectedCategories : ['random'];
    const apiUrl = import.meta.env.VITE_API_URL || '';

    try {
      const res = await fetch(`${apiUrl}/movie`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category: categories[0],
          difficulty,
          exclude: shownMovies,
        }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || 'Request failed');
      }
      const data = await res.json();
      addMovie(data.movie);
      setCurrentMovie(data.movie);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setShownMovies([]);
    setCurrentMovie(null);
    setRevealed(false);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(168,85,247,0.35),_transparent_30%),linear-gradient(135deg,_#020617_0%,_#111827_45%,_#4c1d95_100%)] px-4 py-8 text-slate-100">
      <div className="mx-auto flex max-w-3xl flex-col gap-6 rounded-[2rem] border border-white/10 bg-slate-950/60 p-6 shadow-[0_25px_80px_rgba(0,0,0,0.45)] backdrop-blur-xl">
        <div className="space-y-4 rounded-2xl border border-fuchsia-400/20 bg-gradient-to-r from-fuchsia-500/10 via-purple-500/10 to-cyan-500/10 p-5">
          <p className="text-sm font-semibold uppercase tracking-[0.35em] text-fuchsia-300">
            Dumb Charades
          </p>
          <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Pick a movie title for your next round
          </h1>
          <p className="max-w-2xl text-sm text-slate-300 sm:text-base">
            Choose a category and difficulty, then generate a fresh title that won’t repeat in the current session.
          </p>
        </div>

        <div className="grid gap-4 rounded-2xl border border-white/10 bg-slate-900/70 p-4 shadow-inner shadow-black/20 sm:grid-cols-[1.4fr_0.8fr]">
          <CategorySelector
            value={selectedCategories}
            onChange={setSelectedCategories}
          />
          <DifficultySelector value={difficulty} onChange={setDifficulty} />
        </div>

        <div className="flex flex-col gap-3 sm:flex-row">
          <GetMovieButton
            onClick={handleGetMovie}
            disabled={loading}
            loading={loading}
          />
          <ResetButton onClick={handleReset} disabled={loading} />
        </div>

        {error && (
          <div className="rounded-2xl border border-red-400/40 bg-red-500/10 p-3 text-sm text-red-200 shadow-sm shadow-red-500/10">
            {error}
          </div>
        )}

        {currentMovie && (
          <MovieCard
            title={currentMovie}
            revealed={revealed}
            onReveal={() => setRevealed(true)}
          />
        )}

        <div className="rounded-2xl border border-cyan-400/20 bg-slate-950/70 p-4 text-sm text-slate-400 shadow-lg shadow-cyan-950/30">
          <p className="font-medium text-cyan-300">Session progress</p>
          <p>
            {shownMovies.length} movie{shownMovies.length === 1 ? '' : 's'} already shown
          </p>
          <p className="mt-1 text-slate-400">
            Active pools: {selectedCategories.length ? selectedCategories.join(', ') : 'random'}
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
