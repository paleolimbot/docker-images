FROM openjdk:18-buster
RUN apt-get update && \
  apt-get install -y python3-pip && \
  pip3 install requests beautifulsoup4

RUN mkdir /argo-checker && mkdir /nc
COPY argo-checker.py /argo-checker/argo-checker.py
RUN python3 /argo-checker/argo-checker.py check --update
WORKDIR /nc
ENTRYPOINT ["python3", "/argo-checker/argo-checker.py"]
