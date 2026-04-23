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
        'retries': opts.retries,
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
        'writepages': opts.writepages,
        'youtube_include_dash_manifest': opts.youtube_include_dash_manifest,
        'encoding': opts.encoding,
        'extract_flat': opts.extract_flat,
        'mark_watched': opts.mark_watched,
        'merge_output_format': opts.merge_output_format,
        'postprocessors': [],
        'fixup': opts.fixup,
        'source_address': opts.source_address,
        'call_home': opts.call_home,
        'sleep_interval': opts.sleep_interval,
        'max_sleep_interval': opts.max_sleep_interval,
        'sleep_interval_subtitles': opts.sleep_interval_subtitles,
        'external_downloader': opts.external_downloader,
        'list_thumbnails': opts.list_thumbnails,
        'match_filter': None,
        'no_color': opts.no_color,
        'ffmpeg_location': opts.ffmpeg_location,
        'hls_prefer_native': opts.hls_prefer_native,
        'hls_use_mpegts': opts.hls_use_mpegts,
        'hls_split_discontinuity': opts.hls_split_discontinuity,
        'concurrent_fragment_downloads': opts.concurrent_fragment_downloads,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            retcode = ydl.download(args)
    except DownloadError:
        sys.exit(1)
    except SameFileError as e:
        sys.exit(f'ERROR: {e}')
    except KeyboardInterrupt:
        write_string('\nERROR: Interrupted by user\n', out=sys.stderr)
        sys.exit(1)
    except MaxDownloadsReached:
        ydl.to_screen('[info] Maximum number of downloads reached')
        sys.exit(0)
    except ExistingVideoReached:
        ydl.to_screen('[info] Encountered a video that is already in the archive, stopping due to --break-on-existing')
        sys.exit(0)

    sys.exit(retcode)


if __name__ == '__main__':
    main()
