import { Outlet, NavLink } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Building2, 
  MapPin, 
  Bell,
  Activity
} from 'lucide-react'
import { cn } from '@/lib/utils'

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/hospitals', label: 'Hospitals', icon: Building2 },
  { path: '/hotspots', label: 'Hotspots', icon: MapPin },
  { path: '/alerts', label: 'Alerts', icon: Bell },
]

export default function DashboardLayout() {
  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-full w-64 bg-card border-r border-border">
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="h-16 border-b border-border flex items-center px-6">
            <div className="flex items-center gap-2">
              <Activity className="h-6 w-6 text-primary" />
              <span className="text-xl font-bold">Fever Oracle</span>
            </div>
            <span className="ml-2 text-xs text-muted-foreground">Admin</span>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    cn(
                      "flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors",
                      isActive
                        ? "bg-primary text-primary-foreground"
                        : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                    )
                  }
                >
                  <Icon className="h-5 w-5" />
                  {item.label}
                </NavLink>
              )
            })}
          </nav>
        </div>
      </aside>

      {/* Main Content */}
      <main className="ml-64">
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  )
}

