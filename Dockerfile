FROM node:alpine AS development

ENV NODE_ENV development

WORKDIR /react-app

COPY . /react-app

RUN npm install

CMD ["npm", "run", "dev"]