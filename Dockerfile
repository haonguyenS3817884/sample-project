FROM node:alpine AS development

ENV NODE_ENV development

WORKDIR /react-app

COPY . /react-app

RUN npm install

EXPOSE 3000

CMD ["npm", "run", "dev"]