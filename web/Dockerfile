FROM node:20-slim AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
COPY . /web
WORKDIR /web

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

RUN pnpm run build

FROM nginx

COPY --from=base /web/dist /static

COPY nginx.conf /etc/nginx/templates/default.conf.template