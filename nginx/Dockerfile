FROM nginx:latest
RUN mkdir -p /home/staticfiles/ /home/staticfiles/
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY htpasswd /etc/nginx/.htpasswd