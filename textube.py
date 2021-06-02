#!/usr/bin/env python3.9

import argparse
import concurrent.futures as cofu
import logging
import pathlib
import sys

import ytapi

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Download subtitles for a youtube channel/playlist')

    parser.add_argument('-v', '--verbose', action='store_true')

    parser.add_argument('-q', '--quiet', action='store_true')

    parser.add_argument('-l', '--list', action='store_true',
        help='only list target IDs')

    parser.add_argument('-o', '--output-dir', type=pathlib.Path, default='.', metavar='path',
        help='output destination, otherwise current directory')

    parser.add_argument('-c', '--connections', type=int, default=10, metavar='count',
        help='number of parallel connections to use')

    parser.add_argument('ids', nargs='+', metavar='ID',
        help='channel or playlist id')

    args = parser.parse_args()

    logger = logging.getLogger('root')
    logger.setLevel(logging.DEBUG if args.verbose else logging.ERROR if args.quiet else logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    logger.debug(f'saving subtitles in: {args.output_dir.resolve()}')
    logger.debug(f'using {args.connections} connections')
    logger.debug(f'getting videos from: {" ".join(args.ids)}')

    ids = (e for plId in args.ids for e in ytapi.fetch_items(plId, selector=lambda e: e['videoId']))
    with cofu.ThreadPoolExecutor(args.connections, initializer=ytapi.ConnectionManager.threadInit) as executor:
        future_id = {executor.submit(ytapi.get_captions_from_config, vid) : vid for vid in ids}
        for future in cofu.as_completed(future_id):
            videoId = future_id[future]
            text = future.result()
            if text is not None:
                logger.debug(f'saving subtitles for {videoId}')
                with open(args.output_dir / videoId, 'w') as f:
                    f.write(text)
            else:
                logger.warning(f'no subs for {videoId}')
