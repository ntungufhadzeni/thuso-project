FROM nginx:latest
RUN mkdir -p /home/static /home/media
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY htpasswd /etc/nginx/.htpasswd