# coding: utf-8
# Copyright (c) 2016, 2021, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from __future__ import print_function
import click
import oci  # noqa: F401
import six  # noqa: F401
import sys  # noqa: F401
from oci_cli import cli_constants  # noqa: F401
from oci_cli import cli_util
from oci_cli import json_skeleton_utils
from oci_cli import custom_types  # noqa: F401
from oci_cli.aliasing import CommandGroupWithAlias
from services.key_management.src.oci_cli_key_management.generated import kms_service_cli


@click.command(cli_util.override('kms_crypto.kms_crypto_root_group.command_name', 'kms-crypto'), cls=CommandGroupWithAlias, help=cli_util.override('kms_crypto.kms_crypto_root_group.help', """API for managing and performing operations with keys and vaults. (For the API for managing secrets, see the Vault Service
Secret Management API. For the API for retrieving secrets, see the Vault Service Secret Retrieval API.)"""), short_help=cli_util.override('kms_crypto.kms_crypto_root_group.short_help', """Vault Service Key Management API"""))
@cli_util.help_option_group
def kms_crypto_root_group():
    pass


@click.command(cli_util.override('kms_crypto.signed_data_group.command_name', 'signed-data'), cls=CommandGroupWithAlias, help="""""")
@cli_util.help_option_group
def signed_data_group():
    pass


@click.command(cli_util.override('kms_crypto.verified_data_group.command_name', 'verified-data'), cls=CommandGroupWithAlias, help="""""")
@cli_util.help_option_group
def verified_data_group():
    pass


@click.command(cli_util.override('kms_crypto.exported_key_data_group.command_name', 'exported-key-data'), cls=CommandGroupWithAlias, help="""The response to a request to export key material.""")
@cli_util.help_option_group
def exported_key_data_group():
    pass


@click.command(cli_util.override('kms_crypto.decrypted_data_group.command_name', 'decrypted-data'), cls=CommandGroupWithAlias, help="""""")
@cli_util.help_option_group
def decrypted_data_group():
    pass


@click.command(cli_util.override('kms_crypto.generated_key_group.command_name', 'generated-key'), cls=CommandGroupWithAlias, help="""""")
@cli_util.help_option_group
def generated_key_group():
    pass


@click.command(cli_util.override('kms_crypto.encrypted_data_group.command_name', 'encrypted-data'), cls=CommandGroupWithAlias, help="""""")
@cli_util.help_option_group
def encrypted_data_group():
    pass


kms_service_cli.kms_service_group.add_command(kms_crypto_root_group)
kms_crypto_root_group.add_command(signed_data_group)
kms_crypto_root_group.add_command(verified_data_group)
kms_crypto_root_group.add_command(exported_key_data_group)
kms_crypto_root_group.add_command(decrypted_data_group)
kms_crypto_root_group.add_command(generated_key_group)
kms_crypto_root_group.add_command(encrypted_data_group)


