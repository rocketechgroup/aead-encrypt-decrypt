--- Query returns the following error: Query error: AEAD.DECRYPT_STRING failed: Keyset deserialization failed: Error reading keyset data: Could not parse the input stream as a Keyset-proto. at [5:1]
DECLARE kms_resource_name STRING;
SET kms_resource_name = 'gcp-kms://projects/rocketech-de-pgcp-sandbox/locations/europe-west2/keyRings/aead-example/cryptoKeys/symmetric_demo';


SELECT
  AEAD.DECRYPT_STRING(
    KEYS.NEW_WRAPPED_KEYSET(kms_resource_name, 'AEAD_AES_GCM_256'),
    FROM_BASE64(salary),
    ''
  )
 FROM `rocketech-de-pgcp-sandbox.aead_encrypt_decrypt.encrypted_input` LIMIT 1000
