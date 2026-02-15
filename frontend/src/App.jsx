import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import Login from './Login'
import Signup from './Signup'
import Dashboard from './Dashboard'

function ProtectedRoute({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(null)

  useEffect(() => {
    const token = localStorage.getItem('token')
    setIsAuthenticated(!!token)
  }, [])

  if (isAuthenticated === null) {
    return <div style={{minHeight: '100vh', background: '#0a0e27', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff'}}>Loading...</div>
  }

  return isAuthenticated ? children : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
