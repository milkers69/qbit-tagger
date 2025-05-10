# https://qbittorrent-api.readthedocs.io/en/latest/apidoc/client.html#qbittorrentapi.client.Client
# https://qbittorrent-api.readthedocs.io/en/latest/apidoc/torrents.html#qbittorrentapi.torrents.TorrentDictionary
# https://qbittorrent-api.readthedocs.io/en/latest/apidoc/definitions.html#qbittorrentapi.definitions.TrackerStatus
import logging
import os

import qbittorrentapi

# create logger with default config
logger = logging.getLogger("qbit-tagger")
logging.basicConfig(level=logging.INFO)

# parse variables with reasonable default values
host = os.getenv("HOST", "127.0.0.1:8080")
tag = os.getenv("TAG", "Not Working")
username = os.getenv("USERNAME", "admin")
password = os.getenv("PASSWORD", "adminadmin")

# intialize client
qbt_client = qbittorrentapi.Client(
    host=host, username=username, password=password, FORCE_SCHEME_FROM_HOST=True
)

# try to login, throws qbittorrentapi.LoginFailed exception
qbt_client.auth_log_in()
logger.info("Logged into qbittorrent at %s", host)

# hashes to update tag on
torrents_to_add_tag = set()
torrents_to_remove_tag = set()

# load torrents
torrents = qbt_client.torrents_info(status_filter="seeding")
logger.info("Loaded %i torrents from qbittorrent", len(torrents))

# for all torrents
for torrent in torrents:
    # torrents that are tagged and working now
    if tag in torrent.tags and any(tracker.status == 2 for tracker in torrent.trackers):
        torrents_to_remove_tag.add(torrent.hash)
    # torrents that are not tagged and not working now
    elif tag not in torrent.tags and all(
        tracker.status in (0, 1, 4) for tracker in torrent.trackers
    ):
        torrents_to_add_tag.add(torrent.hash)

# cleanup tagged torrents that are working now
if torrents_to_remove:
    logger.info("Removing tag '%s' from %i torrents", tag, len(torrents_to_remove_tag))
    qbt_client.torrent_tags.remove_tags(
        tags=tag,
        torrent_hashes=torrents_to_remove_tag,
    )

# tag torrents that are not working now
if torrents_to_add:
    logger.info("Adding tag '%s' to %i torrents", tag, len(torrents_to_add_tag))
    qbt_client.torrent_tags.add_tags(
        tags=tag,
        torrent_hashes=torrents_to_add_tag,
    )
