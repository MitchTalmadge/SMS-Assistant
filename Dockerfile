FROM python:3

ENV FLASK_APP=/app/src/main.py
ENV HOST=0.0.0.0
ENV PORT=5000

# Setup working environment
RUN mkdir /app
COPY . /app
WORKDIR /app

# Install selenium dependencies
RUN apt update && \
    apt upgrade -y && \
    apt install -y  chromium \
                    chromium-driver

# Set display port to avoid crash
ENV DISPLAY=:99

# Install python requirements
RUN pip install -r requirements.txt

# Start
ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]