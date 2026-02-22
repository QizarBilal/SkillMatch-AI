import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import API_BASE_URL from './config'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [emailFocused, setEmailFocused] = useState(false)
  const [passwordFocused, setPasswordFocused] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const res = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })

      const data = await res.json()

      if (!res.ok) {
        setError(data.detail || 'Login failed')
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
      padding: '20px'
    },
    authCard: {
      background: 'rgba(15, 23, 42, 0.6)',
      backdropFilter: 'blur(20px)',
      border: '1px solid rgba(99, 102, 241, 0.2)',
      borderRadius: '24px',
      padding: '48px 40px',
      width: '100%',
      maxWidth: '440px',
      boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4), 0 0 80px rgba(99, 102, 241, 0.1)',
    },
    logoSection: {
      textAlign: 'center',
      marginBottom: '40px'
    },
    logo: {
      fontSize: '32px',
      fontWeight: '700',
      background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      marginBottom: '8px',
      letterSpacing: '-0.5px'
    },
    subtitle: {
      fontSize: '14px',
      color: 'rgba(226, 232, 240, 0.6)',
      fontWeight: '400'
    },
    form: {
      display: 'flex',
      flexDirection: 'column',
      gap: '24px'
    },
    inputGroup: {
      position: 'relative'
    },
    label: {
      position: 'absolute',
      left: '16px',
      top: '16px',
      fontSize: '14px',
      color: 'rgba(226, 232, 240, 0.5)',
      pointerEvents: 'none',
      transition: 'all 0.2s ease',
      transform: emailFocused || email ? 'translateY(-24px) scale(0.85)' : 'translateY(0) scale(1)',
      transformOrigin: 'left'
    },
    labelPassword: {
      position: 'absolute',
      left: '16px',
      top: '16px',
      fontSize: '14px',
      color: 'rgba(226, 232, 240, 0.5)',
      pointerEvents: 'none',
      transition: 'all 0.2s ease',
      transform: passwordFocused || password ? 'translateY(-24px) scale(0.85)' : 'translateY(0) scale(1)',
      transformOrigin: 'left'
    },
    input: {
      width: '100%',
      padding: '16px',
      background: 'rgba(30, 41, 59, 0.5)',
      border: '1px solid rgba(148, 163, 184, 0.2)',
      borderRadius: '12px',
      color: '#e2e8f0',
      fontSize: '15px',
      outline: 'none',
      transition: 'all 0.3s ease',
      boxShadow: emailFocused ? '0 0 0 3px rgba(99, 102, 241, 0.1), 0 0 20px rgba(99, 102, 241, 0.2)' : 'none',
      boxSizing: 'border-box'
    },
    inputPassword: {
      width: '100%',
      padding: '16px',
      paddingRight: '50px',
      background: 'rgba(30, 41, 59, 0.5)',
      border: '1px solid rgba(148, 163, 184, 0.2)',
      borderRadius: '12px',
      color: '#e2e8f0',
      fontSize: '15px',
      outline: 'none',
      transition: 'all 0.3s ease',
      boxShadow: passwordFocused ? '0 0 0 3px rgba(99, 102, 241, 0.1), 0 0 20px rgba(99, 102, 241, 0.2)' : 'none',
      boxSizing: 'border-box'
    },
    togglePassword: {
      position: 'absolute',
      right: '16px',
      top: '16px',
      background: 'none',
      border: 'none',
      color: 'rgba(226, 232, 240, 0.5)',
      cursor: 'pointer',
      fontSize: '14px',
      padding: 0,
      transition: 'color 0.2s'
    },
    error: {
      background: 'rgba(239, 68, 68, 0.1)',
      border: '1px solid rgba(239, 68, 68, 0.3)',
      borderRadius: '8px',
      padding: '12px 16px',
      color: '#fca5a5',
      fontSize: '14px',
      animation: 'shake 0.4s ease'
    },
    button: {
      padding: '16px',
      background: loading ? 'rgba(99, 102, 241, 0.5)' : 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
      border: 'none',
      borderRadius: '12px',
      color: '#ffffff',
      fontSize: '16px',
      fontWeight: '600',
      cursor: loading ? 'not-allowed' : 'pointer',
      transition: 'all 0.3s ease',
      boxShadow: loading ? 'none' : '0 4px 20px rgba(99, 102, 241, 0.4)',
      transform: loading ? 'scale(1)' : 'scale(1)',
      marginTop: '8px'
    },
    footer: {
      textAlign: 'center',
      marginTop: '32px',
      paddingTop: '24px',
      borderTop: '1px solid rgba(148, 163, 184, 0.1)'
    },
    footerText: {
      color: 'rgba(226, 232, 240, 0.6)',
      fontSize: '14px'
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
      `}</style>
      
      <div style={styles.authCard}>
        <div style={styles.logoSection}>
          <div style={styles.logo}>SkillMatch</div>
          <div style={styles.subtitle}>AI Resume Intelligence Platform</div>
        </div>

        <form onSubmit={handleSubmit} style={styles.form}>
          {error && <div style={styles.error}>{error}</div>}

          <div style={styles.inputGroup}>
            <label style={styles.label}>Email</label>
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
            <label style={styles.labelPassword}>Password</label>
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
          </div>

          <button type="submit" disabled={loading} style={styles.button}>
            {loading ? <span style={styles.spinner}></span> : 'Login'}
          </button>
        </form>

        <div style={styles.footer}>
          <span style={styles.footerText}>
            Don't have an account?
            <a href="/signup" style={styles.link}>Create account</a>
          </span>
        </div>
      </div>
    </div>
  )
}
