FROM joyzoursky/python-chromedriver:3.8

ENV BASENAME=""
ENV FLASK_APP=/app/src/main.py
ENV HOST=0.0.0.0
ENV PORT=5000

# Setup working environment
RUN mkdir /app
COPY . /app
WORKDIR /app

# Install python requirements
RUN pip install -r requirements.txt

# Start
ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]
