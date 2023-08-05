# -*- coding: utf-8 -*-

"""Utilities."""

import contextlib
import gzip
import logging
import os
import shutil
import tarfile
import zipfile
from io import BytesIO, StringIO
from pathlib import Path, PurePosixPath
from subprocess import check_output  # noqa: S404
from typing import TYPE_CHECKING, Union
from urllib.parse import urlparse
from urllib.request import urlretrieve
from uuid import uuid4

import pandas as pd
import requests

if TYPE_CHECKING:
    import rdflib

logger = logging.getLogger(__name__)


def download(
    url: str,
    path: Union[str, Path],
    force: bool = True,
    clean_on_failure: bool = True,
    backend: str = 'urllib',
    **kwargs,
) -> None:
    """Download a file from a given URL.

    :param url: URL to download
    :param path: Path to download the file to
    :param force: If false and the file already exists, will not re-download.
    :param clean_on_failure: If true, will delete the file on any exception raised during download
    :param backend: The downloader to use. Choose 'urllib' or 'requests'
    :param kwargs: The keyword arguments to pass to :func:`urllib.request.urlretrieve` or to `requests.get`
        depending on the backend chosen. If using 'requests' backend, `stream` is set to True by default.

    :raises Exception: Thrown if an error besides a keyboard interrupt is thrown during download
    :raises KeyboardInterrupt: If a keyboard interrupt is thrown during download
    :raises ValueError: If an invalid backend is chosen
    """
    if os.path.exists(path) and not force:
        logger.debug('did not re-download %s from %s', path, url)
        return

    try:
        if backend == 'urllib':
            logger.info('downloading from %s to %s', url, path)
            urlretrieve(url, path, **kwargs)  # noqa:S310
        elif backend == 'requests':
            kwargs.setdefault('stream', True)
            # see https://requests.readthedocs.io/en/master/user/quickstart/#raw-response-content
            # pattern from https://stackoverflow.com/a/39217788/5775947
            with requests.get(url, **kwargs) as response, open(path, 'wb') as file:
                logger.info('downloading (stream=%s) from %s to %s', kwargs['stream'], url, path)
                shutil.copyfileobj(response.raw, file)
        else:
            raise ValueError(f'Invalid backend: {backend}. Use "requests" or "urllib".')
    except (Exception, KeyboardInterrupt):
        if clean_on_failure:
            try:
                os.remove(path)
            except FileExistsError:
                pass  # if the file can't be deleted then no problem
        raise


def name_from_url(url: str) -> str:
    """Get the filename from the end of the URL."""
    parse_result = urlparse(url)
    path = PurePosixPath(parse_result.path)
    name = path.name
    return name


def mkdir(path: Path, ensure_exists: bool = True, suffix_check: bool = True) -> None:
    """Make a directory (or parent directory if a file is given) if flagged with ``ensure_exists``."""
    if ensure_exists:
        if suffix_check and path.suffix:  # if it looks like a file path
            path.parent.mkdir(exist_ok=True, parents=True)
        else:
            path.mkdir(exist_ok=True, parents=True)


@contextlib.contextmanager
def mock_envvar(k: str, v: str):
    """Mock the environment variable then delete it after the test is over."""
    os.environ[k] = v
    yield
    del os.environ[k]


def getenv_path(envvar: str, default: Path, ensure_exists: bool = True) -> Path:
    """Get an environment variable representing a path, or use the default."""
    rv = Path(os.getenv(envvar, default=default))
    mkdir(rv, ensure_exists=ensure_exists)
    return rv


def n() -> str:
    """Get a random string for testing."""
    return str(uuid4())


def get_df_io(df: pd.DataFrame, sep: str = '\t', index: bool = False, **kwargs) -> BytesIO:
    """Get the dataframe as bytes."""
    sio = StringIO()
    df.to_csv(sio, sep=sep, index=index, **kwargs)
    sio.seek(0)
    bio = BytesIO(sio.read().encode('utf-8'))
    return bio


def write_zipfile_csv(
    df: pd.DataFrame,
    path: Union[str, Path],
    inner_path: str, sep='\t',
    index: bool = False,
    **kwargs,
) -> None:
    """Write a dataframe to an inner CSV file to a zip archive."""
    bytes_io = get_df_io(df, sep=sep, index=index, **kwargs)
    with zipfile.ZipFile(file=path, mode='w') as zip_file:
        with zip_file.open(inner_path, mode='w') as file:
            file.write(bytes_io.read())


def read_zipfile_csv(path: Union[str, Path], inner_path: str, sep='\t', **kwargs) -> pd.DataFrame:
    """Read an inner CSV file from a zip archive."""
    with zipfile.ZipFile(file=path) as zip_file:
        with zip_file.open(inner_path) as file:
            return pd.read_csv(file, sep=sep, **kwargs)


def write_tarfile_csv(
    df: pd.DataFrame,
    path: Union[str, Path],
    inner_path: str,
    sep='\t',
    index: bool = False,
    **kwargs,
) -> None:
    """Write a dataframe to an inner CSV file from a tar archive."""
    raise NotImplementedError
    # bytes_io = get_df_io(df, sep=sep, index=index, **kwargs)
    # with tarfile.open(path, mode='w') as tar_file:
    #    with tar_file.open(inner_path, mode='w') as file:  # type: ignore
    #        file.write(bytes_io.read())


def read_tarfile_csv(path: Union[str, Path], inner_path: str, sep='\t', **kwargs) -> pd.DataFrame:
    """Read an inner CSV file from a tar archive."""
    with tarfile.open(path) as tar_file:
        with tar_file.extractfile(inner_path) as file:  # type: ignore
            return pd.read_csv(file, sep=sep, **kwargs)


def read_rdf(path: Union[str, Path], **kwargs) -> 'rdflib.Graph':
    """Read an RDF file with :mod:`rdflib`."""
    import rdflib
    if isinstance(path, str):
        path = Path(path)
    graph = rdflib.Graph()
    with (
        gzip.open(path, 'rb')  # type: ignore
        if isinstance(path, Path) and path.suffix == '.gz' else
        open(path)
    ) as file:
        graph.parse(file, **kwargs)
    return graph


def get_commit(org: str, repo: str, provider: str = 'git') -> str:
    """Get last commit hash for the given repo."""
    if provider == 'git':
        output = check_output(['git', 'ls-remote', f'https://github.com/{org}/{repo}'])  # noqa
        lines = (line.strip().split('\t') for line in output.decode('utf8').splitlines())
        rv = next(line[0] for line in lines if line[1] == 'HEAD')
    elif provider == 'github':
        res = requests.get(f'https://api.github.com/repos/{org}/{repo}/branches/master')
        res_json = res.json()
        rv = res_json['commit']['sha']
    else:
        raise NotImplementedError(f'invalid implementation: {provider}')
    return rv
