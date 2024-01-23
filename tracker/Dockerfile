FROM python:3.12.1-alpine3.19

WORKDIR /usr/src/app

COPY . .

RUN apk add --no-cache gcc musl-dev
RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "./tracker.py"]
