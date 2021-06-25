FROM python:3.9

RUN pip install --upgrade pip
RUN pip3 install fastapi uvicorn aioredis asyncpg
COPY . .
CMD ['uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8000']