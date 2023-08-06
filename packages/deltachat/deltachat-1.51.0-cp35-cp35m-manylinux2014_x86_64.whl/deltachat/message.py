""" The Message object. """

import os
import re
from . import props
from .cutil import from_dc_charpointer, as_dc_charpointer
from .capi import lib, ffi
from . import const
from datetime import datetime


class Message(object):
    """ Message object.

    You obtain instances of it through :class:`deltachat.account.Account` or
    :class:`deltachat.chat.Chat`.
    """
    def __init__(self, account, dc_msg):
        self.account = account
        assert isinstance(self.account._dc_context, ffi.CData)
        assert isinstance(dc_msg, ffi.CData)
        assert dc_msg != ffi.NULL
        self._dc_msg = dc_msg
        self.id = lib.dc_msg_get_id(dc_msg)
        assert self.id is not None and self.id >= 0, repr(self.id)

    def __eq__(self, other):
        return self.account == other.account and self.id == other.id

    def __repr__(self):
        c = self.get_sender_contact()
        typ = "outgoing" if self.is_outgoing() else "incoming"
        return "<Message {} sys={} {} id={} sender={}/{} chat={}/{}>".format(
            typ, self.is_system_message(), repr(self.text[:10]),
            self.id, c.id, c.addr, self.chat.id, self.chat.get_name())

    @classmethod
    def from_db(cls, account, id):
        assert id > 0
        return cls(account, ffi.gc(
                lib.dc_get_msg(account._dc_context, id),
                lib.dc_msg_unref
        ))

    @classmethod
    def new_empty(cls, account, view_type):
        """ create a non-persistent message.

        :param: view_type is "text", "audio", "video", "file"
        """
        view_type_code = get_viewtype_code_from_name(view_type)
        return Message(account, ffi.gc(
            lib.dc_msg_new(account._dc_context, view_type_code),
            lib.dc_msg_unref
        ))

    def create_chat(self):
        """ create or get an existing chat (group) object for this message.

        If the message is a deaddrop contact request
        the sender will become an accepted contact.

        :returns: a :class:`deltachat.chat.Chat` object.
        """
        from .chat import Chat
        chat_id = lib.dc_create_chat_by_msg_id(self.account._dc_context, self.id)
        ctx = self.account._dc_context
        self._dc_msg = ffi.gc(lib.dc_get_msg(ctx, self.id), lib.dc_msg_unref)
        return Chat(self.account, chat_id)

    @props.with_doc
    def text(self):
        """unicode text of this messages (might be empty if not a text message). """
        return from_dc_charpointer(lib.dc_msg_get_text(self._dc_msg))

    def set_text(self, text):
        """set text of this message. """
        lib.dc_msg_set_text(self._dc_msg, as_dc_charpointer(text))

    @props.with_doc
    def filename(self):
        """filename if there was an attachment, otherwise empty string. """
        return from_dc_charpointer(lib.dc_msg_get_file(self._dc_msg))

    def set_file(self, path, mime_type=None):
        """set file for this message from path and mime_type. """
        mtype = ffi.NULL if mime_type is None else as_dc_charpointer(mime_type)
        if not os.path.exists(path):
            raise ValueError("path does not exist: {!r}".format(path))
        lib.dc_msg_set_file(self._dc_msg, as_dc_charpointer(path), mtype)

    @props.with_doc
    def basename(self):
        """basename of the attachment if it exists, otherwise empty string. """
        return from_dc_charpointer(lib.dc_msg_get_filename(self._dc_msg))

    @props.with_doc
    def filemime(self):
        """mime type of the file (if it exists)"""
        return from_dc_charpointer(lib.dc_msg_get_filemime(self._dc_msg))

    def is_system_message(self):
        """ return True if this message is a system/info message. """
        return bool(lib.dc_msg_is_info(self._dc_msg))

    def is_setup_message(self):
        """ return True if this message is a setup message. """
        return lib.dc_msg_is_setupmessage(self._dc_msg)

    def get_setupcodebegin(self):
        """ return the first characters of a setup code in a setup message. """
        return from_dc_charpointer(lib.dc_msg_get_setupcodebegin(self._dc_msg))

    def is_encrypted(self):
        """ return True if this message was encrypted. """
        return bool(lib.dc_msg_get_showpadlock(self._dc_msg))

    def is_forwarded(self):
        """ return True if this message was forwarded. """
        return bool(lib.dc_msg_is_forwarded(self._dc_msg))

    def get_message_info(self):
        """ Return informational text for a single message.

        The text is multiline and may contain eg. the raw text of the message.
        """
        return from_dc_charpointer(lib.dc_get_msg_info(self.account._dc_context, self.id))

    def continue_key_transfer(self, setup_code):
        """ extract key and use it as primary key for this account. """
        res = lib.dc_continue_key_transfer(
                self.account._dc_context,
                self.id,
                as_dc_charpointer(setup_code)
        )
        if res == 0:
            raise ValueError("could not decrypt")

    @props.with_doc
    def time_sent(self):
        """UTC time when the message was sent.

        :returns: naive datetime.datetime() object.
        """
        ts = lib.dc_msg_get_timestamp(self._dc_msg)
        return datetime.utcfromtimestamp(ts)

    @props.with_doc
    def time_received(self):
        """UTC time when the message was received.

        :returns: naive datetime.datetime() object or None if message is an outgoing one.
        """
        ts = lib.dc_msg_get_received_timestamp(self._dc_msg)
        if ts:
            return datetime.utcfromtimestamp(ts)

    @props.with_doc
    def ephemeral_timer(self):
        """Ephemeral timer in seconds

        :returns: timer in seconds or None if there is no timer
        """
        timer = lib.dc_msg_get_ephemeral_timer(self._dc_msg)
        if timer:
            return timer

    @props.with_doc
    def ephemeral_timestamp(self):
        """UTC time when the message will be deleted.

        :returns: naive datetime.datetime() object or None if the timer is not started.
        """
        ts = lib.dc_msg_get_ephemeral_timestamp(self._dc_msg)
        if ts:
            return datetime.utcfromtimestamp(ts)

    @property
    def quoted_text(self):
        """Text inside the quote

        :returns: Quoted text"""
        return from_dc_charpointer(lib.dc_msg_get_quoted_text(self._dc_msg))

    @property
    def quote(self):
        """Quote getter

        :returns: Quoted message, if found in the database"""
        msg = lib.dc_msg_get_quoted_msg(self._dc_msg)
        if msg:
            return Message(self.account, ffi.gc(msg, lib.dc_msg_unref))

    @quote.setter
    def quote(self, quoted_message):
        """Quote setter"""
        lib.dc_msg_set_quote(self._dc_msg, quoted_message._dc_msg)

    def get_mime_headers(self):
        """ return mime-header object for an incoming message.

        This only returns a non-None object if ``save_mime_headers``
        config option was set and the message is incoming.

        :returns: email-mime message object (with headers only, no body).
        """
        import email.parser
        mime_headers = lib.dc_get_mime_headers(self.account._dc_context, self.id)
        if mime_headers:
            s = ffi.string(ffi.gc(mime_headers, lib.dc_str_unref))
            if isinstance(s, bytes):
                return email.message_from_bytes(s)
            return email.message_from_string(s)

    @property
    def error(self):
        """Error message"""
        return from_dc_charpointer(lib.dc_msg_get_error(self._dc_msg))

    @property
    def chat(self):
        """chat this message was posted in.

        :returns: :class:`deltachat.chat.Chat` object
        """
        from .chat import Chat
        chat_id = lib.dc_msg_get_chat_id(self._dc_msg)
        return Chat(self.account, chat_id)

    def get_sender_chat(self):
        """return the 1:1 chat with the sender of this message.

        :returns: :class:`deltachat.chat.Chat` instance
        """
        return self.get_sender_contact().get_chat()

    def get_sender_contact(self):
        """return the contact of who wrote the message.

        :returns: :class:`deltachat.chat.Contact` instance
        """
        from .contact import Contact
        contact_id = lib.dc_msg_get_from_id(self._dc_msg)
        return Contact(self.account, contact_id)

    #
    # Message State query methods
    #
    @property
    def _msgstate(self):
        if self.id == 0:
            dc_msg = self._dc_msg
        else:
            # load message from db to get a fresh/current state
            dc_msg = ffi.gc(
                lib.dc_get_msg(self.account._dc_context, self.id),
                lib.dc_msg_unref
            )
        return lib.dc_msg_get_state(dc_msg)

    def is_in_fresh(self):
        """ return True if Message is incoming fresh message (un-noticed).

        Fresh messages are not noticed nor seen and are typically
        shown in notifications.
        """
        return self._msgstate == const.DC_STATE_IN_FRESH

    def is_in_noticed(self):
        """Return True if Message is incoming and noticed.

        Eg. chat opened but message not yet read - noticed messages
        are not counted as unread but were not marked as read nor resulted in MDNs.
        """
        return self._msgstate == const.DC_STATE_IN_NOTICED

    def is_in_seen(self):
        """Return True if Message is incoming, noticed and has been seen.

        Eg. chat opened but message not yet read - noticed messages
        are not counted as unread but were not marked as read nor resulted in MDNs.
        """
        return self._msgstate == const.DC_STATE_IN_SEEN

    def is_outgoing(self):
        """Return True if Message is outgoing. """
        return self._msgstate in (
            const.DC_STATE_OUT_PREPARING, const.DC_STATE_OUT_PENDING,
            const.DC_STATE_OUT_FAILED, const.DC_STATE_OUT_MDN_RCVD,
            const.DC_STATE_OUT_DELIVERED)

    def is_out_preparing(self):
        """Return True if Message is outgoing, but its file is being prepared.
        """
        return self._msgstate == const.DC_STATE_OUT_PREPARING

    def is_out_pending(self):
        """Return True if Message is outgoing, but is pending (no single checkmark).
        """
        return self._msgstate == const.DC_STATE_OUT_PENDING

    def is_out_failed(self):
        """Return True if Message is unrecoverably failed.
        """
        return self._msgstate == const.DC_STATE_OUT_FAILED

    def is_out_delivered(self):
        """Return True if Message was successfully delivered to the server (one checkmark).

        Note, that already delivered messages may get into the state  is_out_failed().
        """
        return self._msgstate == const.DC_STATE_OUT_DELIVERED

    def is_out_mdn_received(self):
        """Return True if message was marked as read by the recipient(s) (two checkmarks;
        this requires goodwill on the receiver's side). If a sent message changes to this
        state, you'll receive the event DC_EVENT_MSG_READ.
        """
        return self._msgstate == const.DC_STATE_OUT_MDN_RCVD

    #
    # Message type query methods
    #

    @property
    def _view_type(self):
        assert self.id > 0
        return lib.dc_msg_get_viewtype(self._dc_msg)

    def is_text(self):
        """ return True if it's a text message. """
        return self._view_type == const.DC_MSG_TEXT

    def is_image(self):
        """ return True if it's an image message. """
        return self._view_type == const.DC_MSG_IMAGE

    def is_gif(self):
        """ return True if it's a gif message. """
        return self._view_type == const.DC_MSG_GIF

    def is_audio(self):
        """ return True if it's an audio message. """
        return self._view_type == const.DC_MSG_AUDIO

    def is_video(self):
        """ return True if it's a video message. """
        return self._view_type == const.DC_MSG_VIDEO

    def is_file(self):
        """ return True if it's a file message. """
        return self._view_type == const.DC_MSG_FILE

    def mark_seen(self):
        """ mark this message as seen. """
        self.account.mark_seen_messages([self.id])


