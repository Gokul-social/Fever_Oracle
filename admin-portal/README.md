# Fever Oracle - Admin Portal

Admin dashboard for Fever Oracle system monitoring and management.

## Features

- **Dashboard**: Overview statistics (hospitals, patients, hotspots, alerts)
- **Hospitals**: Table view of connected hospitals and their cases
- **Hotspots**: Predicted outbreak hotspots with risk levels
- **Alerts**: System alerts with similarity match scores

## Tech Stack

- React 18
- Vite
- TailwindCSS
- React Router
- Axios

## Development

```bash
# Install dependencies
npm install

# Start dev server (port 7000)
npm run dev

# Build for production
npm run build
```

## Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:5000
```

## Docker

```bash
# Build image
docker build -t fever-oracle-admin-portal .

# Run container
docker run -p 7000:7000 fever-oracle-admin-portal
```

## API Endpoints

The admin portal expects these backend endpoints:

- `GET /admin/stats` - Dashboard statistics
- `GET /admin/hospitals` - Hospitals list
- `GET /admin/hotspots` - Predicted hotspots
- `GET /admin/alerts` - System alerts

