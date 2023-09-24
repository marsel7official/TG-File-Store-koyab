FROM python:3.8-slim-buster
RUN git clone https://github.com/Rajbhaiya/file-sharing/ /app
WORKDIR /app
RUN pip3 install -r requirements.txt

CMD ["bash", "start"]
