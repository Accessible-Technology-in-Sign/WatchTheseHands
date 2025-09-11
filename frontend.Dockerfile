FROM node:18.19.1-slim@sha256:246bf34b0c7cf8d9ff7cbe0c1ff44b178051f06c432c8e7df1645f1bd20b0352
WORKDIR /app
COPY ./WebAnnotationEngine/package.json ./
RUN npm i
COPY ./WebAnnotationEngine/ ./
RUN npm run build
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]
EXPOSE 5173
