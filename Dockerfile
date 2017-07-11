FROM python:2-onbuild

RUN brew update && brew upgrade --all && brew cleanup && brew prune
RUN install docker-machine

COPY start.sh /start.sh

EXPOSE 8000

CMD ["/start.sh"]
