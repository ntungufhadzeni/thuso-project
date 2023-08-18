FROM nginx:latest
RUN mkdir -p /home/staticfiles && mkdir /home/mediafiles
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d