# some code for handling DC_MSG_* view types

_view_type_mapping = {
    const.DC_MSG_TEXT: 'text',
    const.DC_MSG_IMAGE: 'image',
    const.DC_MSG_GIF: 'gif',
    const.DC_MSG_AUDIO: 'audio',
    const.DC_MSG_VIDEO: 'video',
    const.DC_MSG_FILE: 'file'
}


def get_viewtype_code_from_name(view_type_name):
    for code, value in _view_type_mapping.items():
        if value == view_type_name:
            return code
    raise ValueError("message typecode not found for {!r}, "
                     "available {!r}".format(view_type_name, list(_view_type_mapping.values())))


#
# some helper code for turning system messages into hook events
#

def map_system_message(msg):
    if msg.is_system_message():
        res = parse_system_add_remove(msg.text)
        if not res:
            return
        action, affected, actor = res
        affected = msg.account.get_contact_by_addr(affected)
        if actor == "me":
            actor = None
        else:
            actor = msg.account.get_contact_by_addr(actor)
        d = dict(chat=msg.chat, contact=affected, actor=actor, message=msg)
        return "ac_member_" + res[0], d


def extract_addr(text):
    m = re.match(r'.*\((.+@.+)\)', text)
    if m:
        text = m.group(1)
    text = text.rstrip(".")
    return text.strip()


def parse_system_add_remove(text):
    """ return add/remove info from parsing the given system message text.

    returns a (action, affected, actor) triple """

    # Member Me (x@y) removed by a@b.
    # Member x@y added by a@b
    # Member With space (tmp1@x.org) removed by tmp2@x.org.
    # Member With space (tmp1@x.org) removed by Another member (tmp2@x.org).",
    # Group left by some one (tmp1@x.org).
    # Group left by tmp1@x.org.
    text = text.lower()
    m = re.match(r'member (.+) (removed|added) by (.+)', text)
    if m:
        affected, action, actor = m.groups()
        return action, extract_addr(affected), extract_addr(actor)
    if text.startswith("group left by "):
        addr = extract_addr(text[13:])
        if addr:
            return "removed", addr, addr
