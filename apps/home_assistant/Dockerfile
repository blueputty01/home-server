# syntax=docker/dockerfile:1
FROM ghcr.io/home-assistant/home-assistant:stable
# Install dependencies: bash, ffmpeg (for ffplay), tzdata for cron correctness
RUN apk update && apk add --no-cache ffplay