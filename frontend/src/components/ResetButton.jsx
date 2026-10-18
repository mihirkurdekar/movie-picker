import React from 'react';
import { motion } from 'framer-motion';
import { RotateCcw } from 'lucide-react';

function ResetButton({ onClick, disabled }) {
  return (
    <motion.button
      whileHover={{ scale: 1.02, backgroundColor: 'rgba(255,255,255,0.1)' }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      disabled={disabled}
      className="flex items-center justify-center gap-2 rounded-2xl border border-white/10 bg-white/5 px-6 py-4 font-semibold text-slate-300 transition-colors disabled:cursor-not-allowed disabled:opacity-40"
    >
      <RotateCcw size={18} />
      <span>Reset</span>
    </motion.button>
  );
}

export default ResetButton;
