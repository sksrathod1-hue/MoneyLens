import React, { useEffect, useState } from "react";

interface ScrambleTextProps {
  text: string;
  isHovered: boolean;
  className?: string;
}

const CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+~|}{[]:;?><";

export const ScrambleText: React.FC<ScrambleTextProps> = ({ text, isHovered, className = "" }) => {
  const [displayedText, setDisplayedText] = useState<string>(text);

  useEffect(() => {
    if (!isHovered) {
      setDisplayedText(text);
      return;
    }

    let progress = 0; // Float counter for 0.25 chars/tick (4 frames per character)
    const textLength = text.length;

    const interval = setInterval(() => {
      progress += 0.25;
      const revealIndex = Math.floor(progress);

      if (revealIndex >= textLength) {
        setDisplayedText(text);
        clearInterval(interval);
        return;
      }

      let currentScramble = "";
      for (let i = 0; i < textLength; i++) {
        if (text[i] === " ") {
          currentScramble += " ";
        } else if (i < revealIndex) {
          currentScramble += text[i];
        } else {
          // Scramble all characters not yet revealed
          const randomChar = CHARS[Math.floor(Math.random() * CHARS.length)];
          currentScramble += randomChar;
        }
      }
      setDisplayedText(currentScramble);
    }, 25);

    return () => clearInterval(interval);
  }, [isHovered, text]);

  return <span className={className}>{displayedText}</span>;
};
export default ScrambleText;
