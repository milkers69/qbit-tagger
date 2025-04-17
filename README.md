# qbit-tagger

examples

`docker run --rm --network host --pull=always -e HOST="192.168.69.69:8080" -e TAG="Not Working" ghcr.io/milkers69/qbit-tagger:main`

`docker run --rm --network host --pull=always -e HOST="192.168.69.69:8080" -e TAG="Not Working" -e USERNAME="admin" -e PASSWORD="adminadmin" ghcr.io/milkers69/qbit-tagger:main`

```
networks:
  internal:
    internal: true
  external:

services:
  qbittorrent:
    ...
    networks:
      - internal
      - external
    ...
  qbit-tagger:
    image: ghcr.io/milkers69/qbit-tagger:main
    environment:
      - HOST=http://qbittorrent:8080
      - TAG=Not Working
      - USERNAME=admin
      - PASSWORD=adminadmin
    # run every 15mins instead of just once
    entrypoint: sh -c "sleep 30; while true; do python3 /app/app.py; sleep $((60*15)); done"
    networks:
      - internal
    depends_on:
      - qbittorrent
    restart: unless-stopped
```
