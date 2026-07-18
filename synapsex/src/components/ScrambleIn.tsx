import React, { useEffect, useState } from "react";

interface ScrambleInProps {
  text: string;
  delay: number; // in ms
  triggered: boolean;
  className?: string;
}

const CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+~|}{[]:;?><";

export const ScrambleIn: React.FC<ScrambleInProps> = ({ text, delay, triggered, className = "" }) => {
  const [displayedText, setDisplayedText] = useState<string>("");
  const [hasStarted, setHasStarted] = useState<boolean>(false);

  useEffect(() => {
    if (!triggered) {
      setDisplayedText("");
      setHasStarted(false);
      return;
    }

    const timer = setTimeout(() => {
      setHasStarted(true);
    }, delay);

    return () => clearTimeout(timer);
  }, [triggered, delay]);

  useEffect(() => {
    if (!hasStarted) return;

    let progress = 0; // Float counter for 0.5 chars/frame
    const textLength = text.length;

    const interval = setInterval(() => {
      progress += 0.5;
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
        } else if (i < revealIndex + 3) {
          // Show random character if within 3 characters of reveal index
          const randomChar = CHARS[Math.floor(Math.random() * CHARS.length)];
          currentScramble += randomChar;
        } else {
          // Beyond that is empty
          currentScramble += "";
        }
      }
      setDisplayedText(currentScramble);
    }, 25);

    return () => clearInterval(interval);
  }, [hasStarted, text]);

  if (!hasStarted) {
    // Before triggered: render non-breaking space
    return <span className={className} dangerouslySetInnerHTML={{ __html: "&nbsp;" }} />;
  }

  return <span className={className}>{displayedText}</span>;
};
export default ScrambleIn;
