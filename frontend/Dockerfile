# Stage 1: Build stage
FROM node:20.11.0-alpine3.18 AS builder

WORKDIR /app
COPY package.json package-lock.json ./

# Install all dependencies including 'devDependencies'
RUN npm ci

COPY . .

# Build the application
RUN npm run build

# Remove development dependencies
RUN npm prune --production

# Stage 2: Runtime stage
FROM node:20.11.0-alpine3.18

WORKDIR /app

# Copy built artifacts and necessary files from the builder stage
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

ENV PORT 3000
EXPOSE 3000

CMD ["node", "build"]
