# Admin Portal Setup Guide

## Quick Start

### Local Development

```bash
cd admin-portal
npm install
npm run dev
```

Access at: http://localhost:7000

### Docker

```bash
# Build and run
docker-compose up -d admin-portal

# Or build separately
docker build -t fever-oracle-admin-portal ./admin-portal
docker run -p 7000:7000 fever-oracle-admin-portal
```

## Project Structure

```
admin-portal/
├── src/
│   ├── components/          # Reusable components
│   │   ├── LoadingSpinner.jsx
│   │   ├── ErrorMessage.jsx
│   │   └── StatCard.jsx
│   ├── layouts/             # Layout components
│   │   └── DashboardLayout.jsx
│   ├── pages/               # Page components
│   │   ├── Dashboard.jsx
│   │   ├── Hospitals.jsx
│   │   ├── Hotspots.jsx
│   │   └── Alerts.jsx
│   ├── lib/                 # Utilities
│   │   ├── api.js           # Axios API client
│   │   └── utils.js         # Helper functions
│   ├── App.jsx              # Main app component
│   ├── main.jsx             # Entry point
│   └── index.css            # Global styles
├── Dockerfile
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## API Integration

The admin portal connects to backend API endpoints:

- `GET /admin/stats` → Dashboard statistics
- `GET /admin/hospitals` → Hospitals list
- `GET /admin/hotspots` → Predicted hotspots
- `GET /admin/alerts` → System alerts

All endpoints are configured in `src/lib/api.js`.

## Features

- ✅ Modern React + Vite setup
- ✅ TailwindCSS styling
- ✅ Sidebar navigation
- ✅ Loading states
- ✅ Error handling
- ✅ Mock data fallbacks
- ✅ Responsive design
- ✅ Clean component structure

## Customization

### Change API URL

Edit `.env` or set environment variable:
```env
VITE_API_URL=http://your-backend-url:5000
```

### Add New Pages

1. Create page component in `src/pages/`
2. Add route in `src/App.jsx`
3. Add nav item in `src/layouts/DashboardLayout.jsx`

### Styling

All styles use TailwindCSS. Customize colors in `tailwind.config.js`.

