# AEAD Encrypt / Decrypt
This is an example with the attempt to encrypt data at field level from a JSONL file using AEAD GCM,
load the data into BigQuery and decrypt the data using BigQuery's AEAD functions. 

Both encryption & decryption are done using the same KMS key ring. 

## Build & Run
> Please note due to support issues with the Tinker library on a Silicon Mac, this code does not yet work on it
```
WIP