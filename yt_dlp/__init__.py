#!/usr/bin/env python3
# coding: utf-8

"""
yt-dlp - A feature-rich command-line audio/video downloader

Fork of yt-dlp with additional features and fixes.
"""

__license__ = 'Unlicense'
__version__ = '2024.01.01'

from .YoutubeDL import YoutubeDL
from .extractor import gen_extractors, list_extractors


def main(argv=None):
    """Main entry point for the yt-dlp command-line interface."""
    from .options import parseOpts
    from .utils import (
        DownloadError,
        ExistingVideoReached,
        MaxDownloadsReached,
        SameFileError,
        decodeOption,
        preferredencoding,
        render_table,
        write_string,
    )
    import sys
    import traceback

    setproctitle = None
    try:
        from setproctitle import setproctitle
    except ImportError:
        pass

    if setproctitle:
        setproctitle('yt-dlp')

    parser, opts, args = parseOpts(argv)

    # Ensure compatibility with older Python versions
    if sys.version_info < (3, 7):
        sys.exit('ERROR: Python 3.7 or higher is required for yt-dlp.')

    # Set up the downloader with parsed options
    ydl_opts = {
        'verbose': opts.verbose,
        'quiet': opts.quiet,
        'no_warnings': opts.no_warnings,
        'format': opts.format,
        'outtmpl': opts.outtmpl,
        'restrictfilenames': opts.restrictfilenames,
        'nooverwrites': opts.nooverwrites,
        'continuedl': opts.continue_dl,
        'noprogress': opts.noprogress,
        'playliststart': opts.playliststart,
        'playlistend': opts.playlistend,
        'playlistreverse': opts.playlist_reverse,
        'playlistrandom': opts.playlist_random,
        'noplaylist': opts.noplaylist,
        'logtostderr': opts.logtostderr,
        'consoletitle': opts.consoletitle,
        'prefer_free_formats': opts.prefer_free_formats,
        'geo_bypass': opts.geo_bypass,
        'geo_bypass_country': opts.geo_bypass_country,
        'geo_bypass_ip_block': opts.geo_bypass_ip_block,
        'socket_timeout': opts.socket_timeout,
        'proxy': opts.proxy,
        # Increased default retries from 10 to 15 for more reliable downloads on flaky connections
        'retries': opts.retries if opts.retries is not None else 15,
        'fragment_retries': opts.fragment_retries,
        'skip_unavailable_fragments': opts.skip_unavailable_fragments,
        'keepvideo': opts.keepvideo,
        'merge_output_format': opts.merge_output_format,
        'subtitleslangs': opts.subtitleslangs,
        'writesubtitles': opts.writesubtitles,
        'writeautomaticsub': opts.writeautomaticsub,
        'allsubtitles': opts.allsubtitles,
        'listsubtitles': opts.listsubtitles,
        'subtitlesformat': opts.subtitlesformat,
        'embedsubtitles': opts.embedsubtitles,
        'embedthumbnail': opts.embedthumbnail,
        'addmetadata': opts.addmetadata,
        'writethumbnail': opts.writethumbnail,
        'write_all_thumbnails': opts.write_all_thumbnails,
        'writedescription': opts.writedescription,
        'writeinfojson': opts.writeinfojson,
        'writeannotations': opts.writeannotations,
        'writep