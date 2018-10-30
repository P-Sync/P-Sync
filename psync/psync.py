#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, hashlib, zlib, collections, struct, operator


StagingEntry = collections.namedtuple('StagingEntry', [
    'ctime_s', 'ctime_n', 'mtime_s', 'mtime_n', 'dev', 'ino', 'mode',
    'uid', 'gid', 'size', 'sha1', 'flags', 'path',
])


def write_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)


def read_file(path):
    with open(path, 'rb') as f:
        return f.read()


def init(repo):
    os.mkdir(repo)
    os.mkdir(os.path.join(repo, '.psync'))
    for name in ['objects', 'refs', 'refs/heads']:
        os.mkdir(os.path.join(repo, '.psync', name))
    write_file(os.path.join(repo, '.psync', 'HEAD'),
               b'ref: refs/heads/master')
    print('initialized empty psync repository: {}'.format(repo))


def hash_object(data, obj_type, write=True):
    header = '{} {}'.format(obj_type, len(data)).encode()
    full_data = header + b'\x00' + data
    sha1 = hashlib.sha1(full_data).hexdigest()
    if write:
        path = os.path.join('.psync', 'objects', sha1[:2], sha1[2:])
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            write_file(path, zlib.compress(full_data))
    return sha1


def read_index():
    try:
        data = read_file(os.path.join('.psync', 'index'))
    except FileNotFoundError:
        return []
    digest = hashlib.sha1(data[:-20]).digest()
    assert digest == data[-20:], 'invalid index checksum'
    signature, version, num_entries = struct.unpack('!4sLL', data[:12])
    assert signature == b'DIRC', \
            'invalid index signature {}'.format(signature)
    assert version == 2, 'unknown index version {}'.format(version)
    entry_data = data[12:-20]
    entries = []
    i = 0
    while i + 62 < len(entry_data):
        fields_end = i + 62
        fields = struct.unpack('!LLLLLLLLLL20sH',
                               entry_data[i:fields_end])
        path_end = entry_data.index(b'\x00', fields_end)
        path = entry_data[fields_end:path_end]
        entry = StagingEntry(*(fields + (path.decode(),)))
        entries.append(entry)
        entry_len = ((62 + len(path) + 8) // 8) * 8
        i += entry_len
    assert len(entries) == num_entries
    return entries


def list_files(details=False):
    for entry in read_index():
        if details:
            stage = (entry.flags >> 12) & 3
            print('{:6o} {} {:}\t{}'.format(
                    entry.mode, entry.sha1.hex(), stage, entry.path))
        else:
            print(entry.path)


def get_status():
    paths = set()
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d != '.psync']
        for file in files:
            path = os.path.join(root, file)
            path = path.replace('\\', '/')
            if path.startswith('./'):
                path = path[2:]
            paths.add(path)
    entries_by_path = {e.path: e for e in read_index()}
    entry_paths = set(entries_by_path)
    changed = {p for p in (paths & entry_paths)
               if hash_object(read_file(p), 'blob', write=False) !=
                  entries_by_path[p].sha1.hex()}
    new = paths - entry_paths
    deleted = entry_paths - paths
    return (sorted(changed), sorted(new), sorted(deleted))


def status():
    changed, new, deleted = get_status()
    if changed:
        print('changed files:')
        for path in changed:
            print('   ', path)
    if new:
        print('new files:')
        for path in new:
            print('   ', path)
    if deleted:
        print('deleted files:')
        for path in deleted:
            print('   ', path)


def write_index(entries):
    packed_entries = []
    for entry in entries:
        entry_head = struct.pack('!LLLLLLLLLL20sH',
                entry.ctime_s, entry.ctime_n, entry.mtime_s, entry.mtime_n,
                entry.dev, entry.ino, entry.mode, entry.uid, entry.gid,
                entry.size, entry.sha1, entry.flags)
        path = entry.path.encode()
        length = ((62 + len(path) + 8) // 8) * 8
        packed_entry = entry_head + path + b'\x00' * (length - 62 - len(path))
        packed_entries.append(packed_entry)
    header = struct.pack('!4sLL', b'DIRC', 2, len(entries))
    all_data = header + b''.join(packed_entries)
    digest = hashlib.sha1(all_data).digest()
    write_file(os.path.join('.psync', 'index'), all_data + digest)


def add(paths):
    paths = [p.replace('\\', '/') for p in paths]
    all_entries = read_index()
    entries = [e for e in all_entries if e.path not in paths]
    for path in paths:
        sha1 = hash_object(read_file(path), 'blob')
        st = os.stat(path)
        flags = len(path.encode())
        assert flags < (1 << 12)
        entry = StagingEntry(
                int(st.st_ctime), 0, int(st.st_mtime), 0, st.st_dev,
                st.st_ino, st.st_mode, st.st_uid, st.st_gid, st.st_size,
                bytes.fromhex(sha1), flags, path)
        entries.append(entry)
    entries.sort(key=operator.attrgetter('path'))
    write_index(entries)