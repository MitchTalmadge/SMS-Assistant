FROM robcherry/docker-chromedriver:headless

# Setup working environment
RUN mkdir /app
COPY . /app
COPY docker/entrypoint.sh /app
WORKDIR /app

# Install requirements
RUN pip install -r requirements.txt

# Start
ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]