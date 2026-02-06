import { useState, useEffect } from "react"

const styles = {
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
    padding: '20px 48px',
    borderBottom: '1px solid rgba(99, 102, 241, 0.15)',
    background: 'rgba(10, 14, 39, 0.6)',
    backdropFilter: 'blur(12px)',
  },
  logo: {
    fontSize: '22px',
    fontWeight: '700',
    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    letterSpacing: '-0.02em',
  },
  tagline: {
    fontSize: '12px',
    color: '#94a3b8',
    marginLeft: '16px',
    fontWeight: '500',
  },
  statusBadge: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px',
    padding: '6px 14px',
    background: 'rgba(16, 185, 129, 0.1)',
    border: '1px solid rgba(16, 185, 129, 0.3)',
    borderRadius: '20px',
    fontSize: '11px',
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
    padding: '60px 48px 40px',
    textAlign: 'center',
  },
  heroTitle: {
    fontSize: '48px',
    fontWeight: '800',
    marginBottom: '12px',
    background: 'linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    letterSpacing: '-0.03em',
  },
  heroSubtitle: {
    fontSize: '16px',
    color: '#94a3b8',
    marginBottom: '32px',
    fontWeight: '400',
  },
  divider: {
    height: '2px',
    background: 'linear-gradient(90deg, transparent 0%, #6366f1 50%, transparent 100%)',
    maxWidth: '600px',
    margin: '0 auto',
  },
  container: {
    maxWidth: '1400px',
    margin: '0 auto',
    padding: '40px 48px',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(480px, 1fr))',
    gap: '24px',
    marginBottom: '32px',
  },
  card: {
    background: 'rgba(15, 20, 40, 0.7)',
    border: '1px solid rgba(99, 102, 241, 0.2)',
    borderRadius: '16px',
    padding: '32px',
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
    backdropFilter: 'blur(8px)',
    transition: 'all 0.3s ease',
  },
  cardHover: {
    transform: 'translateY(-2px)',
    boxShadow: '0 12px 40px rgba(99, 102, 241, 0.2)',
  },
  sectionTitle: {
    fontSize: '14px',
    fontWeight: '700',
    color: '#cbd5e1',
    marginBottom: '20px',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
  },
  uploadZone: {
    border: '2px dashed rgba(99, 102, 241, 0.35)',
    borderRadius: '16px',
    padding: '56px 40px 48px',
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
    minHeight: '280px',
  },
  uploadZoneActive: {
    border: '2px dashed #6366f1',
    background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(139, 92, 246, 0.12) 100%)',
    transform: 'scale(1.02)',
    boxShadow: '0 0 40px rgba(99, 102, 241, 0.3), inset 0 0 60px rgba(99, 102, 241, 0.1)',
  },
  uploadIconWrapper: {
    width: '88px',
    height: '88px',
    margin: '0 0 24px 0',
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
    transform: 'scale(1.1) rotate(10deg)',
    background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(139, 92, 246, 0.25) 100%)',
    border: '2px solid #6366f1',
    boxShadow: '0 0 30px rgba(99, 102, 241, 0.5)',
  },
  uploadIcon: {
    fontSize: '40px',
    opacity: 0.95,
    transition: 'all 0.3s ease',
    lineHeight: 1,
  },
  uploadTextPrimary: {
    fontSize: '17px',
    fontWeight: '600',
    color: '#e2e8f0',
    marginBottom: '10px',
    letterSpacing: '-0.01em',
    lineHeight: 1.3,
  },
  uploadTextSecondary: {
    fontSize: '13px',
    color: '#64748b',
    marginBottom: '28px',
    fontWeight: '400',
    lineHeight: 1.5,
    maxWidth: '280px',
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
    padding: '6px 12px',
    background: 'rgba(139, 92, 246, 0.12)',
    border: '1px solid rgba(139, 92, 246, 0.35)',
    borderRadius: '8px',
    fontSize: '11px',
    color: '#a78bfa',
    fontWeight: '600',
    letterSpacing: '0.02em',
    textTransform: 'uppercase',
  },
  filePreview: {
    marginTop: '24px',
    padding: '20px',
    background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.08) 100%)',
    border: '1px solid rgba(16, 185, 129, 0.4)',
    borderRadius: '12px',
    transition: 'all 0.3s ease',
    boxShadow: '0 4px 12px rgba(16, 185, 129, 0.1)',
  },
  filePreviewHover: {
    transform: 'translateY(-2px)',
    boxShadow: '0 8px 20px rgba(16, 185, 129, 0.2)',
  },
  fileInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    marginBottom: '12px',
  },
  fileIconCircle: {
    width: '44px',
    height: '44px',
    borderRadius: '50%',
    background: 'rgba(16, 185, 129, 0.2)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '20px',
    flexShrink: 0,
  },
  fileDetails: {
    flex: 1,
  },
  fileName: {
    fontSize: '14px',
    color: '#10b981',
    fontWeight: '700',
    marginBottom: '4px',
    letterSpacing: '-0.01em',
  },
  fileSize: {
    fontSize: '11px',
    color: '#64748b',
    fontWeight: '500',
  },
  replaceBtn: {
    padding: '8px 16px',
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
    transform: 'translateY(-1px)',
    boxShadow: '0 4px 12px rgba(239, 68, 68, 0.3)',
  },
  textarea: {
    width: 'calc(100% - 4px)',
    minHeight: '280px',
    background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.04) 0%, rgba(139, 92, 246, 0.04) 100%)',
    border: '2px dashed rgba(99, 102, 241, 0.35)',
    borderRadius: '12px',
    padding: '20px',
    color: '#e2e8f0',
    fontSize: '14px',
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
    fontSize: '13px',
    color: '#94a3b8',
    marginBottom: '16px',
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
  actionSection: {
    display: 'flex',
    justifyContent: 'center',
    marginBottom: '48px',
  },
  primaryBtn: {
    padding: '16px 48px',
    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
    border: 'none',
    borderRadius: '12px',
    color: '#ffffff',
    fontSize: '15px',
    fontWeight: '700',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    boxShadow: '0 8px 24px rgba(99, 102, 241, 0.4)',
    letterSpacing: '0.02em',
  },
  primaryBtnHover: {
    transform: 'translateY(-2px)',
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
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '20px',
  },
  resultCard: {
    background: 'rgba(15, 20, 40, 0.8)',
    border: '1px solid rgba(99, 102, 241, 0.25)',
    borderRadius: '14px',
    padding: '24px',
    transition: 'all 0.3s ease',
  },
  resultCardHover: {
    transform: 'translateY(-3px)',
    boxShadow: '0 10px 30px rgba(99, 102, 241, 0.25)',
  },
  resultLabel: {
    fontSize: '11px',
    fontWeight: '700',
    color: '#64748b',
    textTransform: 'uppercase',
    letterSpacing: '0.08em',
    marginBottom: '12px',
  },
  resultValue: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#e8eaf0',
    marginBottom: '4px',
  },
  resultMeta: {
    fontSize: '12px',
    color: '#94a3b8',
  },
  chipContainer: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '8px',
    marginTop: '8px',
  },
  skillChip: {
    padding: '8px 14px',
    background: 'rgba(16, 185, 129, 0.15)',
    border: '1px solid rgba(16, 185, 129, 0.4)',
    borderRadius: '20px',
    fontSize: '12px',
    color: '#10b981',
    fontWeight: '600',
    transition: 'all 0.2s ease',
  },
  keywordChip: {
    padding: '8px 14px',
    background: 'rgba(99, 102, 241, 0.15)',
    border: '1px solid rgba(99, 102, 241, 0.4)',
    borderRadius: '20px',
    fontSize: '12px',
    color: '#818cf8',
    fontWeight: '600',
    transition: 'all 0.2s ease',
  },
  chipHover: {
    transform: 'scale(1.05)',
    boxShadow: '0 4px 12px rgba(99, 102, 241, 0.3)',
  },
  datasetIndicator: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px',
    padding: '8px 16px',
    background: 'rgba(16, 185, 129, 0.12)',
    border: '1px solid rgba(16, 185, 129, 0.3)',
    borderRadius: '8px',
    marginTop: '8px',
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
  },
  overlayContent: {
    maxWidth: '900px',
    width: '90%',
    textAlign: 'center',
  },
  stageTitle: {
    fontSize: '20px',
    fontWeight: '700',
    color: '#e2e8f0',
    marginBottom: '24px',
    letterSpacing: '-0.02em',
  },
  scanPanel: {
    background: 'rgba(15, 20, 40, 0.8)',
    border: '1px solid rgba(99, 102, 241, 0.3)',
    borderRadius: '16px',
    padding: '0',
    position: 'relative',
    overflow: 'hidden',
    maxWidth: '800px',
    width: '90%',
    margin: '0 auto',
  },
  previewContainer: {
    position: 'relative',
    width: '100%',
    height: '500px',
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
    padding: '40px',
    background: 'white',
    color: '#1a1a1a',
    overflow: 'auto',
    fontFamily: 'Georgia, serif',
    fontSize: '14px',
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
    height: '80px',
    background: 'linear-gradient(180deg, transparent, rgba(99, 102, 241, 0.4), rgba(139, 92, 246, 0.4), transparent)',
    boxShadow: '0 0 40px rgba(99, 102, 241, 0.6)',
    animation: 'scanBeam 1.2s ease-in-out infinite',
    filter: 'blur(2px)',
  },
  scanStatus: {
    marginTop: '24px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '12px',
    fontSize: '16px',
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
    padding: '32px',
    marginBottom: '20px',
  },
  terminalPanel: {
    background: 'rgba(10, 14, 27, 0.9)',
    border: '1px solid rgba(99, 102, 241, 0.3)',
    borderRadius: '12px',
    padding: '24px',
    maxHeight: '400px',
    overflow: 'auto',
    textAlign: 'left',
    fontFamily: 'monospace',
    fontSize: '13px',
    lineHeight: '1.8',
    color: '#cbd5e1',
  },
  skillGrid: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '12px',
    justifyContent: 'center',
    marginTop: '24px',
  },
  animatedChip: {
    padding: '10px 18px',
    background: 'rgba(16, 185, 129, 0.15)',
    border: '1px solid rgba(16, 185, 129, 0.4)',
    borderRadius: '20px',
    fontSize: '13px',
    color: '#10b981',
    fontWeight: '600',
    animation: 'slideIn 0.4s ease',
  },
  keywordChipAnimated: {
    padding: '10px 18px',
    background: 'rgba(99, 102, 241, 0.15)',
    border: '1px solid rgba(99, 102, 241, 0.4)',
    borderRadius: '20px',
    fontSize: '13px',
    color: '#818cf8',
    fontWeight: '600',
    animation: 'slideIn 0.4s ease',
  },
  successBanner: {
    background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%)',
    border: '1px solid rgba(16, 185, 129, 0.5)',
    borderRadius: '12px',
    padding: '24px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '12px',
    fontSize: '16px',
    color: '#10b981',
    fontWeight: '600',
  },
  shimmerPanel: {
    background: 'rgba(15, 20, 40, 0.8)',
    border: '1px solid rgba(99, 102, 241, 0.3)',
    borderRadius: '12px',
    padding: '32px',
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
    padding: '20px',
    textAlign: 'left',
    fontSize: '12px',
    color: '#cbd5e1',
    maxHeight: '300px',
    overflow: 'auto',
  },
  tableRow: {
    padding: '8px 0',
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
}

