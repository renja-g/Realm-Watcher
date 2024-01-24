# stage 1
FROM python:3.12.1-alpine3.19 as builder-stage

WORKDIR /tmp

RUN apk add --no-cache gcc musl-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# stage 2
FROM python:3.12.1-alpine3.19

WORKDIR /usr/src/app

COPY --from=builder-stage /tmp/requirements.txt /usr/src/app/requirements.txt

RUN apk add --no-cache gcc musl-dev
RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt

COPY . .

EXPOSE 12227

CMD ["python", "-u", "./ratelimiter.py"]
