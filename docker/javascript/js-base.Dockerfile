FROM node:18
WORKDIR /app
COPY entrypoint.js .
CMD ["sleep", "infinity"]
