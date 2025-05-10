FROM alpine:latest
VOLUME /home/git
RUN apk fix && \
  apk --no-cache --update add git git-lfs gpg less patch perl openssh tailscale && \
  git lfs install && \
  adduser git --home /home/git -D

WORKDIR /setup
COPY ./tailscale.sh .
RUN chmod +x tailscale.sh
ENTRYPOINT ["./tailscale.sh"]
