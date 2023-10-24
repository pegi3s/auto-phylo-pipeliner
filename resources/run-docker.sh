#!/bin/bash

SCRIPT_PATH="$(dirname -- "${BASH_SOURCE[0]}")"
if [[ -f "$SCRIPT_PATH/../setup.cfg" ]]; then
  VERSION=$(cat "$SCRIPT_PATH/../setup.cfg" | grep version | cut -d'=' -f2 | sed -e 's/ //g')
else
  VERSION=latest
fi


FIFOPATH=$(mktemp -u)
mkfifo -m 600 "$FIFOPATH"

# Watches fifo file to open the URLs received through it
while read -r url < "$FIFOPATH"
do
  xdg-open "$url"
done &

xdg_open_id=$!

# Stops fifo watcher and deletes fifo file on script exit
function close_xdg {
  kill -SIGTERM "$xdg_open_id"
  rm "$FIFOPATH"
}
trap close_xdg EXIT


docker run --rm -ti --user $(id -u):$(id -g) \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $HOME/.Xauthority:/root/.Xauthority \
  -v "${FIFOPATH}":/fifo \
  -v "${PWD}":"${PWD}" \
  -v "$(which xdg-open)":/usr/bin/xdg-open \
  -e DOCKER_BROWSER_FIFO="/fifo" \
  -w "${PWD}" \
  pegi3s/auto-phylo-pipeliner:$VERSION
