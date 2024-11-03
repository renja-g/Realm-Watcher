FROM nginx:1.27.2-alpine

COPY . /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf

RUN nginx -t

HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget --quiet --tries=1 --spider http://localhost:80 || exit 1
