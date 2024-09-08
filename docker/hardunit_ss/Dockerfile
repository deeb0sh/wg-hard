FROM alpine:latest

WORKDIR /app

COPY app/* .
COPY 00-ss-rust.conf /etc/sysctl.d/00-ss-rust.conf

ENV PYTHONUNBUFFERED=1
ENV RUST_BACKTRACE=full
RUN apk --no-cache update
RUN apk add --no-cache wireguard-tools iptables python3 py3-pip shadowsocks-rust
RUN ln -sf python3 /usr/bin/python
RUN python3 - m enpip 
RUN pip3 install --no-cache --break-system-packages -r requirements.txt 

CMD ["python3", "server.py"]

EXPOSE 8388/tcp 8388/udp 5000/tcp

