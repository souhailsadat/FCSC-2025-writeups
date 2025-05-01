FROM alpine:3.21
WORKDIR /usr/app
COPY ./src/package.json .
RUN apk add --update --no-cache    \
	nodejs~=22                     \
	npm~=10                        \
	socat~=1.8                     \
	chromium-chromedriver~=135  && \
	npm install
COPY ./src .
ENV FLAG=FCSC{flag_placeholder}
EXPOSE 4000
CMD ["socat", "tcp-listen:4000,reuseaddr,fork", "exec:'node /usr/app/bot.js'"]
