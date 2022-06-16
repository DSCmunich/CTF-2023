FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        chromium chromium-driver \
        python3 python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install selenium \
    && useradd -m -s /bin/bash browser

USER browser
WORKDIR /home/browser

COPY . .

EXPOSE 8080
CMD python3 app.py
