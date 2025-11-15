import { AlertCircle } from 'lucide-react'

export default function ErrorMessage({ message, className = '' }) {
  return (
    <div className={`flex items-center gap-2 p-4 bg-destructive/10 border border-destructive/20 rounded-lg text-destructive ${className}`}>
      <AlertCircle className="h-5 w-5 flex-shrink-0" />
      <p className="text-sm font-medium">{message || 'An error occurred. Please try again.'}</p>
    </div>
  )
}

