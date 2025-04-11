FROM node:16.13.0-buster

WORKDIR /app/

COPY package*.json /app/

RUN npm i

COPY . .

CMD ["npm", "run", "start"]
