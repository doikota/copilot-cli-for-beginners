
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# Yarn の署名鍵を登録し、APT の参照先を設定する
RUN mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://dl.yarnpkg.com/debian/pubkey.gpg \
       | gpg --dearmor --yes \
       -o /etc/apt/keyrings/yarn-archive-keyring.gpg \
    && for f in /etc/apt/sources.list.d/*; do \
         if [ -f "$f" ]; then \
           sed -i '\|dl.yarnpkg.com/debian|d' "$f"; \
         fi; \
       done \
    && printf '%s\n' \
       'deb [signed-by=/etc/apt/keyrings/yarn-archive-keyring.gpg] https://dl.yarnpkg.com/debian/ stable main' \
       > /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends locales \
    && sed -i 's/^# *\(ja_JP.UTF-8 UTF-8\)/\1/' /etc/locale.gen \
    && locale-gen \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=ja_JP.UTF-8
ENV LC_ALL=ja_JP.UTF-8