FROM node:14-alpine

# Create app directory
WORKDIR /code

# Install app dependencies
COPY package*.json ./
RUN npm install

# Bundle app source
COPY ./assets /code/assets
COPY ./webpack.config.js .

CMD [ "npm", "run", "dev" ]
