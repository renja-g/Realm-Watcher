# stage 1
FROM python:3.12.1-alpine3.19 as builder

WORKDIR /usr/src/app

RUN apk add --no-cache gcc musl-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# stage 2
FROM python:3.12.1-alpine3.19

WORKDIR /usr/src/app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .

EXPOSE 12227

CMD ["python", "-u", "./ratelimiter.py"]
