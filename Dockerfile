FROM python:3.8-slim-buster
RUN git clone https://github.com/Rajbhaiya/TG-File-Store /app
WORKDIR /app
RUN python3 -m pip install --no-cache-dir -r requirements.txt

CMD ["bash", "start"]
