FROM alpine:latest

WORKDIR /app

COPY app/* .

ENV PYTHONUNBUFFERED=1
ENV RUST_BACKTRACE=full
RUN apk --no-cache update
RUN apk add --no-cache wireguard-tools iptables python3 py3-pip dumb-init shadowsocks-rust
RUN ln -sf python3 /usr/bin/python
RUN python3 - m enpip 
RUN pip3 install --no-cache --break-system-packages -r requirements.txt 

CMD ["/usr/bin/dumb-init", "python3", "server.py"]

EXPOSE 51820/udp 5000/tcp

