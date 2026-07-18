import React from "react";
import { motion } from "framer-motion";

interface HamburgerProps {
  isOpen: boolean;
  onClick: () => void;
  className?: string;
}

export const SquashHamburger: React.FC<HamburgerProps> = ({ isOpen, onClick, className = "" }) => {
  // Desktop dimensions: 18x12px, bar height 1.5px
  // Mobile dimensions: 15x10px, bar height 1.2px
  // Since we want this to be responsive, we can style it dynamically with Tailwind.
  
  const spring = { stiffness: 300, damping: 20 };

  return (
    <button
      onClick={onClick}
      className={`relative flex items-center justify-center focus:outline-none ${className}`}
      aria-label="Toggle Menu"
    >
      {/* Desktop Hamburger (hidden on mobile) */}
      <div className="hidden sm:block relative w-[18px] h-[12px]">
        {/* Top Bar */}
        <motion.span
          animate={isOpen ? { rotate: 45, y: 5.25 } : { rotate: 0, y: 0 }}
          transition={spring}
          className="absolute left-0 top-0 w-full h-[1.5px] bg-white origin-center"
        />
        {/* Middle Bar */}
        <motion.span
          animate={isOpen ? { opacity: 0, scale: 0.5 } : { opacity: 1, scale: 1 }}
          transition={spring}
          className="absolute left-0 top-[5.25px] w-full h-[1.5px] bg-white origin-center"
        />
        {/* Bottom Bar */}
        <motion.span
          animate={isOpen ? { rotate: -45, y: -5.25 } : { rotate: 0, y: 0 }}
          transition={spring}
          className="absolute left-0 bottom-0 w-full h-[1.5px] bg-white origin-center"
        />
      </div>

      {/* Mobile Hamburger (visible on mobile) */}
      <div className="block sm:hidden relative w-[15px] h-[10px]">
        {/* Top Bar */}
        <motion.span
          animate={isOpen ? { rotate: 45, y: 4.4 } : { rotate: 0, y: 0 }}
          transition={spring}
          className="absolute left-0 top-0 w-full h-[1.2px] bg-white origin-center"
        />
        {/* Middle Bar */}
        <motion.span
          animate={isOpen ? { opacity: 0, scale: 0.5 } : { opacity: 1, scale: 1 }}
          transition={spring}
          className="absolute left-0 top-[4.4px] w-full h-[1.2px] bg-white origin-center"
        />
        {/* Bottom Bar */}
        <motion.span
          animate={isOpen ? { rotate: -45, y: -4.4 } : { rotate: 0, y: 0 }}
          transition={spring}
          className="absolute left-0 bottom-0 w-full h-[1.2px] bg-white origin-center"
        />
      </div>
    </button>
  );
};
