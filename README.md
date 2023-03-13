# AEAD Encrypt / Decrypt
This is an example with the attempt to encrypt data at field level from a JSONL file using AEAD GCM,
load the data into BigQuery and decrypt the data using BigQuery's AEAD functions. 

Both encryption & decryption are done using the same KMS key ring. 

## Build & Run
Install `bazel` first which is required by the Tink library. 
```
brew install bazel
```
Build the container
```
docker build -t aead-encrypt-decrypt .
```