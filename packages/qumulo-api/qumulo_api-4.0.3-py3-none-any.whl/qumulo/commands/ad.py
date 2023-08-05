# Copyright (c) 2013 Qumulo, Inc.
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


import qumulo.lib.auth
import qumulo.lib.opts
import qumulo.lib.util
import qumulo.rest.ad as ad

from qumulo.lib.opts import str_decode


class ListAdCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_list'
    SYNOPSIS = 'List Active Directory configuration'

    @staticmethod
    def main(conninfo, credentials, _args):
        print(ad.list_ad(conninfo, credentials))


class PollAdCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_poll'
    SYNOPSIS = 'Poll Active Directory configuration'

    @staticmethod
    def main(conninfo, credentials, _args):
        print(ad.poll_ad(conninfo, credentials))


def add_ad_options(parser, creds_required):
    parser.add_argument(
        '-d',
        '--domain',
        type=str_decode,
        default=None,
        required=True,
        help='Fully-qualified name of Domain Controller',
    )
    parser.add_argument(
        '-u',
        '--username',
        type=str_decode,
        default=None,
        help='Username on Domain Controller',
        required=creds_required,
    )
    parser.add_argument(
        '-p',
        '--password',
        type=str_decode,
        default=None,
        help='Password on Domain Controller (insecure, visible via ps)',
    )


class JoinAdCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_join'
    SYNOPSIS = 'Join an Active Directory Domain'

    @staticmethod
    def options(parser):
        add_ad_options(parser, True)
        parser.add_argument(
            '--domain-netbios',
            type=str_decode,
            required=False,
            help='NetBIOS name of the domain. By default, the first part of '
            'the domain name is used.',
        )
        parser.add_argument(
            '-o',
            '--ou',
            type=str_decode,
            default='',
            required=False,
            help='Organizational Unit to join to',
        )
        parser.add_argument(
            '--use-ad-posix-attributes',
            action='store_true',
            required=False,
            help='Use AD POSIX attributes.',
        )
        parser.add_argument(
            '--base-dn',
            required=False,
            help='When using LDAP POSIX extensions, query using this base DN',
        )

    @staticmethod
    def main(conninfo, credentials, args):
        if args.password is None:
            password = qumulo.lib.opts.read_password(prompt='Password: ')
        else:
            password = args.password

        print(
            ad.join_ad(
                conninfo,
                credentials,
                args.domain,
                args.username,
                password,
                args.ou,
                domain_netbios=args.domain_netbios,
                enable_ldap=args.use_ad_posix_attributes,
                base_dn=args.base_dn,
            )
        )


class LeaveAdCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_leave'
    SYNOPSIS = 'Leave an Active Directory Domain'

    @staticmethod
    def options(parser):
        add_ad_options(parser, False)

    @staticmethod
    def main(conninfo, credentials, args):
        if args.username is not None and args.password is None:
            password = qumulo.lib.opts.read_password(prompt='Password: ')
        else:
            password = args.password

        print(ad.leave_ad(conninfo, credentials, args.domain, args.username, password))


class CancelAdCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_cancel'
    SYNOPSIS = 'Cancel current AD join/leave operation and clear errors'

    @staticmethod
    def main(conninfo, credentials, _args):
        print(ad.cancel_ad(conninfo, credentials))


class GetAdvancedAdSettingsCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_get_advanced_settings'
    SYNOPSIS = 'Get advanced Active Directory settings'

    @staticmethod
    def main(conninfo, credentials, _args):
        print(ad.get_advanced_settings(conninfo, credentials))


class SetAdvancedAdSettingsCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_set_advanced_settings'
    SYNOPSIS = 'Modify advanced Active Directory settings'
    CHOICES = ('off', 'prefer', 'require')

    @staticmethod
    def options(parser):
        parser.add_argument(
            '--signing',
            choices=SetAdvancedAdSettingsCommand.CHOICES,
            help='Configure DCERPC signing to be off, prefer signing, or require '
            'signing. The default is to prefer signing.',
        )
        parser.add_argument(
            '--sealing',
            choices=SetAdvancedAdSettingsCommand.CHOICES,
            help='Configure DCERPC sealing to be off, prefer sealing, or require '
            'sealing. The default is to prefer sealing.',
        )
        parser.add_argument(
            '--crypto',
            choices=SetAdvancedAdSettingsCommand.CHOICES,
            help='Configure DCERPC to not use encryption, prefer AES encryption, or '
            'require AES encryption. The default is to prefer AES encryption.',
        )

    @staticmethod
    def main(conninfo, credentials, args):
        settings = {
            'signing': args.signing,
            'sealing': args.sealing,
            'crypto': args.crypto,
        }

        # At least one of the arguments must be specified.
        if all(v is None for k, v in settings.items()):
            raise ValueError(
                'Must set at least one of --signing, --sealing, or --crypto.'
            )

        # Get the original settings if any arguments are unspecified; we'll use an etag
        # to avoid race conditions.
        if any(v is None for k, v in settings.items()):
            old_settings, etag = ad.get_advanced_settings(conninfo, credentials)
            settings['if_match'] = etag

            # Choose between the existing value for a parameter or the user-provided
            # value based on whether the user actually provided a value.
            def choose_value(name, value_choices):
                choice = getattr(args, name)
                if choice is None:
                    return old_settings[name]

                # The SetAdvancedAdSettingsCommand.CHOICES tuple is laid out in the same
                # order as the ad.VALID_SIGNING_CHOICES, ad.VALID_SEALING_CHOICES, and
                # ad.VALID_ENCRYPTION_CHOICES tuples, so that finding the index in the
                # first yields the API value in the other.
                choice_index = SetAdvancedAdSettingsCommand.CHOICES.index(choice)
                return value_choices[choice_index]

            settings['signing'] = choose_value('signing', ad.VALID_SIGNING_CHOICES)
            settings['sealing'] = choose_value('sealing', ad.VALID_SEALING_CHOICES)
            settings['crypto'] = choose_value('crypto', ad.VALID_ENCRYPTION_CHOICES)

        print(ad.set_advanced_settings(conninfo, credentials, **settings))


class UidToSidsGetCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_uid_to_sids'
    SYNOPSIS = 'Get SIDs from UID'

    @staticmethod
    def options(parser):
        parser.add_argument(
            '-u',
            '--uid',
            help='Get the SIDs that correspond to this UID',
            required=True,
        )

    @staticmethod
    def main(conninfo, credentials, args):
        print(ad.uid_to_sid_get(conninfo, credentials, args.uid))


class UsernameToSidsGetCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_username_to_sids'
    SYNOPSIS = 'Get SIDs from an AD username'

    @staticmethod
    def options(parser):
        parser.add_argument(
            '-u',
            '--username',
            help='Get the SIDs that correspond to this username',
            required=True,
        )

    @staticmethod
    def main(conninfo, credentials, args):
        print(ad.username_to_sid_get(conninfo, credentials, args.username))


class NameToAccountCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_name_to_accounts'
    SYNOPSIS = 'Get all account info for a sAMAccountName'

    @staticmethod
    def options(parser):
        parser.add_argument(
            '-n',
            '--name',
            help='Get account info for this sAMAccountName',
            required=True,
        )

    @staticmethod
    def main(conninfo, credentials, args):
        print(ad.name_to_ad_accounts(conninfo, credentials, args.name))


class SidToUidGetCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_sid_to_uid'
    SYNOPSIS = 'Get UID from SID'

    @staticmethod
    def options(parser):
        parser.add_argument(
            '-s',
            '--sid',
            help='Get the UID that corresponds to this SID',
            required=True,
        )

    @staticmethod
    def main(conninfo, credentials, args):
        print(ad.sid_to_uid_get(conninfo, credentials, args.sid))


class SidToUsernameGetCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_sid_to_username'
    SYNOPSIS = 'Get AD username from SID'

    @staticmethod
    def options(parser):
        parser.add_argument(
            '-s',
            '--sid',
            help='Get the AD username that corresponds to this SID',
            required=True,
        )

    @staticmethod
    def main(conninfo, credentials, args):
        print(ad.sid_to_username_get(conninfo, credentials, args.sid))


class SidToGidGetCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_sid_to_gid'
    SYNOPSIS = 'Get GID from SID'

    @staticmethod
    def options(parser):
        parser.add_argument(
            '-s',
            '--sid',
            help='Get the GID that corresponds to this SID',
            required=True,
        )

    @staticmethod
    def main(conninfo, credentials, args):
        print(ad.sid_to_gid_get(conninfo, credentials, args.sid))


class SidToAccountCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_sid_to_account'
    SYNOPSIS = 'Get all account info for a SID'

    @staticmethod
    def options(parser):
        parser.add_argument(
            '-s',
            '--sid',
            help='Get the GID that corresponds to this SID',
            required=True,
        )

    @staticmethod
    def main(conninfo, credentials, args):
        print(ad.sid_to_ad_account(conninfo, credentials, args.sid))


class DNToAccountCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_distinguished_name_to_account'
    SYNOPSIS = 'Get all account info for a distinguished name'

    @staticmethod
    def options(parser):
        parser.add_argument(
            '-d',
            '--distinguished-name',
            help='Get the account with this DN (e.g. CN=user,DC=example,DC=com',
            required=True,
        )

    @staticmethod
    def main(conninfo, credentials, args):
        print(
            ad.distinguished_name_to_ad_account(
                conninfo, credentials, args.distinguished_name
            )
        )


class GidToSidGetCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_gid_to_sids'
    SYNOPSIS = 'Get SIDs from GID'

    @staticmethod
    def options(parser):
        parser.add_argument(
            '-g',
            '--gid',
            help='Get the SIDs that corresponds to this GID',
            required=True,
        )

    @staticmethod
    def main(conninfo, credentials, args):
        print(ad.gid_to_sid_get(conninfo, credentials, args.gid))


class SidToExpandedGroupSidsGetCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_expand_groups'
    SYNOPSIS = (
        'Get the SIDs of all the groups that the given SID is a '
        'member of (including nested groups).'
    )

    @staticmethod
    def options(parser):
        parser.add_argument(
            '-s',
            '--sid',
            help='Get the SIDS of all the groups this SID belongs '
            '(including all nested groups).',
            required=True,
        )

    @staticmethod
    def main(conninfo, credentials, args):
        print(ad.sid_to_expanded_group_sids_get(conninfo, credentials, args.sid))


class ClearCacheCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ad_clear_cache'
    SYNOPSIS = (
        'Clear the AD ID mapping cache on the current node. '
        'This does not affect the rest of the cluster!'
    )

    @staticmethod
    def main(conninfo, credentials, _args):
        ad.clear_cache_post(conninfo, credentials)
