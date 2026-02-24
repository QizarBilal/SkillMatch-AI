import { useState, useEffect } from 'react';

export default function PremiumLoader() {
  const [textIndex, setTextIndex] = useState(0);
  const loadingTexts = [
    "INITIALIZING AI ENGINE",
    "NLP MODELS LOADED",
    "ANALYZING RESUME DATA",
    "PREPARING DASHBOARD"
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setTextIndex((prev) => (prev + 1) % loadingTexts.length);
    }, 875);
    return () => clearInterval(interval);
  }, [loadingTexts.length]);

  return (
    <div className="loader-overlay">
      <style>{`
        .loader-overlay {
          position: fixed;
          inset: 0;
          background-color: #020617; /* Slate 950 */
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          z-index: 9999;
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
          overflow: hidden;
        }

        .bg-mesh {
          position: absolute;
          inset: 0;
          background-image: 
            radial-gradient(at 20% 20%, rgba(99, 102, 241, 0.08) 0px, transparent 50%),
            radial-gradient(at 80% 80%, rgba(168, 85, 247, 0.08) 0px, transparent 50%);
          z-index: 0;
        }

        .loader-content {
          position: relative;
          z-index: 10;
          display: flex;
          flex-direction: column;
          align-items: center;
        }
        
        .loader-svg-container {
          margin-bottom: 32px;
          filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.15));
        }

        .spin-slow {
          transform-origin: 64px 64px;
          animation: spin 8s linear infinite;
        }

        .spin-fast {
          transform-origin: 64px 64px;
          animation: spin 1.5s cubic-bezier(0.6, 0.1, 0.4, 0.9) infinite;
        }
        
        .spin-reverse {
          transform-origin: 64px 64px;
          animation: spin-reverse 2.5s cubic-bezier(0.4, 0, 0.2, 1) infinite;
        }

        .pulse-core {
          transform-origin: 64px 64px;
          animation: pulse-scale 2s ease-in-out infinite alternate;
        }

        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        
        @keyframes spin-reverse {
          from { transform: rotate(360deg); }
          to { transform: rotate(0deg); }
        }

        @keyframes pulse-scale {
          0% { transform: scale(0.85); opacity: 0.7; }
          100% { transform: scale(1.15); opacity: 1; }
        }

        .logo-text {
          font-size: 22px;
          font-weight: 600;
          color: #f8fafc;
          letter-spacing: -0.02em;
          margin-bottom: 24px;
          display: flex;
          align-items: center;
          gap: 6px;
        }

        .logo-text span {
          background: linear-gradient(135deg, #818cf8, #c084fc);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .status-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          width: 240px;
        }

        .status-text-wrapper {
          height: 16px;
          overflow: hidden;
          position: relative;
          display: flex;
          justify-content: center;
          width: 100%;
        }

        .status-text {
          font-size: 11px;
          font-weight: 600;
          color: #94a3b8;
          letter-spacing: 0.2em;
          text-transform: uppercase;
          animation: slide-up-fade 0.875s cubic-bezier(0.16, 1, 0.3, 1) forwards;
          position: absolute;
        }

        .progress-track {
          margin-top: 16px;
          width: 100%;
          height: 2px;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 2px;
          overflow: hidden;
          position: relative;
        }

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, transparent, #818cf8, #c084fc);
          width: 0%;
          animation: progress-fill 3.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
          position: absolute;
          left: 0;
          top: 0;
        }

        .progress-fill::after {
          content: '';
          position: absolute;
          right: 0;
          top: 0;
          height: 100%;
          width: 8px;
          background: #ffffff;
          box-shadow: 0 0 10px 2px rgba(192, 132, 252, 0.8);
          border-radius: 50%;
        }

        @keyframes slide-up-fade {
          0% { opacity: 0; transform: translateY(10px); }
          15% { opacity: 1; transform: translateY(0); }
          85% { opacity: 1; transform: translateY(0); }
          100% { opacity: 0; transform: translateY(-10px); }
        }

        @keyframes progress-fill {
          0% { width: 0%; }
          100% { width: 100%; }
        }
      `}</style>

      <div className="bg-mesh"></div>

      <div className="loader-content">
        <div className="loader-svg-container">
          <svg width="128" height="128" viewBox="0 0 128 128" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#6366f1" />
                <stop offset="100%" stopColor="#a855f7" />
              </linearGradient>
              <linearGradient id="ringGradReverse" x1="100%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor="#ec4899" />
                <stop offset="100%" stopColor="#8b5cf6" />
              </linearGradient>
              <filter id="svgGlow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="3" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
              </filter>
            </defs>

            {/* Faint static background track */}
            <circle cx="64" cy="64" r="54" stroke="rgba(255,255,255,0.03)" strokeWidth="1" />

            {/* Outer dotted tracking ring */}
            <g className="spin-slow">
              <circle cx="64" cy="64" r="54" stroke="rgba(148, 163, 184, 0.2)" strokeWidth="1.5" strokeDasharray="2 6" strokeLinecap="round" />
            </g>

            {/* Primary sweeping ring */}
            <circle
              cx="64" cy="64" r="42"
              stroke="url(#ringGrad)"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeDasharray="180 300"
              className="spin-fast"
              filter="url(#svgGlow)"
            />

            {/* Inner inverse ring */}
            <circle
              cx="64" cy="64" r="30"
              stroke="url(#ringGradReverse)"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeDasharray="60 140"
              className="spin-reverse"
            />

            {/* Brain/Core element */}
            <g className="pulse-core">
              <circle cx="64" cy="64" r="12" fill="rgba(99,102,241,0.05)" stroke="#818cf8" strokeWidth="1.5" />
              <circle cx="64" cy="64" r="4" fill="#ffffff" filter="url(#svgGlow)" />
            </g>
          </svg>
        </div>

        <div className="logo-text">
          Skill<span>Match</span>
        </div>

        <div className="status-container">
          <div className="status-text-wrapper">
            <div key={textIndex} className="status-text">
              {loadingTexts[textIndex]}
            </div>
          </div>
          <div className="progress-track">
            <div className="progress-fill"></div>
          </div>
        </div>
      </div>
    </div>
  );
}
