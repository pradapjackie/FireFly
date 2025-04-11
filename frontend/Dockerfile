FROM node:16.13.0-buster as build-stage

ARG REACT_APP_TEST_DEV_MODE
ENV REACT_APP_TEST_DEV_MODE=$REACT_APP_TEST_DEV_MODE

WORKDIR /app/

COPY ./nginx.conf /nginx.conf

COPY package*.json /app/

RUN npm i --only=prod --no-optional --legacy-peer-deps

COPY . .

RUN npm run build

FROM nginx:stable-alpine as prod

COPY --from=build-stage /app/build/ /usr/share/nginx/html

COPY --from=build-stage /nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
