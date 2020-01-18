# base image
FROM node:12.3.1

# set working directory
WORKDIR /usr/src/app

RUN mkdir -p /usr/src/shared

# add `/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /usr/src/app/package.json
RUN npm install
RUN npm install -g @angular/cli

# add app
COPY . /usr/src/app

EXPOSE 80

# start app
CMD ng serve --host 0.0.0.0 --port 80
