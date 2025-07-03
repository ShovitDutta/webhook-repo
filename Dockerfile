FROM node:18-alpine
WORKDIR /app
RUN apk add --no-cache gcc musl-dev python3-dev
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN npm install --force --silent
EXPOSE 5000
CMD ["python", "server.py"]