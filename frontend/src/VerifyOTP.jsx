import { useState, useEffect } from 'react'
import { useNavigate, useLocation, Link } from 'react-router-dom'
import { useAuth } from './App'
import api from './api'

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

export default function VerifyOTP() {
    const { isMobile } = useWindowSize();
    const [otp, setOtp] = useState('')
    const [loading, setLoading] = useState(false)
    const [resending, setResending] = useState(false)
    const [error, setError] = useState('')
    const [success, setSuccess] = useState('')
    const [otpFocused, setOtpFocused] = useState(false)

    const navigate = useNavigate()
    const location = useLocation()
    const { login } = useAuth()

    const queryParams = new URLSearchParams(location.search)
    const email = queryParams.get('email') || ''

    useEffect(() => {
        if (!email) {
            navigate('/signup')
        }
    }, [email, navigate])

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setSuccess('')

        if (otp.length !== 6) {
            setError('OTP must be exactly 6 digits')
            return
        }

        setLoading(true)

        try {
            const data = await api.post('/auth/verify-otp', { email, otp })
            if (data && data.token) {
                login(data.token, { user_id: data.user_id, email: data.email })
                navigate('/dashboard')
            }
        } catch (err) {
            setError(err.message || 'Verification failed')
            setLoading(false)
        }
    }

    const handleResend = async () => {
        setError('')
        setSuccess('')
        setResending(true)

        try {
            await api.post('/auth/resend-otp', { email })
            setSuccess('A new OTP has been sent to your email.')
        } catch (err) {
            setError(err.message || 'Failed to resend OTP')
        } finally {
            setResending(false)
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
            textAlign: 'center'
        },
        logoSection: {
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
        emailDisplay: {
            color: '#ffffff',
            fontWeight: '600',
            marginTop: '8px',
            fontSize: '14px'
        },
        form: {
            display: 'flex',
            flexDirection: 'column',
            gap: isMobile ? '20px' : '24px',
            marginTop: '20px'
        },
        inputGroup: {
            position: 'relative',
            textAlign: 'left'
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
            boxSizing: 'border-box',
            textAlign: 'center',
            letterSpacing: '4px',
            fontWeight: '600'
        },
        messageBox: {
            borderRadius: '8px',
            padding: isMobile ? '10px 14px' : '12px 16px',
            fontSize: isMobile ? '13px' : '14px',
            textAlign: 'left',
            marginBottom: '10px'
        },
        error: {
            background: 'rgba(239, 68, 68, 0.1)',
            border: '1px solid rgba(239, 68, 68, 0.3)',
            color: '#fca5a5',
            animation: 'shake 0.4s ease'
        },
        success: {
            background: 'rgba(34, 197, 94, 0.1)',
            border: '1px solid rgba(34, 197, 94, 0.3)',
            color: '#86efac'
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
        resendButton: {
            background: 'none',
            border: 'none',
            color: '#6366f1',
            textDecoration: 'none',
            fontWeight: '500',
            marginLeft: '6px',
            cursor: resending ? 'not-allowed' : 'pointer',
            opacity: resending ? 0.7 : 1,
            fontSize: 'inherit',
            padding: 0
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
        .primary-btn:hover {
          transform: translateY(-2px) !important;
          box-shadow: 0 6px 30px rgba(99, 102, 241, 0.5) !important;
        }
        .primary-btn:active {
          transform: translateY(0) !important;
        }
        .text-btn:hover {
          color: #818cf8 !important;
        }
        input:focus {
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1), 0 0 20px rgba(99, 102, 241, 0.2) !important;
        }
      `}</style>

            <div style={styles.authCard}>
                <div style={styles.logoSection}>
                    <div style={styles.logo}>Check your email</div>
                    <div style={styles.subtitle}>We've sent a 6-digit code to</div>
                    <div style={styles.emailDisplay}>{email}</div>
                </div>

                {error && <div style={{ ...styles.messageBox, ...styles.error }}>{error}</div>}
                {success && <div style={{ ...styles.messageBox, ...styles.success }}>{success}</div>}

                <form onSubmit={handleSubmit} style={styles.form}>
                    <div style={styles.inputGroup}>
                        <label style={{ ...styles.label, transform: otpFocused || otp ? 'translateY(-24px) scale(0.85)' : 'translateY(0)' }}>6-Digit OTP</label>
                        <input
                            type="text"
                            maxLength="6"
                            value={otp}
                            onChange={(e) => setOtp(e.target.value.replace(/\\D/g, ''))}
                            onFocus={() => setOtpFocused(true)}
                            onBlur={() => setOtpFocused(false)}
                            style={styles.input}
                            required
                        />
                    </div>

                    <button type="submit" disabled={loading} style={styles.button} className={!loading ? 'primary-btn' : ''}>
                        {loading ? <span style={styles.spinner}></span> : 'Verify Code'}
                    </button>
                </form>

                <div style={styles.footer}>
                    <span style={styles.footerText}>
                        Didn't receive a code?
                        <button
                            type="button"
                            onClick={handleResend}
                            disabled={resending}
                            style={styles.resendButton}
                            className="text-btn"
                        >
                            {resending ? 'Sending...' : 'Resend'}
                        </button>
                    </span>
                    <div style={{ marginTop: '12px' }}>
                        <Link to="/signup" style={{ color: '#94a3b8', fontSize: '13px', textDecoration: 'none' }} className="text-btn">
                            Use a different email
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    )
}
