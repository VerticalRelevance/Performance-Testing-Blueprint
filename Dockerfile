FROM locustio/locust
COPY . /home/locust/app
WORKDIR /home/locust/app
RUN pip3 install -r requirements.txt
ENTRYPOINT locust -f characterization/characterization.py
