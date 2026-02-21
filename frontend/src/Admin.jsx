import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"

export default function Admin() {
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isAdmin, setIsAdmin] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    checkAdminAccess()
    fetchAnalytics()
  }, [])

  const checkAdminAccess = async () => {
    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login')
      return
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/admin/validate', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        if (!data.is_admin) {
          alert('Admin access required')
          navigate('/dashboard')
        } else {
          setIsAdmin(true)
        }
      } else {
        navigate('/dashboard')
      }
    } catch (error) {
      console.error('Admin validation error:', error)
      navigate('/dashboard')
    }
  }

  const fetchAnalytics = async () => {
    const token = localStorage.getItem('token')
    try {
      const response = await fetch('http://127.0.0.1:8000/admin/analytics', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        setAnalytics(data)
      }
    } catch (error) {
      console.error('Analytics fetch error:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.clear()
    navigate('/login')
  }

  if (loading || !isAdmin) {
    return (
      <div style={{minHeight: '100vh', background: '#0a0e27', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff'}}>
        Loading...
      </div>
    )
  }

  return (
    <div style={{minHeight: '100vh', background: 'linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1428 100%)', color: '#e8eaf0', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif'}}>
      
      <nav style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '20px 48px', borderBottom: '1px solid rgba(99, 102, 241, 0.15)', background: 'rgba(10, 14, 39, 0.6)', backdropFilter: 'blur(12px)'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: '24px'}}>
          <div style={{fontSize: '22px', fontWeight: '700', background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'}}>
            SkillMatch Admin
          </div>
          <button 
            onClick={() => navigate('/dashboard')}
            style={{padding: '8px 16px', background: 'rgba(99, 102, 241, 0.15)', border: '1px solid rgba(99, 102, 241, 0.3)', borderRadius: '8px', color: '#6366f1', fontSize: '12px', fontWeight: '600', cursor: 'pointer'}}
          >
            ← Back to Dashboard
          </button>
        </div>
        <button 
          onClick={handleLogout}
          style={{padding: '8px 16px', background: 'rgba(239, 68, 68, 0.12)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', color: '#ef4444', fontSize: '12px', fontWeight: '600', cursor: 'pointer'}}
        >
          Logout
        </button>
      </nav>

      <div style={{padding: '40px 48px'}}>
        
        <div style={{marginBottom: '40px'}}>
          <h1 style={{fontSize: '36px', fontWeight: '800', marginBottom: '8px'}}>Analytics Dashboard</h1>
          <p style={{fontSize: '14px', color: '#94a3b8'}}>System-wide statistics and insights</p>
        </div>

        {analytics && (
          <>
            
            <div style={{display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px', marginBottom: '40px'}}>
              <div style={{padding: '24px', background: 'rgba(15, 20, 40, 0.6)', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.2)'}}>
                <div style={{fontSize: '13px', color: '#94a3b8', fontWeight: '600', marginBottom: '8px'}}>Total Users</div>
                <div style={{fontSize: '32px', fontWeight: '700', color: '#6366f1'}}>{analytics.summary.total_users}</div>
              </div>
              <div style={{padding: '24px', background: 'rgba(15, 20, 40, 0.6)', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.2)'}}>
                <div style={{fontSize: '13px', color: '#94a3b8', fontWeight: '600', marginBottom: '8px'}}>Total Submissions</div>
                <div style={{fontSize: '32px', fontWeight: '700', color: '#8b5cf6'}}>{analytics.summary.total_submissions}</div>
              </div>
              <div style={{padding: '24px', background: 'rgba(15, 20, 40, 0.6)', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.2)'}}>
                <div style={{fontSize: '13px', color: '#94a3b8', fontWeight: '600', marginBottom: '8px'}}>Total Analyses</div>
                <div style={{fontSize: '32px', fontWeight: '700', color: '#ec4899'}}>{analytics.summary.total_analyses}</div>
              </div>
              <div style={{padding: '24px', background: 'rgba(15, 20, 40, 0.6)', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.2)'}}>
                <div style={{fontSize: '13px', color: '#94a3b8', fontWeight: '600', marginBottom: '8px'}}>Avg Match Score</div>
                <div style={{fontSize: '32px', fontWeight: '700', color: '#10b981'}}>{analytics.summary.average_match_score}%</div>
              </div>
            </div>

            
            <div style={{display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px', marginBottom: '40px'}}>
              
              <div style={{padding: '24px', background: 'rgba(15, 20, 40, 0.6)', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.2)'}}>
                <h2 style={{fontSize: '18px', fontWeight: '700', marginBottom: '20px', color: '#fb923c'}}>Top Missing Skills</h2>
                <div style={{display: 'flex', flexDirection: 'column', gap: '12px'}}>
                  {analytics.top_missing_skills.slice(0, 10).map((item, idx) => (
                    <div key={idx} style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px', background: 'rgba(251, 146, 60, 0.1)', borderRadius: '8px', border: '1px solid rgba(251, 146, 60, 0.2)'}}>
                      <div>
                        <span style={{fontSize: '14px', fontWeight: '600', color: '#e2e8f0'}}>{idx + 1}. {item.skill}</span>
                      </div>
                      <div style={{display: 'flex', alignItems: 'center', gap: '12px'}}>
                        <span style={{fontSize: '12px', color: '#94a3b8'}}>{item.percentage}%</span>
                        <span style={{fontSize: '14px', fontWeight: '700', color: '#fb923c'}}>{item.count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              
              <div style={{padding: '24px', background: 'rgba(15, 20, 40, 0.6)', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.2)'}}>
                <h2 style={{fontSize: '18px', fontWeight: '700', marginBottom: '20px', color: '#4ade80'}}>Recommendation Distribution</h2>
                <div style={{display: 'flex', flexDirection: 'column', gap: '16px'}}>
                  <div>
                    <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '4px'}}>
                      <span style={{fontSize: '13px', color: '#4ade80'}}>Strong Fit</span>
                      <span style={{fontSize: '13px', fontWeight: '600', color: '#4ade80'}}>{analytics.recommendation_distribution.strong_fit}</span>
                    </div>
                    <div style={{height: '6px', background: 'rgba(74, 222, 128, 0.2)', borderRadius: '3px', overflow: 'hidden'}}>
                      <div style={{height: '100%', background: '#4ade80', width: `${(analytics.recommendation_distribution.strong_fit / analytics.recommendation_distribution.total * 100)}%`}}></div>
                    </div>
                  </div>
                  <div>
                    <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '4px'}}>
                      <span style={{fontSize: '13px', color: '#fbbf24'}}>Moderate Fit</span>
                      <span style={{fontSize: '13px', fontWeight: '600', color: '#fbbf24'}}>{analytics.recommendation_distribution.moderate_fit}</span>
                    </div>
                    <div style={{height: '6px', background: 'rgba(251, 191, 36, 0.2)', borderRadius: '3px', overflow: 'hidden'}}>
                      <div style={{height: '100%', background: '#fbbf24', width: `${(analytics.recommendation_distribution.moderate_fit / analytics.recommendation_distribution.total * 100)}%`}}></div>
                    </div>
                  </div>
                  <div>
                    <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '4px'}}>
                      <span style={{fontSize: '13px', color: '#fb923c'}}>Low Fit</span>
                      <span style={{fontSize: '13px', fontWeight: '600', color: '#fb923c'}}>{analytics.recommendation_distribution.low_fit}</span>
                    </div>
                    <div style={{height: '6px', background: 'rgba(251, 146, 60, 0.2)', borderRadius: '3px', overflow: 'hidden'}}>
                      <div style={{height: '100%', background: '#fb923c', width: `${(analytics.recommendation_distribution.low_fit / analytics.recommendation_distribution.total * 100)}%`}}></div>
                    </div>
                  </div>
                  <div>
                    <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '4px'}}>
                      <span style={{fontSize: '13px', color: '#ef4444'}}>Not Suitable</span>
                      <span style={{fontSize: '13px', fontWeight: '600', color: '#ef4444'}}>{analytics.recommendation_distribution.not_suitable}</span>
                    </div>
                    <div style={{height: '6px', background: 'rgba(239, 68, 68, 0.2)', borderRadius: '3px', overflow: 'hidden'}}>
                      <div style={{height: '100%', background: '#ef4444', width: `${(analytics.recommendation_distribution.not_suitable / analytics.recommendation_distribution.total * 100)}%`}}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            
            <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
              
              <div style={{padding: '24px', background: 'rgba(15, 20, 40, 0.6)', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.2)'}}>
                <h2 style={{fontSize: '18px', fontWeight: '700', marginBottom: '20px', color: '#6366f1'}}>Top Job Roles</h2>
                <div style={{display: 'flex', flexDirection: 'column', gap: '8px'}}>
                  {analytics.top_job_roles.map((item, idx) => (
                    <div key={idx} style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 12px', background: 'rgba(99, 102, 241, 0.1)', borderRadius: '6px'}}>
                      <span style={{fontSize: '13px', color: '#e2e8f0'}}>{item.role}</span>
                      <span style={{fontSize: '13px', fontWeight: '600', color: '#6366f1'}}>{item.count}</span>
                    </div>
                  ))}
                </div>
              </div>

              
              <div style={{padding: '24px', background: 'rgba(15, 20, 40, 0.6)', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.2)'}}>
                <h2 style={{fontSize: '18px', fontWeight: '700', marginBottom: '20px', color: '#8b5cf6'}}>Skill Category Distribution</h2>
                <div style={{display: 'flex', flexDirection: 'column', gap: '16px'}}>
                  {Object.entries(analytics.skill_category_distribution).map(([category, stats]) => (
                    <div key={category}>
                      <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '6px'}}>
                        <span style={{fontSize: '13px', color: '#cbd5e1', textTransform: 'capitalize'}}>{category}</span>
                        <span style={{fontSize: '13px', color: '#94a3b8'}}>M: {stats.matched} / Miss: {stats.missing}</span>
                      </div>
                      <div style={{display: 'flex', gap: '4px', height: '6px'}}>
                        <div style={{flex: stats.matched, background: '#4ade80', borderRadius: '3px'}}></div>
                        <div style={{flex: stats.missing, background: '#fb923c', borderRadius: '3px'}}></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
