"""Move S3 objects."""
from concurrent import futures
from typing import List

import boto3

from .delete import delete_object


def move_object(source_bucket: str, source_key: str, destination_bucket: str, destination_key: str) -> None:
    """Move S3 object from source bucket and key to destination.

    Parameters
    ----------
    source_bucket : str
        S3 bucket where the object is stored.

    source_key : str
        S3 key where the object is referenced.

    destination_bucket : str
        S3 destination bucket.

    destination_key : str
        S3 destination key.

    Examples
    --------
    >>> move_object(
    ...    source_bucket='bucket',
    ...    source_key='myFiles/song.mp3',
    ...    destination_bucket='bucket',
    ...    destination_key='myMusic/song.mp3'
    ... )

    """
    session = boto3.session.Session()
    s3 = session.resource("s3")

    s3.meta.client.copy(
        {'Bucket': source_bucket, 'Key': source_key},
        destination_bucket,
        destination_key
    )

    delete_object(source_bucket, source_key)


def move_keys(
    source_bucket: str,
    source_keys: List[str],
    destination_bucket: str,
    destination_keys: List[str],
    threads: int = 5
) -> None:
    """Move a list of S3 objects from source bucket to destination.

    Parameters
    ----------
    source_bucket : str
        S3 bucket where the objects are stored.

    source_keys : List[str]
        S3 keys where the objects are referenced.

    destination_bucket : str
        S3 destination bucket.

    destination_keys : List[str]
        S3 destination keys.

    threads : int, optional
        Number of parallel uploads, by default 5.

    Raises
    ------
    IndexError
        When the source_keys and destination_keys have different length.
    ValueError
        When the keys list is empty.

    Examples
    --------
    >>> move_keys(
    ...     source_bucket='bucket',
    ...     source_keys=[
    ...         'myFiles/song.mp3',
    ...         'myFiles/photo.jpg'
    ...     ],
    ...     destination_bucket='bucket',
    ...     destination_keys=[
    ...         'myMusic/song.mp3',
    ...         'myPhotos/photo.jpg'
    ...     ]
    ... )

    """
    if len(source_keys) != len(destination_keys):
        raise IndexError("Key lists must have the same length")

    if len(source_keys) == 0:
        raise ValueError("Key list length must be greater than zero")

    with futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executors = (
            executor.submit(move_object, source_bucket, source, destination_bucket, destination)
            for source, destination in zip(source_keys, destination_keys)
        )

        for ex in executors:
            ex.result()
