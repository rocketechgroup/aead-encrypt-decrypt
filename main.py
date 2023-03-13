import logging
import tink
import base64

from google.cloud import bigquery
from tink import aead
from tink.integration import gcpkms


def init_aead(kek_uri):
    # Initialise Tink
    try:
        aead.register()
    except tink.TinkError as e:
        logging.error('Error initialising Tink: %s', e)
        return 1

    # Read the GCP credentials and setup client
    try:
        gcpkms.GcpKmsClient.register_client(
            kek_uri, "")
    except tink.TinkError as e:
        logging.error('Error initializing GCP client: %s', e)
        return 1

    # Create envelope AEAD primitive using AES256 GCM for encrypting the data
    try:
        template = aead.aead_key_templates.create_kms_envelope_aead_key_template(
            kek_uri=kek_uri,
            dek_template=aead.aead_key_templates.AES256_GCM
        )
        handle = tink.new_keyset_handle(template)
        env_aead = handle.primitive(aead.Aead)
    except tink.TinkError as e:
        logging.error('Error creating primitive: %s', e)
        return 1
    return env_aead


def encrypt(env_aead, input_data):
    output = env_aead.encrypt(plaintext=str(input_data).encode('utf-8'), associated_data=b'')
    encoded_bytes = base64.b64encode(output)
    encoded_string = encoded_bytes.decode("utf-8")

    return encoded_string


def exec(project_id, env_aead):
    client = bigquery.Client(project=project_id)
    dataset_id = 'aead_encrypt_decrypt'
    table_id = 'encrypted_input'

    rows = [
        {'col1': encrypt(env_aead, 3000)},
        {'col1': encrypt(env_aead, 30000)},
        {'col1': encrypt(env_aead, 200000)}
    ]

    print(rows)

    # Create the table reference object
    table_ref = f'{dataset_id}.{table_id}'

    # Insert the data into the table
    client.insert_rows_json(table=table_ref, json_rows=rows)

    print('Data inserted into table {}.{}'.format(dataset_id, table_id))


env_aead = init_aead(
    kek_uri='gcp-kms://projects/rocketech-de-pgcp-sandbox/locations/europe-west2/keyRings/aead-example/cryptoKeys/symmetric_demo')
exec(project_id='rocketech-de-pgcp-sandbox', env_aead=env_aead)
