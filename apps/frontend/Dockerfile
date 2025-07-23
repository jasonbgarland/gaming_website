# Production-ready Dockerfile for Next.js (with Tailwind CSS)
FROM node:20-alpine AS deps
WORKDIR /app
# Copy package files first for better layer caching
COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./
RUN \
  if [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm install --frozen-lockfile; \
  fi

# Build the Next.js app
FROM node:20-alpine AS builder
WORKDIR /app

# Accept build arguments for Next.js environment variables
ARG NEXT_PUBLIC_AUTH_API_URL
ARG NEXT_PUBLIC_GAME_API_URL
ARG NEXT_PUBLIC_GAME_SERVICE_URL

# Set environment variables for build
ENV NEXT_PUBLIC_AUTH_API_URL=$NEXT_PUBLIC_AUTH_API_URL
ENV NEXT_PUBLIC_GAME_API_URL=$NEXT_PUBLIC_GAME_API_URL
ENV NEXT_PUBLIC_GAME_SERVICE_URL=$NEXT_PUBLIC_GAME_SERVICE_URL

COPY --from=deps /app/node_modules ./node_modules
# Copy package.json first for better caching
COPY package.json ./
# Copy source code last (changes most frequently)
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Production image, copy built assets and run Next.js
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# If you use a custom next.config.js, uncomment below
# COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000
CMD ["npm", "start"]
