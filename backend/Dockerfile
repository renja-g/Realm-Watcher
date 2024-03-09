# Stage 1: Build
FROM python:3.12.2-alpine3.19 as builde

WORKDIR /build

COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.12.2-alpine3.19 as runtime

COPY --from=builde /root/.local /root/.local
COPY /app /app
COPY init.sh .

# Make scripts in .local usable
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

CMD sh init.sh && uvicorn app.main:app --host 0.0.0.0 --port 8000