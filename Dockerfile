FROM python:3.7.4-alpine
WORKDIR /app
COPY . ./
RUN pip install --no-cache-dir -r requirements.txt
CMD python Alice.py