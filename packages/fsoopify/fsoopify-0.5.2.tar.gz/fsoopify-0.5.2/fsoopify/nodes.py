#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
import os
from typing import Iterable, List, Any, Union
from abc import abstractmethod, ABC
from enum import Enum
import io
import shutil

import portalocker

from .paths import Path
from .size import Size
from .serialize import load, dump
from .serialize_ctx import load_context, Context
from .tree import ContentTree
from .atomic import open_atomic
from .utils import copyfileobj
from .openers import FileOpener, FileOpenerBase


class NodeType(Enum):
    file = 1
    dir = 2


class NodeInfo(ABC):
    ''' the abstract base class for file system node. '''

    def __init__(self, path):
        # path alwasys be abs
        self._path: Path = Path(path).get_abspath()

    def __str__(self):
        return str(self._path)

    def __repr__(self):
        return '{}(\'{}\')'.format(type(self).__name__, self._path)

    def __fspath__(self):
        return str(self._path)

    @property
    def path(self) -> Path:
        '''
        return a Path object.
        '''
        return self._path

    def rename(self, dest_path: str):
        '''
        use `os.rename()` to move the node.
        '''
        if not isinstance(dest_path, str):
            raise TypeError
        os.rename(self._path, dest_path)
        self._path = Path(dest_path).get_abspath()

    def get_parent(self, level=1):
        '''
        get parent dir as a `DirectoryInfo`.

        return `None` if self is top.
        '''
        parent_path = self.path.get_parent(level)
        if parent_path:
            return DirectoryInfo(parent_path)

    @staticmethod
    def from_path(path):
        '''
        create from path.

        return `None` if path is not exists.
        '''
        if os.path.isdir(path):
            return DirectoryInfo(path)

        if os.path.isfile(path):
            return FileInfo(path)

        return None

    @staticmethod
    def from_cwd():
        '''
        get a `DirectoryInfo` by `os.getcwd()`
        '''
        return DirectoryInfo(os.getcwd())

    @staticmethod
    def from_argv0():
        '''
        get a `FileInfo` by `sys.argv[0]`
        '''
        return FileInfo(sys.argv[0])

    # common methods

    @property
    @abstractmethod
    def node_type(self):
        raise NotImplementedError

    def is_exists(self):
        '''
        get whether the node is exists on disk.
        '''
        return os.path.exists(self._path)

    def is_directory(self):
        '''
        get whether the node is a exists directory.
        '''
        return False

    def is_file(self):
        '''
        get whether the node is a exists file.
        '''
        return False

    def is_symlink(self):
        ''' get whether the node is a symbolic link node. '''
        return os.path.islink(self._path)

    # abstract methods

    @abstractmethod
    def delete(self):
        ''' remove the node from disk. '''
        raise NotImplementedError

    @abstractmethod
    def create_hardlink(self, dest_path: str):
        ''' create hardlink for the node. '''
        raise NotImplementedError

    @abstractmethod
    def create_symlink(self, dest_path: str):
        ''' create symbolic link for the node. '''
        raise NotImplementedError


