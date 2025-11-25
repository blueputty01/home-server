# syntax=docker/dockerfile:1
FROM alpine:3.20

# Install dependencies: bash, ffmpeg (for ffplay), tzdata for cron correctness
RUN apk add --no-cache bash ffmpeg tzdata

WORKDIR /app

# Copy scripts and audio assets
COPY manager.sh fadeloop.sh ./
COPY noise/ ./noise/

# Create symlink for easier invocation
RUN ln -s /app/manager.sh /usr/local/bin/noise-manager && \
    chmod +x /app/manager.sh /app/fadeloop.sh

# Copy entrypoint
COPY entrypoint.sh ./
RUN chmod +x /app/entrypoint.sh

ENV NOISE_CRON=""

# Healthcheck relies on noise-manager script
# (Compose overrides can redefine it.)

ENTRYPOINT ["/app/entrypoint.sh"]
