FROM python:3.10-slim-bullseye
LABEL maintainer="AvBerTech"

ENV telegram_api_token = ''
ENV gizmo_api_token = ''
ENV gizmo_server_ip = ''
ENV db_table = ''

ARG DEBIAN_FRONTEND=noninteractive

RUN adduser --disabled-password gizmo_bot --gecos "gizmo_bot" >> /dev/null
RUN apt-get update && DEBCONF_NOWARNINGS=yes DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && apt-get clean

WORKDIR /home/gizmo_bot/

COPY --chown=gizmo_bot:gizmo_bot ./bot /home/gizmo_bot/bot
COPY --chown=gizmo_bot:gizmo_bot ./requirements.txt /home/gizmo_bot/