FROM node:18-alpine
RUN apk add --no-cache gcc musl-dev python3-dev
RUN python3 -m ensurepip && pip3 install --upgrade pip
WORKDIR /app
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN npm install --force --silent
EXPOSE 5000
CMD ["python3", "server.py"]