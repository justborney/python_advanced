FROM fluent/fluentd:v1.12.0-debian-1.0
USER root
RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-document", "--version", "5.1.4"]
#RUN ["gem", "install", "fluent-plugin-elasticsearch:5.1.4", "fluent-plugin-grok-parser:2.6.2"]
RUN ["fluent-gem", "install", "fluent-plugin-grok-parser"]
USER fluent

#FROM fluent/fluentd:v1.12.0-debian-1.0
#
#RUN gem install fluent-plugin-elasticsearch:5.1.4 fluent-plugin-grok-parser \
#    && gem sources --clear-all
#gem install fluent-plugin-grok-parser -v 0.0.2