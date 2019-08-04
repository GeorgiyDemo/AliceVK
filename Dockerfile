FROM python:3.7.4-alpine
WORKDIR /app
COPY . ./
RUN apk add --no-cache tzdata
ENV TZ=Europe/Moscow
RUN pip install --no-cache-dir -r requirements.txt
CMD python Alice.py