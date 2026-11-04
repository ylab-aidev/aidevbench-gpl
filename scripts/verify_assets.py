#!/usr/bin/env python3
"""Verify downloaded release assets of aidevbench-gpl and rejoin split archives.

usage: python3 verify_assets.py DOWNLOAD_DIR [--join] [--members]
  DOWNLOAD_DIR  folder that holds the release assets (and nothing needs to be renamed)
  --join        write each split asset back into one file (NAME without the .NN suffix)
  --members     also check the SHA-256 of every member inside the tar assets
Uses manifest/release-assets.json next to this script's parent folder. Only the Python
standard library is needed."""
import hashlib
import json
import os
import sys
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, '..', 'manifest', 'release-assets.json')


def sha256_files(paths):
    digest = hashlib.sha256()
    for path in paths:
        with open(path, 'rb') as stream:
            for block in iter(lambda: stream.read(1 << 20), b''):
                digest.update(block)
    return digest.hexdigest()


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__)
        return 2
    folder, join, check_members = argv[0], '--join' in argv, '--members' in argv
    manifest = json.load(open(MANIFEST, encoding='utf-8'))
    failures = 0
    for asset in manifest['assets']:
        paths = [os.path.join(folder, item['name']) for item in asset['files']]
        missing = [p for p in paths if not os.path.exists(p)]
        if missing:
            print('MISSING', asset['asset'], ', '.join(os.path.basename(p) for p in missing))
            failures += 1
            continue
        for item, path in zip(asset['files'], paths):
            if sha256_files([path]) != item['sha256']:
                print('BAD', item['name'])
                failures += 1
        if sha256_files(paths) != asset['whole']['sha256']:
            print('BAD (joined)', asset['asset'])
            failures += 1
            continue
        print('OK', asset['asset'])
        whole = paths[0]
        if len(paths) > 1 and join:
            whole = os.path.join(folder, asset['asset'])
            with open(whole, 'wb') as out:
                for path in paths:
                    with open(path, 'rb') as stream:
                        for block in iter(lambda: stream.read(1 << 20), b''):
                            out.write(block)
            print('   joined ->', os.path.basename(whole))
        if check_members and asset['asset'].endswith('.tar') and os.path.exists(whole) and (len(paths) == 1 or join):
            expected = {m['member']: m['sha256'] for m in asset['members'] if 'sha256' in m}
            with tarfile.open(whole) as tar:
                for info in tar:
                    if info.isfile() and info.name in expected:
                        digest = hashlib.sha256(tar.extractfile(info).read()).hexdigest()
                        if digest != expected.pop(info.name):
                            print('   BAD member', info.name)
                            failures += 1
            for name in expected:
                print('   MISSING member', name)
                failures += 1
    print('FAILED' if failures else 'ALL OK', failures)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
