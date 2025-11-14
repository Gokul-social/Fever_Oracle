FROM node:20-alpine

WORKDIR /app

# Copy package files first (for better Docker layer caching)
COPY package.json ./

# Copy lockfile if it exists (optional for development)
# The * makes it optional - won't fail if file doesn't exist
COPY package-lock.json* ./

# Install dependencies
# For development, use npm install which is more forgiving
# npm ci is stricter and requires exact lockfile match
RUN if [ -f package-lock.json ]; then \
      echo "Found package-lock.json, attempting npm ci..." && \
      (npm ci --legacy-peer-deps 2>&1 || (echo "npm ci failed, using npm install instead" && npm install --legacy-peer-deps)); \
    else \
      echo "No package-lock.json found, using npm install" && \
      npm install --legacy-peer-deps; \
    fi

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Start development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

