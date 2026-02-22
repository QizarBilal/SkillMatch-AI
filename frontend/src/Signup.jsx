import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import API_BASE_URL from './config'

const useWindowSize = () => {
  const [windowSize, setWindowSize] = useState({
    width: typeof window !== 'undefined' ? window.innerWidth : 1200,
    isMobile: typeof window !== 'undefined' ? window.innerWidth < 768 : false,
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        isMobile: window.innerWidth < 768,
      });
    };

    window.addEventListener('resize', handleResize);
    handleResize();

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
};

export default function Signup() {
  const { isMobile } = useWindowSize();
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [emailFocused, setEmailFocused] = useState(false)
  const [passwordFocused, setPasswordFocused] = useState(false)
  const [confirmFocused, setConfirmFocused] = useState(false)
  const navigate = useNavigate()

  const getPasswordStrength = () => {
    if (!password) return { strength: 0, label: '', color: '' }
    let strength = 0
    if (password.length >= 6) strength++
    if (password.length >= 10) strength++
    if (/[A-Z]/.test(password)) strength++
    if (/[0-9]/.test(password)) strength++
    if (/[^A-Za-z0-9]/.test(password)) strength++

    if (strength <= 1) return { strength: 20, label: 'Weak', color: '#ef4444' }
    if (strength === 2) return { strength: 40, label: 'Fair', color: '#f59e0b' }
    if (strength === 3) return { strength: 60, label: 'Good', color: '#eab308' }
    if (strength === 4) return { strength: 80, label: 'Strong', color: '#22c55e' }
    return { strength: 100, label: 'Very Strong', color: '#10b981' }
  }

  const passwordStrength = getPasswordStrength()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }

    setLoading(true)

    try {
      const res = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })

      const data = await res.json()

      if (!res.ok) {
        setError(data.detail || 'Registration failed')
        setLoading(false)
        return
      }

      localStorage.setItem('token', data.token)
      localStorage.setItem('user_id', data.user_id)
      localStorage.setItem('user_email', data.email)

      navigate('/dashboard')
    } catch (err) {
      setError('Network error. Please try again.')
      setLoading(false)
    }
  }

  const styles = {
    container: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1629 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
      padding: isMobile ? '16px' : '20px'
    },
    authCard: {
      background: 'rgba(15, 23, 42, 0.6)',
      backdropFilter: 'blur(20px)',
      border: '1px solid rgba(99, 102, 241, 0.2)',
      borderRadius: isMobile ? '16px' : '24px',
      padding: isMobile ? '32px 24px' : '48px 40px',
      width: '100%',
      maxWidth: isMobile ? '100%' : '440px',
      boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4), 0 0 80px rgba(99, 102, 241, 0.1)',
    },
    logoSection: {
      textAlign: 'center',
      marginBottom: isMobile ? '28px' : '40px'
    },
    logo: {
      fontSize: isMobile ? '24px' : '32px',
      fontWeight: '700',
      background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      marginBottom: '8px',
      letterSpacing: '-0.5px'
    },
    subtitle: {
      fontSize: isMobile ? '13px' : '14px',
      color: 'rgba(226, 232, 240, 0.6)',
      fontWeight: '400'
    },
    form: {
      display: 'flex',
      flexDirection: 'column',
      gap: isMobile ? '20px' : '24px'
    },
    inputGroup: {
      position: 'relative'
    },
    label: {
      position: 'absolute',
      left: isMobile ? '14px' : '16px',
      top: isMobile ? '14px' : '16px',
      fontSize: isMobile ? '13px' : '14px',
      color: 'rgba(226, 232, 240, 0.5)',
      pointerEvents: 'none',
      transition: 'all 0.2s ease',
      transformOrigin: 'left'
    },
    input: {
      width: '100%',
      padding: isMobile ? '14px' : '16px',
      background: 'rgba(30, 41, 59, 0.5)',
      border: '1px solid rgba(148, 163, 184, 0.2)',
      borderRadius: isMobile ? '10px' : '12px',
      color: '#e2e8f0',
      fontSize: isMobile ? '16px' : '15px',
      outline: 'none',
      transition: 'all 0.3s ease',
      boxSizing: 'border-box'
    },
    inputPassword: {
      width: '100%',
      padding: isMobile ? '14px' : '16px',
      paddingRight: isMobile ? '44px' : '50px',
      background: 'rgba(30, 41, 59, 0.5)',
      border: '1px solid rgba(148, 163, 184, 0.2)',
      borderRadius: isMobile ? '10px' : '12px',
      color: '#e2e8f0',
      fontSize: isMobile ? '16px' : '15px',
      outline: 'none',
      transition: 'all 0.3s ease',
      boxSizing: 'border-box'
    },
    togglePassword: {
      position: 'absolute',
      right: isMobile ? '4px' : '6px',
      top: '50%',
      transform: 'translateY(-50%)',
      background: 'none',
      border: 'none',
      color: 'rgba(226, 232, 240, 0.5)',
      cursor: 'pointer',
      fontSize: isMobile ? '18px' : '20px',
      padding: '8px',
      transition: 'color 0.2s',
      minWidth: '44px',
      minHeight: '44px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    },
    strengthBar: {
      height: isMobile ? '3px' : '4px',
      background: 'rgba(148, 163, 184, 0.2)',
      borderRadius: '2px',
      marginTop: isMobile ? '6px' : '8px',
      overflow: 'hidden'
    },
    strengthFill: {
      height: '100%',
      width: `${passwordStrength.strength}%`,
      background: passwordStrength.color,
      transition: 'all 0.3s ease',
      borderRadius: '2px'
    },
    strengthLabel: {
      fontSize: isMobile ? '11px' : '12px',
      color: passwordStrength.color,
      marginTop: '4px',
      fontWeight: '500'
    },
    mismatchWarning: {
      fontSize: isMobile ? '11px' : '12px',
      color: '#fca5a5',
      marginTop: '4px'
    },
    error: {
      background: 'rgba(239, 68, 68, 0.1)',
      border: '1px solid rgba(239, 68, 68, 0.3)',
      borderRadius: '8px',
      padding: isMobile ? '10px 14px' : '12px 16px',
      color: '#fca5a5',
      fontSize: isMobile ? '13px' : '14px',
      animation: 'shake 0.4s ease'
    },
    button: {
      padding: isMobile ? '14px' : '16px',
      background: loading ? 'rgba(99, 102, 241, 0.5)' : 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
      border: 'none',
      borderRadius: isMobile ? '10px' : '12px',
      color: '#ffffff',
      fontSize: isMobile ? '15px' : '16px',
      fontWeight: '600',
      cursor: loading ? 'not-allowed' : 'pointer',
      transition: 'all 0.3s ease',
      boxShadow: loading ? 'none' : '0 4px 20px rgba(99, 102, 241, 0.4)',
      transform: loading ? 'scale(1)' : 'scale(1)',
      marginTop: isMobile ? '4px' : '8px',
      minHeight: '44px',
    },
    footer: {
      textAlign: 'center',
      marginTop: isMobile ? '24px' : '32px',
      paddingTop: isMobile ? '20px' : '24px',
      borderTop: '1px solid rgba(148, 163, 184, 0.1)'
    },
    footerText: {
      color: 'rgba(226, 232, 240, 0.6)',
      fontSize: isMobile ? '13px' : '14px'
    },
    link: {
      color: '#6366f1',
      textDecoration: 'none',
      fontWeight: '500',
      marginLeft: '6px',
      transition: 'color 0.2s'
    },
    spinner: {
      display: 'inline-block',
      width: '16px',
      height: '16px',
      border: '2px solid rgba(255, 255, 255, 0.3)',
      borderTop: '2px solid #ffffff',
      borderRadius: '50%',
      animation: 'spin 0.6s linear infinite'
    }
  }

  return (
    <div style={styles.container}>
      <style>{`
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-8px); }
          75% { transform: translateX(8px); }
        }
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        button:hover {
          transform: translateY(-2px) !important;
          box-shadow: 0 6px 30px rgba(99, 102, 241, 0.5) !important;
        }
        button:active {
          transform: translateY(0) !important;
        }
        a:hover {
          color: #818cf8 !important;
        }
        input:focus {
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1), 0 0 20px rgba(99, 102, 241, 0.2) !important;
        }
      `}</style>
      
      <div style={styles.authCard}>
        <div style={styles.logoSection}>
          <div style={styles.logo}>SkillMatch</div>
          <div style={styles.subtitle}>AI Resume Intelligence Platform</div>
        </div>

        <form onSubmit={handleSubmit} style={styles.form}>
          {error && <div style={styles.error}>{error}</div>}

          <div style={styles.inputGroup}>
            <label style={{...styles.label, transform: emailFocused || email ? 'translateY(-24px) scale(0.85)' : 'translateY(0)'}}>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onFocus={() => setEmailFocused(true)}
              onBlur={() => setEmailFocused(false)}
              style={styles.input}
              required
            />
          </div>

          <div style={styles.inputGroup}>
            <label style={{...styles.label, transform: passwordFocused || password ? 'translateY(-24px) scale(0.85)' : 'translateY(0)'}}>Password</label>
            <input
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onFocus={() => setPasswordFocused(true)}
              onBlur={() => setPasswordFocused(false)}
              style={styles.inputPassword}
              required
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              style={styles.togglePassword}
            >
              {showPassword ? '👁️' : '👁️‍🗨️'}
            </button>
            {password && (
              <>
                <div style={styles.strengthBar}>
                  <div style={styles.strengthFill}></div>
                </div>
                <div style={styles.strengthLabel}>{passwordStrength.label}</div>
              </>
            )}
          </div>

          <div style={styles.inputGroup}>
            <label style={{...styles.label, transform: confirmFocused || confirmPassword ? 'translateY(-24px) scale(0.85)' : 'translateY(0)'}}>Confirm Password</label>
            <input
              type={showConfirmPassword ? 'text' : 'password'}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              onFocus={() => setConfirmFocused(true)}
              onBlur={() => setConfirmFocused(false)}
              style={styles.inputPassword}
              required
            />
            <button
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              style={styles.togglePassword}
            >
              {showConfirmPassword ? '👁️' : '👁️‍🗨️'}
            </button>
            {confirmPassword && password !== confirmPassword && (
              <div style={styles.mismatchWarning}>Passwords do not match</div>
            )}
          </div>

          <button type="submit" disabled={loading} style={styles.button}>
            {loading ? <span style={styles.spinner}></span> : 'Create Account'}
          </button>
        </form>

        <div style={styles.footer}>
          <span style={styles.footerText}>
            Already have an account?
            <a href="/login" style={styles.link}>Login</a>
          </span>
        </div>
      </div>
    </div>
  )
}
