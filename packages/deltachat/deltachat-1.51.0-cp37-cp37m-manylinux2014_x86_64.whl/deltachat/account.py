""" Account class implementation. """

from __future__ import print_function
from contextlib import contextmanager
from email.utils import parseaddr
from threading import Event
import os
from array import array
from . import const
from .capi import ffi, lib
from .cutil import as_dc_charpointer, from_dc_charpointer, iter_array, DCLot
from .chat import Chat
from .message import Message
from .contact import Contact
from .tracker import ImexTracker, ConfigureTracker
from . import hookspec
from .events import EventThread


class MissingCredentials(ValueError):
    """ Account is missing `addr` and `mail_pw` config values. """


class Account(object):
    """ Each account is tied to a sqlite database file which is fully managed
    by the underlying deltachat core library.  All public Account methods are
    meant to be memory-safe and return memory-safe objects.
    """
    MissingCredentials = MissingCredentials

    def __init__(self, db_path, os_name=None, logging=True):
        """ initialize account object.

        :param db_path: a path to the account database. The database
                        will be created if it doesn't exist.
        :param os_name: this will be put to the X-Mailer header in outgoing messages
        """
        # initialize per-account plugin system
        self._pm = hookspec.PerAccount._make_plugin_manager()
        self._logging = logging

        self.add_account_plugin(self)

        self.db_path = db_path
        if hasattr(db_path, "encode"):
            db_path = db_path.encode("utf8")

        self._dc_context = ffi.gc(
            lib.dc_context_new(as_dc_charpointer(os_name), db_path, ffi.NULL),
            lib.dc_context_unref,
        )
        if self._dc_context == ffi.NULL:
            raise ValueError("Could not dc_context_new: {} {}".format(os_name, db_path))

        self._shutdown_event = Event()
        self._event_thread = EventThread(self)
        self._configkeys = self.get_config("sys.config_keys").split()
        hook = hookspec.Global._get_plugin_manager().hook
        hook.dc_account_init(account=self)

    def disable_logging(self):
        """ disable logging. """
        self._logging = False

    def enable_logging(self):
        """ re-enable logging. """
        self._logging = True

    # def __del__(self):
    #    self.shutdown()

    def log(self, msg):
        if self._logging:
            self._pm.hook.ac_log_line(message=msg)

    def _check_config_key(self, name):
        if name not in self._configkeys:
            raise KeyError("{!r} not a valid config key, existing keys: {!r}".format(
                           name, self._configkeys))

    def get_info(self):
        """ return dictionary of built config parameters. """
        lines = from_dc_charpointer(lib.dc_get_info(self._dc_context))
        d = {}
        for line in lines.split("\n"):
            if not line.strip():
                continue
            key, value = line.split("=", 1)
            d[key.lower()] = value
        return d

    def set_stock_translation(self, id, string):
        """ set stock translation string.

        :param id: id of stock string (const.DC_STR_*)
        :param value: string to set as new transalation
        :returns: None
        """
        string = string.encode("utf8")
        res = lib.dc_set_stock_translation(self._dc_context, id, string)
        if res == 0:
            raise ValueError("could not set translation string")

    def set_config(self, name, value):
        """ set configuration values.

        :param name: config key name (unicode)
        :param value: value to set (unicode)
        :returns: None
        """
        self._check_config_key(name)
        name = name.encode("utf8")
        if name == b"addr" and self.is_configured():
            raise ValueError("can not change 'addr' after account is configured.")
        if value is not None:
            value = value.encode("utf8")
        else:
            value = ffi.NULL
        lib.dc_set_config(self._dc_context, name, value)

    def get_config(self, name):
        """ return unicode string value.

        :param name: configuration key to lookup (eg "addr" or "mail_pw")
        :returns: unicode value
        :raises: KeyError if no config value was found.
        """
        if name != "sys.config_keys":
            self._check_config_key(name)
        name = name.encode("utf8")
        res = lib.dc_get_config(self._dc_context, name)
        assert res != ffi.NULL, "config value not found for: {!r}".format(name)
        return from_dc_charpointer(res)

    def _preconfigure_keypair(self, addr, public, secret):
        """See dc_preconfigure_keypair() in deltachat.h.

        In other words, you don't need this.
        """
        res = lib.dc_preconfigure_keypair(self._dc_context,
                                          as_dc_charpointer(addr),
                                          as_dc_charpointer(public),
                                          as_dc_charpointer(secret))
        if res == 0:
            raise Exception("Failed to set key")

    def update_config(self, kwargs):
        """ update config values.

        :param kwargs: name=value config settings for this account.
                       values need to be unicode.
        :returns: None
        """
        for key, value in kwargs.items():
            self.set_config(key, str(value))

    def is_configured(self):
        """ determine if the account is configured already; an initial connection
        to SMTP/IMAP has been verified.

        :returns: True if account is configured.
        """
        return True if lib.dc_is_configured(self._dc_context) else False

    def set_avatar(self, img_path):
        """Set self avatar.

        :raises ValueError: if profile image could not be set
        :returns: None
        """
        if img_path is None:
            self.set_config("selfavatar", None)
        else:
            assert os.path.exists(img_path), img_path
            self.set_config("selfavatar", img_path)

    def check_is_configured(self):
        """ Raise ValueError if this account is not configured. """
        if not self.is_configured():
            raise ValueError("need to configure first")

    def get_latest_backupfile(self, backupdir):
        """ return the latest backup file in a given directory.
        """
        res = lib.dc_imex_has_backup(self._dc_context, as_dc_charpointer(backupdir))
        if res == ffi.NULL:
            return None
        return from_dc_charpointer(res)

    def get_blobdir(self):
        """ return the directory for files.

        All sent files are copied to this directory if necessary.
        Place files there directly to avoid copying.
        """
        return from_dc_charpointer(lib.dc_get_blobdir(self._dc_context))

    def get_self_contact(self):
        """ return this account's identity as a :class:`deltachat.contact.Contact`.

        :returns: :class:`deltachat.contact.Contact`
        """
        return Contact(self, const.DC_CONTACT_ID_SELF)

    def create_contact(self, obj, name=None):
        """ create a (new) Contact or return an existing one.

        Calling this method will always result in the same
        underlying contact id.  If there already is a Contact
        with that e-mail address, it is unblocked and its display
        `name` is updated if specified.

        :param obj: email-address, Account or Contact instance.
        :param name: (optional) display name for this contact
        :returns: :class:`deltachat.contact.Contact` instance.
        """
        (name, addr) = self.get_contact_addr_and_name(obj, name)
        name = as_dc_charpointer(name)
        addr = as_dc_charpointer(addr)
        contact_id = lib.dc_create_contact(self._dc_context, name, addr)
        return Contact(self, contact_id)

    def get_contact(self, obj):
        if isinstance(obj, Contact):
            return obj
        (_, addr) = self.get_contact_addr_and_name(obj)
        return self.get_contact_by_addr(addr)

    def get_contact_addr_and_name(self, obj, name=None):
        if isinstance(obj, Account):
            if not obj.is_configured():
                raise ValueError("can only add addresses from configured accounts")
            addr, displayname = obj.get_config("addr"), obj.get_config("displayname")
        elif isinstance(obj, Contact):
            if obj.account != self:
                raise ValueError("account mismatch {}".format(obj))
            addr, displayname = obj.addr, obj.name
        elif isinstance(obj, str):
            displayname, addr = parseaddr(obj)
        else:
            raise TypeError("don't know how to create chat for %r" % (obj, ))

        if name is None and displayname:
            name = displayname
        return (name, addr)

    def delete_contact(self, contact):
        """ delete a Contact.

        :param contact: contact object obtained
        :returns: True if deletion succeeded (contact was deleted)
        """
        contact_id = contact.id
        assert contact.account == self
        assert contact_id > const.DC_CHAT_ID_LAST_SPECIAL
        return bool(lib.dc_delete_contact(self._dc_context, contact_id))

    def get_contact_by_addr(self, email):
        """ get a contact for the email address or None if it's blocked or doesn't exist. """
        _, addr = parseaddr(email)
        addr = as_dc_charpointer(addr)
        contact_id = lib.dc_lookup_contact_id_by_addr(self._dc_context, addr)
        if contact_id:
            return self.get_contact_by_id(contact_id)

    def get_contact_by_id(self, contact_id):
        """ return Contact instance or None.
        :param contact_id: integer id of this contact.
        :returns: None or :class:`deltachat.contact.Contact` instance.
        """
        return Contact(self, contact_id)

    def get_blocked_contacts(self):
        """ return a list of all blocked contacts.

        :returns: list of :class:`deltachat.contact.Contact` objects.
        """
        dc_array = ffi.gc(
            lib.dc_get_blocked_contacts(self._dc_context),
            lib.dc_array_unref
        )
        return list(iter_array(dc_array, lambda x: Contact(self, x)))

    def get_contacts(self, query=None, with_self=False, only_verified=False):
        """ get a (filtered) list of contacts.

        :param query: if a string is specified, only return contacts
                      whose name or e-mail matches query.
        :param only_verified: if true only return verified contacts.
        :param with_self: if true the self-contact is also returned.
        :returns: list of :class:`deltachat.contact.Contact` objects.
        """
        flags = 0
        query = as_dc_charpointer(query)
        if only_verified:
            flags |= const.DC_GCL_VERIFIED_ONLY
        if with_self:
            flags |= const.DC_GCL_ADD_SELF
        dc_array = ffi.gc(
            lib.dc_get_contacts(self._dc_context, flags, query),
            lib.dc_array_unref
        )
        return list(iter_array(dc_array, lambda x: Contact(self, x)))

    def get_fresh_messages(self):
        """ yield all fresh messages from all chats. """
        dc_array = ffi.gc(
            lib.dc_get_fresh_msgs(self._dc_context),
            lib.dc_array_unref
        )
        yield from iter_array(dc_array, lambda x: Message.from_db(self, x))

    def create_chat(self, obj):
        """ Create a 1:1 chat with Account, Contact or e-mail address. """
        return self.create_contact(obj).create_chat()

    def _create_chat_by_message_id(self, msg_id):
        return Chat(self, lib.dc_create_chat_by_msg_id(self._dc_context, msg_id))

    def create_group_chat(self, name, contacts=None, verified=False):
        """ create a new group chat object.

        Chats are unpromoted until the first message is sent.

        :param contacts: list of contacts to add
        :param verified: if true only verified contacts can be added.
        :returns: a :class:`deltachat.chat.Chat` object.
        """
        bytes_name = name.encode("utf8")
        chat_id = lib.dc_create_group_chat(self._dc_context, int(verified), bytes_name)
        chat = Chat(self, chat_id)
        if contacts is not None:
            for contact in contacts:
                chat.add_contact(contact)
        return chat

    def get_chats(self):
        """ return list of chats.

        :returns: a list of :class:`deltachat.chat.Chat` objects.
        """
        dc_chatlist = ffi.gc(
            lib.dc_get_chatlist(self._dc_context, 0, ffi.NULL, 0),
            lib.dc_chatlist_unref
        )

        assert dc_chatlist != ffi.NULL
        chatlist = []
        for i in range(0, lib.dc_chatlist_get_cnt(dc_chatlist)):
            chat_id = lib.dc_chatlist_get_chat_id(dc_chatlist, i)
            chatlist.append(Chat(self, chat_id))
        return chatlist

    def get_deaddrop_chat(self):
        return Chat(self, const.DC_CHAT_ID_DEADDROP)

    def get_device_chat(self):
        return Contact(self, const.DC_CONTACT_ID_DEVICE).create_chat()

    def get_message_by_id(self, msg_id):
        """ return Message instance.
        :param msg_id: integer id of this message.
        :returns: :class:`deltachat.message.Message` instance.
        """
        return Message.from_db(self, msg_id)

    def get_chat_by_id(self, chat_id):
        """ return Chat instance.
        :param chat_id: integer id of this chat.
        :returns: :class:`deltachat.chat.Chat` instance.
        :raises: ValueError if chat does not exist.
        """
        res = lib.dc_get_chat(self._dc_context, chat_id)
        if res == ffi.NULL:
            raise ValueError("cannot get chat with id={}".format(chat_id))
        lib.dc_chat_unref(res)
        return Chat(self, chat_id)

    def mark_seen_messages(self, messages):
        """ mark the given set of messages as seen.

        :param messages: a list of message ids or Message instances.
        """
        arr = array("i")
        for msg in messages:
            msg = getattr(msg, "id", msg)
            arr.append(msg)
        msg_ids = ffi.cast("uint32_t*", ffi.from_buffer(arr))
        lib.dc_markseen_msgs(self._dc_context, msg_ids, len(messages))

    def forward_messages(self, messages, chat):
        """ Forward list of messages to a chat.

        :param messages: list of :class:`deltachat.message.Message` object.
        :param chat: :class:`deltachat.chat.Chat` object.
        :returns: None
        """
        msg_ids = [msg.id for msg in messages]
        lib.dc_forward_msgs(self._dc_context, msg_ids, len(msg_ids), chat.id)

    def delete_messages(self, messages):
        """ delete messages (local and remote).

        :param messages: list of :class:`deltachat.message.Message` object.
        :returns: None
        """
        msg_ids = [msg.id for msg in messages]
        lib.dc_delete_msgs(self._dc_context, msg_ids, len(msg_ids))

    def export_self_keys(self, path):
        """ export public and private keys to the specified directory.

        Note that the account does not have to be started.
        """
        return self._export(path, imex_cmd=const.DC_IMEX_EXPORT_SELF_KEYS)

    def export_all(self, path):
        """return new file containing a backup of all database state
        (chats, contacts, keys, media, ...). The file is created in the
        the `path` directory.

        Note that the account has to be stopped; call stop_io() if necessary.
        """
        export_files = self._export(path, const.DC_IMEX_EXPORT_BACKUP)
        if len(export_files) != 1:
            raise RuntimeError("found more than one new file")
        return export_files[0]

    def _export(self, path, imex_cmd):
        with self.temp_plugin(ImexTracker()) as imex_tracker:
            self.imex(path, imex_cmd)
            return imex_tracker.wait_finish()

    def import_self_keys(self, path):
        """ Import private keys found in the `path` directory.
        The last imported key is made the default keys unless its name
        contains the string legacy. Public keys are not imported.

        Note that the account does not have to be started.
        """
        self._import(path, imex_cmd=const.DC_IMEX_IMPORT_SELF_KEYS)

    def import_all(self, path):
        """import delta chat state from the specified backup `path` (a file).

        The account must be in unconfigured state for import to attempted.
        """
        assert not self.is_configured(), "cannot import into configured account"
        self._import(path, imex_cmd=const.DC_IMEX_IMPORT_BACKUP)

    def _import(self, path, imex_cmd):
        with self.temp_plugin(ImexTracker()) as imex_tracker:
            self.imex(path, imex_cmd)
            imex_tracker.wait_finish()

    def imex(self, path, imex_cmd):
        lib.dc_imex(self._dc_context, imex_cmd, as_dc_charpointer(path), ffi.NULL)

    def initiate_key_transfer(self):
        """return setup code after a Autocrypt setup message
        has been successfully sent to our own e-mail address ("self-sent message").
        If sending out was unsuccessful, a RuntimeError is raised.
        """
        self.check_is_configured()
        res = lib.dc_initiate_key_transfer(self._dc_context)
        if res == ffi.NULL:
            raise RuntimeError("could not send out autocrypt setup message")
        return from_dc_charpointer(res)

    def get_setup_contact_qr(self):
        """ get/create Setup-Contact QR Code as ascii-string.

        this string needs to be transferred to another DC account
        in a second channel (typically used by mobiles with QRcode-show + scan UX)
        where qr_setup_contact(qr) is called.
        """
        res = lib.dc_get_securejoin_qr(self._dc_context, 0)
        return from_dc_charpointer(res)

    def check_qr(self, qr):
        """ check qr code and return :class:`ScannedQRCode` instance representing the result"""
        res = ffi.gc(
            lib.dc_check_qr(self._dc_context, as_dc_charpointer(qr)),
            lib.dc_lot_unref
        )
        lot = DCLot(res)
        if lot.state() == const.DC_QR_ERROR:
            raise ValueError("invalid or unknown QR code: {}".format(lot.text1()))
        return ScannedQRCode(lot)

    def qr_setup_contact(self, qr):
        """ setup contact and return a Chat after contact is established.

        Note that this function may block for a long time as messages are exchanged
        with the emitter of the QR code.  On success a :class:`deltachat.chat.Chat` instance
        is returned.
        :param qr: valid "setup contact" QR code (all other QR codes will result in an exception)
        """
        assert self.check_qr(qr).is_ask_verifycontact()
        chat_id = lib.dc_join_securejoin(self._dc_context, as_dc_charpointer(qr))
        if chat_id == 0:
            raise ValueError("could not setup secure contact")
        return Chat(self, chat_id)

    def qr_join_chat(self, qr):
        """ join a chat group through a QR code.

        Note that this function may block for a long time as messages are exchanged
        with the emitter of the QR code.  On success a :class:`deltachat.chat.Chat` instance
        is returned which is the chat that we just joined.

        :param qr: valid "join-group" QR code (all other QR codes will result in an exception)
        """
        assert self.check_qr(qr).is_ask_verifygroup()
        chat_id = lib.dc_join_securejoin(self._dc_context, as_dc_charpointer(qr))
        if chat_id == 0:
            raise ValueError("could not join group")
        return Chat(self, chat_id)

    def set_location(self, latitude=0.0, longitude=0.0, accuracy=0.0):
        """set a new location. It effects all chats where we currently
        have enabled location streaming.

        :param latitude: float (use 0.0 if not known)
        :param longitude: float (use 0.0 if not known)
        :param accuracy: float (use 0.0 if not known)
        :raises: ValueError if no chat is currently streaming locations
        :returns: None
        """
        dc_res = lib.dc_set_location(self._dc_context, latitude, longitude, accuracy)
        if dc_res == 0:
            raise ValueError("no chat is streaming locations")

    #
    # meta API for start/stop and event based processing
    #

    def add_account_plugin(self, plugin, name=None):
        """ add an account plugin which implements one or more of
        the :class:`deltachat.hookspec.PerAccount` hooks.
        """
        self._pm.register(plugin, name=name)
        self._pm.check_pending()
        return plugin

    def remove_account_plugin(self, plugin, name=None):
        """ remove an account plugin. """
        self._pm.unregister(plugin, name=name)

    @contextmanager
    def temp_plugin(self, plugin):
        """ run a with-block with the given plugin temporarily registered. """
        self._pm.register(plugin)
        yield plugin
        self._pm.unregister(plugin)

    def stop_ongoing(self):
        """ Stop ongoing securejoin, configuration or other core jobs. """
        lib.dc_stop_ongoing_process(self._dc_context)

    def start_io(self):
        """ start this account's IO scheduling (Rust-core async scheduler)

        If this account is not configured an Exception is raised.
        You need to call account.configure() and account.wait_configure_finish()
        before.

        You may call `stop_scheduler`, `wait_shutdown` or `shutdown` after the
        account is started.

        If you are using this from a test, you may want to call
        wait_all_initial_fetches() afterwards.

        :raises MissingCredentials: if `addr` and `mail_pw` values are not set.
        :raises ConfigureFailed: if the account could not be configured.

        :returns: None
        """
        if not self.is_configured():
            raise ValueError("account not configured, cannot start io")
        lib.dc_start_io(self._dc_context)

    def maybe_network(self):
        """This function should be called when there is a hint
        that the network is available again,
        e.g. as a response to system event reporting network availability.
        The library will try to send pending messages out immediately.

        Moreover, to have a reliable state
        when the app comes to foreground with network available,
        it may be reasonable to call the function also at that moment.

        It is okay to call the function unconditionally when there is
        network available, however, calling the function
        _without_ having network may interfere with the backoff algorithm
        and will led to let the jobs fail faster, with fewer retries
        and may avoid messages being sent out.

        Finally, if the context was created by the dc_accounts_t account manager
        (currently not implemented in the Python bindings),
        use dc_accounts_maybe_network() instead of this function
        """
        lib.dc_maybe_network(self._dc_context)

    def configure(self, reconfigure=False):
        """ Start configuration process and return a Configtracker instance
        on which you can block with wait_finish() to get a True/False success
        value for the configuration process.
        """
        assert self.is_configured() == reconfigure
        if not self.get_config("addr") or not self.get_config("mail_pw"):
            raise MissingCredentials("addr or mail_pwd not set in config")
        configtracker = ConfigureTracker(self)
        self.add_account_plugin(configtracker)
        lib.dc_configure(self._dc_context)
        return configtracker

    def wait_shutdown(self):
        """ wait until shutdown of this account has completed. """
        self._shutdown_event.wait()

    def stop_io(self):
        """ stop core IO scheduler if it is running. """
        self.log("stop_ongoing")
        self.stop_ongoing()

        self.log("dc_stop_io (stop core IO scheduler)")
        lib.dc_stop_io(self._dc_context)

    def shutdown(self):
        """ shutdown and destroy account (stop callback thread, close and remove
        underlying dc_context)."""
        if self._dc_context is None:
            return

        self.stop_io()

        self.log("remove dc_context references")

        # if _dc_context is unref'ed the event thread should quickly
        # receive the termination signal. However, some python code might
        # still hold a reference and so we use a secondary signal
        # to make sure the even thread terminates if it receives any new
        # event, indepedently from waiting for the core to send NULL to
        # get_next_event().
        self._event_thread.mark_shutdown()
        self._dc_context = None

        self.log("wait for event thread to finish")
        try:
            self._event_thread.wait(timeout=2)
        except RuntimeError as e:
            self.log("Waiting for event thread failed: {}".format(e))

        if self._event_thread.is_alive():
            self.log("WARN: event thread did not terminate yet, ignoring.")

        self._shutdown_event.set()

        hook = hookspec.Global._get_plugin_manager().hook
        hook.dc_account_after_shutdown(account=self)
        self.log("shutdown finished")


class ScannedQRCode:
    def __init__(self, dc_lot):
        self._dc_lot = dc_lot

    def is_ask_verifycontact(self):
        return self._dc_lot.state() == const.DC_QR_ASK_VERIFYCONTACT

    def is_ask_verifygroup(self):
        return self._dc_lot.state() == const.DC_QR_ASK_VERIFYGROUP

    @property
    def contact_id(self):
        return self._dc_lot.id()
