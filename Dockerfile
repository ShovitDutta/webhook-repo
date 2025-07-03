FROM node:18-alpine
WORKDIR /app
RUN apk add --no-cache gcc musl-dev python3-dev
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY package*.json ./
RUN npm install --force --silent
COPY . .
EXPOSE 5000
CMD ["python", "server.py"]