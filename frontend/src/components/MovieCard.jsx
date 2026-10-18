import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Eye, CheckCircle2 } from 'lucide-react';

function MovieCard({ title, revealed, onReveal }) {
  return (
    <div className="w-full max-w-xl mx-auto relative">
      {/* Ambient Background Glow */}
      <div className="absolute -inset-4 bg-gradient-to-r from-fuchsia-600 via-purple-600 to-cyan-600 rounded-[3rem] blur-2xl opacity-20 animate-pulse" />
      
      <motion.div 
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="relative overflow-hidden rounded-[3rem] border border-white/20 bg-slate-900/80 backdrop-blur-2xl p-10 text-center shadow-2xl"
      >
        <p className="mb-8 text-xs font-black uppercase tracking-[0.4em] text-fuchsia-400 opacity-80">
          The Chosen Title
        </p>
        
        <div className="relative h-32 flex items-center justify-center mb-12">
          <AnimatePresence mode="wait">
            {!revealed ? (
              <motion.div
                key="hidden"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.2, ease: 'easeOut' }}
                className="text-7xl font-black text-slate-800 italic tracking-tighter"
              >
                ???
              </motion.div>
            ) : (
              <motion.div
                key="revealed"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ type: 'spring', stiffness: 260, damping: 22 }}
                className="text-4xl font-black text-white tracking-tight sm:text-6xl bg-gradient-to-b from-white to-slate-300 bg-clip-text text-transparent"
              >
                {title}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        <div className="flex justify-center">
          {!revealed ? (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onReveal}
              className="flex items-center gap-3 px-8 py-4 rounded-full bg-white text-slate-900 font-bold shadow-xl shadow-white/10 transition-all"
            >
              <Eye size={20} />
              <span className="text-sm">Reveal Title</span>
            </motion.button>
          ) : (
            <motion.div 
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex items-center gap-3 px-8 py-4 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold"
            >
              <CheckCircle2 size={20} />
              <span className="text-sm">Revealed!</span>
            </motion.div>
          )}
        </div>
      </motion.div>
    </div>
  );
}

export default MovieCard;
