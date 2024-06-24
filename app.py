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

# https://qbittorrent-api.readthedocs.io/en/latest/apidoc/definitions.html#qbittorrentapi.definitions.TrackerStatus
torrents_to_remove = set()
torrents_to_add = set()
# for all torrents
for torrent in qbt_client.torrents_info():
    # torrents that are tagged and working now
    if tag in torrent.tags and any(tracker.status == 2 for tracker in torrent.trackers):
        torrents_to_remove.add(torrent.hash)
    # torrents that are not tagged and not working now
    elif tag not in torrent.tags and all(tracker.status in (0, 1, 4) for tracker in torrent.trackers):
        torrents_to_add.add(torrent.hash)
    
# cleanup tagged torrents that are working now
qbt_client.torrent_tags.remove_tags(
    tags=tag,
    torrent_hashes=torrents_to_remove,
)

# tag torrents that are not working now
qbt_client.torrent_tags.add_tags(
    tags=tag,
    torrent_hashes=torrents_to_add,
)
