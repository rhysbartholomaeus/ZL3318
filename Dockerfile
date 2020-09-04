FROM centos:8

#RUN yum -y groupinstall "Development Tools"
RUN yum install -y  gcc gcc-c++ make git patch openssl-devel zlib-devel readline-devel \
sqlite-devel bzip2-devel curl git wget swig \
python3 python3-pip python3-devel

RUN python3 -m venv /app/.venv && \
    /app/.venv/bin/pip3 install --upgrade pip && \
    /app/.venv/bin/pip3 install --upgrade wheel && \
    /app/.venv/bin/pip3 install --upgrade setuptools

COPY . /app

RUN /app/.venv/bin/pip3 install -f /download -r /app/requirements.txt

RUN git clone https://github.com/happyalu/pyflite.git && \
cd pyflite && \
git clone https://github.com/festvox/flite && \
cd flite && \
./configure --enable-shared && \
make && \
make get_voices && \
cd .. && \
/app/.venv/bin/python setup.py build && \
/app/.venv/bin/python setup.py install

RUN mkdir -p /app/voices && cp /pyflite/flite/voices/* /app/voices/

EXPOSE 5645

WORKDIR /app

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV LD_LIBRARY_PATH="/pyflite/flite/build/x86_64-linux-gnu/lib/:${LD_LIBRARY_PATH}"

CMD ["sh", "-c", "/app/.venv/bin/flask run --host 0.0.0.0 --port 5645"]