@decrypted_data_group.command(name=cli_util.override('kms_crypto.decrypt.command_name', 'decrypt'), help=u"""Decrypts data using the given [DecryptDataDetails] resource.

The top level --endpoint parameter must be supplied for this operation. \n[Command Reference](decrypt)""")
@cli_util.option('--ciphertext', required=True, help=u"""The encrypted data to decrypt.""")
@cli_util.option('--key-id', required=True, help=u"""The OCID of the key used to encrypt the ciphertext.""")
@cli_util.option('--associated-data', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Information that can be used to provide an encryption context for the encrypted data. The length of the string representation of the associated data must be fewer than 4096 characters.""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--logging-context', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Information that provides context for audit logging. You can provide this additional data as key-value pairs to include in audit logs when audit logging is enabled.""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--key-version-id', help=u"""The OCID of the keyVersion used to encrypt the ciphertext.""")
@cli_util.option('--encryption-algorithm', type=custom_types.CliCaseInsensitiveChoice(["AES_256_GCM", "RSA_OAEP_SHA_1", "RSA_OAEP_SHA_256"]), help=u"""Encryption algorithm to be used while encrypting/decrypting data using a customer key AES_256_GCM is the supported value AES keys and uses GCM mode of operation RSA_OAEP_SHA_1 and RSA_OAEP_SHA_256 are supported for RSA keys and use OAEP padding.""")
@json_skeleton_utils.get_cli_json_input_option({'associated-data': {'module': 'key_management', 'class': 'dict(str, string)'}, 'logging-context': {'module': 'key_management', 'class': 'dict(str, string)'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'associated-data': {'module': 'key_management', 'class': 'dict(str, string)'}, 'logging-context': {'module': 'key_management', 'class': 'dict(str, string)'}}, output_type={'module': 'key_management', 'class': 'DecryptedData'})
@cli_util.wrap_exceptions
def decrypt(ctx, from_json, ciphertext, key_id, associated_data, logging_context, key_version_id, encryption_algorithm):

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    _details = {}
    _details['ciphertext'] = ciphertext
    _details['keyId'] = key_id

    if associated_data is not None:
        _details['associatedData'] = cli_util.parse_json_parameter("associated_data", associated_data)

    if logging_context is not None:
        _details['loggingContext'] = cli_util.parse_json_parameter("logging_context", logging_context)

    if key_version_id is not None:
        _details['keyVersionId'] = key_version_id

    if encryption_algorithm is not None:
        _details['encryptionAlgorithm'] = encryption_algorithm

    client = cli_util.build_client('key_management', 'kms_crypto', ctx)
    result = client.decrypt(
        decrypt_data_details=_details,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@encrypted_data_group.command(name=cli_util.override('kms_crypto.encrypt.command_name', 'encrypt'), help=u"""Encrypts data using the given [EncryptDataDetails] resource. Plaintext included in the example request is a base64-encoded value of a UTF-8 string.

The top level --endpoint parameter must be supplied for this operation. \n[Command Reference](encrypt)""")
@cli_util.option('--key-id', required=True, help=u"""The OCID of the key to encrypt with.""")
@cli_util.option('--plaintext', required=True, help=u"""The plaintext data to encrypt.""")
@cli_util.option('--associated-data', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Information that can be used to provide an encryption context for the encrypted data. The length of the string representation of the associated data must be fewer than 4096 characters.""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--logging-context', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Information that provides context for audit logging. You can provide this additional data as key-value pairs to include in the audit logs when audit logging is enabled.""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--key-version-id', help=u"""The OCID of the keyVersion used to encrypt the ciphertext.""")
@cli_util.option('--encryption-algorithm', type=custom_types.CliCaseInsensitiveChoice(["AES_256_GCM", "RSA_OAEP_SHA_1", "RSA_OAEP_SHA_256"]), help=u"""Encryption algorithm to be used while encrypting/decrypting data using a customer key AES_256_GCM is the supported value AES keys and uses GCM mode of operation RSA_OAEP_SHA_1 and RSA_OAEP_SHA_256 are supported for RSA keys and use OAEP padding.""")
@json_skeleton_utils.get_cli_json_input_option({'associated-data': {'module': 'key_management', 'class': 'dict(str, string)'}, 'logging-context': {'module': 'key_management', 'class': 'dict(str, string)'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'associated-data': {'module': 'key_management', 'class': 'dict(str, string)'}, 'logging-context': {'module': 'key_management', 'class': 'dict(str, string)'}}, output_type={'module': 'key_management', 'class': 'EncryptedData'})
@cli_util.wrap_exceptions
def encrypt(ctx, from_json, key_id, plaintext, associated_data, logging_context, key_version_id, encryption_algorithm):

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    _details = {}
    _details['keyId'] = key_id
    _details['plaintext'] = plaintext

    if associated_data is not None:
        _details['associatedData'] = cli_util.parse_json_parameter("associated_data", associated_data)

    if logging_context is not None:
        _details['loggingContext'] = cli_util.parse_json_parameter("logging_context", logging_context)

    if key_version_id is not None:
        _details['keyVersionId'] = key_version_id

    if encryption_algorithm is not None:
        _details['encryptionAlgorithm'] = encryption_algorithm

    client = cli_util.build_client('key_management', 'kms_crypto', ctx)
    result = client.encrypt(
        encrypt_data_details=_details,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@exported_key_data_group.command(name=cli_util.override('kms_crypto.export_key.command_name', 'export-key'), help=u"""Exports a specific version of a master encryption key according to the details of the request. For their protection, keys that you create and store on a hardware security module (HSM) can never leave the HSM. You can only export keys stored on the server. For export, the key version is encrypted by an RSA public key that you provide.

The top level --endpoint parameter must be supplied for this operation. \n[Command Reference](exportKey)""")
@cli_util.option('--key-id', required=True, help=u"""The OCID of the master encryption key associated with the key version you want to export.""")
@cli_util.option('--algorithm', required=True, type=custom_types.CliCaseInsensitiveChoice(["RSA_OAEP_AES_SHA256", "RSA_OAEP_SHA256"]), help=u"""The encryption algorithm to use to encrypt exportable key material from a software-backed key. Specifying `RSA_OAEP_AES_SHA256` invokes the RSA AES key wrap mechanism, which generates a temporary AES key. The temporary AES key is wrapped by the RSA public wrapping key provided along with the request, creating a wrapped temporary AES key. The temporary AES key is also used to wrap the exportable key material. The wrapped temporary AES key and the wrapped exportable key material are concatenated, producing concatenated blob output that jointly represents them. Specifying `RSA_OAEP_SHA256` means that the software key is wrapped by the RSA public wrapping key provided along with the request.""")
@cli_util.option('--public-key', required=True, help=u"""The PEM format of the 2048-bit, 3072-bit, or 4096-bit RSA wrapping key in your possession that you want to use to encrypt the key.""")
@cli_util.option('--key-version-id', help=u"""The OCID of the specific key version to export. If not specified, the service exports the current key version.""")
@cli_util.option('--logging-context', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Information that provides context for audit logging. You can provide this additional data as key-value pairs to include in the audit logs when audit logging is enabled.""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@json_skeleton_utils.get_cli_json_input_option({'logging-context': {'module': 'key_management', 'class': 'dict(str, string)'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'logging-context': {'module': 'key_management', 'class': 'dict(str, string)'}}, output_type={'module': 'key_management', 'class': 'ExportedKeyData'})
@cli_util.wrap_exceptions
def export_key(ctx, from_json, key_id, algorithm, public_key, key_version_id, logging_context):

    kwargs = {}

    _details = {}
    _details['keyId'] = key_id
    _details['algorithm'] = algorithm
    _details['publicKey'] = public_key

    if key_version_id is not None:
        _details['keyVersionId'] = key_version_id

    if logging_context is not None:
        _details['loggingContext'] = cli_util.parse_json_parameter("logging_context", logging_context)

    client = cli_util.build_client('key_management', 'kms_crypto', ctx)
    result = client.export_key(
        export_key_details=_details,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@generated_key_group.command(name=cli_util.override('kms_crypto.generate_data_encryption_key.command_name', 'generate-data-encryption-key'), help=u"""Generates a key that you can use to encrypt or decrypt data.

The top level --endpoint parameter must be supplied for this operation. \n[Command Reference](generateDataEncryptionKey)""")
@cli_util.option('--include-plaintext-key', required=True, type=click.BOOL, help=u"""If true, the generated key is also returned unencrypted.""")
@cli_util.option('--key-id', required=True, help=u"""The OCID of the master encryption key to encrypt the generated data encryption key with.""")
@cli_util.option('--key-shape', required=True, type=custom_types.CLI_COMPLEX_TYPE, help=u"""""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--associated-data', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Information that can be used to provide an encryption context for the encrypted data. The length of the string representation of the associated data must be fewer than 4096 characters.""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--logging-context', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Information that provides context for audit logging. You can provide this additional data by formatting it as key-value pairs to include in audit logs when audit logging is enabled.""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@json_skeleton_utils.get_cli_json_input_option({'associated-data': {'module': 'key_management', 'class': 'dict(str, string)'}, 'key-shape': {'module': 'key_management', 'class': 'KeyShape'}, 'logging-context': {'module': 'key_management', 'class': 'dict(str, string)'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'associated-data': {'module': 'key_management', 'class': 'dict(str, string)'}, 'key-shape': {'module': 'key_management', 'class': 'KeyShape'}, 'logging-context': {'module': 'key_management', 'class': 'dict(str, string)'}}, output_type={'module': 'key_management', 'class': 'GeneratedKey'})
@cli_util.wrap_exceptions
def generate_data_encryption_key(ctx, from_json, include_plaintext_key, key_id, key_shape, associated_data, logging_context):

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    _details = {}
    _details['includePlaintextKey'] = include_plaintext_key
    _details['keyId'] = key_id
    _details['keyShape'] = cli_util.parse_json_parameter("key_shape", key_shape)

    if associated_data is not None:
        _details['associatedData'] = cli_util.parse_json_parameter("associated_data", associated_data)

    if logging_context is not None:
        _details['loggingContext'] = cli_util.parse_json_parameter("logging_context", logging_context)

    client = cli_util.build_client('key_management', 'kms_crypto', ctx)
    result = client.generate_data_encryption_key(
        generate_key_details=_details,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@signed_data_group.command(name=cli_util.override('kms_crypto.sign.command_name', 'sign'), help=u"""Creates a digital signature for a message or message digest by using the private key in an asymmetric key. To verify the generated signature, you can use the Verify operation or use the public key in the same asymmetric key outside of KMS

The top level --endpoint parameter must be supplied for this operation. \n[Command Reference](sign)""")
@cli_util.option('--message', required=True, help=u"""The Base64-encoded binary data object denoting the message or message digest to be signed. Message can be upto 4096 size in bytes. To sign a larger message, provide the message digest.""")
@cli_util.option('--key-id', required=True, help=u"""The OCID of the key used to sign the message""")
@cli_util.option('--signing-algorithm', required=True, type=custom_types.CliCaseInsensitiveChoice(["SHA_224_RSA_PKCS_PSS", "SHA_256_RSA_PKCS_PSS", "SHA_384_RSA_PKCS_PSS", "SHA_512_RSA_PKCS_PSS", "SHA_224_RSA_PKCS1_V1_5", "SHA_256_RSA_PKCS1_V1_5", "SHA_384_RSA_PKCS1_V1_5", "SHA_512_RSA_PKCS1_V1_5", "ECDSA_SHA_256", "ECDSA_SHA_384", "ECDSA_SHA_512"]), help=u"""The algorithm to be used for signing the message or message digest For RSA keys, there are two supported Signature Schemes: PKCS1 and PSS along with different Hashing algorithms. For ECDSA keys, ECDSA is the supported signature scheme with different hashing algorithms. In case of passing digest for signing, make sure the same hashing algorithm is specified as used for created for digest.""")
@cli_util.option('--key-version-id', help=u"""The OCID of the keyVersion used to sign the message.""")
@cli_util.option('--message-type', type=custom_types.CliCaseInsensitiveChoice(["RAW", "DIGEST"]), help=u"""Denotes whether the value of the message parameter is a raw message or a message digest. The default value, RAW, indicates a message. To indicate a message digest, use DIGEST.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'key_management', 'class': 'SignedData'})
@cli_util.wrap_exceptions
def sign(ctx, from_json, message, key_id, signing_algorithm, key_version_id, message_type):

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    _details = {}
    _details['message'] = message
    _details['keyId'] = key_id
    _details['signingAlgorithm'] = signing_algorithm

    if key_version_id is not None:
        _details['keyVersionId'] = key_version_id

    if message_type is not None:
        _details['messageType'] = message_type

    client = cli_util.build_client('key_management', 'kms_crypto', ctx)
    result = client.sign(
        sign_data_details=_details,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@verified_data_group.command(name=cli_util.override('kms_crypto.verify.command_name', 'verify'), help=u"""Verifies a digital signature that was generated by the Sign operation using the public key in the same asymmetric key. You can also verify the digital signature by using the public key in the asymmetric key outside of KMS

The top level --endpoint parameter must be supplied for this operation. \n[Command Reference](verify)""")
@cli_util.option('--key-id', required=True, help=u"""The OCID of the key used to sign the message""")
@cli_util.option('--key-version-id', required=True, help=u"""The OCID of the keyVersion used to sign the message""")
@cli_util.option('--signature', required=True, help=u"""The Base64-encoded binary data object denoting the cryptographic signature that was generated for the message.""")
@cli_util.option('--message', required=True, help=u"""The Base64-encoded binary data object denoting the message or message digest to be signed. Message can be upto 4096 size in bytes. To sign a larger message, provide the message digest.""")
@cli_util.option('--signing-algorithm', required=True, type=custom_types.CliCaseInsensitiveChoice(["SHA_224_RSA_PKCS_PSS", "SHA_256_RSA_PKCS_PSS", "SHA_384_RSA_PKCS_PSS", "SHA_512_RSA_PKCS_PSS", "SHA_224_RSA_PKCS1_V1_5", "SHA_256_RSA_PKCS1_V1_5", "SHA_384_RSA_PKCS1_V1_5", "SHA_512_RSA_PKCS1_V1_5", "ECDSA_SHA_256", "ECDSA_SHA_384", "ECDSA_SHA_512"]), help=u"""The algorithm to be used for signing the message or message digest For RSA keys, there are two supported Signature Schemes: PKCS1 and PSS along with different Hashing algorithms. For ECDSA keys, ECDSA is the supported signature scheme with different hashing algorithms. In case of passing digest for signing, make sure the same hashing algorithm is specified as used for created for digest.""")
@cli_util.option('--message-type', type=custom_types.CliCaseInsensitiveChoice(["RAW", "DIGEST"]), help=u"""Denotes whether the value of the message parameter is a raw message or a message digest. The default value, RAW, indicates a message. To indicate a message digest, enter DIGEST.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'key_management', 'class': 'VerifiedData'})
@cli_util.wrap_exceptions
def verify(ctx, from_json, key_id, key_version_id, signature, message, signing_algorithm, message_type):

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    _details = {}
    _details['keyId'] = key_id
    _details['keyVersionId'] = key_version_id
    _details['signature'] = signature
    _details['message'] = message
    _details['signingAlgorithm'] = signing_algorithm

    if message_type is not None:
        _details['messageType'] = message_type

    client = cli_util.build_client('key_management', 'kms_crypto', ctx)
    result = client.verify(
        verify_data_details=_details,
        **kwargs
    )
    cli_util.render_response(result, ctx)
