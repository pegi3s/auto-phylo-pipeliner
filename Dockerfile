FROM python:3.8-alpine

VOLUME /data

RUN apk update && apk add gcc musl-dev libffi-dev tk fontconfig ttf-dejavu

# Builds and installs the project
COPY . /auto-phylo-pipeliner
RUN cd /auto-phylo-pipeliner && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install -e .[dev] && \
    python3 -m build && \
    name=$(ls dist/auto_phylo_pipeliner*.whl) && pip install $name && \
    cd / && rm -rf /auto-phylo-pipeliner

WORKDIR /data

CMD auto-phylo-pipeliner
