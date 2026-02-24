import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import { useEffect, useState, createContext, useContext } from 'react'
import Login from './Login'
import Signup from './Signup'
import Dashboard from './Dashboard'
import Admin from './Admin'
import PremiumLoader from './PremiumLoader'

const AuthContext = createContext(null)

export const useAuth = () => useContext(AuthContext)

function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [initialLoading, setInitialLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    const timer = setTimeout(() => {
      setInitialLoading(false)
    }, 3500)

    return () => clearTimeout(timer)
  }, [])

  useEffect(() => {
    const handleAuthError = () => {
      setToken(null)
      navigate('/login')
    }
    window.addEventListener('auth-error', handleAuthError)
    return () => window.removeEventListener('auth-error', handleAuthError)
  }, [navigate])

  const login = (newToken, userData = {}) => {
    localStorage.setItem('token', newToken)
    if (userData.user_id) localStorage.setItem('user_id', userData.user_id)
    if (userData.email) localStorage.setItem('user_email', userData.email)
    setToken(newToken)
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user_id')
    localStorage.removeItem('user_email')
    localStorage.removeItem('skillmatch_result')
    setToken(null)
    navigate('/login')
  }

  if (initialLoading) {
    return <PremiumLoader />
  }

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

function ProtectedRoute({ children, requireAuth = true }) {
  const { token } = useAuth()

  if (requireAuth && !token) {
    return <Navigate to="/login" replace />
  }

  if (!requireAuth && token) {
    return <Navigate to="/dashboard" replace />
  }

  return children
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<ProtectedRoute requireAuth={false}><Login /></ProtectedRoute>} />
          <Route path="/signup" element={<ProtectedRoute requireAuth={false}><Signup /></ProtectedRoute>} />
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/admin" element={<ProtectedRoute><Admin /></ProtectedRoute>} />
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

