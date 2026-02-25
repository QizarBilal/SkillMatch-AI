import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from './App'
import api from './api'
import jsPDF from 'jspdf'
import 'jspdf-autotable'

const useWindowSize = () => {
  const [windowSize, setWindowSize] = useState({
    width: typeof window !== 'undefined' ? window.innerWidth : 1200,
    isMobile: typeof window !== 'undefined' ? window.innerWidth < 768 : false,
    isTablet: typeof window !== 'undefined' ? window.innerWidth >= 768 && window.innerWidth < 1024 : false,
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        isMobile: window.innerWidth < 768,
        isTablet: window.innerWidth >= 768 && window.innerWidth < 1024,
      });
    };

    window.addEventListener('resize', handleResize);
    handleResize();

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
};

const getResponsiveStyles = (isMobile, isTablet) => ({
  app: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1428 100%)',
    color: '#e8eaf0',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif',
  },
  nav: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: isMobile ? '12px 16px' : isTablet ? '16px 24px' : '20px 48px',
    borderBottom: '1px solid rgba(99, 102, 241, 0.15)',
    background: 'rgba(10, 14, 39, 0.6)',
    backdropFilter: 'blur(12px)',
    flexWrap: isMobile ? 'wrap' : 'nowrap',
    gap: isMobile ? '12px' : '0',
  },
  logo: {
    fontSize: isMobile ? '16px' : isTablet ? '19px' : '22px',
    fontWeight: '700',
    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    letterSpacing: '-0.02em',
  },
  tagline: {
    fontSize: isMobile ? '10px' : '12px',
    color: '#94a3b8',
    marginLeft: isMobile ? '8px' : '16px',
    fontWeight: '500',
    display: isMobile ? 'none' : 'inline',
  },
  navRight: {
    display: 'flex',
    alignItems: 'center',
    gap: isMobile ? '8px' : '16px',
    flexWrap: 'wrap',
  },
  userEmail: {
    fontSize: isMobile ? '11px' : '13px',
    color: '#cbd5e1',
    fontWeight: '500',
    maxWidth: isMobile ? '120px' : 'none',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  logoutBtn: {
    padding: isMobile ? '6px 12px' : '8px 16px',
    background: 'rgba(239, 68, 68, 0.12)',
    border: '1px solid rgba(239, 68, 68, 0.3)',
    borderRadius: '8px',
    color: '#ef4444',
    fontSize: isMobile ? '11px' : '12px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
  },
  statusBadge: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px',
    padding: isMobile ? '4px 10px' : '6px 14px',
    background: 'rgba(16, 185, 129, 0.1)',
    border: '1px solid rgba(16, 185, 129, 0.3)',
    borderRadius: '20px',
    fontSize: isMobile ? '10px' : '11px',
    color: '#10b981',
    fontWeight: '600',
  },
  liveDot: {
    width: '6px',
    height: '6px',
    borderRadius: '50%',
    background: '#10b981',
    boxShadow: '0 0 8px rgba(16, 185, 129, 0.6)',
    animation: 'pulse 2s infinite',
  },
  hero: {
    padding: isMobile ? '32px 16px 24px' : isTablet ? '40px 24px 32px' : '60px 48px 40px',
    textAlign: 'center',
  },
  heroTitle: {
    fontSize: isMobile ? '28px' : isTablet ? '36px' : '48px',
    fontWeight: '800',
    marginBottom: '12px',
    background: 'linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    letterSpacing: '-0.03em',
  },
  heroSubtitle: {
    fontSize: isMobile ? '13px' : isTablet ? '14px' : '16px',
    color: '#94a3b8',
    marginBottom: isMobile ? '20px' : '32px',
    fontWeight: '400',
    padding: isMobile ? '0 8px' : '0',
  },
  divider: {
    height: '2px',
    background: 'linear-gradient(90deg, transparent 0%, #6366f1 50%, transparent 100%)',
    maxWidth: isMobile ? '90%' : '600px',
    margin: '0 auto',
  },
  container: {
    maxWidth: '1400px',
    margin: '0 auto',
    padding: isMobile ? '20px 16px' : isTablet ? '32px 24px' : '40px 48px',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: isMobile ? '1fr' : isTablet ? '1fr' : 'repeat(auto-fit, minmax(480px, 1fr))',
    gap: isMobile ? '16px' : '24px',
    marginBottom: isMobile ? '20px' : '32px',
  },
  card: {
    background: 'rgba(15, 20, 40, 0.7)',
    border: '1px solid rgba(99, 102, 241, 0.2)',
    borderRadius: isMobile ? '12px' : '16px',
    padding: isMobile ? '20px' : isTablet ? '24px' : '32px',
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
    backdropFilter: 'blur(8px)',
    transition: 'all 0.3s ease',
  },
  cardHover: {
    transform: isMobile ? 'none' : 'translateY(-2px)',
    boxShadow: '0 12px 40px rgba(99, 102, 241, 0.2)',
  },
  sectionTitle: {
    fontSize: isMobile ? '12px' : '14px',
    fontWeight: '700',
    color: '#cbd5e1',
    marginBottom: isMobile ? '16px' : '20px',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
  },
  uploadZone: {
    border: '2px dashed rgba(99, 102, 241, 0.35)',
    borderRadius: isMobile ? '12px' : '16px',
    padding: isMobile ? '32px 20px' : isTablet ? '40px 28px' : '56px 40px 48px',
    textAlign: 'center',
    cursor: 'pointer',
    transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
    background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%)',
    position: 'relative',
    overflow: 'hidden',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: isMobile ? '200px' : isTablet ? '240px' : '280px',
  },
  uploadZoneActive: {
    border: '2px dashed #6366f1',
    background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(139, 92, 246, 0.12) 100%)',
    transform: isMobile ? 'none' : 'scale(1.02)',
    boxShadow: '0 0 40px rgba(99, 102, 241, 0.3), inset 0 0 60px rgba(99, 102, 241, 0.1)',
  },
  uploadIconWrapper: {
    width: isMobile ? '64px' : isTablet ? '72px' : '88px',
    height: isMobile ? '64px' : isTablet ? '72px' : '88px',
    margin: isMobile ? '0 0 16px 0' : '0 0 24px 0',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(139, 92, 246, 0.12) 100%)',
    borderRadius: '50%',
    border: '2px solid rgba(99, 102, 241, 0.35)',
    transition: 'all 0.4s ease',
    flexShrink: 0,
  },
  uploadIconWrapperActive: {
    transform: isMobile ? 'scale(1.05)' : 'scale(1.1) rotate(10deg)',
    background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(139, 92, 246, 0.25) 100%)',
    border: '2px solid #6366f1',
    boxShadow: '0 0 30px rgba(99, 102, 241, 0.5)',
  },
  uploadIcon: {
    fontSize: isMobile ? '28px' : isTablet ? '34px' : '40px',
    opacity: 0.95,
    transition: 'all 0.3s ease',
    lineHeight: 1,
  },
  uploadTextPrimary: {
    fontSize: isMobile ? '14px' : isTablet ? '15px' : '17px',
    fontWeight: '600',
    color: '#e2e8f0',
    marginBottom: '10px',
    letterSpacing: '-0.01em',
    lineHeight: 1.3,
  },
  uploadTextSecondary: {
    fontSize: isMobile ? '11px' : '13px',
    color: '#64748b',
    marginBottom: isMobile ? '16px' : '28px',
    fontWeight: '400',
    lineHeight: 1.5,
    maxWidth: isMobile ? '90%' : '280px',
  },
  fileTypes: {
    display: 'flex',
    gap: '10px',
    justifyContent: 'center',
    alignItems: 'center',
    flexWrap: 'wrap',
    marginTop: '0',
  },
  fileTypeBadge: {
    padding: isMobile ? '5px 10px' : '6px 12px',
    background: 'rgba(139, 92, 246, 0.12)',
    border: '1px solid rgba(139, 92, 246, 0.35)',
    borderRadius: '8px',
    fontSize: isMobile ? '10px' : '11px',
    color: '#a78bfa',
    fontWeight: '600',
    letterSpacing: '0.02em',
    textTransform: 'uppercase',
  },
  filePreview: {
    marginTop: isMobile ? '16px' : '24px',
    padding: isMobile ? '16px' : '20px',
    background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.08) 100%)',
    border: '1px solid rgba(16, 185, 129, 0.4)',
    borderRadius: '12px',
    transition: 'all 0.3s ease',
    boxShadow: '0 4px 12px rgba(16, 185, 129, 0.1)',
  },
  filePreviewHover: {
    transform: isMobile ? 'none' : 'translateY(-2px)',
    boxShadow: '0 8px 20px rgba(16, 185, 129, 0.2)',
  },
  fileInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    marginBottom: '12px',
    flexWrap: isMobile ? 'wrap' : 'nowrap',
  },
  fileIconCircle: {
    width: isMobile ? '36px' : '44px',
    height: isMobile ? '36px' : '44px',
    borderRadius: '50%',
    background: 'rgba(16, 185, 129, 0.2)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: isMobile ? '16px' : '20px',
    flexShrink: 0,
  },
  fileDetails: {
    flex: 1,
    minWidth: 0,
  },
  fileName: {
    fontSize: isMobile ? '12px' : '14px',
    color: '#10b981',
    fontWeight: '700',
    marginBottom: '4px',
    letterSpacing: '-0.01em',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  },
  fileSize: {
    fontSize: '11px',
    color: '#64748b',
    fontWeight: '500',
  },
  replaceBtn: {
    padding: isMobile ? '6px 12px' : '8px 16px',
    background: 'rgba(239, 68, 68, 0.12)',
    border: '1px solid rgba(239, 68, 68, 0.3)',
    borderRadius: '8px',
    color: '#ef4444',
    fontSize: '12px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
  },
  replaceBtnHover: {
    background: 'rgba(239, 68, 68, 0.2)',
    border: '1px solid #ef4444',
    transform: isMobile ? 'none' : 'translateY(-1px)',
    boxShadow: '0 4px 12px rgba(239, 68, 68, 0.3)',
  },
  textarea: {
    width: 'calc(100% - 4px)',
    minHeight: isMobile ? '200px' : isTablet ? '240px' : '280px',
    background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.04) 0%, rgba(139, 92, 246, 0.04) 100%)',
    border: '2px dashed rgba(99, 102, 241, 0.35)',
    borderRadius: '12px',
    padding: isMobile ? '16px' : '20px',
    color: '#e2e8f0',
    fontSize: isMobile ? '13px' : '14px',
    fontFamily: 'inherit',
    resize: 'none',
    transition: 'all 0.3s ease',
    outline: 'none',
    lineHeight: 1.7,
    letterSpacing: '0.01em',
    boxSizing: 'border-box',
  },
  textareaFocus: {
    border: '2px dashed #6366f1',
    background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%)',
    boxShadow: '0 0 0 3px rgba(99, 102, 241, 0.1)',
  },
  charCounter: {
    fontSize: '11px',
    color: '#64748b',
    marginTop: '4px',
    textAlign: 'right',
    fontWeight: '500',
  },
  textareaWrapper: {
    position: 'relative',
    width: '100%',
  },
  textareaLabel: {
    fontSize: isMobile ? '12px' : '13px',
    color: '#94a3b8',
    marginBottom: isMobile ? '12px' : '16px',
    fontWeight: '500',
    display: 'block',
    lineHeight: 1.4,
  },
  textareaHint: {
    fontSize: '11px',
    color: '#64748b',
    marginTop: '12px',
    marginBottom: '8px',
    display: 'block',
    lineHeight: 1.5,
    fontWeight: '400',
  },
  modeToggle: {
    display: 'flex',
    gap: '8px',
    marginBottom: '16px',
    background: 'rgba(15, 20, 40, 0.6)',
    padding: '4px',
    borderRadius: '8px',
    border: '1px solid rgba(99, 102, 241, 0.2)',
  },
  modeButton: {
    flex: 1,
    padding: isMobile ? '6px 12px' : '8px 16px',
    background: 'transparent',
    border: 'none',
    borderRadius: '6px',
    color: '#94a3b8',
    fontSize: isMobile ? '12px' : '13px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    whiteSpace: 'nowrap',
  },
  modeButtonActive: {
    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
    color: '#ffffff',
    boxShadow: '0 4px 12px rgba(99, 102, 241, 0.4)',
  },
  actionSection: {
    display: 'flex',
    justifyContent: 'center',
    marginBottom: isMobile ? '32px' : '48px',
  },
  primaryBtn: {
    padding: isMobile ? '12px 32px' : isTablet ? '14px 40px' : '16px 48px',
    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
    border: 'none',
    borderRadius: '12px',
    color: '#ffffff',
    fontSize: isMobile ? '14px' : '15px',
    fontWeight: '700',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    boxShadow: '0 8px 24px rgba(99, 102, 241, 0.4)',
    letterSpacing: '0.02em',
    width: isMobile ? '100%' : 'auto',
  },
  primaryBtnHover: {
    transform: isMobile ? 'none' : 'translateY(-2px)',
    boxShadow: '0 12px 32px rgba(99, 102, 241, 0.6)',
  },
  primaryBtnDisabled: {
    opacity: 0.5,
    cursor: 'not-allowed',
  },
  loader: {
    display: 'inline-block',
    width: '16px',
    height: '16px',
    border: '2px solid rgba(255, 255, 255, 0.3)',
    borderTop: '2px solid #ffffff',
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
    marginRight: '10px',
  },
  resultsGrid: {
    display: 'grid',
    gridTemplateColumns: isMobile ? '1fr' : isTablet ? 'repeat(auto-fit, minmax(250px, 1fr))' : 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: isMobile ? '12px' : '20px',
  },
  resultCard: {
    background: 'rgba(15, 20, 40, 0.8)',
    border: '1px solid rgba(99, 102, 241, 0.25)',
    borderRadius: isMobile ? '12px' : '14px',
    padding: isMobile ? '16px' : '24px',
    transition: 'all 0.3s ease',
  },
  resultCardHover: {
    transform: isMobile ? 'none' : 'translateY(-3px)',
    boxShadow: '0 10px 30px rgba(99, 102, 241, 0.25)',
  },
  resultLabel: {
    fontSize: '11px',
    fontWeight: '700',
    color: '#64748b',
    textTransform: 'uppercase',
    letterSpacing: '0.08em',
    marginBottom: isMobile ? '8px' : '12px',
  },
  resultValue: {
    fontSize: isMobile ? '16px' : '18px',
    fontWeight: '600',
    color: '#e8eaf0',
    marginBottom: '4px',
  },
  resultMeta: {
    fontSize: isMobile ? '11px' : '12px',
    color: '#94a3b8',
  },
  chipContainer: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: isMobile ? '6px' : '8px',
    marginTop: '8px',
  },
  skillChip: {
    padding: isMobile ? '6px 10px' : '8px 14px',
    background: 'rgba(16, 185, 129, 0.15)',
    border: '1px solid rgba(16, 185, 129, 0.4)',
    borderRadius: '20px',
    fontSize: isMobile ? '11px' : '12px',
    color: '#10b981',
    fontWeight: '600',
    transition: 'all 0.2s ease',
  },
  keywordChip: {
    padding: isMobile ? '6px 10px' : '8px 14px',
    background: 'rgba(99, 102, 241, 0.15)',
    border: '1px solid rgba(99, 102, 241, 0.4)',
    borderRadius: '20px',
    fontSize: isMobile ? '11px' : '12px',
    color: '#818cf8',
    fontWeight: '600',
    transition: 'all 0.2s ease',
  },
  chipHover: {
    transform: isMobile ? 'none' : 'scale(1.05)',
    boxShadow: '0 4px 12px rgba(99, 102, 241, 0.3)',
  },
  datasetIndicator: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px',
    padding: isMobile ? '6px 12px' : '8px 16px',
    background: 'rgba(16, 185, 129, 0.12)',
    border: '1px solid rgba(16, 185, 129, 0.3)',
    borderRadius: '8px',
    marginTop: '8px',
    fontSize: isMobile ? '11px' : '13px',
  },
  updateDot: {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    background: '#10b981',
    boxShadow: '0 0 10px rgba(16, 185, 129, 0.8)',
  },
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'rgba(10, 14, 39, 0.95)',
    backdropFilter: 'blur(20px)',
    zIndex: 9999,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    animation: 'fadeIn 0.3s ease',
    padding: isMobile ? '16px' : '0',
  },
  overlayContent: {
    maxWidth: isMobile ? '100%' : '900px',
    width: '90%',
    textAlign: 'center',
  },
  stageTitle: {
    fontSize: isMobile ? '16px' : isTablet ? '18px' : '20px',
    fontWeight: '700',
    color: '#e2e8f0',
    marginBottom: isMobile ? '16px' : '24px',
    letterSpacing: '-0.02em',
  },
  scanPanel: {
    background: 'rgba(15, 20, 40, 0.8)',
    border: '1px solid rgba(99, 102, 241, 0.3)',
    borderRadius: isMobile ? '12px' : '16px',
    padding: '0',
    position: 'relative',
    overflow: 'hidden',
    maxWidth: isMobile ? '100%' : '800px',
    width: '90%',
    margin: '0 auto',
  },
  previewContainer: {
    position: 'relative',
    width: '100%',
    height: isMobile ? '300px' : isTablet ? '400px' : '500px',
    background: 'rgba(10, 14, 27, 0.6)',
    borderRadius: '12px',
    overflow: 'hidden',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  previewFrame: {
    width: '100%',
    height: '100%',
    border: 'none',
    background: 'white',
  },
  previewImage: {
    maxWidth: '100%',
    maxHeight: '100%',
    objectFit: 'contain',
  },
  docPreview: {
    width: '100%',
    height: '100%',
    padding: isMobile ? '20px' : '40px',
    background: 'white',
    color: '#1a1a1a',
    overflow: 'auto',
    fontFamily: 'Georgia, serif',
    fontSize: isMobile ? '12px' : '14px',
    lineHeight: '1.8',
  },
  scanOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    pointerEvents: 'none',
    background: 'linear-gradient(180deg, transparent 0%, rgba(99, 102, 241, 0.03) 50%, transparent 100%)',
  },
  scanBeam: {
    position: 'absolute',
    left: 0,
    right: 0,
    height: isMobile ? '60px' : '80px',
    background: 'linear-gradient(180deg, transparent, rgba(99, 102, 241, 0.4), rgba(139, 92, 246, 0.4), transparent)',
    boxShadow: '0 0 40px rgba(99, 102, 241, 0.6)',
    animation: 'scanBeam 1.2s ease-in-out infinite',
    filter: 'blur(2px)',
  },
  scanStatus: {
    marginTop: isMobile ? '16px' : '24px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '12px',
    fontSize: isMobile ? '14px' : '16px',
    color: '#cbd5e1',
    fontWeight: '500',
  },
  scanPulse: {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    background: '#6366f1',
    boxShadow: '0 0 12px rgba(99, 102, 241, 0.8)',
    animation: 'pulse 1.5s ease-in-out infinite',
  },
  scanBar: {
    position: 'absolute',
    left: 0,
    right: 0,
    height: '3px',
    background: 'linear-gradient(90deg, transparent, #6366f1, transparent)',
    animation: 'scan 2s ease-in-out infinite',
  },
  previewCard: {
    background: 'rgba(99, 102, 241, 0.1)',
    border: '2px solid rgba(99, 102, 241, 0.3)',
    borderRadius: '12px',
    padding: isMobile ? '20px' : '32px',
    marginBottom: '20px',
  },
  terminalPanel: {
    background: 'rgba(10, 14, 27, 0.9)',
    border: '1px solid rgba(99, 102, 241, 0.3)',
    borderRadius: '12px',
    padding: isMobile ? '16px' : '24px',
    maxHeight: isMobile ? '300px' : '400px',
    overflow: 'auto',
    textAlign: 'left',
    fontFamily: 'monospace',
    fontSize: isMobile ? '11px' : '13px',
    lineHeight: '1.8',
    color: '#cbd5e1',
  },
  skillGrid: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: isMobile ? '8px' : '12px',
    justifyContent: 'center',
    marginTop: isMobile ? '16px' : '24px',
  },
  animatedChip: {
    padding: isMobile ? '8px 14px' : '10px 18px',
    background: 'rgba(16, 185, 129, 0.15)',
    border: '1px solid rgba(16, 185, 129, 0.4)',
    borderRadius: '20px',
    fontSize: isMobile ? '11px' : '13px',
    color: '#10b981',
    fontWeight: '600',
    animation: 'slideIn 0.4s ease',
  },
  keywordChipAnimated: {
    padding: isMobile ? '8px 14px' : '10px 18px',
    background: 'rgba(99, 102, 241, 0.15)',
    border: '1px solid rgba(99, 102, 241, 0.4)',
    borderRadius: '20px',
    fontSize: isMobile ? '11px' : '13px',
    color: '#818cf8',
    fontWeight: '600',
    animation: 'slideIn 0.4s ease',
  },
  successBanner: {
    background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%)',
    border: '1px solid rgba(16, 185, 129, 0.5)',
    borderRadius: '12px',
    padding: isMobile ? '16px' : '24px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '12px',
    fontSize: isMobile ? '14px' : '16px',
    color: '#10b981',
    fontWeight: '600',
  },
  textDisplayGrid: {
    display: 'grid',
    gridTemplateColumns: isMobile ? '1fr' : isTablet ? '1fr' : 'repeat(2, 1fr)',
    gap: isMobile ? '16px' : '24px',
    marginBottom: isMobile ? '20px' : '32px',
  },
  textDisplayCard: {
    background: 'rgba(15, 20, 40, 0.7)',
    border: '1px solid rgba(99, 102, 241, 0.2)',
    borderRadius: isMobile ? '12px' : '16px',
    padding: isMobile ? '16px' : '24px',
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
    transition: 'all 0.3s ease',
    maxHeight: isMobile ? '300px' : '400px',
    display: 'flex',
    flexDirection: 'column',
  },
  textDisplayCardHover: {
    transform: isMobile ? 'none' : 'translateY(-2px)',
    boxShadow: '0 12px 40px rgba(99, 102, 241, 0.2)',
  },
  textDisplayTitle: {
    fontSize: isMobile ? '12px' : '14px',
    fontWeight: '700',
    color: '#cbd5e1',
    marginBottom: isMobile ? '12px' : '16px',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
  },
  textDisplayContent: {
    flex: 1,
    overflow: 'auto',
    background: 'rgba(10, 14, 27, 0.6)',
    borderRadius: '12px',
    padding: isMobile ? '12px' : '20px',
    fontSize: isMobile ? '11px' : '13px',
    lineHeight: '1.8',
    color: '#94a3b8',
    whiteSpace: 'pre-wrap',
    wordWrap: 'break-word',
    fontFamily: 'monospace',
  },
  shimmerPanel: {
    background: 'rgba(15, 20, 40, 0.8)',
    border: '1px solid rgba(99, 102, 241, 0.3)',
    borderRadius: '12px',
    padding: isMobile ? '20px' : '32px',
    position: 'relative',
    overflow: 'hidden',
  },
  shimmer: {
    position: 'absolute',
    top: 0,
    left: '-100%',
    width: '100%',
    height: '100%',
    background: 'linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.3), transparent)',
    animation: 'shimmer 2s ease-in-out infinite',
  },
  tablePreview: {
    background: 'rgba(10, 14, 27, 0.9)',
    border: '1px solid rgba(99, 102, 241, 0.3)',
    borderRadius: '12px',
    padding: isMobile ? '12px' : '20px',
    textAlign: 'left',
    fontSize: isMobile ? '11px' : '12px',
    color: '#cbd5e1',
    maxHeight: isMobile ? '200px' : '300px',
    overflow: 'auto',
  },
  tableRow: {
    padding: isMobile ? '6px 0' : '8px 0',
    borderBottom: '1px solid rgba(99, 102, 241, 0.2)',
  },
  pulsingDots: {
    display: 'inline-flex',
    gap: '4px',
    marginLeft: '8px',
  },
  dot: {
    width: '6px',
    height: '6px',
    borderRadius: '50%',
    background: '#6366f1',
    animation: 'pulse 1.4s ease-in-out infinite',
  },
  nlpDebugSection: {
    marginTop: isMobile ? '24px' : '40px',
    marginBottom: isMobile ? '24px' : '40px',
  },
  nlpDebugHeader: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: isMobile ? '16px 20px' : '20px 32px',
    background: 'rgba(15, 20, 40, 0.7)',
    border: '1px solid rgba(99, 102, 241, 0.2)',
    borderRadius: isMobile ? '12px' : '16px',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    marginBottom: '16px',
  },
  nlpDebugHeaderHover: {
    background: 'rgba(15, 20, 40, 0.9)',
    border: '1px solid rgba(99, 102, 241, 0.4)',
    transform: isMobile ? 'none' : 'translateY(-1px)',
    boxShadow: '0 8px 24px rgba(99, 102, 241, 0.2)',
  },
  nlpDebugTitle: {
    fontSize: isMobile ? '14px' : '16px',
    fontWeight: '700',
    color: '#e2e8f0',
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    letterSpacing: '-0.01em',
  },
  nlpDebugToggle: {
    fontSize: isMobile ? '18px' : '20px',
    color: '#6366f1',
    transition: 'transform 0.3s ease',
  },
  nlpDebugToggleExpanded: {
    transform: 'rotate(180deg)',
  },
  nlpDebugContent: {
    display: 'grid',
    gridTemplateColumns: isMobile ? '1fr' : isTablet ? '1fr' : 'repeat(2, 1fr)',
    gap: isMobile ? '16px' : '24px',
  },
  nlpCard: {
    background: 'rgba(15, 20, 40, 0.7)',
    border: '1px solid rgba(99, 102, 241, 0.2)',
    borderRadius: isMobile ? '12px' : '16px',
    padding: isMobile ? '20px' : '28px',
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
    transition: 'all 0.3s ease',
  },
  nlpCardHover: {
    transform: isMobile ? 'none' : 'translateY(-2px)',
    boxShadow: '0 12px 40px rgba(99, 102, 241, 0.2)',
  },
  nlpCardTitle: {
    fontSize: isMobile ? '12px' : '13px',
    fontWeight: '700',
    color: '#cbd5e1',
    marginBottom: isMobile ? '12px' : '16px',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  nlpTextPreview: {
    background: 'rgba(10, 14, 27, 0.6)',
    borderRadius: '12px',
    padding: isMobile ? '12px' : '16px',
    fontSize: isMobile ? '11px' : '12px',
    lineHeight: '1.8',
    color: '#94a3b8',
    maxHeight: isMobile ? '150px' : '200px',
    overflow: 'auto',
    whiteSpace: 'pre-wrap',
    wordWrap: 'break-word',
    fontFamily: 'monospace',
    marginBottom: '16px',
  },
  nlpMetaBadge: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '6px',
    padding: isMobile ? '5px 10px' : '6px 12px',
    background: 'rgba(139, 92, 246, 0.12)',
    border: '1px solid rgba(139, 92, 246, 0.3)',
    borderRadius: '8px',
    fontSize: '11px',
    color: '#a78bfa',
    fontWeight: '600',
    marginTop: '8px',
  },
  adminBtn: {
    padding: isMobile ? '6px 12px' : '8px 16px',
    background: 'rgba(139, 92, 246, 0.15)',
    border: '1px solid rgba(139, 92, 246, 0.3)',
    borderRadius: '8px',
    color: '#8b5cf6',
    fontSize: isMobile ? '11px' : '12px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
  },
  successCheckmark: {
    fontSize: isMobile ? '24px' : '32px',
  },
});

