# -*- coding: utf-8 -*-
import json
import re

from datetime import timedelta, datetime
from DictObject import DictObject
from luckydonaldUtils.logger import logging
from luckydonaldUtils.encoding import unicode_type, to_unicode as u, to_native as n
from luckydonaldUtils.exceptions import assert_type_or_raise

from ..exceptions import TgApiServerException, TgApiParseException
from ..exceptions import TgApiTypeError, TgApiResponseException
from ..exceptions import TgApiException

from ..api_types.sendable.inline import InlineQueryResult
from ..api_types import from_array_list

from .base import BotBase


from ..api_types.sendable.files import InputFile

# sync imports
from time import sleep
import requests.exceptions
import requests



__author__ = 'luckydonald'
__all__ = ["SyncBot", "Bot"]

logger = logging.getLogger(__name__)


class SyncBot(BotBase):
    def _load_info(self):
        """
        This functions stores the id and the username of the bot.
        Called by `.username` and `.id` properties.

        This function is synchronous.
        In fact, `AsyncBot` uses `SyncBot` to load those.
        :return:
        """

        myself = self.get_me()
        if self.return_python_objects:
            self._me = myself
        else:
            from ..api_types.receivable.peer import User
            self._me = User.from_array(myself["result"])
        # end if
    # end def

    def do(self, command, files=None, use_long_polling=False, request_timeout=None, **query):
        """
        Send a request to the api.

        If the bot is set to return the json objects, it will look like this:

        ```json
        {
            "ok": bool,
            "result": {...},
            # optionally present:
            "description": "human-readable description of the result",
            "error_code": int
        }
        ```

        :param command: The Url command parameter
        :type  command: str

        :param request_timeout: When the request should time out. Default: `None`
        :type  request_timeout: int

        :param files: if it needs to send files.

        :param use_long_polling: if it should use long polling. Default: `False`
                                (see http://docs.python-requests.org/en/latest/api/#requests.Response.iter_content)
        :type  use_long_polling: bool

        :param query: all the other `**kwargs` will get json encoded.

        :return: The json response from the server, or, if `self.return_python_objects` is `True`, a parsed return type.
        :rtype:  DictObject.DictObject | pytgbot.api_types.receivable.Receivable
        """

        url, params, files = self._prepare_request(command, query)
        r = requests.post(
            url,
            params=params,
            files=files,
            stream=use_long_polling,
            verify=True,  # No self signed certificates. Telegram should be trustworthy anyway...
            timeout=request_timeout
        )

        json = r.json()
        return self._postprocess_request(r.request, response=r, json=json)
    # end def do

    def _do_fileupload(self, file_param_name, value, _command=None, **kwargs):
        """
        :param file_param_name: For what field the file should be uploaded.
        :type  file_param_name: str

        :param value: File to send. You can either pass a file_id as String to resend a file
                      file that is already on the Telegram servers, or upload a new file,
                      specifying the file path as :class:`pytgbot.api_types.sendable.files.InputFile`.
        :type  value: pytgbot.api_types.sendable.files.InputFile | str

        :param _command: Overwrite the sended command.
                         Default is to convert `file_param_name` to camel case (`"voice_note"` -> `"sendVoiceNote"`)

        :param kwargs: will get json encoded.

        :return: The json response from the server, or, if `self.return_python_objects` is `True`, a parsed return type.
        :rtype:  DictObject.DictObject | pytgbot.api_types.receivable.Receivable

        :raises TgApiTypeError, TgApiParseException, TgApiServerException: Everything from :meth:`Bot.do`, and :class:`TgApiTypeError`
        """

        if isinstance(value, str):
            kwargs[file_param_name] = str(value)
        elif isinstance(value, unicode_type):
            kwargs[file_param_name] = n(value)
        elif isinstance(value, InputFile):
            kwargs["files"] = value.get_request_files(file_param_name)
        else:
            raise TgApiTypeError("Parameter {key} is not type (str, {text_type}, {input_file_type}), but type {type}".format(
                key=file_param_name, type=type(value), input_file_type=InputFile, text_type=unicode_type))
        # end if
        if not _command:
            # command as camelCase  # "voice_note" -> "sendVoiceNote"  # https://stackoverflow.com/a/10984923/3423324
            command = re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), "send_" + file_param_name)
        else:
            command = _command
        # end def
        return self.do(command, **kwargs)
    # end def _do_fileupload

    def send_msg(self, *args, **kwargs):
        """ alias to :func:`send_message` """
        return self.send_message(*args, **kwargs)
    # end def send_msg

    # start of generated functions

    def get_updates(self, offset=None, limit=100, poll_timeout=None, allowed_updates=None, request_timeout=None, delta=timedelta(milliseconds=100), error_as_empty=False):
        """
        Use this method to receive incoming updates using long polling (See https://en.wikipedia.org/wiki/Push_technology#Long_polling).
        An Array of Update objects is returned.

        You can choose to set `error_as_empty` to `True` or `False`.
        If `error_as_empty` is set to `True`, it will log that exception as warning, and fake an empty result,
        intended for use in for loops. In case of such error (and only in such case) it contains an "exception" field.
        Ìt will look like this: `{"result": [], "exception": e}`
        This is useful if you want to use a for loop, but ignore Network related burps.

        If `error_as_empty` is set to `False` however, all `requests.RequestException` exceptions are normally raised.

        :keyword offset: (Optional)	Identifier of the first update to be returned.
                 Must be greater by one than the highest among the identifiers of previously received updates.
                 By default, updates starting with the earliest unconfirmed update are returned.
                 An update is considered confirmed as soon as :func:`get_updates` is called with
                 an offset higher than its `update_id`.
        :type offset: int

        :param limit: Limits the number of updates to be retrieved. Values between 1—100 are accepted. Defaults to 100
        :type  limit: int

        :param poll_timeout: Timeout in seconds for long polling, e.g. how long we want to wait maximum.
                               Defaults to 0, i.e. usual short polling.
        :type  poll_timeout: int

        :param allowed_updates: List the types of updates you want your bot to receive.
                                  For example, specify [“message”, “edited_channel_post”, “callback_query”] to only
                                  receive updates of these types. See Update for a complete list of available update
                                  types. Specify an empty list to receive all updates regardless of type (default).
                                  If not specified, the previous setting will be used. Please note that this parameter
                                  doesn't affect updates created before the call to the get_updates,
                                  so unwanted updates may be received for a short period of time.
        :type allowed_updates: list of str


        :param request_timeout: Timeout of the request. Not the long polling server side timeout.
                                  If not specified, it is set to `poll_timeout`+2.
        :type request_timeout: int

        :param delta: Wait minimal 'delta' seconds, between requests. Useful in a loop.
        :type  delta: datetime.

        :param error_as_empty: If errors which subclasses `requests.RequestException` will be logged but not raised.
                 Instead the returned DictObject will contain an "exception" field containing the exception occured,
                 the "result" field will be an empty list `[]`. Defaults to `False`.
        :type  error_as_empty: bool


        Returns:

        :return: An Array of Update objects is returned,
                 or an empty array if there was an requests.RequestException and error_as_empty is set to True.
        :rtype: list of pytgbot.api_types.receivable.updates.Update
        """
        assert(offset is None or isinstance(offset, int))
        assert(limit is None or isinstance(limit, int))
        assert(poll_timeout is None or isinstance(poll_timeout, int))
        assert(allowed_updates is None or isinstance(allowed_updates, list))
        if poll_timeout and not request_timeout is None:
            request_timeout = poll_timeout + 2
        # end if

        if delta.total_seconds() > poll_timeout:
            now = datetime.now()
            if self._last_update - now < delta:
                wait = ((now - self._last_update) - delta).total_seconds()  # can be 0.2
                wait = 0 if wait < 0 else wait
                if wait != 0:
                    logger.debug("Sleeping {i} seconds.".format(i=wait))
                # end if
                sleep(wait)
            # end if
        # end if
        self._last_update = datetime.now()
        use_long_polling = poll_timeout != 0
        try:
            result = self.do(
                "getUpdates", offset=offset, limit=limit, timeout=poll_timeout, allowed_updates=allowed_updates,
                use_long_polling=use_long_polling, request_timeout=request_timeout
            )
            return self._get_updates__process_result(result)
        except (requests.exceptions.RequestException, TgApiException) as e:
            if error_as_empty:
                if not isinstance(e, requests.exceptions.Timeout) or not use_long_polling:
                    logger.warning(
                        "Network related error happened in get_updates(), but will be ignored: " + str(e),
                        exc_info=True
                    )
                # end if
                self._last_update = datetime.now()
                return DictObject(result=[], exception=e)
            else:
                raise
            # end if
        # end try
    # end def get_updates

    def set_webhook(self, url, certificate=None, ip_address=None, max_connections=None, allowed_updates=None, drop_pending_updates=None):
        """
        Use this method to specify a url and receive incoming updates via an outgoing webhook. Whenever there is an update for the bot, we will send an HTTPS POST request to the specified url, containing a JSON-serialized Update. In case of an unsuccessful request, we will give up after a reasonable amount of attempts. Returns True on success.
        If you'd like to make sure that the Webhook request comes from Telegram, we recommend using a secret path in the URL, e.g. https://www.example.com/<token>. Since nobody else knows your bot's token, you can be pretty sure it's us.

        Notes1. You will not be able to receive updates using getUpdates for as long as an outgoing webhook is set up.2. To use a self-signed certificate, you need to upload your public key certificate using certificate parameter. Please upload as InputFile, sending a String will not work.3. Ports currently supported for Webhooks: 443, 80, 88, 8443.
        NEW! If you're having any trouble setting up webhooks, please check out this amazing guide to Webhooks.


        https://core.telegram.org/bots/api#setwebhook



        Parameters:

        :param url: HTTPS url to send updates to. Use an empty string to remove webhook integration
        :type  url: str|unicode


        Optional keyword parameters:

        :param certificate: Upload your public key certificate so that the root certificate in use can be checked. See our self-signed guide for details.
        :type  certificate: pytgbot.api_types.sendable.files.InputFile

        :param ip_address: The fixed IP address which will be used to send webhook requests instead of the IP address resolved through DNS
        :type  ip_address: str|unicode

        :param max_connections: Maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to 40. Use lower values to limit the load on your bot's server, and higher values to increase your bot's throughput.
        :type  max_connections: int

        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify ["message", "edited_channel_post", "callback_query"] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all update types except chat_member (default). If not specified, the previous setting will be used.Please note that this parameter doesn't affect updates created before the call to the setWebhook, so unwanted updates may be received for a short period of time.
        :type  allowed_updates: list of str|unicode

        :param drop_pending_updates: Pass True to drop all pending updates
        :type  drop_pending_updates: bool

        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._set_webhook__make_request(url=url, certificate=certificate, ip_address=ip_address, max_connections=max_connections, allowed_updates=allowed_updates, drop_pending_updates=drop_pending_updates)
        return self._set_webhook__process_result(result)
    # end def set_webhook

    def delete_webhook(self, drop_pending_updates=None):
        """
        Use this method to remove webhook integration if you decide to switch back to getUpdates. Returns True on success.

        https://core.telegram.org/bots/api#deletewebhook



        Optional keyword parameters:

        :param drop_pending_updates: Pass True to drop all pending updates
        :type  drop_pending_updates: bool

        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._delete_webhook__make_request(drop_pending_updates=drop_pending_updates)
        return self._delete_webhook__process_result(result)
    # end def delete_webhook

    def get_webhook_info(self):
        """
        Use this method to get current webhook status. Requires no parameters. On success, returns a WebhookInfo object. If the bot is using getUpdates, will return an object with the url field empty.

        https://core.telegram.org/bots/api#getwebhookinfo



        Returns:

        :return: On success, returns a WebhookInfo object
        :rtype:  pytgbot.api_types.receivable.updates.WebhookInfo
        """
        result = self._get_webhook_info__make_request()
        return self._get_webhook_info__process_result(result)
    # end def get_webhook_info

    def get_me(self):
        """
        A simple method for testing your bot's auth token. Requires no parameters. Returns basic information about the bot in form of a User object.

        https://core.telegram.org/bots/api#getme



        Returns:

        :return: Returns basic information about the bot in form of a User object
        :rtype:  pytgbot.api_types.receivable.peer.User
        """
        result = self._get_me__make_request()
        return self._get_me__process_result(result)
    # end def get_me

    def log_out(self):
        """
        Use this method to log out from the cloud Bot API server before launching the bot locally. You must log out the bot before running it locally, otherwise there is no guarantee that the bot will receive updates. After a successful call, you can immediately log in on a local server, but will not be able to log in back to the cloud Bot API server for 10 minutes. Returns True on success. Requires no parameters.

        https://core.telegram.org/bots/api#logout



        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._log_out__make_request()
        return self._log_out__process_result(result)
    # end def log_out

    def send_message(self, chat_id, text, parse_mode=None, entities=None, disable_web_page_preview=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send text messages. On success, the sent Message is returned.

        https://core.telegram.org/bots/api#sendmessage



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param text: Text of the message to be sent, 1-4096 characters after entities parsing
        :type  text: str|unicode


        Optional keyword parameters:

        :param parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
        :type  parse_mode: str|unicode

        :param entities: List of special entities that appear in message text, which can be specified instead of parse_mode
        :type  entities: list of pytgbot.api_types.receivable.media.MessageEntity

        :param disable_web_page_preview: Disables link previews for links in this message
        :type  disable_web_page_preview: bool

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardRemove | pytgbot.api_types.sendable.reply_markup.ForceReply

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_message__make_request(chat_id=chat_id, text=text, parse_mode=parse_mode, entities=entities, disable_web_page_preview=disable_web_page_preview, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_message__process_result(result)
    # end def send_message

    def forward_message(self, chat_id, from_chat_id, message_id, disable_notification=None):
        """
        Use this method to forward messages of any kind. On success, the sent Message is returned.

        https://core.telegram.org/bots/api#forwardmessage



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param from_chat_id: Unique identifier for the chat where the original message was sent (or channel username in the format @channelusername)
        :type  from_chat_id: int | str|unicode

        :param message_id: Message identifier in the chat specified in from_chat_id
        :type  message_id: int


        Optional keyword parameters:

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._forward_message__make_request(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id, disable_notification=disable_notification)
        return self._forward_message__process_result(result)
    # end def forward_message

    def copy_message(self, chat_id, from_chat_id, message_id, caption=None, parse_mode=None, caption_entities=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to copy messages of any kind. The method is analogous to the method forwardMessage, but the copied message doesn't have a link to the original message. Returns the MessageId of the sent message on success.

        https://core.telegram.org/bots/api#copymessage



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param from_chat_id: Unique identifier for the chat where the original message was sent (or channel username in the format @channelusername)
        :type  from_chat_id: int | str|unicode

        :param message_id: Message identifier in the chat specified in from_chat_id
        :type  message_id: int


        Optional keyword parameters:

        :param caption: New caption for media, 0-1024 characters after entities parsing. If not specified, the original caption is kept
        :type  caption: str|unicode

        :param parse_mode: Mode for parsing entities in the new caption. See formatting options for more details.
        :type  parse_mode: str|unicode

        :param caption_entities: List of special entities that appear in the new caption, which can be specified instead of parse_mode
        :type  caption_entities: list of pytgbot.api_types.receivable.media.MessageEntity

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardRemove | pytgbot.api_types.sendable.reply_markup.ForceReply

        Returns:

        :return: Returns the MessageId of the sent message on success
        :rtype:  pytgbot.api_types.receivable.responses.MessageId
        """
        result = self._copy_message__make_request(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id, caption=caption, parse_mode=parse_mode, caption_entities=caption_entities, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._copy_message__process_result(result)
    # end def copy_message

    def send_photo(self, chat_id, photo, caption=None, parse_mode=None, caption_entities=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send photos. On success, the sent Message is returned.

        https://core.telegram.org/bots/api#sendphoto



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param photo: Photo to send. Pass a file_id as String to send a photo that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a photo from the Internet, or upload a new photo using multipart/form-data. The photo must be at most 10 MB in size. The photo's width and height must not exceed 10000 in total. Width and height ratio must be at most 20. More info on Sending Files »
        :type  photo: pytgbot.api_types.sendable.files.InputFile | str|unicode


        Optional keyword parameters:

        :param caption: Photo caption (may also be used when resending photos by file_id), 0-1024 characters after entities parsing
        :type  caption: str|unicode

        :param parse_mode: Mode for parsing entities in the photo caption. See formatting options for more details.
        :type  parse_mode: str|unicode

        :param caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
        :type  caption_entities: list of pytgbot.api_types.receivable.media.MessageEntity

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardRemove | pytgbot.api_types.sendable.reply_markup.ForceReply

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_photo__make_request(chat_id=chat_id, photo=photo, caption=caption, parse_mode=parse_mode, caption_entities=caption_entities, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_photo__process_result(result)
    # end def send_photo

    def send_audio(self, chat_id, audio, caption=None, parse_mode=None, caption_entities=None, duration=None, performer=None, title=None, thumb=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send audio files, if you want Telegram clients to display them in the music player. Your audio must be in the .MP3 or .M4A format. On success, the sent Message is returned. Bots can currently send audio files of up to 50 MB in size, this limit may be changed in the future.
        For sending voice messages, use the sendVoice method instead.

        https://core.telegram.org/bots/api#sendaudio



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param audio: Audio file to send. Pass a file_id as String to send an audio file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get an audio file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files »
        :type  audio: pytgbot.api_types.sendable.files.InputFile | str|unicode


        Optional keyword parameters:

        :param caption: Audio caption, 0-1024 characters after entities parsing
        :type  caption: str|unicode

        :param parse_mode: Mode for parsing entities in the audio caption. See formatting options for more details.
        :type  parse_mode: str|unicode

        :param caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
        :type  caption_entities: list of pytgbot.api_types.receivable.media.MessageEntity

        :param duration: Duration of the audio in seconds
        :type  duration: int

        :param performer: Performer
        :type  performer: str|unicode

        :param title: Track name
        :type  title: str|unicode

        :param thumb: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files »
        :type  thumb: pytgbot.api_types.sendable.files.InputFile | str|unicode

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardRemove | pytgbot.api_types.sendable.reply_markup.ForceReply

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_audio__make_request(chat_id=chat_id, audio=audio, caption=caption, parse_mode=parse_mode, caption_entities=caption_entities, duration=duration, performer=performer, title=title, thumb=thumb, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_audio__process_result(result)
    # end def send_audio

    def send_document(self, chat_id, document, thumb=None, caption=None, parse_mode=None, caption_entities=None, disable_content_type_detection=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send general files. On success, the sent Message is returned. Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future.

        https://core.telegram.org/bots/api#senddocument



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param document: File to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files »
        :type  document: pytgbot.api_types.sendable.files.InputFile | str|unicode


        Optional keyword parameters:

        :param thumb: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files »
        :type  thumb: pytgbot.api_types.sendable.files.InputFile | str|unicode

        :param caption: Document caption (may also be used when resending documents by file_id), 0-1024 characters after entities parsing
        :type  caption: str|unicode

        :param parse_mode: Mode for parsing entities in the document caption. See formatting options for more details.
        :type  parse_mode: str|unicode

        :param caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
        :type  caption_entities: list of pytgbot.api_types.receivable.media.MessageEntity

        :param disable_content_type_detection: Disables automatic server-side content type detection for files uploaded using multipart/form-data
        :type  disable_content_type_detection: bool

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardRemove | pytgbot.api_types.sendable.reply_markup.ForceReply

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_document__make_request(chat_id=chat_id, document=document, thumb=thumb, caption=caption, parse_mode=parse_mode, caption_entities=caption_entities, disable_content_type_detection=disable_content_type_detection, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_document__process_result(result)
    # end def send_document

    def send_video(self, chat_id, video, duration=None, width=None, height=None, thumb=None, caption=None, parse_mode=None, caption_entities=None, supports_streaming=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send video files, Telegram clients support mp4 videos (other formats may be sent as Document). On success, the sent Message is returned. Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future.

        https://core.telegram.org/bots/api#sendvideo



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param video: Video to send. Pass a file_id as String to send a video that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a video from the Internet, or upload a new video using multipart/form-data. More info on Sending Files »
        :type  video: pytgbot.api_types.sendable.files.InputFile | str|unicode


        Optional keyword parameters:

        :param duration: Duration of sent video in seconds
        :type  duration: int

        :param width: Video width
        :type  width: int

        :param height: Video height
        :type  height: int

        :param thumb: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files »
        :type  thumb: pytgbot.api_types.sendable.files.InputFile | str|unicode

        :param caption: Video caption (may also be used when resending videos by file_id), 0-1024 characters after entities parsing
        :type  caption: str|unicode

        :param parse_mode: Mode for parsing entities in the video caption. See formatting options for more details.
        :type  parse_mode: str|unicode

        :param caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
        :type  caption_entities: list of pytgbot.api_types.receivable.media.MessageEntity

        :param supports_streaming: Pass True, if the uploaded video is suitable for streaming
        :type  supports_streaming: bool

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardRemove | pytgbot.api_types.sendable.reply_markup.ForceReply

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_video__make_request(chat_id=chat_id, video=video, duration=duration, width=width, height=height, thumb=thumb, caption=caption, parse_mode=parse_mode, caption_entities=caption_entities, supports_streaming=supports_streaming, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_video__process_result(result)
    # end def send_video

    def send_animation(self, chat_id, animation, duration=None, width=None, height=None, thumb=None, caption=None, parse_mode=None, caption_entities=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound). On success, the sent Message is returned. Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future.

        https://core.telegram.org/bots/api#sendanimation



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param animation: Animation to send. Pass a file_id as String to send an animation that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get an animation from the Internet, or upload a new animation using multipart/form-data. More info on Sending Files »
        :type  animation: pytgbot.api_types.sendable.files.InputFile | str|unicode


        Optional keyword parameters:

        :param duration: Duration of sent animation in seconds
        :type  duration: int

        :param width: Animation width
        :type  width: int

        :param height: Animation height
        :type  height: int

        :param thumb: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files »
        :type  thumb: pytgbot.api_types.sendable.files.InputFile | str|unicode

        :param caption: Animation caption (may also be used when resending animation by file_id), 0-1024 characters after entities parsing
        :type  caption: str|unicode

        :param parse_mode: Mode for parsing entities in the animation caption. See formatting options for more details.
        :type  parse_mode: str|unicode

        :param caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
        :type  caption_entities: list of pytgbot.api_types.receivable.media.MessageEntity

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardRemove | pytgbot.api_types.sendable.reply_markup.ForceReply

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_animation__make_request(chat_id=chat_id, animation=animation, duration=duration, width=width, height=height, thumb=thumb, caption=caption, parse_mode=parse_mode, caption_entities=caption_entities, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_animation__process_result(result)
    # end def send_animation

    def send_voice(self, chat_id, voice, caption=None, parse_mode=None, caption_entities=None, duration=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. For this to work, your audio must be in an .OGG file encoded with OPUS (other formats may be sent as Audio or Document). On success, the sent Message is returned. Bots can currently send voice messages of up to 50 MB in size, this limit may be changed in the future.

        https://core.telegram.org/bots/api#sendvoice



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param voice: Audio file to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files »
        :type  voice: pytgbot.api_types.sendable.files.InputFile | str|unicode


        Optional keyword parameters:

        :param caption: Voice message caption, 0-1024 characters after entities parsing
        :type  caption: str|unicode

        :param parse_mode: Mode for parsing entities in the voice message caption. See formatting options for more details.
        :type  parse_mode: str|unicode

        :param caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
        :type  caption_entities: list of pytgbot.api_types.receivable.media.MessageEntity

        :param duration: Duration of the voice message in seconds
        :type  duration: int

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardRemove | pytgbot.api_types.sendable.reply_markup.ForceReply

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_voice__make_request(chat_id=chat_id, voice=voice, caption=caption, parse_mode=parse_mode, caption_entities=caption_entities, duration=duration, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_voice__process_result(result)
    # end def send_voice

    def send_video_note(self, chat_id, video_note, duration=None, length=None, thumb=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        As of v.4.0, Telegram clients support rounded square mp4 videos of up to 1 minute long. Use this method to send video messages. On success, the sent Message is returned.

        https://core.telegram.org/bots/api#sendvideonote



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param video_note: Video note to send. Pass a file_id as String to send a video note that exists on the Telegram servers (recommended) or upload a new video using multipart/form-data. More info on Sending Files ». Sending video notes by a URL is currently unsupported
        :type  video_note: pytgbot.api_types.sendable.files.InputFile | str|unicode


        Optional keyword parameters:

        :param duration: Duration of sent video in seconds
        :type  duration: int

        :param length: Video width and height, i.e. diameter of the video message
        :type  length: int

        :param thumb: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass "attach://<file_attach_name>" if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files »
        :type  thumb: pytgbot.api_types.sendable.files.InputFile | str|unicode

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardRemove | pytgbot.api_types.sendable.reply_markup.ForceReply

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_video_note__make_request(chat_id=chat_id, video_note=video_note, duration=duration, length=length, thumb=thumb, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_video_note__process_result(result)
    # end def send_video_note

    def send_media_group(self, chat_id, media, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None):
        """
        Use this method to send a group of photos, videos, documents or audios as an album. Documents and audio files can be only grouped in an album with messages of the same type. On success, an array of Messages that were sent is returned.

        https://core.telegram.org/bots/api#sendmediagroup



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param media: A JSON-serialized array describing messages to be sent, must include 2-10 items
        :type  media: list of pytgbot.api_types.sendable.input_media.InputMediaAudio | list of pytgbot.api_types.sendable.input_media.InputMediaDocument | list of pytgbot.api_types.sendable.input_media.InputMediaPhoto | list of pytgbot.api_types.sendable.input_media.InputMediaVideo


        Optional keyword parameters:

        :param disable_notification: Sends messages silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the messages are a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        Returns:

        :return: On success, an array of Messages that were sent is returned
        :rtype:  list of pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_media_group__make_request(chat_id=chat_id, media=media, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply)
        return self._send_media_group__process_result(result)
    # end def send_media_group

    def send_location(self, chat_id, latitude, longitude, horizontal_accuracy=None, live_period=None, heading=None, proximity_alert_radius=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send point on the map. On success, the sent Message is returned.

        https://core.telegram.org/bots/api#sendlocation



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param latitude: Latitude of the location
        :type  latitude: float

        :param longitude: Longitude of the location
        :type  longitude: float


        Optional keyword parameters:

        :param horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
        :type  horizontal_accuracy: float

        :param live_period: Period in seconds for which the location will be updated (see Live Locations, should be between 60 and 86400.
        :type  live_period: int

        :param heading: For live locations, a direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
        :type  heading: int

        :param proximity_alert_radius: For live locations, a maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
        :type  proximity_alert_radius: int

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardRemove | pytgbot.api_types.sendable.reply_markup.ForceReply

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_location__make_request(chat_id=chat_id, latitude=latitude, longitude=longitude, horizontal_accuracy=horizontal_accuracy, live_period=live_period, heading=heading, proximity_alert_radius=proximity_alert_radius, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_location__process_result(result)
    # end def send_location

    def edit_message_live_location(self, latitude, longitude, chat_id=None, message_id=None, inline_message_id=None, horizontal_accuracy=None, heading=None, proximity_alert_radius=None, reply_markup=None):
        """
        Use this method to edit live location messages. A location can be edited until its live_period expires or editing is explicitly disabled by a call to stopMessageLiveLocation. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.

        https://core.telegram.org/bots/api#editmessagelivelocation



        Parameters:

        :param latitude: Latitude of new location
        :type  latitude: float

        :param longitude: Longitude of new location
        :type  longitude: float


        Optional keyword parameters:

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
        :type  message_id: int

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type  inline_message_id: str|unicode

        :param horizontal_accuracy: The radius of uncertainty for the location, measured in meters; 0-1500
        :type  horizontal_accuracy: float

        :param heading: Direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
        :type  heading: int

        :param proximity_alert_radius: Maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
        :type  proximity_alert_radius: int

        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup

        Returns:

        :return: On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message | bool
        """
        result = self._edit_message_live_location__make_request(latitude=latitude, longitude=longitude, chat_id=chat_id, message_id=message_id, inline_message_id=inline_message_id, horizontal_accuracy=horizontal_accuracy, heading=heading, proximity_alert_radius=proximity_alert_radius, reply_markup=reply_markup)
        return self._edit_message_live_location__process_result(result)
    # end def edit_message_live_location

    def stop_message_live_location(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        """
        Use this method to stop updating a live location message before live_period expires. On success, if the message was sent by the bot, the sent Message is returned, otherwise True is returned.

        https://core.telegram.org/bots/api#stopmessagelivelocation



        Optional keyword parameters:

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param message_id: Required if inline_message_id is not specified. Identifier of the message with live location to stop
        :type  message_id: int

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type  inline_message_id: str|unicode

        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup

        Returns:

        :return: On success, if the message was sent by the bot, the sent Message is returned, otherwise True is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message | bool
        """
        result = self._stop_message_live_location__make_request(chat_id=chat_id, message_id=message_id, inline_message_id=inline_message_id, reply_markup=reply_markup)
        return self._stop_message_live_location__process_result(result)
    # end def stop_message_live_location

    def send_venue(self, chat_id, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None, google_place_id=None, google_place_type=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send information about a venue. On success, the sent Message is returned.

        https://core.telegram.org/bots/api#sendvenue



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param latitude: Latitude of the venue
        :type  latitude: float

        :param longitude: Longitude of the venue
        :type  longitude: float

        :param title: Name of the venue
        :type  title: str|unicode

        :param address: Address of the venue
        :type  address: str|unicode


        Optional keyword parameters:

        :param foursquare_id: Foursquare identifier of the venue
        :type  foursquare_id: str|unicode

        :param foursquare_type: Foursquare type of the venue, if known. (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)
        :type  foursquare_type: str|unicode

        :param google_place_id: Google Places identifier of the venue
        :type  google_place_id: str|unicode

        :param google_place_type: Google Places type of the venue. (See supported types.)
        :type  google_place_type: str|unicode

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardRemove | pytgbot.api_types.sendable.reply_markup.ForceReply

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_venue__make_request(chat_id=chat_id, latitude=latitude, longitude=longitude, title=title, address=address, foursquare_id=foursquare_id, foursquare_type=foursquare_type, google_place_id=google_place_id, google_place_type=google_place_type, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_venue__process_result(result)
    # end def send_venue

    def send_contact(self, chat_id, phone_number, first_name, last_name=None, vcard=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send phone contacts. On success, the sent Message is returned.

        https://core.telegram.org/bots/api#sendcontact



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param phone_number: Contact's phone number
        :type  phone_number: str|unicode

        :param first_name: Contact's first name
        :type  first_name: str|unicode


        Optional keyword parameters:

        :param last_name: Contact's last name
        :type  last_name: str|unicode

        :param vcard: Additional data about the contact in the form of a vCard, 0-2048 bytes
        :type  vcard: str|unicode

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove keyboard or to force a reply from the user.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardRemove | pytgbot.api_types.sendable.reply_markup.ForceReply

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_contact__make_request(chat_id=chat_id, phone_number=phone_number, first_name=first_name, last_name=last_name, vcard=vcard, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_contact__process_result(result)
    # end def send_contact

    def send_poll(self, chat_id, question, options, is_anonymous=None, type=None, allows_multiple_answers=None, correct_option_id=None, explanation=None, explanation_parse_mode=None, explanation_entities=None, open_period=None, close_date=None, is_closed=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send a native poll. On success, the sent Message is returned.

        https://core.telegram.org/bots/api#sendpoll



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param question: Poll question, 1-300 characters
        :type  question: str|unicode

        :param options: A JSON-serialized list of answer options, 2-10 strings 1-100 characters each
        :type  options: list of str|unicode


        Optional keyword parameters:

        :param is_anonymous: True, if the poll needs to be anonymous, defaults to True
        :type  is_anonymous: bool

        :param type: Poll type, "quiz" or "regular", defaults to "regular"
        :type  type: str|unicode

        :param allows_multiple_answers: True, if the poll allows multiple answers, ignored for polls in quiz mode, defaults to False
        :type  allows_multiple_answers: bool

        :param correct_option_id: 0-based identifier of the correct answer option, required for polls in quiz mode
        :type  correct_option_id: int

        :param explanation: Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll, 0-200 characters with at most 2 line feeds after entities parsing
        :type  explanation: str|unicode

        :param explanation_parse_mode: Mode for parsing entities in the explanation. See formatting options for more details.
        :type  explanation_parse_mode: str|unicode

        :param explanation_entities: List of special entities that appear in the poll explanation, which can be specified instead of parse_mode
        :type  explanation_entities: list of pytgbot.api_types.receivable.media.MessageEntity

        :param open_period: Amount of time in seconds the poll will be active after creation, 5-600. Can't be used together with close_date.
        :type  open_period: int

        :param close_date: Point in time (Unix timestamp) when the poll will be automatically closed. Must be at least 5 and no more than 600 seconds in the future. Can't be used together with open_period.
        :type  close_date: int

        :param is_closed: Pass True, if the poll needs to be immediately closed. This can be useful for poll preview.
        :type  is_closed: bool

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardRemove | pytgbot.api_types.sendable.reply_markup.ForceReply

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_poll__make_request(chat_id=chat_id, question=question, options=options, is_anonymous=is_anonymous, type=type, allows_multiple_answers=allows_multiple_answers, correct_option_id=correct_option_id, explanation=explanation, explanation_parse_mode=explanation_parse_mode, explanation_entities=explanation_entities, open_period=open_period, close_date=close_date, is_closed=is_closed, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_poll__process_result(result)
    # end def send_poll

    def send_dice(self, chat_id, emoji=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send an animated emoji that will display a random value. On success, the sent Message is returned.

        https://core.telegram.org/bots/api#senddice



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode


        Optional keyword parameters:

        :param emoji: Emoji on which the dice throw animation is based. Currently, must be one of "🎲", "🎯", "🏀", "⚽", "🎳", or "🎰". Dice can have values 1-6 for "🎲", "🎯" and "🎳", values 1-5 for "🏀" and "⚽", and values 1-64 for "🎰". Defaults to "🎲"
        :type  emoji: str|unicode

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardRemove | pytgbot.api_types.sendable.reply_markup.ForceReply

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_dice__make_request(chat_id=chat_id, emoji=emoji, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_dice__process_result(result)
    # end def send_dice

    def send_chat_action(self, chat_id, action):
        """
        Use this method when you need to tell the user that something is happening on the bot's side. The status is set for 5 seconds or less (when a message arrives from your bot, Telegram clients clear its typing status). Returns True on success.

        Example: The ImageBot needs some time to process a request and upload the image. Instead of sending a text message along the lines of "Retrieving image, please wait…", the bot may use sendChatAction with action = upload_photo. The user will see a "sending photo" status for the bot.

        We only recommend using this method when a response from the bot will take a noticeable amount of time to arrive.

        https://core.telegram.org/bots/api#sendchataction



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param action: Type of action to broadcast. Choose one, depending on what the user is about to receive: typing for text messages, upload_photo for photos, record_video or upload_video for videos, record_voice or upload_voice for voice notes, upload_document for general files, find_location for location data, record_video_note or upload_video_note for video notes.
        :type  action: str|unicode


        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._send_chat_action__make_request(chat_id=chat_id, action=action)
        return self._send_chat_action__process_result(result)
    # end def send_chat_action

    def get_user_profile_photos(self, user_id, offset=None, limit=None):
        """
        Use this method to get a list of profile pictures for a user. Returns a UserProfilePhotos object.

        https://core.telegram.org/bots/api#getuserprofilephotos



        Parameters:

        :param user_id: Unique identifier of the target user
        :type  user_id: int


        Optional keyword parameters:

        :param offset: Sequential number of the first photo to be returned. By default, all photos are returned.
        :type  offset: int

        :param limit: Limits the number of photos to be retrieved. Values between 1-100 are accepted. Defaults to 100.
        :type  limit: int

        Returns:

        :return: Returns a UserProfilePhotos object
        :rtype:  pytgbot.api_types.receivable.media.UserProfilePhotos
        """
        result = self._get_user_profile_photos__make_request(user_id=user_id, offset=offset, limit=limit)
        return self._get_user_profile_photos__process_result(result)
    # end def get_user_profile_photos

    def get_file(self, file_id):
        """
        Use this method to get basic info about a file and prepare it for downloading. For the moment, bots can download files of up to 20MB in size. On success, a File object is returned. The file can then be downloaded via the link https://api.telegram.org/file/bot<token>/<file_path>, where <file_path> is taken from the response. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling getFile again.
        Note: This function may not preserve the original file name and MIME type. You should save the file's MIME type and name (if available) when the File object is received.

        https://core.telegram.org/bots/api#getfile



        Parameters:

        :param file_id: File identifier to get info about
        :type  file_id: str|unicode


        Returns:

        :return: On success, a File object is returned
        :rtype:  pytgbot.api_types.receivable.media.File
        """
        result = self._get_file__make_request(file_id=file_id)
        return self._get_file__process_result(result)
    # end def get_file

    def kick_chat_member(self, chat_id, user_id, until_date=None, revoke_messages=None):
        """
        Use this method to kick a user from a group, a supergroup or a channel. In the case of supergroups and channels, the user will not be able to return to the chat on their own using invite links, etc., unless unbanned first. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns True on success.

        https://core.telegram.org/bots/api#kickchatmember



        Parameters:

        :param chat_id: Unique identifier for the target group or username of the target supergroup or channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param user_id: Unique identifier of the target user
        :type  user_id: int


        Optional keyword parameters:

        :param until_date: Date when the user will be unbanned, unix time. If user is banned for more than 366 days or less than 30 seconds from the current time they are considered to be banned forever. Applied for supergroups and channels only.
        :type  until_date: int

        :param revoke_messages: Pass True to delete all messages from the chat for the user that is being removed. If False, the user will be able to see messages in the group that were sent before the user was removed. Always True for supergroups and channels.
        :type  revoke_messages: bool

        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._kick_chat_member__make_request(chat_id=chat_id, user_id=user_id, until_date=until_date, revoke_messages=revoke_messages)
        return self._kick_chat_member__process_result(result)
    # end def kick_chat_member

    def unban_chat_member(self, chat_id, user_id, only_if_banned=None):
        """
        Use this method to unban a previously kicked user in a supergroup or channel. The user will not return to the group or channel automatically, but will be able to join via link, etc. The bot must be an administrator for this to work. By default, this method guarantees that after the call the user is not a member of the chat, but will be able to join it. So if the user is a member of the chat they will also be removed from the chat. If you don't want this, use the parameter only_if_banned. Returns True on success.

        https://core.telegram.org/bots/api#unbanchatmember



        Parameters:

        :param chat_id: Unique identifier for the target group or username of the target supergroup or channel (in the format @username)
        :type  chat_id: int | str|unicode

        :param user_id: Unique identifier of the target user
        :type  user_id: int


        Optional keyword parameters:

        :param only_if_banned: Do nothing if the user is not banned
        :type  only_if_banned: bool

        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._unban_chat_member__make_request(chat_id=chat_id, user_id=user_id, only_if_banned=only_if_banned)
        return self._unban_chat_member__process_result(result)
    # end def unban_chat_member

    def restrict_chat_member(self, chat_id, user_id, permissions, until_date=None):
        """
        Use this method to restrict a user in a supergroup. The bot must be an administrator in the supergroup for this to work and must have the appropriate admin rights. Pass True for all permissions to lift restrictions from a user. Returns True on success.

        https://core.telegram.org/bots/api#restrictchatmember



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type  chat_id: int | str|unicode

        :param user_id: Unique identifier of the target user
        :type  user_id: int

        :param permissions: A JSON-serialized object for new user permissions
        :type  permissions: pytgbot.api_types.receivable.peer.ChatPermissions


        Optional keyword parameters:

        :param until_date: Date when restrictions will be lifted for the user, unix time. If user is restricted for more than 366 days or less than 30 seconds from the current time, they are considered to be restricted forever
        :type  until_date: int

        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._restrict_chat_member__make_request(chat_id=chat_id, user_id=user_id, permissions=permissions, until_date=until_date)
        return self._restrict_chat_member__process_result(result)
    # end def restrict_chat_member

    def promote_chat_member(self, chat_id, user_id, is_anonymous=None, can_manage_chat=None, can_post_messages=None, can_edit_messages=None, can_delete_messages=None, can_manage_voice_chats=None, can_restrict_members=None, can_promote_members=None, can_change_info=None, can_invite_users=None, can_pin_messages=None):
        """
        Use this method to promote or demote a user in a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Pass False for all boolean parameters to demote a user. Returns True on success.

        https://core.telegram.org/bots/api#promotechatmember



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param user_id: Unique identifier of the target user
        :type  user_id: int


        Optional keyword parameters:

        :param is_anonymous: Pass True, if the administrator's presence in the chat is hidden
        :type  is_anonymous: bool

        :param can_manage_chat: Pass True, if the administrator can access the chat event log, chat statistics, message statistics in channels, see channel members, see anonymous administrators in supergroups and ignore slow mode. Implied by any other administrator privilege
        :type  can_manage_chat: bool

        :param can_post_messages: Pass True, if the administrator can create channel posts, channels only
        :type  can_post_messages: bool

        :param can_edit_messages: Pass True, if the administrator can edit messages of other users and can pin messages, channels only
        :type  can_edit_messages: bool

        :param can_delete_messages: Pass True, if the administrator can delete messages of other users
        :type  can_delete_messages: bool

        :param can_manage_voice_chats: Pass True, if the administrator can manage voice chats
        :type  can_manage_voice_chats: bool

        :param can_restrict_members: Pass True, if the administrator can restrict, ban or unban chat members
        :type  can_restrict_members: bool

        :param can_promote_members: Pass True, if the administrator can add new administrators with a subset of their own privileges or demote administrators that he has promoted, directly or indirectly (promoted by administrators that were appointed by him)
        :type  can_promote_members: bool

        :param can_change_info: Pass True, if the administrator can change chat title, photo and other settings
        :type  can_change_info: bool

        :param can_invite_users: Pass True, if the administrator can invite new users to the chat
        :type  can_invite_users: bool

        :param can_pin_messages: Pass True, if the administrator can pin messages, supergroups only
        :type  can_pin_messages: bool

        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._promote_chat_member__make_request(chat_id=chat_id, user_id=user_id, is_anonymous=is_anonymous, can_manage_chat=can_manage_chat, can_post_messages=can_post_messages, can_edit_messages=can_edit_messages, can_delete_messages=can_delete_messages, can_manage_voice_chats=can_manage_voice_chats, can_restrict_members=can_restrict_members, can_promote_members=can_promote_members, can_change_info=can_change_info, can_invite_users=can_invite_users, can_pin_messages=can_pin_messages)
        return self._promote_chat_member__process_result(result)
    # end def promote_chat_member

    def set_chat_administrator_custom_title(self, chat_id, user_id, custom_title):
        """
        Use this method to set a custom title for an administrator in a supergroup promoted by the bot. Returns True on success.

        https://core.telegram.org/bots/api#setchatadministratorcustomtitle



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type  chat_id: int | str|unicode

        :param user_id: Unique identifier of the target user
        :type  user_id: int

        :param custom_title: New custom title for the administrator; 0-16 characters, emoji are not allowed
        :type  custom_title: str|unicode


        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._set_chat_administrator_custom_title__make_request(chat_id=chat_id, user_id=user_id, custom_title=custom_title)
        return self._set_chat_administrator_custom_title__process_result(result)
    # end def set_chat_administrator_custom_title

    def set_chat_permissions(self, chat_id, permissions):
        """
        Use this method to set default chat permissions for all members. The bot must be an administrator in the group or a supergroup for this to work and must have the can_restrict_members admin rights. Returns True on success.

        https://core.telegram.org/bots/api#setchatpermissions



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type  chat_id: int | str|unicode

        :param permissions: New default chat permissions
        :type  permissions: pytgbot.api_types.receivable.peer.ChatPermissions


        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._set_chat_permissions__make_request(chat_id=chat_id, permissions=permissions)
        return self._set_chat_permissions__process_result(result)
    # end def set_chat_permissions

    def export_chat_invite_link(self, chat_id):
        """
        Use this method to generate a new primary invite link for a chat; any previously generated primary link is revoked. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns the new invite link as String on success.

        Note: Each administrator in a chat generates their own invite links. Bots can't use invite links generated by other administrators. If you want your bot to work with invite links, it will need to generate its own link using exportChatInviteLink or by calling the getChat method. If your bot needs to generate a new primary invite link replacing its previous one, use exportChatInviteLink again.


        https://core.telegram.org/bots/api#exportchatinvitelink



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode


        Returns:

        :return: Returns the new invite link as String on success
        :rtype:  str|unicode
        """
        result = self._export_chat_invite_link__make_request(chat_id=chat_id)
        return self._export_chat_invite_link__process_result(result)
    # end def export_chat_invite_link

    def create_chat_invite_link(self, chat_id, expire_date=None, member_limit=None):
        """
        Use this method to create an additional invite link for a chat. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. The link can be revoked using the method revokeChatInviteLink. Returns the new invite link as ChatInviteLink object.

        https://core.telegram.org/bots/api#createchatinvitelink



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode


        Optional keyword parameters:

        :param expire_date: Point in time (Unix timestamp) when the link will expire
        :type  expire_date: int

        :param member_limit: Maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999
        :type  member_limit: int

        Returns:

        :return: Returns the new invite link as ChatInviteLink object
        :rtype:  pytgbot.api_types.receivable.peer.ChatInviteLink
        """
        result = self._create_chat_invite_link__make_request(chat_id=chat_id, expire_date=expire_date, member_limit=member_limit)
        return self._create_chat_invite_link__process_result(result)
    # end def create_chat_invite_link

    def edit_chat_invite_link(self, chat_id, invite_link, expire_date=None, member_limit=None):
        """
        Use this method to edit a non-primary invite link created by the bot. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns the edited invite link as a ChatInviteLink object.

        https://core.telegram.org/bots/api#editchatinvitelink



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param invite_link: The invite link to edit
        :type  invite_link: str|unicode


        Optional keyword parameters:

        :param expire_date: Point in time (Unix timestamp) when the link will expire
        :type  expire_date: int

        :param member_limit: Maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999
        :type  member_limit: int

        Returns:

        :return: Returns the edited invite link as a ChatInviteLink object
        :rtype:  pytgbot.api_types.receivable.peer.ChatInviteLink
        """
        result = self._edit_chat_invite_link__make_request(chat_id=chat_id, invite_link=invite_link, expire_date=expire_date, member_limit=member_limit)
        return self._edit_chat_invite_link__process_result(result)
    # end def edit_chat_invite_link

    def revoke_chat_invite_link(self, chat_id, invite_link):
        """
        Use this method to revoke an invite link created by the bot. If the primary link is revoked, a new link is automatically generated. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns the revoked invite link as ChatInviteLink object.

        https://core.telegram.org/bots/api#revokechatinvitelink



        Parameters:

        :param chat_id: Unique identifier of the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param invite_link: The invite link to revoke
        :type  invite_link: str|unicode


        Returns:

        :return: Returns the revoked invite link as ChatInviteLink object
        :rtype:  pytgbot.api_types.receivable.peer.ChatInviteLink
        """
        result = self._revoke_chat_invite_link__make_request(chat_id=chat_id, invite_link=invite_link)
        return self._revoke_chat_invite_link__process_result(result)
    # end def revoke_chat_invite_link

    def set_chat_photo(self, chat_id, photo):
        """
        Use this method to set a new profile photo for the chat. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns True on success.

        https://core.telegram.org/bots/api#setchatphoto



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param photo: New chat photo, uploaded using multipart/form-data
        :type  photo: pytgbot.api_types.sendable.files.InputFile


        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._set_chat_photo__make_request(chat_id=chat_id, photo=photo)
        return self._set_chat_photo__process_result(result)
    # end def set_chat_photo

    def delete_chat_photo(self, chat_id):
        """
        Use this method to delete a chat photo. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns True on success.

        https://core.telegram.org/bots/api#deletechatphoto



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode


        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._delete_chat_photo__make_request(chat_id=chat_id)
        return self._delete_chat_photo__process_result(result)
    # end def delete_chat_photo

    def set_chat_title(self, chat_id, title):
        """
        Use this method to change the title of a chat. Titles can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns True on success.

        https://core.telegram.org/bots/api#setchattitle



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param title: New chat title, 1-255 characters
        :type  title: str|unicode


        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._set_chat_title__make_request(chat_id=chat_id, title=title)
        return self._set_chat_title__process_result(result)
    # end def set_chat_title

    def set_chat_description(self, chat_id, description=None):
        """
        Use this method to change the description of a group, a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns True on success.

        https://core.telegram.org/bots/api#setchatdescription



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode


        Optional keyword parameters:

        :param description: New chat description, 0-255 characters
        :type  description: str|unicode

        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._set_chat_description__make_request(chat_id=chat_id, description=description)
        return self._set_chat_description__process_result(result)
    # end def set_chat_description

    def pin_chat_message(self, chat_id, message_id, disable_notification=None):
        """
        Use this method to add a message to the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can_pin_messages' admin right in a supergroup or 'can_edit_messages' admin right in a channel. Returns True on success.

        https://core.telegram.org/bots/api#pinchatmessage



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param message_id: Identifier of a message to pin
        :type  message_id: int


        Optional keyword parameters:

        :param disable_notification: Pass True, if it is not necessary to send a notification to all chat members about the new pinned message. Notifications are always disabled in channels and private chats.
        :type  disable_notification: bool

        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._pin_chat_message__make_request(chat_id=chat_id, message_id=message_id, disable_notification=disable_notification)
        return self._pin_chat_message__process_result(result)
    # end def pin_chat_message

    def unpin_chat_message(self, chat_id, message_id=None):
        """
        Use this method to remove a message from the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can_pin_messages' admin right in a supergroup or 'can_edit_messages' admin right in a channel. Returns True on success.

        https://core.telegram.org/bots/api#unpinchatmessage



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode


        Optional keyword parameters:

        :param message_id: Identifier of a message to unpin. If not specified, the most recent pinned message (by sending date) will be unpinned.
        :type  message_id: int

        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._unpin_chat_message__make_request(chat_id=chat_id, message_id=message_id)
        return self._unpin_chat_message__process_result(result)
    # end def unpin_chat_message

    def unpin_all_chat_messages(self, chat_id):
        """
        Use this method to clear the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can_pin_messages' admin right in a supergroup or 'can_edit_messages' admin right in a channel. Returns True on success.

        https://core.telegram.org/bots/api#unpinallchatmessages



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode


        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._unpin_all_chat_messages__make_request(chat_id=chat_id)
        return self._unpin_all_chat_messages__process_result(result)
    # end def unpin_all_chat_messages

    def leave_chat(self, chat_id):
        """
        Use this method for your bot to leave a group, supergroup or channel. Returns True on success.

        https://core.telegram.org/bots/api#leavechat



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
        :type  chat_id: int | str|unicode


        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._leave_chat__make_request(chat_id=chat_id)
        return self._leave_chat__process_result(result)
    # end def leave_chat

    def get_chat(self, chat_id):
        """
        Use this method to get up to date information about the chat (current name of the user for one-on-one conversations, current username of a user, group or channel, etc.). Returns a Chat object on success.

        https://core.telegram.org/bots/api#getchat



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
        :type  chat_id: int | str|unicode


        Returns:

        :return: Returns a Chat object on success
        :rtype:  pytgbot.api_types.receivable.peer.Chat
        """
        result = self._get_chat__make_request(chat_id=chat_id)
        return self._get_chat__process_result(result)
    # end def get_chat

    def get_chat_administrators(self, chat_id):
        """
        Use this method to get a list of administrators in a chat. On success, returns an Array of ChatMember objects that contains information about all chat administrators except other bots. If the chat is a group or a supergroup and no administrators were appointed, only the creator will be returned.

        https://core.telegram.org/bots/api#getchatadministrators



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
        :type  chat_id: int | str|unicode


        Returns:

        :return: On success, returns an Array of ChatMember objects that contains information about all chat administrators except other bots
        :rtype:  list of pytgbot.api_types.receivable.peer.ChatMember
        """
        result = self._get_chat_administrators__make_request(chat_id=chat_id)
        return self._get_chat_administrators__process_result(result)
    # end def get_chat_administrators

    def get_chat_members_count(self, chat_id):
        """
        Use this method to get the number of members in a chat. Returns Int on success.

        https://core.telegram.org/bots/api#getchatmemberscount



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
        :type  chat_id: int | str|unicode


        Returns:

        :return: Returns Int on success
        :rtype:  int
        """
        result = self._get_chat_members_count__make_request(chat_id=chat_id)
        return self._get_chat_members_count__process_result(result)
    # end def get_chat_members_count

    def get_chat_member(self, chat_id, user_id):
        """
        Use this method to get information about a member of a chat. Returns a ChatMember object on success.

        https://core.telegram.org/bots/api#getchatmember



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param user_id: Unique identifier of the target user
        :type  user_id: int


        Returns:

        :return: Returns a ChatMember object on success
        :rtype:  pytgbot.api_types.receivable.peer.ChatMember
        """
        result = self._get_chat_member__make_request(chat_id=chat_id, user_id=user_id)
        return self._get_chat_member__process_result(result)
    # end def get_chat_member

    def set_chat_sticker_set(self, chat_id, sticker_set_name):
        """
        Use this method to set a new group sticker set for a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success.

        https://core.telegram.org/bots/api#setchatstickerset



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type  chat_id: int | str|unicode

        :param sticker_set_name: Name of the sticker set to be set as the group sticker set
        :type  sticker_set_name: str|unicode


        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._set_chat_sticker_set__make_request(chat_id=chat_id, sticker_set_name=sticker_set_name)
        return self._set_chat_sticker_set__process_result(result)
    # end def set_chat_sticker_set

    def delete_chat_sticker_set(self, chat_id):
        """
        Use this method to delete a group sticker set from a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success.

        https://core.telegram.org/bots/api#deletechatstickerset



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        :type  chat_id: int | str|unicode


        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._delete_chat_sticker_set__make_request(chat_id=chat_id)
        return self._delete_chat_sticker_set__process_result(result)
    # end def delete_chat_sticker_set

    def answer_callback_query(self, callback_query_id, text=None, show_alert=None, url=None, cache_time=None):
        """
        Use this method to send answers to callback queries sent from inline keyboards. The answer will be displayed to the user as a notification at the top of the chat screen or as an alert. On success, True is returned.

        Alternatively, the user can be redirected to the specified Game URL. For this option to work, you must first create a game for your bot via @Botfather and accept the terms. Otherwise, you may use links like t.me/your_bot?start=XXXX that open your bot with a parameter.


        https://core.telegram.org/bots/api#answercallbackquery



        Parameters:

        :param callback_query_id: Unique identifier for the query to be answered
        :type  callback_query_id: str|unicode


        Optional keyword parameters:

        :param text: Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters
        :type  text: str|unicode

        :param show_alert: If true, an alert will be shown by the client instead of a notification at the top of the chat screen. Defaults to false.
        :type  show_alert: bool

        :param url: URL that will be opened by the user's client. If you have created a Game and accepted the conditions via @Botfather, specify the URL that opens your game — note that this will only work if the query comes from a callback_game button.Otherwise, you may use links like t.me/your_bot?start=XXXX that open your bot with a parameter.
        :type  url: str|unicode

        :param cache_time: The maximum amount of time in seconds that the result of the callback query may be cached client-side. Telegram apps will support caching starting in version 3.14. Defaults to 0.
        :type  cache_time: int

        Returns:

        :return: On success, True is returned
        :rtype:  bool
        """
        result = self._answer_callback_query__make_request(callback_query_id=callback_query_id, text=text, show_alert=show_alert, url=url, cache_time=cache_time)
        return self._answer_callback_query__process_result(result)
    # end def answer_callback_query

    def set_my_commands(self, commands):
        """
        Use this method to change the list of the bot's commands. Returns True on success.

        https://core.telegram.org/bots/api#setmycommands



        Parameters:

        :param commands: A JSON-serialized list of bot commands to be set as the list of the bot's commands. At most 100 commands can be specified.
        :type  commands: list of pytgbot.api_types.sendable.command.BotCommand


        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._set_my_commands__make_request(commands=commands)
        return self._set_my_commands__process_result(result)
    # end def set_my_commands

    def get_my_commands(self):
        """
        Use this method to get the current list of the bot's commands. Requires no parameters. Returns Array of BotCommand on success.

        https://core.telegram.org/bots/api#getmycommands



        Returns:

        :return: On success, an array of the commands is returned
        :rtype:  list of pytgbot.api_types.sendable.command.BotCommand
        """
        result = self._get_my_commands__make_request()
        return self._get_my_commands__process_result(result)
    # end def get_my_commands

    def edit_message_text(self, text, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None, entities=None, disable_web_page_preview=None, reply_markup=None):
        """
        Use this method to edit text and game messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.

        https://core.telegram.org/bots/api#editmessagetext



        Parameters:

        :param text: New text of the message, 1-4096 characters after entities parsing
        :type  text: str|unicode


        Optional keyword parameters:

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
        :type  message_id: int

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type  inline_message_id: str|unicode

        :param parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
        :type  parse_mode: str|unicode

        :param entities: List of special entities that appear in message text, which can be specified instead of parse_mode
        :type  entities: list of pytgbot.api_types.receivable.media.MessageEntity

        :param disable_web_page_preview: Disables link previews for links in this message
        :type  disable_web_page_preview: bool

        :param reply_markup: A JSON-serialized object for an inline keyboard.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup

        Returns:

        :return: On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message | bool
        """
        result = self._edit_message_text__make_request(text=text, chat_id=chat_id, message_id=message_id, inline_message_id=inline_message_id, parse_mode=parse_mode, entities=entities, disable_web_page_preview=disable_web_page_preview, reply_markup=reply_markup)
        return self._edit_message_text__process_result(result)
    # end def edit_message_text

    def edit_message_caption(self, chat_id=None, message_id=None, inline_message_id=None, caption=None, parse_mode=None, caption_entities=None, reply_markup=None):
        """
        Use this method to edit captions of messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.

        https://core.telegram.org/bots/api#editmessagecaption



        Optional keyword parameters:

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
        :type  message_id: int

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type  inline_message_id: str|unicode

        :param caption: New caption of the message, 0-1024 characters after entities parsing
        :type  caption: str|unicode

        :param parse_mode: Mode for parsing entities in the message caption. See formatting options for more details.
        :type  parse_mode: str|unicode

        :param caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
        :type  caption_entities: list of pytgbot.api_types.receivable.media.MessageEntity

        :param reply_markup: A JSON-serialized object for an inline keyboard.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup

        Returns:

        :return: On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message | bool
        """
        result = self._edit_message_caption__make_request(chat_id=chat_id, message_id=message_id, inline_message_id=inline_message_id, caption=caption, parse_mode=parse_mode, caption_entities=caption_entities, reply_markup=reply_markup)
        return self._edit_message_caption__process_result(result)
    # end def edit_message_caption

    def edit_message_media(self, media, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        """
        Use this method to edit animation, audio, document, photo, or video messages. If a message is part of a message album, then it can be edited only to an audio for audio albums, only to a document for document albums and to a photo or a video otherwise. When an inline message is edited, a new file can't be uploaded. Use a previously uploaded file via its file_id or specify a URL. On success, if the edited message was sent by the bot, the edited Message is returned, otherwise True is returned.

        https://core.telegram.org/bots/api#editmessagemedia



        Parameters:

        :param media: A JSON-serialized object for a new media content of the message
        :type  media: pytgbot.api_types.sendable.input_media.InputMedia


        Optional keyword parameters:

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
        :type  message_id: int

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type  inline_message_id: str|unicode

        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup

        Returns:

        :return: On success, if the edited message was sent by the bot, the edited Message is returned, otherwise True is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message | bool
        """
        result = self._edit_message_media__make_request(media=media, chat_id=chat_id, message_id=message_id, inline_message_id=inline_message_id, reply_markup=reply_markup)
        return self._edit_message_media__process_result(result)
    # end def edit_message_media

    def edit_message_reply_markup(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        """
        Use this method to edit only the reply markup of messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.

        https://core.telegram.org/bots/api#editmessagereplymarkup



        Optional keyword parameters:

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param message_id: Required if inline_message_id is not specified. Identifier of the message to edit
        :type  message_id: int

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type  inline_message_id: str|unicode

        :param reply_markup: A JSON-serialized object for an inline keyboard.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup

        Returns:

        :return: On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message | bool
        """
        result = self._edit_message_reply_markup__make_request(chat_id=chat_id, message_id=message_id, inline_message_id=inline_message_id, reply_markup=reply_markup)
        return self._edit_message_reply_markup__process_result(result)
    # end def edit_message_reply_markup

    def stop_poll(self, chat_id, message_id, reply_markup=None):
        """
        Use this method to stop a poll which was sent by the bot. On success, the stopped Poll with the final results is returned.

        https://core.telegram.org/bots/api#stoppoll



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param message_id: Identifier of the original message with the poll
        :type  message_id: int


        Optional keyword parameters:

        :param reply_markup: A JSON-serialized object for a new message inline keyboard.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup

        Returns:

        :return: On success, the stopped Poll with the final results is returned
        :rtype:  pytgbot.api_types.receivable.media.Poll
        """
        result = self._stop_poll__make_request(chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
        return self._stop_poll__process_result(result)
    # end def stop_poll

    def delete_message(self, chat_id, message_id):
        """
        Use this method to delete a message, including service messages, with the following limitations:- A message can only be deleted if it was sent less than 48 hours ago.- A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.- Bots can delete outgoing messages in private chats, groups, and supergroups.- Bots can delete incoming messages in private chats.- Bots granted can_post_messages permissions can delete outgoing messages in channels.- If the bot is an administrator of a group, it can delete any message there.- If the bot has can_delete_messages permission in a supergroup or a channel, it can delete any message there.Returns True on success.

        https://core.telegram.org/bots/api#deletemessage



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param message_id: Identifier of the message to delete
        :type  message_id: int


        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._delete_message__make_request(chat_id=chat_id, message_id=message_id)
        return self._delete_message__process_result(result)
    # end def delete_message

    def send_sticker(self, chat_id, sticker, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send static .WEBP or animated .TGS stickers. On success, the sent Message is returned.

        https://core.telegram.org/bots/api#sendsticker



        Parameters:

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
        :type  chat_id: int | str|unicode

        :param sticker: Sticker to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a .WEBP file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files »
        :type  sticker: pytgbot.api_types.sendable.files.InputFile | str|unicode


        Optional keyword parameters:

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardMarkup | pytgbot.api_types.sendable.reply_markup.ReplyKeyboardRemove | pytgbot.api_types.sendable.reply_markup.ForceReply

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_sticker__make_request(chat_id=chat_id, sticker=sticker, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_sticker__process_result(result)
    # end def send_sticker

    def get_sticker_set(self, name):
        """
        Use this method to get a sticker set. On success, a StickerSet object is returned.

        https://core.telegram.org/bots/api#getstickerset



        Parameters:

        :param name: Name of the sticker set
        :type  name: str|unicode


        Returns:

        :return: On success, a StickerSet object is returned
        :rtype:  pytgbot.api_types.receivable.stickers.StickerSet
        """
        result = self._get_sticker_set__make_request(name=name)
        return self._get_sticker_set__process_result(result)
    # end def get_sticker_set

    def upload_sticker_file(self, user_id, png_sticker):
        """
        Use this method to upload a .PNG file with a sticker for later use in createNewStickerSet and addStickerToSet methods (can be used multiple times). Returns the uploaded File on success.

        https://core.telegram.org/bots/api#uploadstickerfile



        Parameters:

        :param user_id: User identifier of sticker file owner
        :type  user_id: int

        :param png_sticker: PNG image with the sticker, must be up to 512 kilobytes in size, dimensions must not exceed 512px, and either width or height must be exactly 512px. More info on Sending Files »
        :type  png_sticker: pytgbot.api_types.sendable.files.InputFile


        Returns:

        :return: Returns the uploaded File on success
        :rtype:  pytgbot.api_types.receivable.media.File
        """
        result = self._upload_sticker_file__make_request(user_id=user_id, png_sticker=png_sticker)
        return self._upload_sticker_file__process_result(result)
    # end def upload_sticker_file

    def create_new_sticker_set(self, user_id, name, title, emojis, png_sticker=None, tgs_sticker=None, contains_masks=None, mask_position=None):
        """
        Use this method to create a new sticker set owned by a user. The bot will be able to edit the sticker set thus created. You must use exactly one of the fields png_sticker or tgs_sticker. Returns True on success.

        https://core.telegram.org/bots/api#createnewstickerset



        Parameters:

        :param user_id: User identifier of created sticker set owner
        :type  user_id: int

        :param name: Short name of sticker set, to be used in t.me/addstickers/ URLs (e.g., animals). Can contain only english letters, digits and underscores. Must begin with a letter, can't contain consecutive underscores and must end in "_by_<bot username>". <bot_username> is case insensitive. 1-64 characters.
        :type  name: str|unicode

        :param title: Sticker set title, 1-64 characters
        :type  title: str|unicode

        :param emojis: One or more emoji corresponding to the sticker
        :type  emojis: str|unicode


        Optional keyword parameters:

        :param png_sticker: PNG image with the sticker, must be up to 512 kilobytes in size, dimensions must not exceed 512px, and either width or height must be exactly 512px. Pass a file_id as a String to send a file that already exists on the Telegram servers, pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files »
        :type  png_sticker: pytgbot.api_types.sendable.files.InputFile | str|unicode

        :param tgs_sticker: TGS animation with the sticker, uploaded using multipart/form-data. See https://core.telegram.org/animated_stickers#technical-requirements for technical requirements
        :type  tgs_sticker: pytgbot.api_types.sendable.files.InputFile

        :param contains_masks: Pass True, if a set of mask stickers should be created
        :type  contains_masks: bool

        :param mask_position: A JSON-serialized object for position where the mask should be placed on faces
        :type  mask_position: pytgbot.api_types.receivable.stickers.MaskPosition

        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._create_new_sticker_set__make_request(user_id=user_id, name=name, title=title, emojis=emojis, png_sticker=png_sticker, tgs_sticker=tgs_sticker, contains_masks=contains_masks, mask_position=mask_position)
        return self._create_new_sticker_set__process_result(result)
    # end def create_new_sticker_set

    def add_sticker_to_set(self, user_id, name, emojis, png_sticker=None, tgs_sticker=None, mask_position=None):
        """
        Use this method to add a new sticker to a set created by the bot. You must use exactly one of the fields png_sticker or tgs_sticker. Animated stickers can be added to animated sticker sets and only to them. Animated sticker sets can have up to 50 stickers. Static sticker sets can have up to 120 stickers. Returns True on success.

        https://core.telegram.org/bots/api#addstickertoset



        Parameters:

        :param user_id: User identifier of sticker set owner
        :type  user_id: int

        :param name: Sticker set name
        :type  name: str|unicode

        :param emojis: One or more emoji corresponding to the sticker
        :type  emojis: str|unicode


        Optional keyword parameters:

        :param png_sticker: PNG image with the sticker, must be up to 512 kilobytes in size, dimensions must not exceed 512px, and either width or height must be exactly 512px. Pass a file_id as a String to send a file that already exists on the Telegram servers, pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files »
        :type  png_sticker: pytgbot.api_types.sendable.files.InputFile | str|unicode

        :param tgs_sticker: TGS animation with the sticker, uploaded using multipart/form-data. See https://core.telegram.org/animated_stickers#technical-requirements for technical requirements
        :type  tgs_sticker: pytgbot.api_types.sendable.files.InputFile

        :param mask_position: A JSON-serialized object for position where the mask should be placed on faces
        :type  mask_position: pytgbot.api_types.receivable.stickers.MaskPosition

        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._add_sticker_to_set__make_request(user_id=user_id, name=name, emojis=emojis, png_sticker=png_sticker, tgs_sticker=tgs_sticker, mask_position=mask_position)
        return self._add_sticker_to_set__process_result(result)
    # end def add_sticker_to_set

    def set_sticker_position_in_set(self, sticker, position):
        """
        Use this method to move a sticker in a set created by the bot to a specific position. Returns True on success.

        https://core.telegram.org/bots/api#setstickerpositioninset



        Parameters:

        :param sticker: File identifier of the sticker
        :type  sticker: str|unicode

        :param position: New sticker position in the set, zero-based
        :type  position: int


        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._set_sticker_position_in_set__make_request(sticker=sticker, position=position)
        return self._set_sticker_position_in_set__process_result(result)
    # end def set_sticker_position_in_set

    def delete_sticker_from_set(self, sticker):
        """
        Use this method to delete a sticker from a set created by the bot. Returns True on success.

        https://core.telegram.org/bots/api#deletestickerfromset



        Parameters:

        :param sticker: File identifier of the sticker
        :type  sticker: str|unicode


        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._delete_sticker_from_set__make_request(sticker=sticker)
        return self._delete_sticker_from_set__process_result(result)
    # end def delete_sticker_from_set

    def set_sticker_set_thumb(self, name, user_id, thumb=None):
        """
        Use this method to set the thumbnail of a sticker set. Animated thumbnails can be set for animated sticker sets only. Returns True on success.

        https://core.telegram.org/bots/api#setstickersetthumb



        Parameters:

        :param name: Sticker set name
        :type  name: str|unicode

        :param user_id: User identifier of the sticker set owner
        :type  user_id: int


        Optional keyword parameters:

        :param thumb: A PNG image with the thumbnail, must be up to 128 kilobytes in size and have width and height exactly 100px, or a TGS animation with the thumbnail up to 32 kilobytes in size; see https://core.telegram.org/animated_stickers#technical-requirements for animated sticker technical requirements. Pass a file_id as a String to send a file that already exists on the Telegram servers, pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files ». Animated sticker set thumbnail can't be uploaded via HTTP URL.
        :type  thumb: pytgbot.api_types.sendable.files.InputFile | str|unicode

        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._set_sticker_set_thumb__make_request(name=name, user_id=user_id, thumb=thumb)
        return self._set_sticker_set_thumb__process_result(result)
    # end def set_sticker_set_thumb

    def answer_inline_query(self, inline_query_id, results, cache_time=None, is_personal=None, next_offset=None, switch_pm_text=None, switch_pm_parameter=None):
        """
        Use this method to send answers to an inline query. On success, True is returned.No more than 50 results per query are allowed.

        https://core.telegram.org/bots/api#answerinlinequery



        Parameters:

        :param inline_query_id: Unique identifier for the answered query
        :type  inline_query_id: str|unicode

        :param results: A JSON-serialized array of results for the inline query
        :type  results: list of pytgbot.api_types.sendable.inline.InlineQueryResult


        Optional keyword parameters:

        :param cache_time: The maximum amount of time in seconds that the result of the inline query may be cached on the server. Defaults to 300.
        :type  cache_time: int

        :param is_personal: Pass True, if results may be cached on the server side only for the user that sent the query. By default, results may be returned to any user who sends the same query
        :type  is_personal: bool

        :param next_offset: Pass the offset that a client should send in the next query with the same text to receive more results. Pass an empty string if there are no more results or if you don't support pagination. Offset length can't exceed 64 bytes.
        :type  next_offset: str|unicode

        :param switch_pm_text: If passed, clients will display a button with specified text that switches the user to a private chat with the bot and sends the bot a start message with the parameter switch_pm_parameter
        :type  switch_pm_text: str|unicode

        :param switch_pm_parameter: Deep-linking parameter for the /start message sent to the bot when user presses the switch button. 1-64 characters, only A-Z, a-z, 0-9, _ and - are allowed.Example: An inline bot that sends YouTube videos can ask the user to connect the bot to their YouTube account to adapt search results accordingly. To do this, it displays a 'Connect your YouTube account' button above the results, or even before showing any. The user presses the button, switches to a private chat with the bot and, in doing so, passes a start parameter that instructs the bot to return an oauth link. Once done, the bot can offer a switch_inline button so that the user can easily return to the chat where they wanted to use the bot's inline capabilities.
        :type  switch_pm_parameter: str|unicode

        Returns:

        :return: On success, True is returned
        :rtype:  bool
        """
        result = self._answer_inline_query__make_request(inline_query_id=inline_query_id, results=results, cache_time=cache_time, is_personal=is_personal, next_offset=next_offset, switch_pm_text=switch_pm_text, switch_pm_parameter=switch_pm_parameter)
        return self._answer_inline_query__process_result(result)
    # end def answer_inline_query

    def send_invoice(self, chat_id, title, description, payload, provider_token, start_parameter, currency, prices, provider_data=None, photo_url=None, photo_size=None, photo_width=None, photo_height=None, need_name=None, need_phone_number=None, need_email=None, need_shipping_address=None, send_phone_number_to_provider=None, send_email_to_provider=None, is_flexible=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send invoices. On success, the sent Message is returned.

        https://core.telegram.org/bots/api#sendinvoice



        Parameters:

        :param chat_id: Unique identifier for the target private chat
        :type  chat_id: int

        :param title: Product name, 1-32 characters
        :type  title: str|unicode

        :param description: Product description, 1-255 characters
        :type  description: str|unicode

        :param payload: Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use for your internal processes.
        :type  payload: str|unicode

        :param provider_token: Payments provider token, obtained via Botfather
        :type  provider_token: str|unicode

        :param start_parameter: Unique deep-linking parameter that can be used to generate this invoice when used as a start parameter
        :type  start_parameter: str|unicode

        :param currency: Three-letter ISO 4217 currency code, see more on currencies
        :type  currency: str|unicode

        :param prices: Price breakdown, a JSON-serialized list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.)
        :type  prices: list of pytgbot.api_types.sendable.payments.LabeledPrice


        Optional keyword parameters:

        :param provider_data: A JSON-serialized data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.
        :type  provider_data: str|unicode

        :param photo_url: URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service. People like it better when they see what they are paying for.
        :type  photo_url: str|unicode

        :param photo_size: Photo size
        :type  photo_size: int

        :param photo_width: Photo width
        :type  photo_width: int

        :param photo_height: Photo height
        :type  photo_height: int

        :param need_name: Pass True, if you require the user's full name to complete the order
        :type  need_name: bool

        :param need_phone_number: Pass True, if you require the user's phone number to complete the order
        :type  need_phone_number: bool

        :param need_email: Pass True, if you require the user's email address to complete the order
        :type  need_email: bool

        :param need_shipping_address: Pass True, if you require the user's shipping address to complete the order
        :type  need_shipping_address: bool

        :param send_phone_number_to_provider: Pass True, if user's phone number should be sent to provider
        :type  send_phone_number_to_provider: bool

        :param send_email_to_provider: Pass True, if user's email address should be sent to provider
        :type  send_email_to_provider: bool

        :param is_flexible: Pass True, if the final price depends on the shipping method
        :type  is_flexible: bool

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Pay total price' button will be shown. If not empty, the first button must be a Pay button.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_invoice__make_request(chat_id=chat_id, title=title, description=description, payload=payload, provider_token=provider_token, start_parameter=start_parameter, currency=currency, prices=prices, provider_data=provider_data, photo_url=photo_url, photo_size=photo_size, photo_width=photo_width, photo_height=photo_height, need_name=need_name, need_phone_number=need_phone_number, need_email=need_email, need_shipping_address=need_shipping_address, send_phone_number_to_provider=send_phone_number_to_provider, send_email_to_provider=send_email_to_provider, is_flexible=is_flexible, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_invoice__process_result(result)
    # end def send_invoice

    def answer_shipping_query(self, shipping_query_id, ok, shipping_options=None, error_message=None):
        """
        If you sent an invoice requesting a shipping address and the parameter is_flexible was specified, the Bot API will send an Update with a shipping_query field to the bot. Use this method to reply to shipping queries. On success, True is returned.

        https://core.telegram.org/bots/api#answershippingquery



        Parameters:

        :param shipping_query_id: Unique identifier for the query to be answered
        :type  shipping_query_id: str|unicode

        :param ok: Specify True if delivery to the specified address is possible and False if there are any problems (for example, if delivery to the specified address is not possible)
        :type  ok: bool


        Optional keyword parameters:

        :param shipping_options: Required if ok is True. A JSON-serialized array of available shipping options.
        :type  shipping_options: list of pytgbot.api_types.sendable.payments.ShippingOption

        :param error_message: Required if ok is False. Error message in human readable form that explains why it is impossible to complete the order (e.g. "Sorry, delivery to your desired address is unavailable'). Telegram will display this message to the user.
        :type  error_message: str|unicode

        Returns:

        :return: On success, True is returned
        :rtype:  bool
        """
        result = self._answer_shipping_query__make_request(shipping_query_id=shipping_query_id, ok=ok, shipping_options=shipping_options, error_message=error_message)
        return self._answer_shipping_query__process_result(result)
    # end def answer_shipping_query

    def answer_pre_checkout_query(self, pre_checkout_query_id, ok, error_message=None):
        """
        Once the user has confirmed their payment and shipping details, the Bot API sends the final confirmation in the form of an Update with the field pre_checkout_query. Use this method to respond to such pre-checkout queries. On success, True is returned. Note: The Bot API must receive an answer within 10 seconds after the pre-checkout query was sent.

        https://core.telegram.org/bots/api#answerprecheckoutquery



        Parameters:

        :param pre_checkout_query_id: Unique identifier for the query to be answered
        :type  pre_checkout_query_id: str|unicode

        :param ok: Specify True if everything is alright (goods are available, etc.) and the bot is ready to proceed with the order. Use False if there are any problems.
        :type  ok: bool


        Optional keyword parameters:

        :param error_message: Required if ok is False. Error message in human readable form that explains the reason for failure to proceed with the checkout (e.g. "Sorry, somebody just bought the last of our amazing black T-shirts while you were busy filling out your payment details. Please choose a different color or garment!"). Telegram will display this message to the user.
        :type  error_message: str|unicode

        Returns:

        :return: On success, True is returned
        :rtype:  bool
        """
        result = self._answer_pre_checkout_query__make_request(pre_checkout_query_id=pre_checkout_query_id, ok=ok, error_message=error_message)
        return self._answer_pre_checkout_query__process_result(result)
    # end def answer_pre_checkout_query

    def set_passport_data_errors(self, user_id, errors):
        """
        Informs a user that some of the Telegram Passport elements they provided contains errors. The user will not be able to re-submit their Passport to you until the errors are fixed (the contents of the field for which you returned the error must change). Returns True on success.
        Use this if the data submitted by the user doesn't satisfy the standards your service requires for any reason. For example, if a birthday date seems invalid, a submitted document is blurry, a scan shows evidence of tampering, etc. Supply some details in the error message to make sure the user knows how to correct the issues.

        https://core.telegram.org/bots/api#setpassportdataerrors



        Parameters:

        :param user_id: User identifier
        :type  user_id: int

        :param errors: A JSON-serialized array describing the errors
        :type  errors: list of pytgbot.api_types.sendable.passport.PassportElementError


        Returns:

        :return: Returns True on success
        :rtype:  bool
        """
        result = self._set_passport_data_errors__make_request(user_id=user_id, errors=errors)
        return self._set_passport_data_errors__process_result(result)
    # end def set_passport_data_errors

    def send_game(self, chat_id, game_short_name, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None):
        """
        Use this method to send a game. On success, the sent Message is returned.

        https://core.telegram.org/bots/api#sendgame



        Parameters:

        :param chat_id: Unique identifier for the target chat
        :type  chat_id: int

        :param game_short_name: Short name of the game, serves as the unique identifier for the game. Set up your games via Botfather.
        :type  game_short_name: str|unicode


        Optional keyword parameters:

        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :type  disable_notification: bool

        :param reply_to_message_id: If the message is a reply, ID of the original message
        :type  reply_to_message_id: int

        :param allow_sending_without_reply: Pass True, if the message should be sent even if the specified replied-to message is not found
        :type  allow_sending_without_reply: bool

        :param reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Play game_title' button will be shown. If not empty, the first button must launch the game.
        :type  reply_markup: pytgbot.api_types.sendable.reply_markup.InlineKeyboardMarkup

        Returns:

        :return: On success, the sent Message is returned
        :rtype:  pytgbot.api_types.receivable.updates.Message
        """
        result = self._send_game__make_request(chat_id=chat_id, game_short_name=game_short_name, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id, allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)
        return self._send_game__process_result(result)
    # end def send_game

    def set_game_score(self, user_id, score, force=None, disable_edit_message=None, chat_id=None, message_id=None, inline_message_id=None):
        """
        Use this method to set the score of the specified user in a game. On success, if the message was sent by the bot, returns the edited Message, otherwise returns True. Returns an error, if the new score is not greater than the user's current score in the chat and force is False.

        https://core.telegram.org/bots/api#setgamescore



        Parameters:

        :param user_id: User identifier
        :type  user_id: int

        :param score: New score, must be non-negative
        :type  score: int


        Optional keyword parameters:

        :param force: Pass True, if the high score is allowed to decrease. This can be useful when fixing mistakes or banning cheaters
        :type  force: bool

        :param disable_edit_message: Pass True, if the game message should not be automatically edited to include the current scoreboard
        :type  disable_edit_message: bool

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat
        :type  chat_id: int

        :param message_id: Required if inline_message_id is not specified. Identifier of the sent message
        :type  message_id: int

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type  inline_message_id: str|unicode

        Returns:

        :return: On success, if the message was sent by the bot, returns the edited Message, otherwise returns True
        :rtype:  pytgbot.api_types.receivable.updates.Message | bool
        """
        result = self._set_game_score__make_request(user_id=user_id, score=score, force=force, disable_edit_message=disable_edit_message, chat_id=chat_id, message_id=message_id, inline_message_id=inline_message_id)
        return self._set_game_score__process_result(result)
    # end def set_game_score

    def get_game_high_scores(self, user_id, chat_id=None, message_id=None, inline_message_id=None):
        """
        Use this method to get data for high score tables. Will return the score of the specified user and several of their neighbors in a game. On success, returns an Array of GameHighScore objects.

        This method will currently return scores for the target user, plus two of their closest neighbors on each side. Will also return the top three users if the user and his neighbors are not among them. Please note that this behavior is subject to change.


        https://core.telegram.org/bots/api#getgamehighscores



        Parameters:

        :param user_id: Target user id
        :type  user_id: int


        Optional keyword parameters:

        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat
        :type  chat_id: int

        :param message_id: Required if inline_message_id is not specified. Identifier of the sent message
        :type  message_id: int

        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message
        :type  inline_message_id: str|unicode

        Returns:

        :return: On success, returns an Array of GameHighScore objects
        :rtype:  list of pytgbot.api_types.receivable.game.GameHighScore
        """
        result = self._get_game_high_scores__make_request(user_id=user_id, chat_id=chat_id, message_id=message_id, inline_message_id=inline_message_id)
        return self._get_game_high_scores__process_result(result)
    # end def get_game_high_scores
    # end of generated functions
# end class Bot

# allow importing the bot as `pytgbot.bot.syncrounous.Bot`.
Bot = SyncBot
