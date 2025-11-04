FROM python:3.11-slim

ARG USER=devagent
ARG UID=1000
RUN groupadd -g ${UID} ${USER} || true \
 && useradd -m -u ${UID} -g ${UID} ${USER} || true

WORKDIR /workspace

RUN apt-get update \
 && apt-get install -y --no-install-recommends git build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY sandbox/requirements-tests.txt /tmp/requirements-tests.txt
RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir -r /tmp/requirements-tests.txt

USER ${USER}
CMD ["/bin/bash"]
