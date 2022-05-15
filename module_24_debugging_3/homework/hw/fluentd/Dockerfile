FROM fluent/fluentd:v1.14-1

USER root

RUN ["gem", "install", "elasticsearch", "--version", "7.17.0"]
RUN apk add --no-cache --update --virtual .build-deps \
        sudo build-base ruby-dev \
&& sudo gem sources --clear-all \
&& apk del .build-deps
RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-document", "--version", "5.1.4"]
RUN ["fluent-gem", "install", "fluent-plugin-grok-parser"]


COPY conf/fluent.conf /fluentd/etc/

USER fluent