export default function App() {
  const [file, setFile] = useState(null)
  const [jd, setJd] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [uploadHover, setUploadHover] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const [textareaFocus, setTextareaFocus] = useState(false)
  const [hoveredCard, setHoveredCard] = useState(null)
  const [filePreviewHover, setFilePreviewHover] = useState(false)
  const [replaceBtnHover, setReplaceBtnHover] = useState(false)
  const [stage, setStage] = useState(0)
  const [processingData, setProcessingData] = useState(null)
  const [displayedText, setDisplayedText] = useState("")
  const [displayedSkills, setDisplayedSkills] = useState([])
  const [displayedKeywords, setDisplayedKeywords] = useState([])
  const [filePreviewUrl, setFilePreviewUrl] = useState(null)
  const [scanDots, setScanDots] = useState("")

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
      }, 3500)
      
      return () => {
        clearTimeout(timer)
        clearInterval(dotInterval)
      }
    }
    if (stage === 2) {
      const text = processingData?.cleaned_resume_text || ""
      if (!text) {
        setStage(0)
        setLoading(false)
        return
      }
      let index = 0
      const interval = setInterval(() => {
        if (index < text.length) {
          setDisplayedText(text.substring(0, index + 1))
          index += Math.floor(Math.random() * 5) + 2
        } else {
          clearInterval(interval)
          setTimeout(() => setStage(3), 500)
        }
      }, 20)
      return () => clearInterval(interval)
    }
    if (stage === 3) {
      const skills = processingData?.resume_skills || []
      if (!skills.length) {
        setStage(4)
        return
      }
      let index = 0
      const interval = setInterval(() => {
        if (index < skills.length) {
          setDisplayedSkills(prev => [...prev, skills[index]])
          index++
        } else {
          clearInterval(interval)
          setTimeout(() => setStage(4), 1000)
        }
      }, 300)
      return () => clearInterval(interval)
    }
    if (stage === 4) {
      const timer = setTimeout(() => setStage(5), 1500)
      return () => clearTimeout(timer)
    }
    if (stage === 5) {
      const timer = setTimeout(() => setStage(6), 3000)
      return () => clearTimeout(timer)
    }
    if (stage === 6) {
      const keywords = processingData?.job_keywords || []
      if (!keywords.length) {
        setStage(7)
        return
      }
      let index = 0
      const interval = setInterval(() => {
        if (index < keywords.length) {
          setDisplayedKeywords(prev => [...prev, keywords[index]])
          index++
        } else {
          clearInterval(interval)
          setTimeout(() => setStage(7), 1000)
        }
      }, 250)
      return () => clearInterval(interval)
    }
    if (stage === 7) {
      const timer = setTimeout(() => setStage(8), 2500)
      return () => clearTimeout(timer)
    }
    if (stage === 8) {
      const timer = setTimeout(() => {
        setStage(0)
        setResult(processingData)
        setLoading(false)
        if (filePreviewUrl) URL.revokeObjectURL(filePreviewUrl)
        setFilePreviewUrl(null)
      }, 500)
      return () => clearTimeout(timer)
    }
  }, [stage, processingData, filePreviewUrl])

  const submit = async () => {
    if (!file || !jd) return
    
    const previewUrl = URL.createObjectURL(file)
    setFilePreviewUrl(previewUrl)
    
    setLoading(true)
    setStage(1)
    setDisplayedText("")
    setDisplayedSkills([])
    setDisplayedKeywords([])
    
    const form = new FormData()
    form.append("resume", file)
    form.append("job_description", jd)

    try {
      const r = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: form
      })
      
      if (!r.ok) {
        const error = await r.json()
        alert(error.detail || "Failed to process resume. Please try with a PDF or DOCX file.")
        setLoading(false)
        setStage(0)
        return
      }
      
      const data = await r.json()
      setProcessingData(data)
    } catch (err) {
      alert("Network error. Please check if the backend server is running.")
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
                        <div style={{fontSize: '18px', fontWeight: '700', marginBottom: '20px', color: '#111'}}>
                          {file.name}
                        </div>
                        <div style={{color: '#333', whiteSpace: 'pre-wrap'}}>
                          {processingData?.cleaned_resume_text?.substring(0, 800) || 'Loading document preview...'}
                        </div>
                      </div>
                    )}
                    <div style={styles.scanOverlay}>
                      <div style={styles.scanBeam}></div>
                    </div>
                  </div>
                  <div style={styles.scanStatus}>
                    <div style={styles.scanPulse}></div>
                    <span>Scanning your resume with AI{scanDots}</span>
                  </div>
                </div>
              </>
            )}

            {stage === 2 && (
              <>
                <div style={styles.stageTitle}>Extracting structured text</div>
                <div style={styles.terminalPanel}>
                  {displayedText}
                </div>
              </>
            )}

            {stage === 3 && (
              <>
                <div style={styles.stageTitle}>Detected Core Skills ✓</div>
                <div style={styles.skillGrid}>
                  {displayedSkills.map((s, i) => (
                    <div key={i} style={{...styles.animatedChip, animationDelay: `${i * 0.1}s`}}>{s}</div>
                  ))}
                </div>
              </>
            )}

            {stage === 4 && (
              <div style={styles.successBanner}>
                <div style={{fontSize: '32px'}}>✓</div>
                <div>Resume text parsing successful</div>
              </div>
            )}

            {stage === 5 && (
              <>
                <div style={styles.stageTitle}>Analyzing job description semantics</div>
                <div style={styles.shimmerPanel}>
                  <div style={styles.shimmer}></div>
                  <div style={{fontSize: '14px', color: '#cbd5e1', lineHeight: '1.8', textAlign: 'left'}}>
                    {jd.substring(0, 300)}...
                  </div>
                </div>
              </>
            )}

            {stage === 6 && (
              <>
                <div style={styles.stageTitle}>Role Keywords Identified</div>
                <div style={styles.skillGrid}>
                  {displayedKeywords.map((k, i) => (
                    <div key={i} style={{...styles.keywordChipAnimated, animationDelay: `${i * 0.1}s`}}>{k}</div>
                  ))}
                </div>
              </>
            )}

            {stage === 7 && (
              <>
                <div style={styles.stageTitle}>Building structured dataset entry</div>
                <div style={styles.tablePreview}>
                  <div style={styles.tableRow}>
                    <strong>resume_id:</strong> {processingData?.resume_id}
                  </div>
                  <div style={styles.tableRow}>
                    <strong>resume_text:</strong> {processingData?.cleaned_resume_text?.substring(0, 80)}...
                  </div>
                  <div style={styles.tableRow}>
                    <strong>resume_skills:</strong> {processingData?.resume_skills?.join(', ')}
                  </div>
                  <div style={styles.tableRow}>
                    <strong>job_description_text:</strong> {processingData?.cleaned_job_description_text?.substring(0, 80)}...
                  </div>
                  <div style={styles.tableRow}>
                    <strong>job_keywords:</strong> {processingData?.job_keywords?.join(', ')}
                  </div>
                  <div style={{marginTop: '20px', color: '#10b981', fontWeight: '600', textAlign: 'center'}}>
                    Dataset updated successfully ✓
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      )}

      <div style={styles.nav}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <div style={styles.logo}>SkillMatch AI</div>
          <span style={styles.tagline}>Milestone-1 Intelligence Scan</span>
        </div>
        <div style={styles.statusBadge}>
          <div style={styles.liveDot}></div>
          SYSTEM ACTIVE
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
                <div style={styles.fileCard}>
                  <div style={styles.fileIconDisplay}>{getFileIcon(file.name)}</div>
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
          </div>
        </div>

        <div style={styles.actionSection}>
          <button
            onClick={submit}
            disabled={!file || !jd || loading}
            style={{
              ...styles.primaryBtn,
              ...(loading ? styles.primaryBtnDisabled : {}),
              ...(!file || !jd ? styles.primaryBtnDisabled : {})
            }}
            onMouseEnter={e => {
              if (!loading && file && jd) {
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
          <div style={styles.resultsGrid}>
            <div 
              style={{
                ...styles.resultCard,
                ...(hoveredCard === 'meta' ? styles.resultCardHover : {})
              }}
              onMouseEnter={() => setHoveredCard('meta')}
              onMouseLeave={() => setHoveredCard(null)}
            >
              <div style={styles.resultLabel}>Resume Metadata</div>
              <div style={styles.resultValue}>{result.resume_id}</div>
              <div style={styles.resultMeta}>
                {new Date().toLocaleString('en-US', { 
                  dateStyle: 'medium', 
                  timeStyle: 'short' 
                })}
              </div>
              <div style={styles.resultMeta}>
                Processing complete
              </div>
            </div>

            <div 
              style={{
                ...styles.resultCard,
                ...(hoveredCard === 'skills' ? styles.resultCardHover : {})
              }}
              onMouseEnter={() => setHoveredCard('skills')}
              onMouseLeave={() => setHoveredCard(null)}
            >
              <div style={styles.resultLabel}>Extracted Skills</div>
              <div style={styles.resultValue}>{result.resume_skills.length} Skills Detected</div>
              <div style={styles.chipContainer}>
                {result.resume_skills.map(s => (
                  <span 
                    key={s} 
                    style={styles.skillChip}
                    onMouseEnter={e => Object.assign(e.target.style, styles.chipHover)}
                    onMouseLeave={e => {
                      e.target.style.transform = ''
                      e.target.style.boxShadow = ''
                    }}
                  >
                    {s}
                  </span>
                ))}
              </div>
            </div>

            <div 
              style={{
                ...styles.resultCard,
                ...(hoveredCard === 'keywords' ? styles.resultCardHover : {})
              }}
              onMouseEnter={() => setHoveredCard('keywords')}
              onMouseLeave={() => setHoveredCard(null)}
            >
              <div style={styles.resultLabel}>Job Description Keywords</div>
              <div style={styles.resultValue}>{result.job_keywords.length} Keywords Extracted</div>
              <div style={styles.chipContainer}>
                {result.job_keywords.map(k => (
                  <span 
                    key={k} 
                    style={styles.keywordChip}
                    onMouseEnter={e => Object.assign(e.target.style, styles.chipHover)}
                    onMouseLeave={e => {
                      e.target.style.transform = ''
                      e.target.style.boxShadow = ''
                    }}
                  >
                    {k}
                  </span>
                ))}
              </div>
            </div>

            <div 
              style={{
                ...styles.resultCard,
                ...(hoveredCard === 'dataset' ? styles.resultCardHover : {})
              }}
              onMouseEnter={() => setHoveredCard('dataset')}
              onMouseLeave={() => setHoveredCard(null)}
            >
              <div style={styles.resultLabel}>Dataset Status</div>
              <div style={styles.resultValue}>{result.dataset_size} Total Rows</div>
              <div style={styles.datasetIndicator}>
                <div style={styles.updateDot}></div>
                <span style={{ fontSize: '12px', color: '#10b981', fontWeight: '600' }}>
                  Dataset Updated
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
