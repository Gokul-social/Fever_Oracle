import { cn } from '@/lib/utils'

export default function StatCard({ title, value, icon: Icon, className = '' }) {
  return (
    <div className={cn(
      "bg-card border border-border rounded-lg p-6 shadow-sm",
      className
    )}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-muted-foreground">{title}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
        </div>
        {Icon && (
          <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
            <Icon className="h-6 w-6 text-primary" />
          </div>
        )}
      </div>
    </div>
  )
}

