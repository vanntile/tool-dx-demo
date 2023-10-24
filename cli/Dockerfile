FROM alpine:3.18.4

# Enable terminal color
ENV TERM=xterm-color CLICOLOR=1

# Update base python pacakges
RUN apk add zsh curl jq gum

# Use custom directory and user
WORKDIR /app
RUN adduser -h /home/user -S user && chown user /app

# Copy source code
COPY . .

# Use our own custom user
USER user

# Run app
CMD [ "zsh", "tool.sh" ]
