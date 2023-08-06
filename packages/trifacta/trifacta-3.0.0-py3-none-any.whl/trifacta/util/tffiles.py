import tempfile

from trifacta.util import tfrequests


def _make_s3_upload_string(user, awsConfig):
    storageConfig = {
        "protocol": "s3",
        "bucketName": awsConfig["defaultBucket"],
        **awsConfig
    }
    if 'createdAt' in storageConfig:
        storageConfig.pop("createdAt")
    if 'updatedAt' in storageConfig:
        storageConfig.pop("updatedAt")

    uploadDir = user["uploadDir"]

    uploadStr = "/v2/vfs?" + "&".join(
        {"storageConfig%5B" + k + "%5d=" + str(v) for (k, v) in storageConfig.items()}
    )
    uploadStr = uploadStr + "&uploadDir=" + uploadDir
    return uploadStr


def _make_file_upload_string(user):
    storageConfig = {"protocol": "file"}
    uploadDir = user["uploadDir"]

    uploadStr = "/v2/vfs?" + "&".join(
        {"storageConfig%5B" + k + "%5d=" + str(v) for (k, v) in storageConfig.items()}
    )
    uploadStr = uploadStr + "&uploadDir=" + uploadDir
    return uploadStr


def uploadFile(
    path: str = None,
    filename: str = None,
    data: str = None,
    raw=False,
    user=None,
    awsConfig=None,
):
    if data is None and path is None:
        raise(ValueError("You must provide a path to a file or some string data"))

    if filename is None:
        filename = path if path is not None else "data"

    if user is None:
        raise(ValueError("You must provide a valid user object to upload data"))
 
    if awsConfig:
        uploadStr = _make_s3_upload_string(user, awsConfig)
    else:
        uploadStr = _make_file_upload_string(user)
    file = open(path, "rb") if path is not None else StringIO(data)
    r = tfrequests.upload(url=uploadStr, filename=filename, file=file).json()
    file.close()
    return r


def _fetchFile(resp, fd):
    for chunk in resp.iter_content(chunk_size=128):
        fd.write(chunk)


def downloadGet(url: str = None, destination: str = None):
    resp = tfrequests.get(url)
    if not destination:
        fd = tempfile.NamedTemporaryFile(delete=False)
        _fetchFile(resp, fd)
        destination = fd.name
        fd.close()
    else:
        with open(destination, "wb") as fd:
            _fetchFile(resp, fd)
    return destination
