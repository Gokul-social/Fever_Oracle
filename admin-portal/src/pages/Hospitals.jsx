import { useState, useEffect } from 'react'
import { adminAPI } from '@/lib/api'
import LoadingSpinner from '@/components/LoadingSpinner'
import ErrorMessage from '@/components/ErrorMessage'
import { formatNumber } from '@/lib/utils'

export default function Hospitals() {
  const [hospitals, setHospitals] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchHospitals()
  }, [])

  const fetchHospitals = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await adminAPI.getHospitals()
      setHospitals(response.data?.hospitals || response.data || [])
    } catch (err) {
      setError(err.message || 'Failed to load hospitals')
      // Mock data for development
      setHospitals([
        { hospital_name: 'City General Hospital', city: 'New York', active_cases: 45, high_risk_cases: 12 },
        { hospital_name: 'Metro Medical Center', city: 'Los Angeles', active_cases: 38, high_risk_cases: 9 },
        { hospital_name: 'Regional Health Center', city: 'Chicago', active_cases: 52, high_risk_cases: 15 },
        { hospital_name: 'Community Hospital', city: 'Houston', active_cases: 29, high_risk_cases: 7 },
        { hospital_name: 'University Medical', city: 'Phoenix', active_cases: 41, high_risk_cases: 11 },
      ])
    } finally {
      setLoading(false)
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
        <h1 className="text-3xl font-bold">Hospitals</h1>
        <p className="text-muted-foreground mt-1">Connected hospitals and their active cases</p>
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
                  Hospital Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                  City
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                  Active Cases
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                  High Risk Cases
                </th>
              </tr>
            </thead>
            <tbody className="bg-card divide-y divide-border">
              {hospitals.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-6 py-8 text-center text-muted-foreground">
                    No hospitals found
                  </td>
                </tr>
              ) : (
                hospitals.map((hospital, index) => (
                  <tr key={index} className="hover:bg-muted/50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      {hospital.hospital_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">
                      {hospital.city}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      {formatNumber(hospital.active_cases)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-destructive/10 text-destructive">
                        {formatNumber(hospital.high_risk_cases)}
                      </span>
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

