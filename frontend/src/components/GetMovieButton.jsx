import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Loader2 } from 'lucide-react';

function GetMovieButton({ onClick, disabled, loading }) {
  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      disabled={disabled || loading}
      className="relative group flex-1 overflow-hidden rounded-2xl bg-gradient-to-r from-fuchsia-600 via-purple-600 to-cyan-500 px-6 py-4 font-bold text-white shadow-xl shadow-fuchsia-600/30 transition-all hover:shadow-fuchsia-500/50 disabled:cursor-not-allowed disabled:opacity-70"
    >
      <div className="relative z-10 flex items-center justify-center gap-2">
        {loading ? (
          <Loader2 className="animate-spin" size={20} />
        ) : (
          <Sparkles size={20} className="group-hover:rotate-12 transition-transform" />
        )}
        <span className="tracking-tight">
          {loading ? 'Summoning Movie...' : 'Get Movie'}
        </span>
      </div>
      
      {/* Subtle shimmer effect */}
      <motion.div 
        animate={{ x: ['-100%', '200%'] }}
        transition={{ repeat: Infinity, duration: 2, ease: 'linear' }}
        className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -skew-x-12"
      />
    </motion.button>
  );
}

export default GetMovieButton;
