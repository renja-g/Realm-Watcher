FROM node:20.11.0-alpine3.18

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --production

ENV PORT 3000
EXPOSE 3000
CMD ["node", "build"]
