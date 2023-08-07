# Local Emulator for Google Cloud Storage

![CI](https://github.com/oittaa/gcp-storage-emulator/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/oittaa/gcp-storage-emulator/branch/main/graph/badge.svg?token=GpiSgoXsGL)](https://codecov.io/gh/oittaa/gcp-storage-emulator)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Google doesn't (yet) ship an emulator for the Cloud Storage API like they do for
Cloud Datastore.

This is a stub emulator so you can run your tests and do local development without
having to connect to the production Storage APIs.


**THIS IS A WORK IN PROGRESS AND ONLY SUPPORTS A LIMITED SUBSET OF THE API**

---

## Installation

`pip install gcp-storage-emulator`


## CLI Usage


### Starting the emulator
Start the emulator with:

```bash
gcp-storage-emulator start --port=9090
```

By default, data is stored under `./.cloudstorage`. You can configure the folder using the env variables `STORAGE_BASE` (default `./`) and `STORAGE_DIR` (default `.cloudstorage`).

If you wish to run the emulator in a testing environment or if you don't want to persist any data, you can use the `--no-store-on-disk` parameter. For tests, you might want to consider starting up the server from your code (see the [Python APIs](#python-apis))

If you're using the Google client library (e.g. `google-cloud-storage` for Python) then you can set the `STORAGE_EMULATOR_HOST` environment variable to tell the library to connect to your emulator endpoint rather than the standard `https://storage.googleapis.com`, e.g.:

```bash
export STORAGE_EMULATOR_HOST=http://localhost:9090
```


### Wiping data

You can wipe the data by running

```bash
gcp-storage-emulator wipe
```

## Python APIs

To start a server from your code you can do

```python
from gcp_storage_emulator.server import create_server

server = create_server("localhost", 9023, in_memory=False)

server.start()
# ........
server.stop()
```

You can wipe the data by calling `server.wipe()`

This can also be achieved (e.g. during tests) by hitting the `/wipe` endpoint

#### Example

Create a test file `emulator-test.py`.

```python
from google.auth.credentials import AnonymousCredentials
from google.cloud import storage
from gcp_storage_emulator.server import create_server

PORT = 8080
BUCKET = "test-bucket"

server = create_server("localhost", PORT, in_memory=True)
server.start()

client = storage.Client(
    credentials=AnonymousCredentials(),
    project="test",
)
bucket = client.bucket(BUCKET)
bucket = client.create_bucket(bucket)
blob = bucket.blob("blob1")
blob.upload_from_string("test1")
blob = bucket.blob("blob2")
blob.upload_from_string("test2")
for blob in bucket.list_blobs():
    content = blob.download_as_bytes()
    print("Blob [{}]: {}".format(blob.name, content))
server.stop()
```

Run the following commands to test the emulated storage.

```bash
export STORAGE_EMULATOR_HOST=http://localhost:8080
python3 emulator-test.py
```


## Docker

Pull the Docker image.

```bash
docker pull oittaa/gcp-storage-emulator
```

Inside the container instance, the value of the `PORT` environment variable always reflects the port to which requests are sent. It defaults to `8080`. The directory used for the emulated storage is located in `/app/.cloudstorage`. In the following example the host's directory `$(pwd)/cloudstorage` will be bound to the emulated storage.

```
docker run -d \
  -p 8080:8080 \
  --name gcp-storage-emulator \
  -v "$(pwd)"/cloudstorage:/app/.cloudstorage \
  oittaa/gcp-storage-emulator
```
