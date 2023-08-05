# Copyright (c) 2020 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

# XXX: Please add types to the functions in this file. Static type checking in
# Python prevents bugs!
# mypy: ignore-errors


import qumulo.lib.opts
import qumulo.rest.replication as replication_rest

from qumulo.lib.opts import str_decode

BUCKET_STYLE_PATH = 'BUCKET_STYLE_PATH'
BUCKET_STYLE_VIRTUAL_HOSTED = 'BUCKET_STYLE_VIRTUAL_HOSTED'
BUCKET_STYLE_CHOICES = [BUCKET_STYLE_PATH, BUCKET_STYLE_VIRTUAL_HOSTED]


def get_secret_access_key(secret_access_key):
    if secret_access_key is None:
        secret_access_key = qumulo.lib.opts.read_password(
            prompt='Enter secret access key associated with access key ID: '
        )

    return secret_access_key


class CreateObjectRelationshipCommand(qumulo.lib.opts.Subcommand):
    NAME = 'replication_create_object_relationship'

    SYNOPSIS = """
    Create an object replication relationship that initiates a one-time copy of
    file data to S3.
    """

    @staticmethod
    def options(parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '--source-directory-id',
            type=str_decode,
            help='File ID of the source directory',
        )
        group.add_argument(
            '--source-directory-path',
            type=str_decode,
            help='Path of the source directory',
        )

        parser.add_argument(
            '--object-store-address',
            required=False,
            help="""S3-compatible server address. If omitted, Amazon S3 address
                s3.<region>.amazonaws.com will be used.""",
        )

        parser.add_argument(
            '--object-folder',
            required=True,
            help="""Replication destination folder in the bucket. A slash
                separator is automatically used to create a folder.
                For example, a folder "example" and a file path
                (relative to source directory) "dir/file" results in key
                "example/dir/file". A value of "" or "/" replicates to
                the root of the bucket.""",
        )
        parser.add_argument(
            '--use-port',
            required=False,
            type=int,
            help="""HTTPS port to use when communicating with the object store
                (default: 443)""",
        )
        parser.add_argument(
            '--ca-certificate',
            type=str_decode,
            help="""Path to a file containing the public certificate of the
                certificate authority to trust for connections to the object
                store, in PEM format. If not specified, the built-in trusted
                public CAs are used.""",
        )
        parser.add_argument(
            '--bucket',
            required=True,
            help='Replication destination bucket in the object store',
        )
        parser.add_argument(
            '--bucket-addressing-style',
            choices=BUCKET_STYLE_CHOICES,
            help="""Addressing style for requests to the bucket. Set to
                BUCKET_STYLE_PATH for path-style addressing or
                BUCKET_STYLE_VIRTUAL_HOSTED for virtual hosted-style (the
                default). For Amazon S3, virtual hosted-style is recommended as
                path-style is deprecated. Bucket names containing dots (".") or
                characters that are not valid in domain names may require
                path-style. The object-store-address should not include the
                bucket name, regardless of addressing style.""",
        )
        parser.add_argument(
            '--region',
            required=True,
            help='Region the bucket is located in, e.g., us-west-2',
        )
        parser.add_argument(
            '--access-key-id',
            required=True,
            help="""Access key ID to use when communicating with the
                object store""",
        )
        parser.add_argument(
            '--secret-access-key',
            help="""Secret access key to use when communicating with the
		object store""",
        )

    @staticmethod
    def main(conninfo, credentials, args):
        secret_access_key = get_secret_access_key(args.secret_access_key)

        address = args.object_store_address
        if address is None:
            address = 's3.{}.amazonaws.com'.format(args.region)

        optional_args = {}

        if args.source_directory_id is not None:
            optional_args['source_directory_id'] = args.source_directory_id

        if args.source_directory_path is not None:
            optional_args['source_directory_path'] = args.source_directory_path

        if args.use_port is not None:
            optional_args['port'] = args.use_port

        if args.ca_certificate is not None:
            with open(args.ca_certificate) as f:
                optional_args['ca_certificate'] = f.read()

        if args.bucket_addressing_style is not None:
            optional_args['bucket_style'] = args.bucket_addressing_style

        print(
            replication_rest.create_object_relationship(
                conninfo,
                credentials,
                object_store_address=address,
                bucket=args.bucket,
                object_folder=args.object_folder,
                region=args.region,
                access_key_id=args.access_key_id,
                secret_access_key=secret_access_key,
                **optional_args
            )
        )


class ListObjectRelationshipsCommand(qumulo.lib.opts.Subcommand):
    NAME = 'replication_list_object_relationships'

    SYNOPSIS = 'List all the existing object replication relationships.'

    @staticmethod
    def main(conninfo, credentials, _args):
        print(replication_rest.list_object_relationships(conninfo, credentials))


class GetObjectRelationshipCommand(qumulo.lib.opts.Subcommand):
    NAME = 'replication_get_object_relationship'

    SYNOPSIS = 'Get the configuration of the specified object replication relationship.'

    @staticmethod
    def options(parser):
        parser.add_argument(
            '--id',
            required=True,
            help='Unique identifier of the object replication relationship',
        )

    @staticmethod
    def main(conninfo, credentials, args):
        print(replication_rest.get_object_relationship(conninfo, credentials, args.id))


class DeleteObjectRelationshipCommand(qumulo.lib.opts.Subcommand):
    NAME = 'replication_delete_object_relationship'

    SYNOPSIS = (
        'Delete the specified object replication relationship, '
        'which must not be running a job.'
    )

    @staticmethod
    def options(parser):
        parser.add_argument(
            '--id',
            required=True,
            help='Unique identifier of the object replication relationship',
        )

    @staticmethod
    def main(conninfo, credentials, args):
        replication_rest.delete_object_relationship(conninfo, credentials, args.id)


class AbortObjectReplicationCommand(qumulo.lib.opts.Subcommand):
    NAME = 'replication_abort_object_replication'

    SYNOPSIS = (
        'Abort any ongoing replication job for the '
        'specified object replication relationship.'
    )

    @staticmethod
    def options(parser):
        parser.add_argument(
            '--id',
            required=True,
            help='Unique identifier of the object replication relationship',
        )

    @staticmethod
    def main(conninfo, credentials, args):
        replication_rest.abort_object_replication(conninfo, credentials, args.id)


class ListObjectRelationshipStatusesCommand(qumulo.lib.opts.Subcommand):
    NAME = 'replication_list_object_relationship_statuses'

    SYNOPSIS = 'List the statuses for all existing object replication relationships.'

    @staticmethod
    def main(conninfo, credentials, _args):
        print(replication_rest.list_object_relationship_statuses(conninfo, credentials))


class GetObjectRelationshipStatusCommand(qumulo.lib.opts.Subcommand):
    NAME = 'replication_get_object_relationship_status'

    SYNOPSIS = 'Get current status of the specified object replication relationship.'

    @staticmethod
    def options(parser):
        parser.add_argument(
            '--id',
            required=True,
            help='Unique identifier of the object replication relationship',
        )

    @staticmethod
    def main(conninfo, credentials, args):
        print(
            replication_rest.get_object_relationship_status(
                conninfo, credentials, args.id
            )
        )
