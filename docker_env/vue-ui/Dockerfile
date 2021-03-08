FROM node:12
RUN npm install --registry=https://registry.npm.taobao.org
RUN npm run build:prod
CMD ["npm","run","dev"]