export default function Dashboard() {
  const { isMobile, isTablet } = useWindowSize();
  const styles = getResponsiveStyles(isMobile, isTablet);

  const [file, setFile] = useState(null)
  const [jd, setJd] = useState("")
  const [jdFile, setJdFile] = useState(null)
  const [jdInputMode, setJdInputMode] = useState("text")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [isAdmin, setIsAdmin] = useState(false)
  const [uploadHover, setUploadHover] = useState(false)
  const [jdUploadHover, setJdUploadHover] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const [jdDragActive, setJdDragActive] = useState(false)
  const [textareaFocus, setTextareaFocus] = useState(false)
  const [hoveredCard, setHoveredCard] = useState(null)
  const [filePreviewHover, setFilePreviewHover] = useState(false)
  const [replaceBtnHover, setReplaceBtnHover] = useState(false)
  const [stage, setStage] = useState(0)
  const [processingData, setProcessingData] = useState(null)
  const [displayedText, setDisplayedText] = useState("")
  const [displayedSkills, setDisplayedSkills] = useState([])
  const [displayedKeywords, setDisplayedKeywords] = useState([])
  const [displayedFields, setDisplayedFields] = useState([])
  const [filePreviewUrl, setFilePreviewUrl] = useState(null)
  const [scanDots, setScanDots] = useState("")
  const [skillQueue, setSkillQueue] = useState([])
  const [keywordQueue, setKeywordQueue] = useState([])
  const navigate = useNavigate()
  const { logout } = useAuth()
  const [isGeneratingPDF, setIsGeneratingPDF] = useState(false)

  const generatePDF = () => {
    if (!result) return;

    setIsGeneratingPDF(true);

    try {
      const doc = new jsPDF();

      const pageWidth = doc.internal.pageSize.getWidth();
      const margin = 14;

      doc.setFontSize(22);
      doc.setTextColor(30, 41, 59);
      doc.text("SkillMatch Exec Analysis Report", margin, 20);

      doc.setFontSize(12);
      doc.setTextColor(100, 116, 139);
      const dateStr = new Date().toLocaleDateString();
      doc.text(`Generated: ${dateStr}`, margin, 28);

      doc.setDrawColor(226, 232, 240);
      doc.line(margin, 32, pageWidth - margin, 32);

      doc.setFontSize(16);
      doc.setTextColor(15, 23, 42);
      doc.text("Candidate Profile", margin, 42);

      doc.setFontSize(11);
      doc.setTextColor(71, 85, 105);
      doc.text(`Name: ${result.resume_profile?.candidate_name || 'Not Detected'}`, margin, 50);
      doc.text(`Email: ${result.resume_profile?.contact?.email || 'Not Extracted'}`, margin, 56);
      const expStr = result.resume_profile?.experience?.years_estimated ? `${result.resume_profile.experience.years_estimated} years` : 'Not Specified';
      doc.text(`Estimated Experience: ${expStr}`, margin, 62);

      doc.setFontSize(16);
      doc.setTextColor(15, 23, 42);
      doc.text("Job Role Match", margin, 76);

      doc.setFontSize(11);
      doc.setTextColor(71, 85, 105);
      doc.text(`Target Role: ${result.job_profile?.role || 'Not Specified'}`, margin, 84);

      const matchScore = result.comparison?.match_percentage || 0;
      doc.setFontSize(14);
      doc.setTextColor(matchScore >= 75 ? 34 : (matchScore >= 50 ? 217 : 220), matchScore >= 75 ? 197 : (matchScore >= 50 ? 119 : 38), matchScore >= 75 ? 94 : (matchScore >= 50 ? 6 : 38));
      doc.text(`Match Score: ${matchScore.toFixed(1)}%`, margin, 92);

      if (result.comparison?.recommendation) {
        doc.setFontSize(11);
        doc.setTextColor(71, 85, 105);
        doc.text(`System Verdict: ${result.comparison.recommendation}`, margin, 98);
      }

      if (result.comparison?.experience_gap_warning) {
        doc.setFontSize(10);
        doc.setTextColor(220, 38, 38);
        doc.text(`Warning: ${result.comparison.experience_gap_warning}`, margin, 106);
      }

      doc.autoTable({
        startY: 114,
        head: [['Matching Category', 'Skills']],
        body: [
          ['Matched Core Skills', result.comparison?.matched_skills?.join(', ') || 'None'],
          ['Missing Core Skills', result.comparison?.missing_skills?.join(', ') || 'None'],
          ['Additional Skills (Bonus)', result.comparison?.additional_skills?.join(', ') || 'None']
        ],
        theme: 'grid',
        headStyles: { fillColor: [99, 102, 241] },
        styles: { fontSize: 10, cellPadding: 4 },
        columnStyles: { 0: { cellWidth: 50 } }
      });

      if (result.skill_suggestions && result.skill_suggestions.suggested_skills?.length > 0) {
        doc.addPage();
        doc.setFontSize(16);
        doc.setTextColor(15, 23, 42);
        doc.text("AI Skill Recommendations", margin, 20);

        doc.setFontSize(10);
        doc.setTextColor(100, 116, 139);
        doc.text("Based on industry trends and the provided Job Description, prioritizing these skills will improve competitiveness.", margin, 28, { maxWidth: pageWidth - (margin * 2) });

        const suggestionRows = result.skill_suggestions.suggested_skills.map(s => [
          s.skill,
          s.priority,
          s.reason,
          s.explanation
        ]);

        doc.autoTable({
          startY: 38,
          head: [['Skill', 'Priority', 'Reason', 'Explanation']],
          body: suggestionRows,
          theme: 'striped',
          headStyles: { fillColor: [139, 92, 246] },
          styles: { fontSize: 9, cellPadding: 4 },
          columnStyles: {
            0: { cellWidth: 30, fontStyle: 'bold' },
            1: { cellWidth: 20 },
            2: { cellWidth: 40 },
            3: { cellWidth: 'auto' }
          }
        });
      }

      const pageCount = doc.internal.getNumberOfPages();
      for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(150);
        doc.text(`Page ${i} of ${pageCount} | Generated by SkillMatch AI`, margin, doc.internal.pageSize.getHeight() - 10);
      }

      doc.save(`SkillMatch_Analysis_${result.resume_profile?.candidate_name?.replace(/[^a-z0-9]/gi, '_').toLowerCase() || 'Report'}.pdf`);
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Failed to generate PDF report.');
    } finally {
      setIsGeneratingPDF(false);
    }
  }

  const userEmail = localStorage.getItem('user_email') || ''

  useEffect(() => {
    checkAdminStatus()
  }, [])

  const checkAdminStatus = async () => {
    try {
      const data = await api.get('/admin/validate')
      if (data) {
        setIsAdmin(data.is_admin)
      }
    } catch (error) {
      console.error('Admin check error:', error)
    }
  }

  const handleLogout = () => {
    logout()
  }

  useEffect(() => {
    const savedResult = localStorage.getItem('skillmatch_result')
    if (savedResult) {
      try {
        const parsed = JSON.parse(savedResult)
        setResult(parsed)
      } catch (e) {
        localStorage.removeItem('skillmatch_result')
      }
    }
  }, [])

  useEffect(() => {
    if (result) {
      localStorage.setItem('skillmatch_result', JSON.stringify(result))
    }
  }, [result])

  useEffect(() => {
    if (!processingData) return

    if (stage === 1) {
      let dotCount = 0
      const dotInterval = setInterval(() => {
        dotCount = (dotCount + 1) % 4
        setScanDots('.'.repeat(dotCount))
      }, 400)

      const timer = setTimeout(() => {
        setStage(2)
        clearInterval(dotInterval)
        setScanDots("")
      }, 3000)

      return () => {
        clearTimeout(timer)
        clearInterval(dotInterval)
      }
    }
    if (stage === 2) {
      const textSnapshot = processingData?.resume_preprocessed?.clean_text || ""
      if (!textSnapshot) {
        setStage(0)
        setLoading(false)
        return
      }
      let charIndex = 0
      const totalLength = textSnapshot.length
      const interval = setInterval(() => {
        if (charIndex < totalLength) {
          setDisplayedText(textSnapshot.substring(0, charIndex + 1))
          charIndex += Math.floor(Math.random() * 8) + 3
        } else {
          clearInterval(interval)
          setTimeout(() => setStage(3), 800)
        }
      }, 15)
      return () => clearInterval(interval)
    }
    if (stage === 3) {
      const skillsSnapshot = processingData?.resume_skills_extracted || []
      if (!skillsSnapshot.length) {
        setStage(4)
        return
      }
      setSkillQueue([...skillsSnapshot])
      setDisplayedSkills([])
      let queueCopy = [...skillsSnapshot]
      const interval = setInterval(() => {
        if (queueCopy.length > 0) {
          const nextSkill = queueCopy.shift()
          setDisplayedSkills(prev => [...prev, nextSkill])
        } else {
          clearInterval(interval)
          setTimeout(() => setStage(4), 1000)
        }
      }, 220)
      return () => clearInterval(interval)
    }
    if (stage === 4) {
      const fields = [
        { label: 'Name', value: processingData?.resume_profile?.candidate_name },
        { label: 'Email', value: processingData?.resume_profile?.contact?.email },
        { label: 'Phone', value: processingData?.resume_profile?.contact?.phone },
        { label: 'Location', value: processingData?.resume_profile?.contact?.location },
        { label: 'Education', value: processingData?.resume_profile?.education?.degrees?.length > 0 ? processingData.resume_profile.education.degrees.join(', ') : null },
        { label: 'Experience', value: processingData?.resume_profile?.experience?.years_estimated ? `${processingData.resume_profile.experience.years_estimated} years` : null }
      ].filter(f => f && f.value)

      let index = 0
      const interval = setInterval(() => {
        if (index < fields.length) {
          setDisplayedFields(prev => [...prev, fields[index]])
          index++
        } else {
          clearInterval(interval)
          setTimeout(() => setStage(5), 1000)
        }
      }, 300)
      return () => clearInterval(interval)
    }
    if (stage === 5) {
      const timer = setTimeout(() => setStage(6), 2500)
      return () => clearTimeout(timer)
    }
    if (stage === 6) {
      const keywordsSnapshot = processingData?.jd_skills_extracted || []
      if (!keywordsSnapshot.length) {
        setStage(7)
        return
      }
      setKeywordQueue([...keywordsSnapshot])
      setDisplayedKeywords([])
      let queueCopy = [...keywordsSnapshot]
      const interval = setInterval(() => {
        if (queueCopy.length > 0) {
          const nextKeyword = queueCopy.shift()
          setDisplayedKeywords(prev => [...prev, nextKeyword])
        } else {
          clearInterval(interval)
          setTimeout(() => setStage(7), 1000)
        }
      }, 180)
      return () => clearInterval(interval)
    }
    if (stage === 7) {
      const timer = setTimeout(() => {
        setStage(0)
        setResult(processingData)
        setLoading(false)
        setSkillQueue([])
        setKeywordQueue([])
        if (filePreviewUrl) URL.revokeObjectURL(filePreviewUrl)
        setFilePreviewUrl(null)
      }, 800)
      return () => clearTimeout(timer)
    }
  }, [stage, processingData, filePreviewUrl])

  const submit = async () => {
    if (!file || (!jd && !jdFile)) return

    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login')
      return
    }

    const previewUrl = URL.createObjectURL(file)
    setFilePreviewUrl(previewUrl)

    setResult(null)
    setProcessingData(null)
    setLoading(true)
    setStage(1)
    setDisplayedText("")
    setDisplayedSkills([])
    setDisplayedKeywords([])
    setDisplayedFields([])
    setSkillQueue([])
    setKeywordQueue([])

    const form = new FormData()
    form.append("resume", file)

    if (jdFile) {
      form.append("jd_file", jdFile)
    } else if (jd) {
      form.append("job_description", jd)
    }

    try {
      const data = await api.post('/analyze', form)
      if (data) {
        setProcessingData(data)
      }
    } catch (err) {
      alert(err.message || "Failed to process resume")
      setLoading(false)
      setStage(0)
    }
  }

  const handleDrag = e => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = e => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    const f = e.dataTransfer.files?.[0]
    if (f) setFile(f)
  }

  const handleJdDrag = e => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setJdDragActive(true)
    } else if (e.type === "dragleave") {
      setJdDragActive(false)
    }
  }

  const handleJdDrop = e => {
    e.preventDefault()
    e.stopPropagation()
    setJdDragActive(false)
    const f = e.dataTransfer.files?.[0]
    if (f) setJdFile(f)
  }

  const formatFileSize = bytes => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
  }

  const getFileIcon = name => {
    const ext = name.split('.').pop().toLowerCase()
    if (ext === 'pdf') return '📄'
    if (ext === 'docx' || ext === 'doc') return '📝'
    if (ext === 'jpg' || ext === 'jpeg' || ext === 'png') return '🖼️'
    return '📋'
  }

  return (
    <div style={styles.app}>
      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes scan {
          0% { top: 0; }
          100% { top: 100%; }
        }
        @keyframes slideIn {
          from { 
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        @keyframes shimmer {
          0% { left: -100%; }
          100% { left: 100%; }
        }
        @keyframes scanBeam {
          0% { top: -80px; }
        @keyframes fadeOut {
          0% {
            opacity: 1;
            transform: translateY(0);
          }
          100% {
            opacity: 0;
            transform: translateY(-10px);
          }
        }
          100% { top: 100%; }
        }
      `}</style>

      {loading && stage > 0 && (
        <div style={styles.overlay}>
          <div style={styles.overlayContent}>
            {stage === 1 && (
              <>
                <div style={styles.scanPanel}>
                  <div style={styles.previewContainer}>
                    {file.type === 'application/pdf' && (
                      <iframe
                        src={filePreviewUrl}
                        style={styles.previewFrame}
                        title="PDF Preview"
                      />
                    )}
                    {(file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/jpg') && (
                      <img
                        src={filePreviewUrl}
                        alt="Resume Preview"
                        style={styles.previewImage}
                      />
                    )}
                    {file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' && (
                      <div style={styles.docPreview}>
                        <div style={{ fontSize: '18px', fontWeight: '700', marginBottom: '20px', color: '#111' }}>
                          {file.name}
                        </div>
                        <div style={{ color: '#333', whiteSpace: 'pre-wrap' }}>
                          {processingData?.resume_preprocessed?.clean_text?.substring(0, 800) || 'Loading document preview...'}
                        </div>
                      </div>
                    )}
                    <div style={styles.scanOverlay}>
                      <div style={styles.scanBeam}></div>
                    </div>
                  </div>
                  <div style={styles.scanStatus}>
                    <div style={styles.scanPulse}></div>
                    <span>Scanning resume document{scanDots}</span>
                  </div>
                </div>
              </>
            )}

            {stage === 2 && (
              <>
                <div style={styles.stageTitle}>Extracting resume text</div>
                <div style={styles.terminalPanel}>
                  {displayedText}
                </div>
              </>
            )}

            {stage === 3 && (
              <>
                <div style={styles.stageTitle}>Extracting technical skills and tools</div>
                <div style={styles.skillGrid}>
                  {displayedSkills.map((s, i) => (
                    <div key={i} style={{ ...styles.animatedChip, animationDelay: `${i * 0.08}s` }}>{s}</div>
                  ))}
                </div>
              </>
            )}

            {stage === 4 && (
              <>
                <div style={styles.stageTitle}>Extracting structured personal data</div>
                <div style={styles.tablePreview}>
                  {displayedFields.filter(f => f && f.label && f.value).map((field, i) => (
                    <div key={i} style={{
                      ...styles.tableRow,
                      animation: 'slideIn 0.4s ease',
                      animationDelay: `${i * 0.1}s`,
                      animationFillMode: 'backwards'
                    }}>
                      <strong>{field.label}:</strong> {field.value}
                    </div>
                  ))}
                </div>
              </>
            )}

            {stage === 5 && (
              <>
                <div style={styles.stageTitle}>Analyzing job description</div>
                <div style={styles.shimmerPanel}>
                  <div style={styles.shimmer}></div>
                  <div style={{ fontSize: '14px', color: '#cbd5e1', lineHeight: '1.8', textAlign: 'left' }}>
                    {(processingData?.cleaned_job_description_text || jd).substring(0, 400)}...
                  </div>
                </div>
              </>
            )}

            {stage === 6 && (
              <>
                <div style={styles.stageTitle}>Extracting role requirements</div>
                <div style={styles.skillGrid}>
                  {displayedKeywords.map((k, i) => (
                    <div key={i} style={{ ...styles.keywordChipAnimated, animationDelay: `${i * 0.08}s` }}>{k}</div>
                  ))}
                </div>
              </>
            )}

            {stage === 7 && (
              <div style={styles.successBanner}>
                <div style={styles.successCheckmark}>✓</div>
                <div>Document intelligence extraction complete</div>
              </div>
            )}
          </div>
        </div>
      )}

      <div style={styles.nav}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <div style={styles.logo}>SkillMatch AI</div>
          <span style={styles.tagline}>Where Skills Meet Opportunities</span>
        </div>
        <div style={styles.navRight}>
          {isAdmin && (
            <button
              onClick={() => navigate('/admin')}
              style={styles.adminBtn}
            >
              Admin Dashboard
            </button>
          )}
          <div style={styles.userEmail}>{userEmail}</div>
          <button style={styles.logoutBtn} onClick={handleLogout}>Logout</button>
        </div>
      </div>

      <div style={styles.hero}>
        <div style={styles.heroTitle}>SkillMatch Dashboard</div>
        <div style={styles.heroSubtitle}>
          Resume parsing, skill extraction, and keyword intelligence for enterprise hiring workflows
        </div>
        <div style={styles.divider}></div>
      </div>

      <div style={styles.container}>
        <div style={styles.grid}>
          <div
            style={{
              ...styles.card,
              ...(hoveredCard === 'upload' ? styles.cardHover : {})
            }}
            onMouseEnter={() => setHoveredCard('upload')}
            onMouseLeave={() => setHoveredCard(null)}
          >
            <div style={styles.sectionTitle}>
              <span>📄</span> Resume Intake
            </div>

            {!file ? (
              <label
                style={{
                  ...styles.uploadZone,
                  ...((uploadHover || dragActive) ? styles.uploadZoneActive : {})
                }}
                onMouseEnter={() => setUploadHover(true)}
                onMouseLeave={() => setUploadHover(false)}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <input
                  type="file"
                  onChange={e => setFile(e.target.files[0])}
                  style={{ display: 'none' }}
                  accept=".pdf,.docx,.jpg,.png"
                />
                <div style={{
                  ...styles.uploadIconWrapper,
                  ...((uploadHover || dragActive) ? styles.uploadIconWrapperActive : {})
                }}>
                  <div style={styles.uploadIcon}>
                    {dragActive ? '📥' : '☁️'}
                  </div>
                </div>
                <div style={styles.uploadTextPrimary}>
                  {dragActive ? 'Drop your resume here' : 'Upload Resume'}
                </div>
                <div style={styles.uploadTextSecondary}>
                  Click to browse or drag and drop your file
                </div>
                <div style={styles.fileTypes}>
                  <span style={styles.fileTypeBadge}>PDF</span>
                  <span style={styles.fileTypeBadge}>DOCX</span>
                  <span style={styles.fileTypeBadge}>JPG</span>
                  <span style={styles.fileTypeBadge}>PNG</span>
                </div>
              </label>
            ) : (
              <div
                style={{
                  ...styles.filePreview,
                  ...(filePreviewHover ? styles.filePreviewHover : {})
                }}
                onMouseEnter={() => setFilePreviewHover(true)}
                onMouseLeave={() => setFilePreviewHover(false)}
              >
                <div style={styles.fileInfo}>
                  <div style={styles.fileIconCircle}>{getFileIcon(file.name)}</div>
                  <div style={styles.fileDetails}>
                    <div style={styles.fileName}>{file.name}</div>
                    <div style={styles.fileSize}>{formatFileSize(file.size)}</div>
                  </div>
                </div>
                <button
                  style={{
                    ...styles.replaceBtn,
                    ...(replaceBtnHover ? styles.replaceBtnHover : {})
                  }}
                  onClick={() => setFile(null)}
                  onMouseEnter={() => setReplaceBtnHover(true)}
                  onMouseLeave={() => setReplaceBtnHover(false)}
                >
                  ✕ Replace File
                </button>
              </div>
            )}
          </div>

          <div
            style={{
              ...styles.card,
              ...(hoveredCard === 'jd' ? styles.cardHover : {})
            }}
            onMouseEnter={() => setHoveredCard('jd')}
            onMouseLeave={() => setHoveredCard(null)}
          >
            <div style={styles.sectionTitle}>
              <span>📋</span> Job Description Input
            </div>

            <div style={styles.modeToggle}>
              <button
                style={{
                  ...styles.modeButton,
                  ...(jdInputMode === 'text' ? styles.modeButtonActive : {})
                }}
                onClick={() => {
                  setJdInputMode('text')
                  setJdFile(null)
                }}
              >
                ✍️ Type Text
              </button>
              <button
                style={{
                  ...styles.modeButton,
                  ...(jdInputMode === 'file' ? styles.modeButtonActive : {})
                }}
                onClick={() => {
                  setJdInputMode('file')
                  setJd('')
                }}
              >
                📄 Upload File
              </button>
            </div>

            {jdInputMode === 'text' ? (
              <>
                <div style={styles.textareaLabel}>
                  Paste or type the complete job description below
                </div>

                <textarea
                  value={jd}
                  onChange={e => setJd(e.target.value)}
                  onFocus={() => setTextareaFocus(true)}
                  onBlur={() => setTextareaFocus(false)}
                  style={{
                    ...styles.textarea,
                    ...(textareaFocus ? styles.textareaFocus : {})
                  }}
                  placeholder="We are seeking a skilled Data Scientist with expertise in machine learning, Python, SQL, and experience deploying AI models in production environments. Strong communication skills required."
                />

                <div style={styles.textareaHint}>
                  💡 Include skills, qualifications, responsibilities, and requirements for best keyword extraction
                </div>

                <div style={styles.charCounter}>
                  {jd.length} characters
                </div>
              </>
            ) : (
              <>
                {!jdFile ? (
                  <div
                    onDragEnter={handleJdDrag}
                    onDragOver={handleJdDrag}
                    onDragLeave={handleJdDrag}
                    onDrop={handleJdDrop}
                    onClick={() => document.getElementById('jdInput').click()}
                    style={{
                      ...styles.uploadZone,
                      ...(jdUploadHover || jdDragActive ? styles.uploadZoneActive : {})
                    }}
                    onMouseEnter={() => setJdUploadHover(true)}
                    onMouseLeave={() => setJdUploadHover(false)}
                  >
                    <input
                      type="file"
                      id="jdInput"
                      accept=".pdf,.docx,.txt"
                      style={{ display: 'none' }}
                      onChange={e => setJdFile(e.target.files[0])}
                    />

                    <div style={{
                      ...styles.uploadIconWrapper,
                      ...(jdUploadHover || jdDragActive ? styles.uploadIconWrapperActive : {})
                    }}>
                      <span style={styles.uploadIcon}>📋</span>
                    </div>

                    <div style={styles.uploadTextPrimary}>
                      Drop JD file here or click to browse
                    </div>

                    <div style={styles.uploadTextSecondary}>
                      Supports PDF, DOCX, and TXT formats
                    </div>

                    <div style={styles.fileTypes}>
                      <span style={styles.fileTypeBadge}>PDF</span>
                      <span style={styles.fileTypeBadge}>DOCX</span>
                      <span style={styles.fileTypeBadge}>TXT</span>
                    </div>
                  </div>
                ) : (
                  <div style={styles.filePreview}>
                    <div style={styles.fileInfo}>
                      <div style={styles.fileIconCircle}>{getFileIcon(jdFile.name)}</div>
                      <div style={styles.fileDetails}>
                        <div style={styles.fileName}>{jdFile.name}</div>
                        <div style={styles.fileSize}>{formatFileSize(jdFile.size)}</div>
                      </div>
                    </div>
                    <button
                      onClick={() => setJdFile(null)}
                      style={{
                        ...styles.replaceBtn,
                        ...(replaceBtnHover ? styles.replaceBtnHover : {})
                      }}
                      onMouseEnter={() => setReplaceBtnHover(true)}
                      onMouseLeave={() => setReplaceBtnHover(false)}
                    >
                      ✕ Replace
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
        </div>

        <div style={styles.actionSection}>
          <button
            onClick={submit}
            disabled={!file || (!jd && !jdFile) || loading}
            style={{
              ...styles.primaryBtn,
              ...(loading ? styles.primaryBtnDisabled : {}),
              ...(!file || (!jd && !jdFile) ? styles.primaryBtnDisabled : {})
            }}
            onMouseEnter={e => {
              if (!loading && file && (jd || jdFile)) {
                Object.assign(e.target.style, styles.primaryBtnHover)
              }
            }}
            onMouseLeave={e => {
              e.target.style.transform = ''
              e.target.style.boxShadow = '0 8px 24px rgba(99, 102, 241, 0.4)'
            }}
          >
            {loading && <span style={styles.loader}></span>}
            {loading ? 'Extracting Intelligence...' : 'Extract Resume Intelligence'}
          </button>
        </div>

        {result && (
          <div id="skillmatch-report" style={{ position: 'relative', padding: isGeneratingPDF ? '20px' : '0' }}>
            {!isGeneratingPDF && (
              <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '20px' }}>
                <button
                  onClick={generatePDF}
                  style={{
                    background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '8px',
                    padding: '12px 24px',
                    fontSize: '14px',
                    fontWeight: '600',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    boxShadow: '0 4px 12px rgba(16, 185, 129, 0.3)',
                    transition: 'all 0.2s ease'
                  }}
                  onMouseEnter={e => {
                    e.target.style.transform = 'translateY(-2px)'
                    e.target.style.boxShadow = '0 6px 16px rgba(16, 185, 129, 0.4)'
                  }}
                  onMouseLeave={e => {
                    e.target.style.transform = 'translateY(0)'
                    e.target.style.boxShadow = '0 4px 12px rgba(16, 185, 129, 0.3)'
                  }}
                >
                  📥 Download PDF Report
                </button>
              </div>
            )}

            <div
              style={{
                ...styles.card,
                ...(hoveredCard === 'nlpPreview' ? styles.cardHover : {}),
                marginBottom: '32px'
              }}
              onMouseEnter={() => setHoveredCard('nlpPreview')}
              onMouseLeave={() => setHoveredCard(null)}
            >
              <div style={styles.sectionTitle}>
                <span>🔬</span> NLP Processing Preview
              </div>

              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(2, 1fr)',
                gap: '24px'
              }}>
                <div>
                  <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '12px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Processed Resume</div>
                  <div style={{
                    background: 'rgba(10, 14, 27, 0.6)',
                    borderRadius: '12px',
                    padding: '16px',
                    fontSize: '12px',
                    lineHeight: '1.8',
                    color: '#94a3b8',
                    whiteSpace: 'pre-wrap',
                    wordWrap: 'break-word',
                    fontFamily: 'monospace',
                    marginBottom: '16px'
                  }}>
                    {result.resume_preprocessed?.clean_text || 'No processed text'}
                  </div>
                  <div style={{ fontSize: '12px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Extracted Skills</div>
                  <div style={styles.chipContainer}>
                    {result.resume_skills_extracted?.slice(0, 12).map(s => (
                      <span key={s} style={styles.skillChip}>{s}</span>
                    ))}
                  </div>
                </div>

                <div>
                  <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '12px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Processed Job Description</div>
                  <div style={{
                    background: 'rgba(10, 14, 27, 0.6)',
                    borderRadius: '12px',
                    padding: '16px',
                    fontSize: '12px',
                    lineHeight: '1.8',
                    color: '#94a3b8',
                    whiteSpace: 'pre-wrap',
                    wordWrap: 'break-word',
                    fontFamily: 'monospace',
                    marginBottom: '16px'
                  }}>
                    {result.jd_preprocessed?.clean_text || 'No processed text'}
                  </div>
                  <div style={{ fontSize: '12px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Extracted Keywords</div>
                  <div style={styles.chipContainer}>
                    {result.jd_skills_extracted?.slice(0, 12).map(k => (
                      <span key={k} style={styles.keywordChip}>{k}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(2, 1fr)',
              gap: '24px',
              marginBottom: '32px'
            }}>
              <div
                style={{
                  ...styles.card,
                  ...(hoveredCard === 'resumeProfile' ? styles.cardHover : {})
                }}
                onMouseEnter={() => setHoveredCard('resumeProfile')}
                onMouseLeave={() => setHoveredCard(null)}
              >
                <div style={styles.sectionTitle}>
                  <span>👤</span> Resume Structured Profile
                </div>

                <div style={{ marginBottom: '20px' }}>
                  <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Personal Information</div>
                  <div style={{ fontSize: '14px', color: '#e2e8f0', lineHeight: '1.8' }}>
                    {result.resume_profile?.candidate_name && result.resume_profile.candidate_name !== 'N/A' && (
                      <div><strong>Name:</strong> {result.resume_profile.candidate_name}</div>
                    )}
                    {result.resume_profile?.contact?.email && result.resume_profile.contact.email !== 'N/A' && (
                      <div><strong>Email:</strong> {result.resume_profile.contact.email}</div>
                    )}
                    {result.resume_profile?.contact?.phone && result.resume_profile.contact.phone !== 'N/A' && (
                      <div><strong>Phone:</strong> {result.resume_profile.contact.phone}</div>
                    )}
                    {result.resume_profile?.contact?.location && result.resume_profile.contact.location !== 'N/A' && (
                      <div><strong>Location:</strong> {result.resume_profile.contact.location}</div>
                    )}
                  </div>
                </div>

                {(result.resume_profile?.education?.degrees?.length > 0 || result.resume_profile?.education?.fields?.length > 0 || result.resume_profile?.education?.institutions?.length > 0) && (
                  <div style={{ marginBottom: '20px' }}>
                    <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Education</div>
                    <div style={{ fontSize: '14px', color: '#e2e8f0', lineHeight: '1.8' }}>
                      {result.resume_profile?.education?.degrees?.map((d, i) => (
                        <div key={i}><strong>{d}</strong></div>
                      ))}
                      {result.resume_profile?.education?.fields?.length > 0 && (
                        <div style={{ marginTop: '4px' }}><strong>Field:</strong> {result.resume_profile.education.fields.join(', ')}</div>
                      )}
                      {result.resume_profile?.education?.institutions?.length > 0 && (
                        <div style={{ marginTop: '4px' }}><strong>Institution:</strong> {result.resume_profile.education.institutions.join(', ')}</div>
                      )}
                    </div>
                  </div>
                )}

                {(result.resume_profile?.experience?.roles?.length > 0 || result.resume_profile?.experience?.years_estimated) && (
                  <div style={{ marginBottom: '20px' }}>
                    <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Experience</div>
                    <div style={{ fontSize: '14px', color: '#e2e8f0', lineHeight: '1.8' }}>
                      {result.resume_profile?.experience?.roles?.slice(0, 3).map((role, i) => (
                        <div key={i}>• {role}</div>
                      ))}
                      {result.resume_profile?.experience?.years_estimated && (
                        <div style={{ marginTop: '8px' }}><strong>Total Experience:</strong> {result.resume_profile.experience.years_estimated} years</div>
                      )}
                    </div>
                  </div>
                )}

                {result.resume_profile?.technical_expertise?.languages?.length > 0 && (
                  <div>
                    <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Programming Languages</div>
                    <div style={styles.chipContainer}>
                      {result.resume_profile.technical_expertise.languages.slice(0, 10).map(l => (
                        <span key={l} style={styles.skillChip}>{l}</span>
                      ))}
                    </div>
                  </div>
                )}

                {result.resume_profile?.technical_expertise?.skills?.length > 0 && (
                  <div style={{ marginTop: '20px' }}>
                    <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Technical Skills</div>
                    <div style={styles.chipContainer}>
                      {result.resume_profile.technical_expertise.skills.slice(0, 10).map(s => (
                        <span key={s} style={styles.skillChip}>{s}</span>
                      ))}
                    </div>
                  </div>
                )}

                {result.resume_profile?.technical_expertise?.frameworks?.length > 0 && (
                  <div style={{ marginTop: '20px' }}>
                    <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Frameworks</div>
                    <div style={styles.chipContainer}>
                      {result.resume_profile.technical_expertise.frameworks.slice(0, 10).map(f => (
                        <span key={f} style={styles.skillChip}>{f}</span>
                      ))}
                    </div>
                  </div>
                )}

                {result.resume_profile?.technical_expertise?.tools?.length > 0 && (
                  <div style={{ marginTop: '20px' }}>
                    <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Tools</div>
                    <div style={styles.chipContainer}>
                      {result.resume_profile.technical_expertise.tools.slice(0, 10).map(t => (
                        <span key={t} style={styles.skillChip}>{t}</span>
                      ))}
                    </div>
                  </div>
                )}

                {result.resume_profile?.technical_expertise?.databases?.length > 0 && (
                  <div style={{ marginTop: '20px' }}>
                    <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Databases</div>
                    <div style={styles.chipContainer}>
                      {result.resume_profile.technical_expertise.databases.slice(0, 10).map(d => (
                        <span key={d} style={styles.skillChip}>{d}</span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div
                style={{
                  ...styles.card,
                  ...(hoveredCard === 'jobProfile' ? styles.cardHover : {})
                }}
                onMouseEnter={() => setHoveredCard('jobProfile')}
                onMouseLeave={() => setHoveredCard(null)}
              >
                <div style={styles.sectionTitle}>
                  <span>💼</span> Job Requirement Profile
                </div>

                <div style={{ marginBottom: '20px' }}>
                  <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Job Role</div>
                  <div style={{ fontSize: '16px', color: '#e2e8f0', fontWeight: '600' }}>
                    {result.job_profile?.role || 'Not specified'}
                  </div>
                </div>

                {result.job_profile?.required_technical?.languages?.length > 0 && (
                  <div style={{ marginBottom: '20px' }}>
                    <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Required Languages</div>
                    <div style={styles.chipContainer}>
                      {result.job_profile.required_technical.languages.map(l => (
                        <span key={l} style={styles.keywordChip}>{l}</span>
                      ))}
                    </div>
                  </div>
                )}

                {result.job_profile?.required_technical?.skills?.length > 0 && (
                  <div style={{ marginBottom: '20px' }}>
                    <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Required Skills</div>
                    <div style={styles.chipContainer}>
                      {result.job_profile.required_technical.skills.map(s => (
                        <span key={s} style={styles.keywordChip}>{s}</span>
                      ))}
                    </div>
                  </div>
                )}

                {result.job_profile?.required_technical?.frameworks?.length > 0 && (
                  <div style={{ marginBottom: '20px' }}>
                    <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Required Frameworks</div>
                    <div style={styles.chipContainer}>
                      {result.job_profile.required_technical.frameworks.map(f => (
                        <span key={f} style={styles.keywordChip}>{f}</span>
                      ))}
                    </div>
                  </div>
                )}

                {result.job_profile?.required_technical?.tools?.length > 0 && (
                  <div style={{ marginBottom: '20px' }}>
                    <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Required Tools</div>
                    <div style={styles.chipContainer}>
                      {result.job_profile.required_technical.tools.map(t => (
                        <span key={t} style={styles.keywordChip}>{t}</span>
                      ))}
                    </div>
                  </div>
                )}

                <div>
                  <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Experience Required</div>
                  <div style={{ fontSize: '14px', color: '#e2e8f0', lineHeight: '1.8' }}>
                    <div><strong>Years:</strong> {result.job_profile?.requirements?.experience_years || 'Not specified'}</div>
                    {result.job_profile?.requirements?.education?.length > 0 && (
                      <div><strong>Education:</strong> {result.job_profile.requirements.education.join(', ')}</div>
                    )}
                  </div>
                </div>
              </div>

              {result.comparison && (
                <div
                  style={{
                    ...styles.card,
                    ...(hoveredCard === 'comparison' ? styles.cardHover : {}),
                    gridColumn: '1 / -1'
                  }}
                  onMouseEnter={() => setHoveredCard('comparison')}
                  onMouseLeave={() => setHoveredCard(null)}
                >
                  <div style={styles.sectionTitle}>
                    <span>⚖️</span> Profile Comparison Analysis
                  </div>

                  <div style={{ marginBottom: '24px', padding: '16px', background: 'rgba(74, 222, 128, 0.1)', borderRadius: '8px', border: '1px solid rgba(74, 222, 128, 0.3)' }}>
                    <div style={{ fontSize: '14px', color: '#64748b', fontWeight: '600', marginBottom: '4px' }}>Core Match Percentage</div>
                    <div style={{ fontSize: '28px', color: '#4ade80', fontWeight: '700' }}>
                      {result.comparison.match_percentage !== undefined ? result.comparison.match_percentage.toFixed(1) : '0.0'}%
                    </div>
                    {result.comparison.recommendation && (
                      <div style={{ marginTop: '12px', fontSize: '16px', fontWeight: '600', color: result.comparison.recommendation.includes('Strong Fit') || result.comparison.recommendation.includes('Good Skill Match') ? '#4ade80' : result.comparison.recommendation.includes('Partial Match') ? '#fb923c' : '#ef4444' }}>
                        {(result.comparison.recommendation.includes('Strong Fit') || result.comparison.recommendation.includes('Good Skill Match')) && '✅ '}
                        {result.comparison.recommendation.includes('Partial Match') && '⚠️ '}
                        {result.comparison.recommendation.includes('Weak Match') && '❌ '}
                        {result.comparison.recommendation}
                      </div>
                    )}
                  </div>

                  {result.comparison.experience_gap_warning && (
                    <div style={{ marginBottom: '20px', padding: '14px', background: 'rgba(251, 146, 60, 0.1)', borderRadius: '8px', border: '1px solid rgba(251, 146, 60, 0.3)' }}>
                      <div style={{ fontSize: '13px', color: '#fb923c', fontWeight: '600', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <span>⚠️</span>
                        <span>Experience Gap Warning</span>
                      </div>
                      <div style={{ fontSize: '13px', color: '#cbd5e1', lineHeight: '1.5' }}>
                        {result.comparison.experience_gap_warning}
                      </div>
                    </div>
                  )}

                  {result.comparison.matched_skills?.length > 0 && (
                    <div style={{ marginBottom: '20px' }}>
                      <div style={{ fontSize: '13px', color: '#4ade80', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>✓ Matched Core Skills</div>
                      <div style={styles.chipContainer}>
                        {result.comparison.matched_skills.map(s => (
                          <span key={s} style={{ ...styles.skillChip, background: 'rgba(74, 222, 128, 0.2)', border: '1px solid rgba(74, 222, 128, 0.4)', color: '#4ade80' }}>{s}</span>
                        ))}
                      </div>
                    </div>
                  )}

                  {result.comparison.missing_skills?.length > 0 && (
                    <div style={{ marginBottom: '20px' }}>
                      <div style={{ fontSize: '13px', color: '#fb923c', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>⚠ Missing Core Skills</div>
                      <div style={styles.chipContainer}>
                        {result.comparison.missing_skills.map(s => (
                          <span key={s} style={{ ...styles.skillChip, background: 'rgba(251, 146, 60, 0.2)', border: '1px solid rgba(251, 146, 60, 0.4)', color: '#fb923c' }}>{s}</span>
                        ))}
                      </div>
                    </div>
                  )}

                  {result.comparison.additional_skills?.length > 0 && (
                    <div style={{ marginBottom: '20px' }}>
                      <div style={{ fontSize: '13px', color: '#8b5cf6', fontWeight: '600', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>✨ Additional Skills (Bonus)</div>
                      <div style={styles.chipContainer}>
                        {result.comparison.additional_skills.map(s => (
                          <span key={s} style={{ ...styles.skillChip, background: 'rgba(139, 92, 246, 0.2)', border: '1px solid rgba(139, 92, 246, 0.4)', color: '#8b5cf6' }}>{s}</span>
                        ))}
                      </div>
                    </div>
                  )}

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginTop: '24px' }}>
                    <div style={{ padding: '16px', background: result.comparison.experience_match ? 'rgba(74, 222, 128, 0.1)' : 'rgba(239, 68, 68, 0.1)', borderRadius: '8px', border: `1px solid ${result.comparison.experience_match ? 'rgba(74, 222, 128, 0.3)' : 'rgba(239, 68, 68, 0.3)'}` }}>
                      <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '4px' }}>Experience Match</div>
                      <div style={{ fontSize: '20px', fontWeight: '700', color: result.comparison.experience_match ? '#4ade80' : '#ef4444' }}>
                        {result.comparison.experience_match ? '✓ Meets Requirement' : '✗ Below Requirement'}
                      </div>
                    </div>
                    <div style={{ padding: '16px', background: result.comparison.education_match ? 'rgba(74, 222, 128, 0.1)' : 'rgba(239, 68, 68, 0.1)', borderRadius: '8px', border: `1px solid ${result.comparison.education_match ? 'rgba(74, 222, 128, 0.3)' : 'rgba(239, 68, 68, 0.3)'}` }}>
                      <div style={{ fontSize: '13px', color: '#64748b', fontWeight: '600', marginBottom: '4px' }}>Education Match</div>
                      <div style={{ fontSize: '20px', fontWeight: '700', color: result.comparison.education_match ? '#4ade80' : '#ef4444' }}>
                        {result.comparison.education_match ? '✓ Meets Requirement' : '✗ Below Requirement'}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Skill Recommendations System (Synced from GitHub Repository) */}
              {result.skill_suggestions && result.skill_suggestions.suggested_skills?.length > 0 && (
                <div
                  style={{
                    ...styles.card,
                    ...(hoveredCard === 'suggestions' ? styles.cardHover : {}),
                    gridColumn: '1 / -1'
                  }}
                  onMouseEnter={() => setHoveredCard('suggestions')}
                  onMouseLeave={() => setHoveredCard(null)}
                >
                  <div style={styles.sectionTitle}>
                    <span>💡</span> AI Skill Suggestions
                  </div>

                  <div style={{ marginBottom: '16px', padding: '12px', background: 'rgba(139, 92, 246, 0.1)', borderRadius: '8px', border: '1px solid rgba(139, 92, 246, 0.3)' }}>
                    <div style={{ fontSize: '14px', color: '#cbd5e1' }}>
                      Based on the job requirements and industry trends, we recommend learning these skills to improve your match score:
                    </div>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
                    {result.skill_suggestions.suggested_skills.map((suggestion, idx) => (
                      <div
                        key={idx}
                        style={{
                          padding: '16px',
                          background: 'rgba(139, 92, 246, 0.08)',
                          borderRadius: '10px',
                          border: '1px solid rgba(139, 92, 246, 0.2)',
                          transition: 'all 0.3s ease'
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                          <span style={{ fontSize: '15px', fontWeight: '700', color: '#8b5cf6' }}>{suggestion.skill}</span>
                          {suggestion.priority === 'high' && (
                            <span style={{ fontSize: '10px', padding: '3px 8px', background: 'rgba(239, 68, 68, 0.2)', color: '#ef4444', borderRadius: '10px', fontWeight: '600' }}>HIGH</span>
                          )}
                        </div>
                        <div style={{ fontSize: '12px', color: '#94a3b8', marginBottom: '6px', fontStyle: 'italic' }}>{suggestion.reason}</div>
                        <div style={{ fontSize: '13px', color: '#cbd5e1', lineHeight: '1.6' }}>{suggestion.explanation}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
