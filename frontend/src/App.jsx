import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, History, Settings2, Trophy, X, Play } from 'lucide-react';
import CategorySelector from './components/CategorySelector';
import DifficultySelector from './components/DifficultySelector';
import GetMovieButton from './components/GetMovieButton';
import ResetButton from './components/ResetButton';
import MovieCard from './components/MovieCard';

const THEMES = {
  bollywood: { primary: '#e11d48', secondary: '#fb7185', glow: 'rgba(225, 29, 72, 0.3)' },
  hollywood: { primary: '#0ea5e9', secondary: '#38bdf8', glow: 'rgba(14, 165, 233, 0.3)' },
  tollywood: { primary: '#10b981', secondary: '#34d399', glow: 'rgba(16, 185, 129, 0.3)' },
  kollywood: { primary: '#f59e0b', secondary: '#fbbf24', glow: 'rgba(245, 158, 11, 0.3)' },
  punjabi: { primary: '#d946ef', secondary: '#f0abfc', glow: 'rgba(217, 70, 239, 0.3)' },
  mixed_indian: { primary: '#6366f1', secondary: '#818cf8', glow: 'rgba(99, 102, 241, 0.3)' },
  random: { primary: '#64748b', secondary: '#94a3b8', glow: 'rgba(100, 116, 139, 0.3)' },
};

function App() {
  // DEFAULT CATEGORIES: Now selecting a broader range by default
  const [selectedCategories, setSelectedCategories] = useState(['bollywood', 'hollywood', 'random']);
  const [difficulty, setDifficulty] = useState('easy');
  const [shownMovies, setShownMovies] = useState([]);
  const [currentMovie, setCurrentMovie] = useState(null);
  const [revealed, setRevealed] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [gameMode, setGameMode] = useState('setup');

  useEffect(() => {
    const cat = selectedCategories[0] || 'random';
    const theme = THEMES[cat] || THEMES.random;
    document.documentElement.style.setProperty('--theme-primary', theme.primary);
    document.documentElement.style.setProperty('--theme-secondary', theme.secondary);
    document.documentElement.style.setProperty('--theme-glow', theme.glow);
  }, [selectedCategories]);

  const addMovie = (movie) => {
    if (!movie) return;

    setShownMovies((current) => {
      if (current.includes(movie)) return current;
      const updated = [...current, movie];
      if (updated.length > 40) updated.shift();
      return updated;
    });
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
      setCurrentMovie(data.movie);
      setGameMode('playing');
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
    setGameMode('setup');
  };

  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-[#020617] px-4 py-8 text-slate-100 font-sans">
      <div className="orb w-[500px] h-[500px] rounded-full transition-colors duration-1000" style={{ backgroundColor: 'var(--theme-primary)', top: '-10%', left: '-10%' }} />
      <div className="orb w-[600px] h-[600px] rounded-full transition-colors duration-1000" style={{ backgroundColor: 'var(--theme-secondary)', bottom: '-20%', right: '-10%', animationDelay: '-5s' }} />
      <div className="orb w-[400px] h-[400px] rounded-full transition-colors duration-1000" style={{ backgroundColor: 'var(--theme-primary)', top: '30%', right: '20%', animationDelay: '-12s', opacity: 0.2 }} />

      <div className="relative mx-auto flex max-w-5xl flex-col gap-8">
        
        <motion.header 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col items-center text-center gap-3"
        >
          <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-slate-400 text-xs font-bold uppercase tracking-widest">
            <Sparkles size={14} className="text-fuchsia-400" />
            <span>Dumb Charades Edition</span>
          </div>
          <h1 className="text-6xl font-black tracking-tighter sm:text-7xl bg-gradient-to-b from-white to-slate-500 bg-clip-text text-transparent">
            Movie Picker
          </h1>
        </motion.header>

        <AnimatePresence mode="wait">
          {gameMode === 'setup' ? (
            <motion.div 
              key="setup-mode"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 1.1 }}
              className="flex flex-col items-center gap-8"
            >
              {/* Setup Section: Now centered and more prominent */}
              <div className="w-full max-w-2xl glass-panel p-10 rounded-[3rem] space-y-10 text-center">
                <div className="flex items-center justify-center gap-3 text-slate-300 font-semibold text-2xl">
                  <Settings2 size={28} style={{ color: 'var(--theme-primary)' }} />
                  <h2>Game Setup</h2>
                </div>
                
                <div className="space-y-8">
                  <div className="space-y-4">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider block">Category</label>
                    <CategorySelector 
                      value={selectedCategories} 
                      onChange={setSelectedCategories} 
                      isLoading={loading} 
                    />
                  </div>
                  <div className="space-y-4">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider block text-center">Difficulty</label>
                    <div className="flex justify-center">
                      <div className="w-full max-w-xs">
                        <DifficultySelector value={difficulty} onChange={setDifficulty} />
                      </div>
                    </div>
                  </div>
                </div>

                <div className="pt-6">
                  <GetMovieButton 
                    onClick={handleGetMovie} 
                    disabled={loading} 
                    loading={loading} 
                  />
                </div>
              </div>

              <div className="glass-panel p-6 rounded-[2rem] flex items-center gap-4">
                <div className="p-3 rounded-2xl bg-white/10 text-slate-300">
                  <Trophy size={24} />
                </div>
                <div className="text-left">
                  <p className="text-xs font-bold text-slate-500 uppercase">Session History</p>
                  <p className="text-lg font-bold">{shownMovies.length} Movies Played</p>
                </div>
              </div>
            </motion.div>
          ) : (
            <motion.div 
              key="playing-mode"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="flex flex-col items-center gap-8"
            >
              <div className="relative w-full flex flex-col items-center gap-12">
                <MovieCard
                  title={currentMovie}
                  revealed={revealed}
                  onReveal={() => {
                    setRevealed(true);
                    addMovie(currentMovie);
                  }}
                />

                <div className="flex flex-col sm:flex-row gap-4 items-center">
                  <GetMovieButton 
                    onClick={handleGetMovie} 
                    disabled={loading} 
                    loading={loading} 
                  />
                  <button 
                    onClick={() => setGameMode('setup')}
                    className="flex items-center gap-2 px-6 py-4 rounded-2xl border border-white/10 bg-white/5 text-slate-400 font-semibold hover:bg-white/10 transition-all"
                  >
                    <X size={18} />
                    Change Settings
                  </button>
                </div>
              </div>

              <div className="w-full max-w-2xl glass-panel p-6 rounded-[2rem]">
                <div className="flex items-center gap-2 text-slate-400 font-semibold mb-4 text-sm">
                  <History size={16} />
                  <span>Recently Played</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {shownMovies.slice(-10).reverse().map((movie, idx) => (
                    <span key={idx} className="px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs text-slate-500">
                      {movie}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {error && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="fixed bottom-8 right-8 z-50 rounded-2xl border border-red-400/40 bg-red-500/20 backdrop-blur-md p-4 text-sm text-red-200 flex items-center gap-3 shadow-2xl"
          >
            <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
            {error}
          </motion.div>
        )}
      </div>
    </div>
  );
}

export default App;