class FileInfo(NodeInfo):

    def open(self, mode='r', *,
             buffering=-1, encoding=None, newline=None, closefd=True,
             lock=False, atomic=False, or_create=False) -> FileOpenerBase:
        '''
        open the file,
        return a `FileOpener` as context manager.

        - when `lock` set `True`, use `portalocker.lock(LOCK_EX)` to lock the file after it opened.
        - when `atomic` set `True`, read or write as atomic operations.
        - when `or_create` set `True`, create file if it does not exists,
          to prevent raises `FileNotFoundError` with `r+` mode.
        '''
        opener=None

        def kwargs():
            # mode may update so we use kwargs as function.
            return dict(
                mode=mode,
                buffering=buffering,
                encoding=encoding,
                newline=newline,
                closefd=closefd,
                lock=lock,
                opener=opener
            )

        if or_create and 'r' in mode:
            def opener(path, flags):
                return os.open(path, flags | os.O_CREAT)

        if atomic:
            if 'r' in mode and '+' not in mode:
                # readonly mode, ignore atomic flag and open direct.
                pass
            else:
                return open_atomic(self._path, **kwargs())

        return FileOpener(self._path, **kwargs())

    def open_for_read_bytes(self, *, buffering=-1):
        ''' open the file with read bytes mode. '''
        return self.open('rb', buffering=buffering)

    def open_for_read_text(self, *, encoding='utf-8'):
        ''' open the file with read text mode. '''
        return self.open('r', encoding=encoding)

    @property
    def size(self):
        ''' get file size. '''
        return Size(os.path.getsize(self.path))

    def write(self, data, *, mode=None, buffering=-1, encoding=None, newline=None, atomic=False):
        ''' write data into the file. '''
        if mode is None:
            if isinstance(data, (str, io.TextIOBase)):
                mode = 'w'
            elif isinstance(data, (bytes, bytearray, io.BufferedIOBase)):
                mode = 'wb'
            else:
                raise TypeError(type(data))

        with self.open(mode=mode, buffering=buffering, encoding=encoding, newline=newline, atomic=atomic) as fp:
            if isinstance(data, (str, bytes, bytearray)):
                return fp.write(data)
            else:
                read_buffering = buffering
                if read_buffering < 2:
                    read_buffering = io.DEFAULT_BUFFER_SIZE
                return copyfileobj(data, fp)

    def read(self, mode='r', *, buffering=-1, encoding=None, newline=None):
        ''' read all content from the file. '''
        with self.open(mode=mode, buffering=buffering, encoding=encoding, newline=newline) as fp:
            return fp.read()

    def write_text(self, text: str, *, encoding='utf-8', append=True, atomic=False):
        ''' write text into the file. '''
        mode = 'a' if append else 'w'
        return self.write(text, mode=mode, encoding=encoding, atomic=atomic)

    def write_bytes(self, data: Union[bytes, bytearray], *, append=True, atomic=False):
        ''' write bytes into the file. '''
        mode = 'ab' if append else 'wb'
        return self.write(data, mode=mode, atomic=atomic)

    def write_from_stream(self, stream: io.IOBase, *, append=True, atomic=False):
        if not isinstance(stream, io.IOBase):
            raise TypeError(type(stream))
        if not stream.readable():
            raise ValueError('stream is unable to read.')
        mode = 'a' if append else 'w'
        if not isinstance(stream, io.TextIOBase):
            mode += 'b'
        return self.write(stream, mode=mode, atomic=atomic)

    def read_text(self, encoding='utf-8') -> str:
        ''' read all text into memory. '''
        with self.open_for_read_text(encoding=encoding) as fp:
            return fp.read()

    def read_bytes(self) -> bytes:
        ''' read all bytes into memory. '''
        with self.open_for_read_bytes() as fp:
            return fp.read()

    def read_into_stream(self, stream: io.IOBase, *,
                         encoding=None, buffering: int = -1):
        ''' read all content into stream. '''
        if not isinstance(stream, io.IOBase):
            raise TypeError(type(stream))
        if not stream.writable():
            raise ValueError('stream is unable to write.')

        if isinstance(stream, io.TextIOBase):
            fp = self.open_for_read_text(encoding=encoding or 'utf-8')
        else:
            fp = self.open_for_read_bytes(buffering=buffering)

        with fp as fsrc:
            shutil.copyfileobj(fsrc, stream)

    def copy_to(self, dest: Union[str, 'FileInfo', 'DirectoryInfo'], *,
                buffering: int = -1, overwrite=False):
        '''
        copy the file to dest location.

        if `dest` is `DirectoryInfo`, that mean copy into the dir with same name.
        '''
        if isinstance(dest, str):
            dest_path = dest
        elif isinstance(dest, FileInfo):
            dest_path = dest.path
        elif isinstance(dest, DirectoryInfo):
            dest_path = dest.path / self.path.name
        else:
            raise TypeError('dest is not one of `str`, `FileInfo`, `DirectoryInfo`')

        with self.open_for_read_bytes(buffering=buffering) as source:
            # use x mode to ensure dest does not exists.
            mode = 'wb' if overwrite else 'xb'
            with open(dest_path, mode) as dest_file:
                shutil.copyfileobj(source, dest_file)

    def copy_from(self, src: Union[str, 'FileInfo'], *,
                  buffering: int = -1, overwrite=False,
                  lock=False, atomic=False):
        '''
        copy content from src.
        '''

        if isinstance(src, str):
            src = FileInfo(src)
        elif isinstance(src, FileInfo):
            pass
        else:
            raise TypeError('src is not one of `str`, `FileInfo`')

        mode = 'wb' if overwrite else 'xb'
        with self.open(mode, buffering=buffering, lock=lock, atomic=atomic) as dst_fp:
            with src.open_for_read_bytes(buffering=buffering) as src_fp:
                shutil.copyfileobj(src_fp, dst_fp)

    def __iadd__(self, other: Union[str, bytes, bytearray, io.IOBase, 'FileInfo']):
        if isinstance(other, str):
            self.write_text(other)
        elif isinstance(other, (bytes, bytearray)):
            self.write_bytes(other)
        elif isinstance(other, io.IOBase):
            self.write_from_stream(other)
        elif isinstance(other, FileInfo):
            with other.open_for_read_bytes() as fp:
                self.write_from_stream(fp)
        else:
            raise TypeError(type(other))
        return self

    # override common methods

    @property
    def node_type(self):
        return NodeType.file

    def is_exists(self) -> bool:
        return self.is_file()

    def is_file(self) -> bool:
        ''' check if this is a exists file. '''
        return os.path.isfile(self._path)

    # override @abstractmethod

    def delete(self):
        ''' remove the file from disk. '''
        os.remove(self._path)

    def create_hardlink(self, dest_path: str):
        ''' create hardlink for the file. '''
        os.link(self._path, dest_path)

    def create_symlink(self, dest_path: str):
        ''' create symbolic link for the file. '''
        os.symlink(self._path, dest_path, target_is_directory=False)

    # load/dump system.

    def load(self, format=None, *, kwargs={}):
        '''
        deserialize object from the file.

        auto detect format by file extension name if `format` is None.
        for example, `.json` will detect as `json`.

        * raise `FormatNotFoundError` on unknown format.
        * raise `SerializeError` on any serialize exceptions.
        '''
        return load(self, format=format, kwargs=kwargs)

    def dump(self, obj, format=None, *, kwargs={}, atomic=True):
        '''
        serialize the `obj` into file.

        * raise `FormatNotFoundError` on unknown format.
        * raise `SerializeError` on any serialize exceptions.
        '''
        return dump(self, obj, format=format, kwargs=kwargs)

    def load_context(self, format=None, *, load_kwargs={}, dump_kwargs={}, lock=False, atomic=True) -> Context:
        '''
        load the file in a context, auto dump `context.data` into file when context exit.

        - if the file does not exists, `context.data` will be `None`.
        - set `context.data` to `None` will remove the file from disk.
        - by default, `context.save_on_exit` is `True`.
        - if `lock` is `True`, lock the file until the context exit.

        usage:

        ``` py
        with file.load_context() as context:
            # read or edit context.data
            ...
        ```
        '''
        return load_context(self, format, load_kwargs=load_kwargs, dump_kwargs=dump_kwargs, lock=lock, atomic=atomic)

    # hash system

    def get_file_hash(self, *algorithms: str):
        '''
        get lower case hash of file.

        return value is a tuple, you may need to unpack it.

        for example: `get_file_hash('md5', 'sha1')` return `('XXXX1', 'XXXX2')`
        '''
        with self.get_hasher(*algorithms) as hasher:
            read_block = hasher.read_block
            while read_block():
                pass
            return hasher.result

    def get_hasher(self, *algorithms: str):
        '''
        get the hasher to hash the file.
        this is helpful if you are writing with progress bar, etc.

        to use this, read the source from `get_file_hash` method:

        ``` py
        def get_file_hash(self, *algorithms: str):
            with self.get_hasher(*algorithms) as hasher:
                while hasher.read_block():
                    pass
                return hasher.result
        ```
        '''

        from .hashs import Hasher
        return Hasher(self._path, algorithms)


