# Copyright (C) 2019 Majormode.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import collections
import json

from majormode.perseus.constant.obj import ObjectStatus
from majormode.perseus.constant.contact import ContactName
from majormode.perseus.model import obj
from majormode.perseus.model.contact import Contact
from majormode.perseus.model.locale import DEFAULT_LOCALE
from majormode.perseus.model.locale import Locale
from majormode.perseus.service.base_rdbms_service import BaseRdbmsService
from majormode.perseus.service.base_service import BaseService
from majormode.perseus.utils import cast


class ContactService(BaseRdbmsService):
    class ContactAlreadyUsedException(BaseService.BaseServiceException):
        """
        Signal that the specified contact information  is already associated
        with an another user account registered to the platform.
        """
        pass

    class UnverifiedContactException(BaseService.BaseServiceException):
        """
        Signal that the contact information provided by the user has not been
        verified yet and it CANNOT be used for the ongoing procedure.
        """
        pass

    # Define the minimal allowed duration of time expressed in seconds
    # between two consecutive requests to verify a same contact information.
    MINIMAL_TIME_BETWEEN_CONTACT_VERIFICATION_REQUEST = 60 * 5

    def is_contact_available(
            self,
            contact,
            account_id=None,
            connection=None):
        """
        Indicate whether the specified contact information is available and
        verified.

        In the case the contact information would have been already registered
        by a user, indicate whether this contact information has been verified.


        :param contact: An instance `Contact`.

        :param account_id: Identification of the account of the user on behalf
            whom this function is called.

        :param connection: An instance `RdbmsConnection` to be used
            supporting the Python clause `with ...:`.


        :return: A tuple containing the following values:

            * `is_available`: `True` if the specified contact information is not
              yet registered by any accounts, or if it has been registered by the
              account on behalf of whom this function is called; `False` otherwise.

            * `is_verified`: `True` if the specified contact information has been
               verified; `False` otherwise.
        """
        with self.acquire_rdbms_connection(connection=connection) as connection:
            cursor = connection.execute(
                """
                SELECT 
                    is_verified,
                    account_id
                  FROM 
                    account_contact
                  WHERE 
                    name = %(name)s
                    AND value = %(value)s
                    AND object_status = %(OBJECT_STATUS_ENABLED)s
                """,
                {
                    'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
                    'name': contact.name,
                    'value': contact.value
                })
            row = cursor.fetch_one()

            # Check whether this contact information is associated to any accounts.
            if row is None:
                return True, False

            # Retrieve the verification status of this contact information and the
            # account identification of the user who has registered it .
            contact = row.get_object({'account_id': cast.string_to_uuid})

            # If `account_id` has been passed to this function, check whether this
            # user has registered this contact information, in which case this
            # contact information is declared available even if already verified.
            return False if account_id is None else account_id == contact.account_id, contact.is_verified

    def request_contact_verification(
            self,
            contact,
            account_id=None,
            connection=None,
            context=None,
            locale=DEFAULT_LOCALE):
        """
        Request the initiation of the process to verify the specified contact
        information.

        A background task running on the server platform is responsible for
        sending the verification request to the contact address the user has
        provided.  This message contains more likely a HTML link that will
        redirect the user to a web page responsible for confirming this
        contact information (cf. function `confirm_contact`).


        :note: The function ignores any consecutive call for a same contact
            information within a minimal duration of time, to avoid spamming
            the user.

        :note: If a verification request was already generated on behalf of
            another user, the function will silently disable the association
            between this request and this particular user account.  The client
            application MUST request the user who will confirm this contact
            information will have to authenticate in order to add this contact
            information to his account.


        :warning: The function DOESN'T return the identification of the
            verification request so that this identification CANNOT be passed
            to the client application.  Indeed!


        :param contact: An instance `Contact`.

        :param account_id: Identification of the account of the user who
            requests to get his contact information verified.  This argument
            can be `None` when this contact information needs to be verified
            prior to the user account to be created.

        :param connection: A `RdbmsConnection` instance to be used  supporting
            the Python clause `with ...:`.

        :param context: A JSON expression corresponding to the context in
            this contact information has been added and needs to be verified.

        :param locale: A `Locale` instance referencing the preferred language
            of the user that will be used to generate a message to be sent to
            this user.


        :raise IllegalAccessException: If a verification of this contact
            information has been already requested for another account.
        """
        with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
            # Check whether a verification request for this contact information is
            # ongoing.
            cursor = connection.execute(
                """
                SELECT 
                    request_id,
                    account_id,
                    EXTRACT(EPOCH FROM current_timestamp - update_time) AS elapsed_time
                  FROM 
                    account_contact_verification
                  WHERE
                    name = %(name)s
                    AND value = %(value)s
                """,
                {
                    'name': contact.name,
                    'value': contact.value
                })

            row = cursor.fetch_one()
            request = row and row.get_object({
                'account_id': cast.string_to_uuid,
                'request_id': cast.string_to_uuid
            })

            # Generate a verification request for this contact information if none
            # has been generated so far.
            if request is None:
                connection.execute(
                    """
                    INSERT INTO 
                        account_contact_verification(
                            account_id,
                            locale,
                            name,
                            value,
                            context)
                      VALUES 
                        (%(account_id)s,
                         %(locale)s,
                         %(name)s,
                         %(value)s,
                         %(context)s)
                    """,
                    {
                        'account_id': account_id,
                        'context': json.dumps(obj.stringify(context, trimmable=True)),
                        'locale': locale,
                        'name': contact.name,
                        'value': contact.value
                    })

            else:
                # If a verification request was already generated on behalf of another
                # user, we disable the association between this request and a
                # particular user account.  The user who will confirm this contact
                # information will have to authenticate to add this contact information
                # to his account.
                if request.account_id and account_id and request.account_id != account_id:
                    connection.execute(
                        """
                        UPDATE 
                            account_contact_verification
                          SET
                            account_id = NULL,
                            update_time = current_timestamp
                          WHERE
                            request_id = %(request_id)s
                        """,
                        {
                            'request_id': request.request_id
                        })

                # Ignore successive calls for sending a new message to the user that
                # would be requested with a minimal duration of time, to avoid
                # spamming the user.
                if request.elapsed_time > self.MINIMAL_TIME_BETWEEN_CONTACT_VERIFICATION_REQUEST:
                    connection.execute(
                        """
                        UPDATE 
                            account_contact_verification
                          SET
                            request_count = request_count + 1,
                            update_time = current_timestamp
                          WHERE
                            request_id = %(request_id)s
                          """,
                        {
                            'request_id': request.request_id
                        })




















    def __cleanse_contact_references(self, connection, account_id, contact):
        """
        Remove the specified contact information from any other user account
        but the one passed to this function.  Cancel any verification request
        of this contact information that would be still ongoing.


        :param connection: a `RdbmsConnection` instance to be used
            supporting the Python clause `with ...:`.

        :param account_id: identification of the account of the user who has
            confirmed the given contact information.

        :param contact: an instance `Contact` of the contact information that
            the user has confirmed, and which references to it need to be
            removed from any other user account and ongoing verification
            request.
        """
        with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:

            # Remove this contact information from any other user account.
            cursor = connection.execute("""
                DELETE FROM 
                    account_contact
                  WHERE
                    name = %(name)s
                    AND value = %(value)s
                    AND account_id <> %(account_id)s
                  RETURNING
                    account_id""",
                { 'account_id': account_id,
                  'name': contact.name,
                  'value': contact.value})

            account_ids = [ row.get_value('account_id', cast.string_to_uuid) for row in cursor.fetch_all()]

            # Soft-delete accounts that this contact information has been removed
            # from and that have no contact information anymore.
            if account_ids:
                connection.execute(
                    """
                    UPDATE
                        account
                      SET 
                        object_status = %(OBJECT_STATUS_DISABLED)s
                      WHERE
                        account_id IN (%[account_ids]s)
                        AND NOT EXISTS(
                          SELECT
                              true
                            FROM
                              account_contact
                            WHERE
                             account_contact.account_id = account.account_id)
                    """,
                    { 'OBJECT_STATUS_DISABLED': ObjectStatus.disabled,
                      'account_ids': account_ids })

            # Delete any other verification request of this contact information.
            connection.execute("""
                DELETE FROM account_contact_verification
                  WHERE name = %(name)s
                    AND value = %(value)s""",
                { 'name': contact.name,
                  'value': contact.value })


    def __enable_account_contact(self, connection, account_id, contact):
        """
        Enable the contact information of the specified user.


        :param connection: a `RdbmsConnection` instance to be used
            supporting the Python clause `with ...:`.

        :param account_id: identification of the account of a user.

        :param contact: an instance `Contact` of the contact information of
            the user to be enabled.
        """
        account = self.get_account(contact.account_id, check_status=True)

        with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
            cursor = connection.execute(
                """
                UPDATE 
                    account_contact
                  SET 
                    is_verified = true,
                    update_time = current_timestamp
                  WHERE
                    account_id = %(account_id)s
                    AND name = %(name)s
                    AND value = %(value)s
                  RETURNING
                    is_primary
                  """,
                {
                    'account_id': account_id,
                    'name': contact.name,
                    'value': contact.value
                })

            is_primary = cursor.fetch_one().get_value('is_primary')

            # Enable the account of the user if it was pending.
            if account.object_status == ObjectStatus.pending and enable_account:
                connection.execute(
                    """
                    UPDATE 
                        account
                      SET   
                        object_status = %(OBJECT_STATUS_ENABLED)s
                      WHERE
                        account_id = %(account_id)s
                    """,
                    {
                        'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
                        'account_id': account_id
                    })

            # Set this contact information as primary if the user doesn't have any
            # primary contact information.
            if not is_primary:
                cursor = connection.execute(
                    """
                    SELECT EXISTS(
                      SELECT
                          true
                        FROM
                          account_contact
                        WHERE
                          account_id = %(account_id)s
                          AND name = %(name)s
                          AND is_primary)
                    """,
                    {
                        'account_id': account_id,
                        'name': contact.name
                    })

                if cursor.get_row_count() == 0:
                    self.set_primary_contact(account_id, contact, connection=connection)

    @staticmethod
    def __group_contacts_by_name(contacts):
        """
        Return a dictionary of contacts group by their name.


        :param contacts: a list of instances `Contact`.


        :return: a dictionary where the key corresponds to an item of
            `ContactName` and the value a list of contacts that correspond
            to this contact name.


        :raise AssertError: if a contact information is duplicated.
        """
        contacts_by_name = collections.defaultdict(list)

        for contact in contacts:
            assert contact.value not in [_contact.value for _contact in contacts_by_name[contact.name]], \
                'Duplicated contact information'
            contacts_by_name[contact.name].append(contact)

        return contacts_by_name

    @classmethod
    def __subtract_contacts(cls, from_contacts, with_contacts):
        """
        Return a new list of contacts in the first list that are not in the
        second list.


        :note: the function also automatically sets the attribute `is_primary`
            of contact instances to `False` when a contact of the same name is
            in the second list and its attribute `is_primary` is `True`.


        :param from_contacts: a list of contacts to subtract contacts that are
            in the second list.

        :param with_contacts: a list of contacts to be removed from the first
            list of contacts.


        :return: a list with contacts in the first list that are not in the
            second list.
        """
        contact_set1 = cls.__group_contacts_by_name(from_contacts)
        contact_set2 = cls.__group_contacts_by_name(with_contacts)

        contacts = []

        for contact_name in contact_set1:
            # Check whether a contact of this name has been already set as primary
            # in the second list of contacts.  If so, every contact of this name in
            # the first list must be set as not primary.
            is_primary_contact_already_defined = any([_contact.is_primary for _contact in contact_set2[contact_name]])

            # Retrieve the list of contacts from the first list that don't exist in
            # the second list.
            contacts.extend([
                Contact(
                    contact.name,
                    contact.value,
                    not is_primary_contact_already_defined and contact.is_primary,
                    contact.is_verified)
                for contact in contact_set1[contact_name]
                if not any([
                    True
                    for _contact in contact_set2[contact_name]
                    if contact.value == _contact.value
                ])
            ])

        return contacts

    def add_contact(
            self,
            account_id,
            contact,
            connection=None,
            context=None,
            has_been_verified=False,
            locale=DEFAULT_LOCALE,
            to_be_verified=False):
        """
        Add a given contact information to the specified user account as long
        as this contact information has not been verified by another user.

        If this contact information has been verified, the function will
        silently disable this contact information from account of any user who
        would have added it to their account, and cancel any request that
        would have been generated to verify this contact information.


        :param account_id: identification of the account of the user who adds
            his contact information.

        :param contact: An object `Contact`.

        :param connection: An object `RdbmsConnection`.

        :param context: a JSON expression corresponding to the context
            in which this contact has been added and need to be verified.
            This parameter is only used if the parameter `to_be_verified` is
            set to `True`.

        :param has_been_verified: indicate whether this contact information
            has been verified through a challenge/response process.  This
            parameter is intended to be set by the function `confirm_contact`
            only.

        :param locale: indicate the preferred language of the user to write
            the email verification request in.

        :param to_be_verified: indicate whether the platform needs to send a
            request to the user to verify his contact information.  This
            argument cannot be set to `True` if the argument `has_been_verified`
            has been set to `True`.


        :raise ContactAlreadyUsedException: if one of the contacts has been
            already registered and verified by another user.

        :raise InvalidArgumentException: if this contact information is stated
            as verified while no challenge process has been passed.
        """
        from majormode.perseus.service.account.account_service import AccountService

        assert not (has_been_verified and to_be_verified), 'Conflicted values'

        # Check whether this contact has been already added to this account.
        account = AccountService().get_account(
            account_id,
            check_status=True,
            connection=connection,
            include_contacts=True)

        if contact in account.contacts:
            return

        # Check whether this contact would been added to another user account
        # and wether it would have been verified.
        (is_available, is_verified) = self.is_contact_available(contact)
        if not is_available and is_verified:
            raise self.ContactAlreadyUsedException('Another user has already verified this contact information')

        # Check whether this contact information can been stated verified.
        if contact.is_verified and not has_been_verified and account.account_type not in [
                AccountService.AccountType.botnet,
                AccountService.AccountType.sns,
                AccountService.AccountType.test
            ]:
            raise self.InvalidArgumentException('A contact cannot be stated as verified without passing a challenge process')

        # Add this contact information to the specified user account, and
        # generate a verification request if required.
        with self.acquire_rdbms_connection( auto_commit=True, connection=connection) as connection:

            # If verified, disable this contact information from any other user
            # account, and cancel any request that would have been generated to
            # verify this contact information.
            if contact.is_verified:
                connection.execute(
                    """
                    UPDATE
                        account_contact
                      SET
                        object_status = %(OBJECT_STATUS_DISABLED)s
                      WHERE
                        name = %(name)s
                        AND value = %(value)s
                        """,
                    {
                        'OBJECT_STATUS_DISABLED': ObjectStatus.disabled,
                        'name': contact.name,
                        'value': contact.value
                    })

                connection.execute(
                    """
                    DELETE FROM 
                        account_contact_verification
                      WHERE
                        name = %(name)s
                        AND value = %(value)s""",
                    {
                        'name': contact.name,
                        'value': contact.value
                    })

            # Set this contact information as the primary if it has been verified
            # and it his user doesn't have any other contact information than this
            # one.
            if contact.is_verified and not contact.is_primary and not account.contacts:
                contact.is_primary = True

            # Add this contact information to the specified user account.
            connection.execute(
                """
                INSERT INTO
                    account_contact(
                        account_id,
                        name,
                        value,
                        is_primary,
                        is_verified)
                  VALUES 
                    (%(account_id)s,
                     %(name)s,
                     %(value)s,
                     %(is_primary)s,
                     %(is_verified)s)
                """,
                {
                    'account_id': account.account_id,
                    'is_primary': contact.is_primary or False,
                    'name': contact.name,
                    'value': contact.value,
                    'is_verified': contact.is_verified or False
                })

            # If this contact information needs to be verified, generate a
            # verification request that will be sent to the user.
            if to_be_verified and account.account_type == AccountService.AccountType.standard:
                self.request_contact_verification(
                    contact,
                    account_id=account_id,
                    connection=connection,
                    context=context,
                    locale=locale)

    def confirm_contact(
            self,
            app_id,
            request_id,
            auto_sign_in=False,
            connection=None,
            enable_account=True,
            fullname=None,
            locale=None,
            password=None,
            username=None):
        """
        Enable a contact information that a user has confirmed through a
        challenge/response verification process.

        If the user doesn't have any account, the function will automatically
        create an account for him and associate this contact information to
        his account.

        The function silently deletes any other verification requests that
        would have been initiated by other users for this same contact
        information.  The function also automatically soft-deletes any user
        account that would be only linked to this contact information.

        If the user doesn't have any primary contact information defined of
        this type, the function will automatically set this contact
        information as the primary.


        :warning: this function MUST NOT be directly surfaced to any client
            application, but SHOULD be used by the server controller of a
            client application.


        :param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param request_id: identification of the verification request that has
            been sent to the user.

        :param auto_signin: indicate whether the platform is requested to
            sign-in this user once the sign-up procedure completes
            successfully.

        :param enable_account: indicate whether to enable the user account if
            its status was of pending.

        :param fullname: complete full name of the user as given by the user
            himself.  This argument is only used if this contact information
            was not associated to an existing user account.

        :param locale: an instance `Locale` corresponding to the preferred
            language of the user.  This argument is only used if this contact
            information was not associated to an existing user account.

        :param password: password given by the user to allow him later to
            sign-in with his account.  This argument is required if this
            contact information was not associated to an existing user account.

        :param username: screen name or nickname of the user.  A username
            should be totally made-up pseudonym, not reveal the real name of
            the person.  The username is unique across the platform.  A
            username is not case sensitive.  This argument is only used if
            this contact information was not associated to an existing user
            account.


        :return: the function returns an instance `contact` or a tuple of
            instances `contact, session` depending on whether the parameter
            `auto_sign_in` has been set to, respectively `False`, or
            `True`:

             * `contact`: an instance containing the following the members:

                * `account_id` (required): identification of the account of the user
                  who has confirmed this contact information.

                * `locale` (optional): an instance `Locale` representing the
                  preferred language that this user has selected when he has added
                  this contact information to his account, or, if not defined at this
                  time, when he has confirmed this contact information or, if still
                  not defined at this time, the default locale.

                * `name` (required): item of the enumeration `ContactName`.

                * `value`: value of this contact information.

            * `session`: an instance containing the following members;

                * `creation_time` (optional): time when this account has been
                  registered.  This information should be stored by the client
                  application to manage its cache of accounts.

                * `expiration_time` (optional): time when the login session will
                  expire.  This information is provided if the client application
                  requires the platform to automatically sign-in the user (cf.
                  parameter `auto_sigin`).

                * `object_status` (optional): current status of this user account.

                * `session_id` (optional): identification of the login session of
                  the user.  This information is provided if the client application
                  requires the platform to automatically sign-in the user (cf.
                  parameter `auto_sign_in`).


        :raise DeletedObjectException: if the user account has been deleted
            while the argument `check_status` has been set to `True`.

        :raise DisabledObjectException: if the user account has been disabled
            while the argument `check_status` has been set to `True`.

        :raise UndefinedObjectException: if the specified identification
            doesn't refer to a user account registered against the platform.
        """
        with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:

            # Retrieve the attributes of the specified contact verification request.
            cursor = connection.execute(
                """
                DELETE FROM
                    account_contact_verification
                  WHERE
                    request_id = %(request_id)s
                  RETURNING
                    account_id,
                    locale,
                    name, 
                    value
                """,
                {
                    'request_id': request_id
                })
            row = cursor.fetch_one()

            request = row and row.get_object({
                'account_id': cast.string_to_uuid,
                'locale': Locale,
                'name': ContactName
            })

            if request is None:
                raise self.UndefinedObjectException()

            contact = Contact(request.name, request.value, is_verified=True)

            # Remove reference to this contact information from any other user
            # account.  Cancel any verification request of this contact
            # information.
            self.__cleanse_contact_references(connection, request.account_id, contact)

            # If this request was linked to a particular user account, enable his
            # contact information.
            if request.account_id:
                self.__enable_account_contact(connection, request.account_id, contact)
                return contact

            # Otherwise create an account for this user providing this contact
            # information.
            else:
                from majormode.perseus.service.account.account_service import AccountService

                session = AccountService().sign_up(
                    app_id=app_id,
                    connection=connection,
                    contact=contact,
                    has_been_verified=True,
                    username=username,
                    password=password,
                    fullname=fullname,
                    locale=request.locale or locale or DEFAULT_LOCALE,
                    auto_sign_in=auto_sign_in,
                    enable_account=enable_account)

                return contact, session

    def get_contact_verification_request(self, contact):
        """
        Return the request send to a user to verify his contact information.


        :note: this function MUST not be surfaced to client applications.


        :param contact: an instance `Contact`.


        :return: an instance containing the following members:

            * `account_id` (optional): identification of the account of the user
              who requested to verify his contact information, if he was logged in
              when he provided his contact information.

            * `elapsed_time` (required): elapsed time in second between since
              this contact verification request has been generated.

            * `request_id` (required): identification of the contact verification
              request.
        """
        with self.acquire_rdbms_connection(auto_commit=False) as connection:
            cursor = connection.execute(
                """
                SELECT 
                    request_id,
                    account_id,
                    EXTRACT(EPOCH FROM current_timestamp - update_time) AS elapsed_time
                  FROM
                    account_contact_verification
                  WHERE
                    name = %(name)s
                    AND value = %(value)s
                """,
                {
                    'name': contact.name,
                    'value': contact.value
                })
            row = cursor.fetch_one()

            if row is None:
                raise self.UndefinedObjectException('No verification request corresponds to the specified contact')

            return row.get_object({
                'account_id': cast.string_to_uuid,
                'request_id': cast.string_to_uuid
            })

    def get_contacts(self, account_id,
            connection=None):
        """
        Fetch the list of contact information that have been added to the
        specified user account.


        :param account_id: identification of a user account.

        :param connection: a `RdbmsConnection` instance to be used
            supporting the Python clause `with ...:`.


        :return: a list of instances `Contact`.
        """
        with self.acquire_rdbms_connection(connection=connection) as connection:
            cursor = connection.execute(
                """
                SELECT 
                    name,
                    value,
                    is_primary,
                    is_verified
                  FROM
                    account_contact
                  WHERE
                    account_id = %(account_id)s
                    AND object_status = %(OBJECT_STATUS_ENABLED)s
                """,
                {
                    'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
                    'account_id': account_id
                })

            return [Contact.from_object(row.get_object()) for row in cursor.fetch_all()]

    def is_contact_verification_request(
            self,
            name,
            request_id,
            connection=None):
        """
        Indicate whether the specified contact verification request exists.


        :param name: an instance `ContactName` of the contact that is
            requested to be verified.

        :param request_id: identification of the contact verification request.

        :param connection: a `RdbmsConnection` instance to be used
            supporting the Python clause `with ...:`.


        :return: `True` if the specified identification corresponds to a
            contact verification request registered to the platform;
            `False` otherwise.
        """
        with self.acquire_rdbms_connection(connection=connection) as connection:
            cursor = connection.execute(
                """
                SELECT 
                    true
                  FROM
                    account_contact_verification
                  WHERE
                    request_id = %(request_id)s
                    AND name = %(name)s
                """,
                {
                    'name': name,
                    'request_id': request_id
                })

            return cursor.get_row_count() > 0

    def set_primary_contact(self, account_id, contact,
            connection=None):
        """
        Set the specified contact information as the primary for the given
        user account.  This contact information MUST have been verified.  All
        the other contact information of the same type are set as alternates.


        :param account_id: identification of the account of a user.

        :param contact: an instance `Contact` of the contact information of
            the user to set as primary.

        :param connection: a `RdbmsConnection` instance to be used
            supporting the Python clause `with ...:`.


        :raise InvalidOperationException: if this contact information has not
            been verified yet.

        :raise UndefinedObjectException: if this contact information has not
            been associated to this user account.
        """

        # Retrieve the contact information of this user account.
        contacts = self.get_contacts(account_id, connection=connection)

        # Check whether this contact information is defined for this user
        # account.
        try:
            _contact = [ _contact for _contact in contacts if _contact == contact ][0]
        except IndexError:
            raise self.UndefinedObjectException('This contact information is not associated to this user account')

        # Ignore this request if this contact information is already set as the
        # primary contact for this user.
        if _contact.is_primary:
            return

        # Check whether this contact information has been verified, as this is
        # required to set a contact as the primary.
        if not _contact.is_verified:
            raise self.InvalidOperationException('A contact information that is not verified cannot be set as the primary')

        # Update all the contact information of this type for this user account,
        # setting this particular contact information as the primary, and the
        # other as alternates (if they are not already alternates).
        with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
            connection.execute(
                """
                UPDATE 
                    account_contact
                  SET
                    is_primary = (value = %(value)s),
                    update_time = current_timestamp
                  WHERE
                     account_id = %(account_id)s
                    AND name = %(name)s
                    AND is_primary <> (value = %(value)s)
                    AND object_status NOT IN (%(OBJECT_STATUS_DELETED)s, %(OBJECT_STATUS_DISABLED)s)
                """,
                {
                    'OBJECT_STATUS_DELETED': ObjectStatus.deleted,
                    'OBJECT_STATUS_DISABLED': ObjectStatus.disabled,
                    'account_id': account_id,
                    'name': contact.name,
                    'value': contact.value
                })


    # def update_contacts(self, app_id, account_id, contacts):
    #     """
    #
    #
    #     :param app_id: identification of the client application such as a Web,
    #         a desktop, or a mobile application, that accesses the service.
    #
    #     :param account_id: identification of the account of the user whose
    #         contact information is updated.
    #
    #     :param contacts: a list of contact information of the user's account.
    #         A contact information corresponds to the possible following tuples::
    #
    #                `(name, value)`
    #
    #         or::
    #
    #                `(name, value, is_primary)`
    #
    #         or::
    #
    #                `(name, value, is_primary, is_verified)`
    #
    #         where:
    #
    #         * `name`: an item of the enumeration `ContactName`.
    #
    #         * `value`: value of the property representing by a string.
    #
    #         * `is_primary`: indicate whether this contact information is the
    #           primary.  By default, the first contact information of a given
    #           type is the primary.
    #
    #         * `is_verified`: indicate whether this contact information has
    #           been verified, more likely grabbed from a trusted Social
    #           Networking Service (SNS).  This parameter MUST NOT be surfaced
    #           by any public API.
    #
    #         A contact information is optional if a username is provided, or if
    #         the account is a mapping to a 3rd party Social Network Service
    #         (SNS) account.
    #     :return:
    #     """
    #     account = self.get_account(account_id, check_status=True, include_contacts=True)
    #
    #     contacts = contact.format_contacts(contacts)
    #
    #     with self.acquire_rdbms_connection(auto_commit=True) as connection:
    #         connection.execute("""
    #             DELETE FROM account_contact
    #               WHERE account_id = %(account_id)s
    #                 AND property_name IN (%[property_names]s)""",
    #             { 'account_id': account_id,
    #               'property_names': set([ name for (name, _, _, _) in contacts ]) })
    #
    #         for (name, value, is_primary, is_verified) in contacts:
    #             (is_available, is_existing_contact_verified) = self.is_contact_available(app_id, (name, value),
    #                     account_id=account_id)
    #
    #             if not is_available:  # and is_existing_contact_verified:
    #                 raise self.ContactAlreadyUsedException('This contact information is already associated with a user account',
    #                         payload={ 'contact': (name, value) })
    #
    #         if is_verified and account.account_type not in [
    #                 AccountService.AccountType.botnet,
    #                 AccountService.AccountType.sns,
    #                 AccountService.AccountType.test]:
    #             raise self.InvalidArgumentException('Contact of account other than botnet, SNS, and test cannot be stated as verified')
    #
    #         connection.execute("""
    #             INSERT INTO account_contact(
    #                     account_id,
    #                     property_name,
    #                     property_value,
    #                     is_primary,
    #                     is_verified,
    #                     app_id)
    #               VALUES %[values]s""",
    #             {'values': [ (account_id, name, value, is_primary, is_verified, app_id)
    #                     for (name, value, is_primary, is_verified,) in contacts ] })
