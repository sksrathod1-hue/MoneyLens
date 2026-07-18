import React, { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence, useScroll, useTransform, useSpring, useMotionTemplate } from "framer-motion";
import Lenis from "lenis";
import { Activity, Cpu, Layers, ShieldCheck, Download, ArrowUpRight } from "lucide-react";
import { SynapseXLogo } from "./components/SynapseXLogo";
import { SquashHamburger } from "./components/SquashHamburger";
import { ScrambleIn } from "./components/ScrambleIn";
import { ScrambleText } from "./components/ScrambleText";

export default function App() {
  const [entranceComplete, setEntranceComplete] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  // Scramble hover states
  const [isAboutHovered, setIsAboutHovered] = useState(false);
  const [isMetricsHovered, setIsMetricsHovered] = useState(false);
  const [isDownloadHovered, setIsDownloadHovered] = useState(false);

  // Screen width tracking for responsive menu width
  const [screenWidth, setScreenWidth] = useState(typeof window !== "undefined" ? window.innerWidth : 1200);

  // Video refs
  const videoRef1 = useRef<HTMLVideoElement>(null);
  
  // Section refs for scroll animation tracking
  const section2Ref = useRef<HTMLElement>(null);

  // 1. Initialize Lenis Smooth Scrolling on Mount
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: "vertical",
      gestureOrientation: "vertical",
      smoothWheel: true,
    });

    function raf(time: number) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);

    // Screen resize hook
    const handleResize = () => setScreenWidth(window.innerWidth);
    window.addEventListener("resize", handleResize);

    // Trigger hero entrance after 800ms
    const timer = setTimeout(() => {
      setEntranceComplete(true);
    }, 800);

    return () => {
      lenis.destroy();
      window.removeEventListener("resize", handleResize);
      clearTimeout(timer);
    };
  }, []);

  // 2. Mouse Scrubbing video logic for Video #1 (Hero)
  const lastXRef = useRef<number | null>(null);
  const targetTimeRef = useRef<number>(0);
  const isSeekingRef = useRef<boolean>(false);
  const videoDurationRef = useRef<number>(0);

  const handleLoadedMetadata = () => {
    if (videoRef1.current) {
      videoDurationRef.current = videoRef1.current.duration;
    }
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const video = videoRef1.current;
    if (!video || videoDurationRef.current === 0) return;

    if (lastXRef.current === null) {
      lastXRef.current = e.clientX;
      return;
    }

    const deltaX = e.clientX - lastXRef.current;
    lastXRef.current = e.clientX;

    // Delta-based scrub. Sensitivity: 0.8
    const timeDelta = (deltaX / window.innerWidth) * videoDurationRef.current * 0.8;
    let nextTime = targetTimeRef.current + timeDelta;
    nextTime = Math.max(0, Math.min(nextTime, videoDurationRef.current));
    targetTimeRef.current = nextTime;

    if (!isSeekingRef.current) {
      isSeekingRef.current = true;
      video.currentTime = nextTime;
    }
  };

  const handleMouseLeave = () => {
    lastXRef.current = null;
  };

  const handleSeeked = () => {
    const video = videoRef1.current;
    if (!video) return;

    if (Math.abs(video.currentTime - targetTimeRef.current) > 0.05) {
      video.currentTime = targetTimeRef.current;
    } else {
      isSeekingRef.current = false;
    }
  };

  // 3. Cinematic Text Scroll Transforms (Section 2)
  const { scrollYProgress: s2Scroll } = useScroll({
    target: section2Ref,
    offset: ["start end", "end start"]
  });

  const s2Spring = useSpring(s2Scroll, { stiffness: 15, damping: 32, mass: 1.8 });
  const yScaleValue = useTransform(s2Spring, [0, 1], [60, -120]);
  const s2Opacity = useTransform(s2Spring, [0, 0.3, 0.5, 0.8, 1], [0, 0, 1, 1, 0]);
  const transformTemplate = useMotionTemplate`perspective(400px) rotateX(24deg) translateY(${yScaleValue}px) translateZ(15px)`;

  return (
    <div className="w-full text-white bg-black select-none" style={{ fontFamily: '"Space Mono", monospace' }}>
      
      {/* ==================== FIXED NAVBAR ==================== */}
      <motion.header
        initial={{ opacity: 0 }}
        animate={entranceComplete ? { opacity: 1 } : { opacity: 0 }}
        transition={{ duration: 0.8 }}
        className="fixed top-0 left-0 right-0 h-20 z-50 flex items-center justify-between px-4 sm:px-6 md:px-8 pointer-events-none"
      >
        {/* Left navigation pills */}
        <div className="flex items-center gap-2 pointer-events-auto">
          {/* Logo Pill */}
          <motion.div
            animate={
              isMenuOpen
                ? { width: 0, opacity: 0, paddingLeft: 0, paddingRight: 0 }
                : { width: "auto", opacity: 1 }
            }
            transition={{ type: "spring", stiffness: 350, damping: 28 }}
            whileHover={{ scale: 1.02, backgroundColor: "rgba(255,255,255,0.22)" }}
            whileTap={{ scale: 0.98 }}
            className="h-9 sm:h-12 px-3 sm:px-5 bg-white/15 backdrop-blur-md rounded-[10px] sm:rounded-[14px] flex items-center gap-2 cursor-pointer overflow-hidden border border-white/5"
            onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
          >
            <SynapseXLogo className="text-white shrink-0" size={18} />
            <span className="text-white font-medium text-[13px] sm:text-[16px] tracking-tight whitespace-nowrap">
              SynapseX
            </span>
          </motion.div>

          {/* Expanding Menu Pill */}
          <motion.div
            animate={{
              width: isMenuOpen 
                ? (screenWidth < 640 ? "calc(100vw - 32px)" : 290) 
                : (screenWidth < 640 ? 36 : 48)
            }}
            transition={{ type: "spring", stiffness: 350, damping: 28 }}
            className="h-9 sm:h-12 bg-white/15 backdrop-blur-md rounded-[10px] sm:rounded-[14px] flex items-center overflow-hidden border border-white/5"
          >
            {/* Hamburger Trigger button */}
            <div 
              className={`flex items-center justify-center cursor-pointer transition-all duration-200 shrink-0
                ${isMenuOpen 
                  ? "w-7 h-7 sm:w-9 sm:h-9 rounded-[7px] sm:rounded-[11px] bg-white/10 hover:bg-white/20 ml-1 sm:ml-1.5" 
                  : "w-9 h-9 sm:w-12 sm:h-12"
                }`}
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              <SquashHamburger isOpen={isMenuOpen} onClick={() => {}} />
            </div>

            {/* Links rendered in open state */}
            <AnimatePresence>
              {isMenuOpen && (
                <motion.div
                  initial={{ opacity: 0, x: 15 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 15 }}
                  className="flex items-center gap-4 sm:gap-6 pl-4 pr-6 shrink-0"
                >
                  <a
                    href="#about"
                    onClick={(e) => {
                      e.preventDefault();
                      setIsMenuOpen(false);
                      window.scrollTo({ top: window.innerHeight, behavior: "smooth" });
                    }}
                    onMouseEnter={() => setIsAboutHovered(true)}
                    onMouseLeave={() => setIsAboutHovered(false)}
                    className="text-[13px] sm:text-[16px] font-normal text-white/85 hover:text-white"
                  >
                    <ScrambleText text="About" isHovered={isAboutHovered} />
                  </a>
                  <a
                    href="#metrics"
                    onClick={(e) => {
                      e.preventDefault();
                      setIsMenuOpen(false);
                      window.scrollTo({ top: window.innerHeight * 2, behavior: "smooth" });
                    }}
                    onMouseEnter={() => setIsMetricsHovered(true)}
                    onMouseLeave={() => setIsMetricsHovered(false)}
                    className="text-[13px] sm:text-[16px] font-normal text-white/85 hover:text-white"
                  >
                    <ScrambleText text="Metrics" isHovered={isMetricsHovered} />
                  </a>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </div>

        {/* Right Download button */}
        <motion.div
          whileHover={{ scale: 1.03, backgroundColor: "#e2e2e6" }}
          whileTap={{ scale: 0.97 }}
          onMouseEnter={() => setIsDownloadHovered(true)}
          onMouseLeave={() => setIsDownloadHovered(false)}
          className="h-9 sm:h-12 px-3.5 sm:px-6 bg-white rounded-full flex items-center gap-2 cursor-pointer pointer-events-auto select-none border border-white/10"
        >
          <i className="bi bi-apple text-black text-[14px] sm:text-[18px]"></i>
          <span className="text-black font-semibold text-[11px] sm:text-[14px]">
            <ScrambleText text="Download" isHovered={isDownloadHovered} />
          </span>
        </motion.div>
      </motion.header>

      {/* ==================== SECTION 1: HERO ==================== */}
      <section 
        className="relative h-screen h-[100dvh] w-full flex flex-col justify-end px-4 sm:px-6 md:px-8 pt-20 sm:pt-24 pb-8 sm:pb-12 overflow-hidden"
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
      >
        {/* Mouse Scrub Video Container */}
        <div className="absolute inset-0 z-0">
          <video
            ref={videoRef1}
            src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260622_083515_290e5a10-0b95-41af-a5e2-32b6389baa4d.mp4"
            muted
            playsInline
            onLoadedMetadata={handleLoadedMetadata}
            onSeeked={handleSeeked}
            className="w-full h-full object-cover"
          />
          {/* Dot Grid overlay */}
          <div 
            className="absolute inset-0 pointer-events-none opacity-5"
            style={{
              backgroundImage: "radial-gradient(#ffffff 1px, transparent 1px)",
              backgroundSize: "24px 24px"
            }}
          />
        </div>

        {/* Large Display Font Watermark */}
        <div 
          className="absolute inset-0 flex items-center justify-center pointer-events-none select-none z-10"
          style={{ transform: "translateY(50px)" }}
        >
          <h1 
            className="font-anton uppercase tracking-[-4px] leading-none opacity-10 text-[clamp(80px,25vw,521px)] text-transparent"
            style={{
              backgroundImage: "radial-gradient(circle, rgba(142,127,148,0) 0%, #8E7F94 70%)",
              WebkitBackgroundClip: "text",
              backgroundClip: "text",
            }}
          >
            TRANSCENDENCE
          </h1>
        </div>

        {/* Hero content columns */}
        <div className="w-full flex flex-col md:flex-row md:items-end md:justify-between gap-8 z-20">
          {/* Left Column */}
          <div className="flex flex-col gap-6">
            <h1 className="text-white font-light leading-[0.95] tracking-[-0.03em] text-[clamp(40px,10vw,100px)]">
              <ScrambleIn text="Brain" delay={200} triggered={entranceComplete} />
              <br />
              <ScrambleIn text="And Body" delay={500} triggered={entranceComplete} />
            </h1>
            <motion.p
              initial={{ y: 25, opacity: 0 }}
              animate={entranceComplete ? { y: 0, opacity: 1 } : { y: 25, opacity: 0 }}
              transition={{
                duration: 0.9,
                ease: [0.215, 0.610, 0.355, 1.000],
                delay: 0.2
              }}
              className="max-w-sm text-[13px] sm:text-[15px] text-white/60 leading-relaxed font-light"
            >
              Built at the intersection of neuroscience and artificial intelligence. SynapseX continuously maps neural pathways, cognitive load, and physiological states into a single adaptive intelligence layer.
            </motion.p>
          </div>

          {/* Right Column */}
          <h1 className="text-white font-light leading-[0.95] tracking-[-0.03em] text-[clamp(40px,10vw,100px)] text-left md:text-right">
            <ScrambleIn text="One" delay={700} triggered={entranceComplete} />
            <br />
            <ScrambleIn text="Network" delay={1000} triggered={entranceComplete} />
          </h1>
        </div>
      </section>

      {/* ==================== SECTION 2: CINEMATIC TEXT ==================== */}
      <section 
        id="about"
        ref={section2Ref}
        className="relative h-screen h-[100dvh] w-full flex items-center justify-center bg-black overflow-hidden"
      >
        {/* Autoplay Video Background */}
        <div className="absolute inset-0 z-0">
          <video
            autoPlay
            muted
            loop
            playsInline
            src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260622_092455_089c54f8-3b03-4966-9df1-e9746063d0ef.mp4"
            className="w-full h-full object-cover opacity-60"
          />
          {/* Top Gradient Overlay */}
          <div className="absolute top-0 left-0 right-0 h-[180px] bg-gradient-to-b from-[#010103] to-transparent z-10" />
        </div>

        {/* 3D Perspective Transforming Text Container */}
        <div className="max-w-5xl px-6 sm:px-12 z-20">
          <motion.p
            style={{
              transform: transformTemplate,
              opacity: s2Opacity
            }}
            className="font-sans font-normal text-[20px] sm:text-[30px] md:text-[36px] lg:text-[40px] text-white leading-[1.35] tracking-[-0.02em] text-center"
          >
            A neural-AI interface built on the architecture of the human nervous system. SynapseX translates synaptic activity into computational intelligence. Every signal becomes measurable, structured, and visible. It continuously reconstructs internal state as a dynamic neural map. Biological noise is filtered into actionable cognitive patterns.
          </motion.p>
        </div>
      </section>

      {/* ==================== SECTION 3: METRICS ==================== */}
      <section 
        id="metrics"
        className="relative min-h-screen w-full flex items-center justify-center bg-black overflow-hidden py-32 px-6"
      >
        {/* Background Video */}
        <div className="absolute inset-0 z-0">
          <video
            autoPlay
            muted
            loop
            playsInline
            src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260622_095810_ecea3dd2-fc5e-4e41-8696-4219290b6589.mp4"
            className="w-full h-full object-cover opacity-50"
          />
        </div>

        {/* Content Overlay */}
        <div className="relative w-full max-w-6xl z-20 flex flex-col items-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 1.2 }}
            className="text-white/40 text-[12px] sm:text-[14px] tracking-[0.2em] uppercase mb-20 text-center font-semibold"
          >
            Performance Metrics
          </motion.div>

          <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-16 md:gap-8 text-center">
            {/* Metric 1 */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.3 }}
              transition={{ duration: 0.8, delay: 0.1 }}
              className="flex flex-col items-center"
            >
              <h2 className="text-white text-[clamp(48px,8vw,96px)] font-light tracking-[-0.04em] leading-none">
                2.4ms
              </h2>
              <span className="text-white/40 text-[13px] sm:text-[15px] mt-4 tracking-wide uppercase">
                Synaptic Latency
              </span>
            </motion.div>

            {/* Metric 2 */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.3 }}
              transition={{ duration: 0.8, delay: 0.25 }}
              className="flex flex-col items-center"
            >
              <h2 className="text-white text-[clamp(48px,8vw,96px)] font-light tracking-[-0.04em] leading-none">
                99.7%
              </h2>
              <span className="text-white/40 text-[13px] sm:text-[15px] mt-4 tracking-wide uppercase">
                Signal Accuracy
              </span>
            </motion.div>

            {/* Metric 3 */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.3 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="flex flex-col items-center"
            >
              <h2 className="text-white text-[clamp(48px,8vw,96px)] font-light tracking-[-0.04em] leading-none">
                140B
              </h2>
              <span className="text-white/40 text-[13px] sm:text-[15px] mt-4 tracking-wide uppercase">
                Neural Parameters
              </span>
            </motion.div>
          </div>
        </div>
      </section>

      {/* ==================== SECTION 4: ADAPTIVE INTELLIGENCE ==================== */}
      <section 
        className="relative h-screen h-[100dvh] w-full flex flex-col justify-between bg-black overflow-hidden px-8 sm:px-12 md:px-16 py-12 sm:py-16"
      >
        {/* Background Video */}
        <div className="absolute inset-0 z-0">
          <video
            autoPlay
            muted
            loop
            playsInline
            src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260622_095750_32a52ce0-2005-45c9-9093-41f03fde9530.mp4"
            className="w-full h-full object-cover opacity-60"
          />
        </div>

        {/* Top Info Area */}
        <div className="w-full flex flex-col md:flex-row md:justify-between md:items-start gap-6 z-20 pt-8">
          <motion.h2
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 1.0 }}
            className="text-white font-light text-[clamp(32px,6vw,72px)] leading-[0.95] tracking-[-0.03em]"
          >
            Adaptive
            <br />
            Intelligence
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 1.0, delay: 0.2 }}
            className="text-white/50 text-[13px] sm:text-[15px] leading-relaxed max-w-xs md:text-right md:pt-2 font-light"
          >
            The system learns your neural baseline within 72 hours. From there, every cognitive state is mapped, predicted, and optimized in real time.
          </motion.p>
        </div>

        {/* Bottom Description Grid */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 1.0, delay: 0.3 }}
          className="w-full grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-6 z-20 pb-4"
        >
          {/* Tech Spec 1 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7, delay: 0.1 }}
            className="flex flex-col"
          >
            <h4 className="text-white text-[14px] sm:text-[16px] font-normal mb-2 flex items-center gap-2">
              <span className="text-[10px] text-white/50">01//</span> Cortical Mapping
            </h4>
            <p className="text-white/40 text-[12px] sm:text-[14px] leading-relaxed font-light">
              Real-time spatial reconstruction of active neural regions.
            </p>
          </motion.div>

          {/* Tech Spec 2 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7, delay: 0.2 }}
            className="flex flex-col"
          >
            <h4 className="text-white text-[14px] sm:text-[16px] font-normal mb-2 flex items-center gap-2">
              <span className="text-[10px] text-white/50">02//</span> Signal Isolation
            </h4>
            <p className="text-white/40 text-[12px] sm:text-[14px] leading-relaxed font-light">
              Separates cognitive intent from biological noise.
            </p>
          </motion.div>

          {/* Tech Spec 3 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7, delay: 0.3 }}
            className="flex flex-col"
          >
            <h4 className="text-white text-[14px] sm:text-[16px] font-normal mb-2 flex items-center gap-2">
              <span className="text-[10px] text-white/50">03//</span> State Prediction
            </h4>
            <p className="text-white/40 text-[12px] sm:text-[14px] leading-relaxed font-light">
              Anticipates cognitive transitions before they occur.
            </p>
          </motion.div>

          {/* Tech Spec 4 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7, delay: 0.4 }}
            className="flex flex-col"
          >
            <h4 className="text-white text-[14px] sm:text-[16px] font-normal mb-2 flex items-center gap-2">
              <span className="text-[10px] text-white/50">04//</span> Loop Feedback
            </h4>
            <p className="text-white/40 text-[12px] sm:text-[14px] leading-relaxed font-light">
              Closed-loop adjustment based on outcome correlation.
            </p>
          </motion.div>
        </motion.div>
      </section>

      {/* ==================== SECTION 5: ARCHITECTURE ==================== */}
      <section 
        className="relative min-h-screen w-full flex items-center justify-center bg-black overflow-hidden py-32 px-6"
      >
        <div className="w-full max-w-3xl z-20 text-center flex flex-col items-center">
          {/* Heading Block */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.4 }}
            transition={{ duration: 1.0 }}
            className="flex flex-col items-center"
          >
            <span className="text-white/40 text-[12px] sm:text-[14px] tracking-[0.2em] uppercase mb-8 font-semibold">
              Architecture
            </span>
            <h2 className="text-white font-light text-[clamp(28px,6vw,56px)] leading-[1.15] tracking-[-0.02em] mb-10">
              Three layers. Zero friction.
            </h2>
            <p className="text-white/45 text-[15px] sm:text-[17px] leading-relaxed max-w-xl font-light">
              Sensor layer captures raw bioelectric signals. Processing layer isolates intent. Interface layer delivers structured output to any connected system.
            </p>
          </motion.div>

          {/* Layers Stack Cards */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true, amount: 0.4 }}
            transition={{ duration: 1.2, delay: 0.4 }}
            className="mt-20 flex flex-col gap-4 w-full"
          >
            {/* Card 1 */}
            <div className="max-w-md h-[72px] border border-white/10 rounded-lg flex items-center justify-between px-6 w-full mx-auto bg-[#0a0e17]/50 backdrop-blur-sm hover:border-white/20 transition-colors">
              <span className="text-white/30 text-[12px] tracking-[0.15em] uppercase font-bold flex items-center gap-2">
                <Cpu className="w-4 h-4 text-white/50" /> Layer 1
              </span>
              <span className="text-white text-[16px] sm:text-[18px] font-light">
                Capture
              </span>
            </div>

            {/* Card 2 */}
            <div className="max-w-md h-[72px] border border-white/10 rounded-lg flex items-center justify-between px-6 w-full mx-auto bg-[#0a0e17]/50 backdrop-blur-sm hover:border-white/20 transition-colors">
              <span className="text-white/30 text-[12px] tracking-[0.15em] uppercase font-bold flex items-center gap-2">
                <Activity className="w-4 h-4 text-white/50" /> Layer 2
              </span>
              <span className="text-white text-[16px] sm:text-[18px] font-light">
                Process
              </span>
            </div>

            {/* Card 3 */}
            <div className="max-w-md h-[72px] border border-white/10 rounded-lg flex items-center justify-between px-6 w-full mx-auto bg-[#0a0e17]/50 backdrop-blur-sm hover:border-white/20 transition-colors">
              <span className="text-white/30 text-[12px] tracking-[0.15em] uppercase font-bold flex items-center gap-2">
                <Layers className="w-4 h-4 text-white/50" /> Layer 3
              </span>
              <span className="text-white text-[16px] sm:text-[18px] font-light">
                Interface
              </span>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ==================== FOOTER ==================== */}
      <footer 
        className="w-full bg-[#030305] border-t border-white/5 overflow-hidden"
      >
        <div className="w-full flex flex-col md:flex-row min-h-[400px]">
          {/* Left Column: Video Background placeholder */}
          <div className="w-full md:w-1/2 h-[300px] md:h-auto relative z-0">
            <video
              autoPlay
              muted
              loop
              playsInline
              src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260622_080203_fd7f4f85-3a86-4837-8192-85e7bfe68e75.mp4"
              className="w-full h-full object-cover"
            />
          </div>

          {/* Right Column: Information & copyrights */}
          <div className="w-full md:w-1/2 flex flex-col justify-between p-10 sm:p-16 bg-[#030305] z-10">
            <div>
              <div className="flex items-center gap-3 mb-8 select-none">
                <SynapseXLogo className="text-white/70" size={18} />
                <span className="font-semibold text-white/70 text-[15px] tracking-tight">
                  SynapseX
                </span>
              </div>
              <p className="text-white/40 text-[14px] sm:text-[15px] leading-relaxed max-w-sm font-light">
                The next evolution of human-machine interaction. Built for those who refuse to be limited by biology alone.
              </p>
            </div>

            <div className="text-white/25 text-[12px] mt-12 font-light">
              (c) 2026 SynapseX Labs. All rights reserved.
            </div>
          </div>
        </div>
      </footer>

    </div>
  );
}
