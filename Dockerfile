FROM locustio/locust
COPY . /mnt/locust
WORKDIR /mnt/locust
RUN pip3 install -r requirements.txt
ENTRYPOINT locust -f characterization/characterization.py
