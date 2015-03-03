FROM nginx

MAINTAINER Marian Steinbach <marian@giantswarm.io>

ADD nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/*

EXPOSE 80

ENTRYPOINT ["nginx"]
