from __future__ import annotations

__all__ = (
    "download_object",
    "download_file",
    "upload_object",
    "upload_file",
    "fetch_head",
    "ctx_download_file",
)

import contextlib
import tempfile
from typing import Any, Optional, Literal, BinaryIO, Union, AsyncIterator

import aiobotocore
import botocore.client

from lambda_utility.session import create_client
from lambda_utility.path import PathExt
from lambda_utility.schema import (
    S3GetObjectResponse,
    S3PutObjectResponse,
    S3HeadObjectResponse,
)
from lambda_utility.typedefs import PathLike

KB = 1024
DEFAULT_CHUNK_SIZE = 64 * KB


async def download_object(
    bucket: str,
    key: PathLike,
    *,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
    **kwargs: Any,
) -> S3GetObjectResponse:
    """
    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
    """
    if client is None:
        client = create_client("s3", config=config)

    async with client as client_obj:
        resp = await client_obj.get_object(Bucket=bucket, Key=str(key), **kwargs)
        body = await resp["Body"].read()

    return S3GetObjectResponse(
        content_type=resp["ContentType"],
        content_length=resp["ContentLength"],
        response_metadata=resp["ResponseMetadata"],
        metadata=resp["Metadata"],
        body=body,
    )


async def download_file(
    bucket: str,
    key: PathLike,
    filename: PathLike,
    *,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    **kwargs: Any,
) -> S3GetObjectResponse:
    """
    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
    """
    if client is None:
        client = create_client("s3", config=config)

    async with client as client_obj:
        resp = await client_obj.get_object(Bucket=bucket, Key=str(key), **kwargs)

        stream = resp["Body"]
        with open(filename, "wb") as f:
            async for chunk in stream.iter_chunks(chunk_size=chunk_size):
                f.write(chunk)

    return S3GetObjectResponse(
        content_type=resp["ContentType"],
        content_length=resp["ContentLength"],
        response_metadata=resp["ResponseMetadata"],
        metadata=resp["Metadata"],
        body=None,
    )


ACLType = Literal[
    "private",
    "public-read",
    "public-read-write",
    "authenticated-read",
    "aws-exec-read",
    "bucket-owner-read",
    "bucket-owner-full-control",
]


async def upload_object(
    bucket: str,
    key: PathLike,
    body: Union[bytes, BinaryIO],
    *,
    acl: ACLType = "private",
    metadata: Optional[dict[str, str]] = None,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
    **kwargs: Any,
) -> S3PutObjectResponse:
    """
    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object
    """
    if client is None:
        client = create_client("s3", config=config)
    if metadata is None:
        metadata = {}

    async with client as client_obj:
        resp = await client_obj.put_object(
            Bucket=bucket, Key=str(key), Body=body, ACL=acl, Metadata=metadata, **kwargs
        )

    return S3PutObjectResponse(**resp)


async def upload_file(
    bucket: str,
    key: PathLike,
    filepath: PathLike,
    *,
    acl: ACLType = "private",
    metadata: Optional[dict[str, str]] = None,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
    **kwargs: Any,
) -> S3PutObjectResponse:
    """
    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object
    """
    with open(filepath, "rb") as f:
        return await upload_object(
            bucket,
            key,
            f,
            acl=acl,
            metadata=metadata,
            client=client,
            config=config,
            **kwargs,
        )


async def fetch_head(
    bucket: str,
    key: PathLike,
    *,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
    **kwargs: Any,
) -> S3HeadObjectResponse:
    """
    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_object
    """
    if client is None:
        client = create_client("s3", config=config)

    async with client as client_obj:
        resp = await client_obj.head_object(Bucket=bucket, Key=str(key), **kwargs)

    return S3HeadObjectResponse(**resp)


@contextlib.asynccontextmanager
async def ctx_download_file(
    bucket: str,
    key: PathLike,
    *,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
    **kwargs: Any,
) -> AsyncIterator[tuple[PathExt, S3GetObjectResponse]]:
    """
    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
    """
    suffix = PathExt(key).suffix
    with tempfile.NamedTemporaryFile(suffix=suffix) as f:
        resp = await download_object(
            bucket, key, client=client, config=config, **kwargs
        )
        f.write(resp.body or b"")
        resp.body = None
        yield PathExt(f.name), resp
