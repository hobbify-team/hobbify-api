FROM nginx:1.15.8

RUN rm /etc/nginx/nginx.conf
COPY ./compose/production/nginx/nginx.conf /etc/nginx/
RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/production/nginx/project.conf /etc/nginx/conf.d/

COPY ./compose/production/nginx/*.crt /etc/nginx/
COPY ./compose/production/nginx/*.p7b  /etc/nginx/