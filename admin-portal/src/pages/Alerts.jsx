import { useState, useEffect } from 'react'
import { adminAPI } from '@/lib/api'
import LoadingSpinner from '@/components/LoadingSpinner'
import ErrorMessage from '@/components/ErrorMessage'
import { formatDate } from '@/lib/utils'
import { AlertCircle } from 'lucide-react'

export default function Alerts() {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchAlerts()
  }, [])

  const fetchAlerts = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await adminAPI.getAlerts()
      setAlerts(response.data?.alerts || response.data || [])
    } catch (err) {
      setError(err.message || 'Failed to load alerts')
      // Mock data for development
      setAlerts([
        {
          alert_id: 'ALT-001',
          timestamp: new Date().toISOString(),
          description: 'Elevated fever cases detected in Downtown District',
          similarity_match_score: 0.94,
        },
        {
          alert_id: 'ALT-002',
          timestamp: new Date(Date.now() - 3600000).toISOString(),
          description: 'Wastewater viral load threshold exceeded',
          similarity_match_score: 0.87,
        },
        {
          alert_id: 'ALT-003',
          timestamp: new Date(Date.now() - 7200000).toISOString(),
          description: 'Pharmacy OTC sales spike detected',
          similarity_match_score: 0.82,
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 0.9) return 'bg-destructive/10 text-destructive'
    if (score >= 0.7) return 'bg-yellow-100 text-yellow-800'
    return 'bg-green-100 text-green-800'
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Alerts</h1>
        <p className="text-muted-foreground mt-1">System alerts and notifications</p>
      </div>

      {error && (
        <div className="mb-4">
          <ErrorMessage message={error} />
        </div>
      )}

      {/* Alerts List */}
      <div className="space-y-4">
        {alerts.length === 0 ? (
          <div className="bg-card border border-border rounded-lg p-8 text-center text-muted-foreground">
            No alerts found
          </div>
        ) : (
          alerts.map((alert, index) => (
            <div
              key={index}
              className="bg-card border border-border rounded-lg p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-4 flex-1">
                  <div className="h-10 w-10 rounded-full bg-destructive/10 flex items-center justify-center flex-shrink-0">
                    <AlertCircle className="h-5 w-5 text-destructive" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-sm font-semibold">{alert.alert_id}</h3>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getScoreColor(alert.similarity_match_score)}`}>
                        {(alert.similarity_match_score * 100).toFixed(0)}% match
                      </span>
                    </div>
                    <p className="text-sm text-muted-foreground mb-2">{alert.description}</p>
                    <p className="text-xs text-muted-foreground">{formatDate(alert.timestamp)}</p>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

