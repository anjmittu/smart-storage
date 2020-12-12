FROM martindsouza/amazon-ask-cli:latest

USER root

RUN apk add --update git

USER node

WORKDIR /home/node/app