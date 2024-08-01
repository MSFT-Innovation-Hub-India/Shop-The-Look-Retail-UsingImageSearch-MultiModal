FROM node:20.16.0 as base

WORKDIR /app
COPY package*.json ./
COPY .env.local ./
COPY next.config.mjs ./
EXPOSE 3000

FROM base as builder
WORKDIR /app
COPY . .
RUN npm run build


FROM base as production
WORKDIR /app

ENV NODE_ENV=production
RUN npm ci

COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public
COPY --from=builder /app/.env.local ./.env.local
COPY --from=builder /app/next.config.mjs ./next.config.mjs

CMD npm start
