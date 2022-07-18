FROM node:18-alpine3.15

WORKDIR /app

COPY . /app

RUN yarn install

RUN yarn build

ENTRYPOINT yarn start