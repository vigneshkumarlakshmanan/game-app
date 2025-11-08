FROM node:20 AS build
WORKDIR /app
COPY package*.json ./

RUN npm install -g npm@latest
RUN npm install

COPY public ./public
COPY src ./src
RUN npm run build


# production stage
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]
