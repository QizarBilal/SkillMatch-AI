import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import API_BASE_URL from './config'

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

export default function Admin() {
  const { isMobile, isTablet } = useWindowSize();
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
      const response = await fetch(`${API_BASE_URL}/admin/validate`, {
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
      const response = await fetch(`${API_BASE_URL}/admin/analytics`, {
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

  const styles = {
    container: {
      minHeight: '100vh', 
      background: 'linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1428 100%)', 
      color: '#e8eaf0', 
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif'
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
      gap: isMobile ? '12px' : '0'
    },
    navLeft: {
      display: 'flex', 
      alignItems: 'center', 
      gap: isMobile ? '12px' : '24px',
      flexWrap: isMobile ? 'wrap' : 'nowrap'
    },
    logo: {
      fontSize: isMobile ? '16px' : isTablet ? '19px' : '22px', 
      fontWeight: '700', 
      background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)', 
      WebkitBackgroundClip: 'text', 
      WebkitTextFillColor: 'transparent'
    },
    backBtn: {
      padding: isMobile ? '6px 12px' : '8px 16px', 
      background: 'rgba(99, 102, 241, 0.15)', 
      border: '1px solid rgba(99, 102, 241, 0.3)', 
      borderRadius: '8px', 
      color: '#6366f1', 
      fontSize: isMobile ? '11px' : '12px', 
      fontWeight: '600', 
      cursor: 'pointer'
    },
    logoutBtn: {
      padding: isMobile ? '6px 12px' : '8px 16px', 
      background: 'rgba(239, 68, 68, 0.12)', 
      border: '1px solid rgba(239, 68, 68, 0.3)', 
      borderRadius: '8px', 
      color: '#ef4444', 
      fontSize: isMobile ? '11px' : '12px', 
      fontWeight: '600', 
      cursor: 'pointer'
    },
    content: {
      padding: isMobile ? '20px 16px' : isTablet ? '32px 24px' : '40px 48px'
    },
    header: {
      marginBottom: isMobile ? '24px' : '40px'
    },
    title: {
      fontSize: isMobile ? '24px' : isTablet ? '30px' : '36px', 
      fontWeight: '800', 
      marginBottom: '8px'
    },
    subtitle: {
      fontSize: isMobile ? '13px' : '14px', 
      color: '#94a3b8'
    },
    statsGrid: {
      display: 'grid', 
      gridTemplateColumns: isMobile ? '1fr' : isTablet ? 'repeat(2, 1fr)' : 'repeat(4, 1fr)', 
      gap: isMobile ? '12px' : '20px', 
      marginBottom: isMobile ? '24px' : '40px'
    },
    statCard: {
      padding: isMobile ? '16px' : '24px', 
      background: 'rgba(15, 20, 40, 0.6)', 
      borderRadius: isMobile ? '10px' : '12px', 
      border: '1px solid rgba(99, 102, 241, 0.2)'
    },
    statLabel: {
      fontSize: isMobile ? '12px' : '13px', 
      color: '#94a3b8', 
      fontWeight: '600', 
      marginBottom: isMobile ? '6px' : '8px'
    },
    statValue: {
      fontSize: isMobile ? '24px' : isTablet ? '28px' : '32px', 
      fontWeight: '700'
    },
    contentGrid: {
      display: 'grid', 
      gridTemplateColumns: isMobile ? '1fr' : isTablet ? '1fr' : '2fr 1fr', 
      gap: isMobile ? '16px' : '20px', 
      marginBottom: isMobile ? '24px' : '40px'
    },
    card: {
      padding: isMobile ? '16px' : '24px', 
      background: 'rgba(15, 20, 40, 0.6)', 
      borderRadius: isMobile ? '10px' : '12px', 
      border: '1px solid rgba(99, 102, 241, 0.2)'
    },
    cardTitle: {
      fontSize: isMobile ? '16px' : '18px', 
      fontWeight: '700', 
      marginBottom: isMobile ? '16px' : '20px'
    },
    skillItem: {
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'space-between', 
      padding: isMobile ? '10px' : '12px', 
      borderRadius: '8px',
      flexWrap: isMobile ? 'wrap' : 'nowrap',
      gap: isMobile ? '8px' : '0'
    },
    skillName: {
      fontSize: isMobile ? '13px' : '14px', 
      fontWeight: '600', 
      color: '#e2e8f0'
    },
    skillStats: {
      display: 'flex', 
      alignItems: 'center', 
      gap: isMobile ? '8px' : '12px'
    },
    skillPercentage: {
      fontSize: isMobile ? '11px' : '12px', 
      color: '#94a3b8'
    },
    skillCount: {
      fontSize: isMobile ? '13px' : '14px', 
      fontWeight: '700'
    }
  };

  return (
    <div style={styles.container}>
      
      <nav style={styles.nav}>
        <div style={styles.navLeft}>
          <div style={styles.logo}>
            SkillMatch Admin
          </div>
          <button 
            onClick={() => navigate('/dashboard')}
            style={styles.backBtn}
          >
            ← {isMobile ? 'Back' : 'Back to Dashboard'}
          </button>
        </div>
        <button 
          onClick={handleLogout}
          style={styles.logoutBtn}
        >
          Logout
        </button>
      </nav>

      <div style={styles.content}>
        
        <div style={styles.header}>
          <h1 style={styles.title}>Analytics Dashboard</h1>
          <p style={styles.subtitle}>System-wide statistics and insights</p>
        </div>

        {analytics && (
          <>
            
            <div style={styles.statsGrid}>
              <div style={styles.statCard}>
                <div style={styles.statLabel}>Total Users</div>
                <div style={{...styles.statValue, color: '#6366f1'}}>{analytics.summary.total_users}</div>
              </div>
              <div style={styles.statCard}>
                <div style={styles.statLabel}>Total Submissions</div>
                <div style={{...styles.statValue, color: '#8b5cf6'}}>{analytics.summary.total_submissions}</div>
              </div>
              <div style={styles.statCard}>
                <div style={styles.statLabel}>Total Analyses</div>
                <div style={{...styles.statValue, color: '#ec4899'}}>{analytics.summary.total_analyses}</div>
              </div>
              <div style={styles.statCard}>
                <div style={styles.statLabel}>Avg Match Score</div>
                <div style={{...styles.statValue, color: '#10b981'}}>{analytics.summary.average_match_score}%</div>
              </div>
            </div>

            
            <div style={styles.contentGrid}>
              
              <div style={styles.card}>
                <h2 style={{...styles.cardTitle, color: '#fb923c'}}>Top Missing Skills</h2>
                <div style={{display: 'flex', flexDirection: 'column', gap: isMobile ? '8px' : '12px'}}>
                  {analytics.top_missing_skills.slice(0, 10).map((item, idx) => (
                    <div key={idx} style={{...styles.skillItem, background: 'rgba(251, 146, 60, 0.1)', border: '1px solid rgba(251, 146, 60, 0.2)'}}>
                      <div style={styles.skillName}>{idx + 1}. {item.skill}</div>
                      <div style={styles.skillStats}>
                        <span style={styles.skillPercentage}>{item.percentage}%</span>
                        <span style={{...styles.skillCount, color: '#fb923c'}}>{item.count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              
              <div style={styles.card}>
                <h2 style={{...styles.cardTitle, color: '#4ade80'}}>Recommendation Distribution</h2>
                <div style={{display: 'flex', flexDirection: 'column', gap: isMobile ? '12px' : '16px'}}>
                  <div>
                    <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '4px'}}>
                      <span style={{fontSize: isMobile ? '12px' : '13px', color: '#4ade80'}}>Strong Fit</span>
                      <span style={{fontSize: isMobile ? '12px' : '13px', fontWeight: '600', color: '#4ade80'}}>{analytics.recommendation_distribution.strong_fit}</span>
                    </div>
                    <div style={{height: isMobile ? '5px' : '6px', background: 'rgba(74, 222, 128, 0.2)', borderRadius: '3px', overflow: 'hidden'}}>
                      <div style={{height: '100%', background: '#4ade80', width: `${(analytics.recommendation_distribution.strong_fit / analytics.recommendation_distribution.total * 100)}%`}}></div>
                    </div>
                  </div>
                  <div>
                    <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '4px'}}>
                      <span style={{fontSize: isMobile ? '12px' : '13px', color: '#fbbf24'}}>Moderate Fit</span>
                      <span style={{fontSize: isMobile ? '12px' : '13px', fontWeight: '600', color: '#fbbf24'}}>{analytics.recommendation_distribution.moderate_fit}</span>
                    </div>
                    <div style={{height: isMobile ? '5px' : '6px', background: 'rgba(251, 191, 36, 0.2)', borderRadius: '3px', overflow: 'hidden'}}>
                      <div style={{height: '100%', background: '#fbbf24', width: `${(analytics.recommendation_distribution.moderate_fit / analytics.recommendation_distribution.total * 100)}%`}}></div>
                    </div>
                  </div>
                  <div>
                    <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '4px'}}>
                      <span style={{fontSize: isMobile ? '12px' : '13px', color: '#fb923c'}}>Low Fit</span>
                      <span style={{fontSize: isMobile ? '12px' : '13px', fontWeight: '600', color: '#fb923c'}}>{analytics.recommendation_distribution.low_fit}</span>
                    </div>
                    <div style={{height: isMobile ? '5px' : '6px', background: 'rgba(251, 146, 60, 0.2)', borderRadius: '3px', overflow: 'hidden'}}>
                      <div style={{height: '100%', background: '#fb923c', width: `${(analytics.recommendation_distribution.low_fit / analytics.recommendation_distribution.total * 100)}%`}}></div>
                    </div>
                  </div>
                  <div>
                    <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '4px'}}>
                      <span style={{fontSize: isMobile ? '12px' : '13px', color: '#ef4444'}}>Not Suitable</span>
                      <span style={{fontSize: isMobile ? '12px' : '13px', fontWeight: '600', color: '#ef4444'}}>{analytics.recommendation_distribution.not_suitable}</span>
                    </div>
                    <div style={{height: isMobile ? '5px' : '6px', background: 'rgba(239, 68, 68, 0.2)', borderRadius: '3px', overflow: 'hidden'}}>
                      <div style={{height: '100%', background: '#ef4444', width: `${(analytics.recommendation_distribution.not_suitable / analytics.recommendation_distribution.total * 100)}%`}}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            
            <div style={{display: 'grid', gridTemplateColumns: isMobile ? '1fr' : isTablet ? '1fr' : '1fr 1fr', gap: isMobile ? '16px' : '20px'}}>
              
              <div style={styles.card}>
                <h2 style={{...styles.cardTitle, color: '#6366f1'}}>Top Job Roles</h2>
                <div style={{display: 'flex', flexDirection: 'column', gap: isMobile ? '6px' : '8px'}}>
                  {analytics.top_job_roles.map((item, idx) => (
                    <div key={idx} style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: isMobile ? '8px 10px' : '10px 12px', background: 'rgba(99, 102, 241, 0.1)', borderRadius: '6px'}}>
                      <span style={{fontSize: isMobile ? '12px' : '13px', color: '#e2e8f0'}}>{item.role}</span>
                      <span style={{fontSize: isMobile ? '12px' : '13px', fontWeight: '600', color: '#6366f1'}}>{item.count}</span>
                    </div>
                  ))}
                </div>
              </div>

              
              <div style={styles.card}>
                <h2 style={{...styles.cardTitle, color: '#8b5cf6'}}>Skill Category Distribution</h2>
                <div style={{display: 'flex', flexDirection: 'column', gap: isMobile ? '12px' : '16px'}}>
                  {Object.entries(analytics.skill_category_distribution).map(([category, stats]) => (
                    <div key={category}>
                      <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '6px'}}>
                        <span style={{fontSize: isMobile ? '12px' : '13px', color: '#cbd5e1', textTransform: 'capitalize'}}>{category}</span>
                        <span style={{fontSize: isMobile ? '11px' : '13px', color: '#94a3b8'}}>M: {stats.matched} / Miss: {stats.missing}</span>
                      </div>
                      <div style={{display: 'flex', gap: '4px', height: isMobile ? '5px' : '6px'}}>
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
