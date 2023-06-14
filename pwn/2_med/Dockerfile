# docker build -t med . && docker run -p 1337:1337 med
FROM ubuntu:22.10

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update -y --fix-missing && apt upgrade -y && apt install -y build-essential

RUN echo "dd0ddeaf2293dd418123b8fb03022337d7ac6ac3  /lib/x86_64-linux-gnu/libc.so.6" | sha1sum -c

ADD https://yx7.cc/code/ynetd/ynetd-0.1.2.tar.xz /ynetd-0.1.2.tar.xz

RUN tar -xf ynetd-0.1.2.tar.xz

RUN make -C /ynetd-0.1.2/

RUN useradd -m pwn

#note: you have a dummy file for this one
ADD get_flag /bin/get_flag
RUN chmod +x /bin/get_flag

ADD vuln /home/pwn/vuln

RUN chmod 0755 /home/pwn/vuln

EXPOSE 1337

CMD ["/ynetd-0.1.2/ynetd", "-p", "1337", "-u", "pwn", "-d", "/home/pwn", "-se", "y", "./vuln"]