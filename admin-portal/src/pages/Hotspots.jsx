import { useState, useEffect } from 'react'
import { adminAPI } from '@/lib/api'
import LoadingSpinner from '@/components/LoadingSpinner'
import ErrorMessage from '@/components/ErrorMessage'
import { AlertTriangle } from 'lucide-react'

export default function Hotspots() {
  const [hotspots, setHotspots] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchHotspots()
  }, [])

  const fetchHotspots = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await adminAPI.getHotspots()
      setHotspots(response.data?.hotspots || response.data || [])
    } catch (err) {
      setError(err.message || 'Failed to load hotspots')
      // Mock data for development
      setHotspots([
        { area: 'Downtown District', predicted_risk: 'High', lead_time_days: 3 },
        { area: 'Northside Suburbs', predicted_risk: 'Medium', lead_time_days: 7 },
        { area: 'East End', predicted_risk: 'High', lead_time_days: 5 },
        { area: 'West Quarter', predicted_risk: 'Low', lead_time_days: 12 },
        { area: 'Central Plaza', predicted_risk: 'Medium', lead_time_days: 8 },
      ])
    } finally {
      setLoading(false)
    }
  }

  const getRiskColor = (risk) => {
    switch (risk?.toLowerCase()) {
      case 'high':
        return 'bg-destructive/10 text-destructive'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'low':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-muted text-muted-foreground'
    }
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
        <h1 className="text-3xl font-bold">Predicted Hotspots</h1>
        <p className="text-muted-foreground mt-1">Areas with predicted fever outbreak risk</p>
      </div>

      {error && (
        <div className="mb-4">
          <ErrorMessage message={error} />
        </div>
      )}

      {/* Table */}
      <div className="bg-card border border-border rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-muted">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                  Area
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                  Predicted Risk
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                  Lead Time (Days)
                </th>
              </tr>
            </thead>
            <tbody className="bg-card divide-y divide-border">
              {hotspots.length === 0 ? (
                <tr>
                  <td colSpan={3} className="px-6 py-8 text-center text-muted-foreground">
                    No hotspots predicted
                  </td>
                </tr>
              ) : (
                hotspots.map((hotspot, index) => (
                  <tr key={index} className="hover:bg-muted/50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <AlertTriangle className="h-4 w-4 text-muted-foreground" />
                        <span className="text-sm font-medium">{hotspot.area}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getRiskColor(hotspot.predicted_risk)}`}>
                        {hotspot.predicted_risk}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">
                      {hotspot.lead_time_days} days
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

