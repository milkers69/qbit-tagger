import os

import qbittorrentapi

host = os.getenv("HOST")
tag = os.getenv("TAG")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# https://qbittorrent-api.readthedocs.io/en/latest/apidoc/client.html#qbittorrentapi.client.Client
qbt_client = qbittorrentapi.Client(host=host, username=username, password=password)

# try to login, throws qbittorrentapi.LoginFailed exception
qbt_client.auth_log_in()

# get torrents
torrents = qbt_client.torrents_info()

# https://qbittorrent-api.readthedocs.io/en/latest/apidoc/definitions.html#qbittorrentapi.definitions.TrackerStatus
# cleanup tagged torrents that are working now
qbt_client.torrent_tags.remove_tags(
    tags=[tag],
    torrent_hashes=[
        torrent.hash
        for torrent in torrents
        if tag in torrent.tags
        and any(tracker.status == 2 for tracker in torrent.trackers)
    ],
)

# tag torrents that are not working now
qbt_client.torrent_tags.add_tags(
    tags=[tag],
    torrent_hashes=[
        torrent.hash
        for torrent in torrents
        if all(tracker.status in (0, 1, 4) for tracker in torrent.trackers)
    ],
)