class DirectoryInfo(NodeInfo):

    def create(self):
        ''' create directory. '''
        os.mkdir(self.path)

    def ensure_created(self):
        ''' ensure the directory was created. '''
        if not self.is_directory():
            os.makedirs(self.path)

    def iter_items(self, depth: int = 1) -> Iterable[NodeInfo]:
        '''
        get items from directory.
        '''
        if depth is not None and not isinstance(depth, int):
            raise TypeError
        def itor(root, d):
            if d is not None:
                d -= 1
                if d < 0:
                    return
            for name in os.listdir(root):
                path = os.path.join(root, name)
                node = NodeInfo.from_path(path)
                yield node
                if isinstance(node, DirectoryInfo):
                    yield from itor(path, d)
        yield from itor(self._path, depth)

    def list_items(self, depth: int = 1) -> List[NodeInfo]:
        '''
        get items from directory.
        '''
        return list(self.iter_items(depth))

    def has_file(self, name: str):
        '''
        check whether this directory contains the file.
        '''
        return os.path.isfile(self._path / name)

    def has_directory(self, name: str):
        '''
        check whether this directory contains the directory.
        '''
        return os.path.isdir(self._path / name)

    def get_fileinfo(self, name: str):
        '''
        get a `FileInfo` for a file (without create actual file).
        '''
        return FileInfo(os.path.join(self._path, name))

    def get_dirinfo(self, name: str):
        '''
        get a `DirectoryInfo` for a directory (without create actual directory).
        '''
        return DirectoryInfo(os.path.join(self._path, name))

    def get_unique_name(self, name: str, ext: str=''):
        '''
        generate a unique name for new item from the directory.
        '''
        def iter_name():
            yield f'{name}{ext}'
            index = 0
            while True:
                index += 1
                yield f'{name} ({index}){ext}'

        for unique_name in iter_name():
            if not os.path.exists(self._path / unique_name):
                return unique_name

    # tree api

    def get_tree(self, *, as_stream=False) -> ContentTree:
        '''
        Get structure tree from current directory.

        if `as_stream` is `True`,
        collect all files as `file-object` instead of read entire file into memory,
        you need to call `__exit__` after you used it.
        '''
        tree = ContentTree()
        for item in self.list_items():
            name = str(item.path.name)
            if item.node_type == NodeType.file:
                if as_stream:
                    tree.set_context(name, item.open_for_read_bytes())
                else:
                    tree[name] = item.read(mode='rb')
            else:
                tree[name] = item.get_tree()
        return tree

    def make_tree(self, tree: dict, mode: int=0):
        '''
        make directory structure with tree.

        for each items in `tree`,

        - if value is `str` or `bytes`, use the key as filename to create a file, write the value as content;
        - if value is a `dict`, use the key as dirname to create a dir, then use the value to make sub tree.

        `mode` is a const `int` value:

        - `0` mean ignore all `FileExistsError`;
        - `1` mean raise `FileExistsError` when any file exists;
        - `2` mean overwrite all exists files;
        '''
        if mode not in (0, 1, 2):
            raise ValueError(mode)

        for key, value in tree.items():
            if not isinstance(key, str):
                raise TypeError(key)

            if isinstance(value, (str, bytes, bytearray, io.IOBase)):
                subfile = self.get_fileinfo(key)
                if subfile.is_file():
                    if mode == 0:
                        continue
                    elif mode == 1:
                        raise FileExistsError(subfile.path)
                    elif mode == 2:
                        subfile.delete()

                if isinstance(value, str):
                    subfile.write_text(value, append=False)

                elif isinstance(value, (bytes, bytearray)):
                    subfile.write_bytes(value, append=False)

                else:
                    subfile.write_from_stream(value, append=False)

            elif isinstance(value, dict):
                subdir = self.get_dirinfo(key)
                subdir.ensure_created()
                subdir.make_tree(value, mode=mode)

            else:
                raise TypeError((key, value))

    # override common methods

    @property
    def node_type(self):
        return NodeType.dir

    def is_exists(self) -> bool:
        return self.is_directory()

    def is_directory(self) -> bool:
        ''' check if this is a exists directory. '''
        return os.path.isdir(self._path)

    # override @abstractmethod

    def delete(self):
        ''' remove the directory from disk. '''
        os.rmdir(self._path)

    def create_hardlink(self, dest_path: str):
        ''' create hardlink for the directory (includes childs). '''

        # self
        dirinfo = DirectoryInfo(dest_path)
        dirinfo.ensure_created()

        # child
        for item in self.list_items():
            item.create_hardlink(os.path.join(dest_path, item.path.name))

    def create_symlink(self, dest_path: str):
        ''' create symbolic link for the directory. '''
        os.symlink(self._path, dest_path, target_is_directory=True)
