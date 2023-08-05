from .attachment import Attachment
from .customheader import CustomHeader
from .emailaddress import EmailAddress
from .messagebase import MessageBase


class BasicMessage(MessageBase):
    """
    A basic email message similar to one created in a personal email client such as Outlook.
    This message can have many recipients of different types, such as To, CC, and BCC.  This
    message does not support merge fields.

    :Example:

        message = BasicMessage()

        message.subject = "Sending A Test Message (Basic Send)"
        message.html_body = "<html><body>" \
                    "<h1>Sending A Test Message</h1>" \
                    "<p>This is the Html Body of my message.</p>" \
                    "</body></html>"
        message.plain_text_body = "This is the Plain Text Body of my message."

        message.from_email_address = EmailAddress("from@example.com")
        message.reply_to = EmailAddress("replyto@example.com")

        message.add_to_email_address("recipient1@example.com")
        message.add_to_email_address("recipient2@example.com", "Recipient #1")
        message.add_to_email_address(EmailAddress("recipient3@example.com"))
        message.add_to_email_address(EmailAddress("recipient4@example.com", "Recipient #4"))

    """
    
    def __init__(self):
        self._subject = None
        self._plain_text_body = None
        self._html_body = None
        self._amp_body = None
        self._api_template = None
        self._mailing_id = None
        self._message_id = None
        self._charset = None
        self._from_email = None
        self._reply_to = None
        self._attachments = []
        self._custom_headers = []
        self._to_recipients = []
        self._cc_recipients = []
        self._bcc_recipients = []

    @property
    def to_email_address(self):
        """
        Set the To EmailAddress list
        :return list of EmailAddress
        :rtype list
        """
        return self._to_recipients

    @to_email_address.setter
    def to_email_address(self, val: list):
        """
        Get the To EmailAddress list
        :param val: list of EmailAddress
        :rtype val: list
        """
        self._to_recipients = []
        if val is not None:
            for item in val:
                if isinstance(item, EmailAddress):
                    self._to_recipients.append(item)

    def add_to_email_address(self, email_address, friendly_name: str=None):
        """
        Add an EmailAddress to the To recipient list.
        :param email_address: the email address
        :type email_address: object
        :param friendly_name: the recipients friendly name
        :type friendly_name: str
        """
        if isinstance(email_address, EmailAddress):
            self._to_recipients.append(email_address)

        if isinstance(email_address, str):
            self._to_recipients.append(EmailAddress(email_address, friendly_name))

    @property
    def cc_email_address(self):
        """
        Set the CC EmailAddress list
        :return list of EmailAddress
        :rtype list
        """
        return self._cc_recipients

    @cc_email_address.setter
    def cc_email_address(self, val: list):
        """
        Set the CC EmailAddress list
        :param val: list of EmailAddress
        :rtype val: list
        """
        self._cc_recipients = []
        if val is not None:
            for item in val:
                if isinstance(item, EmailAddress):
                    self._cc_recipients.append(item)

    def add_cc_email_address(self, email_address, friendly_name: str = None):
        """
        Add an EmailAddress to the CC recipient list.
        :param email_address: the email address
        :type email_address: object
        :param friendly_name: the recipients friendly name
        :type friendly_name: str
        """
        if isinstance(email_address, EmailAddress):
            self._cc_recipients.append(email_address)

        if isinstance(email_address, str):
            self._cc_recipients.append(EmailAddress(email_address, friendly_name))

    @property
    def bcc_email_address(self):
        """
        Set the BCC EmailAddress list
        :return list of EmailAddress
        :rtype list
        """
        return self._bcc_recipients

    @bcc_email_address.setter
    def bcc_email_address(self, val: list):
        """
        Set the BCC EmailAddress list
        :return list of EmailAddress
        :rtype list
        """
        self._bcc_recipients = []
        if val is not None:
            for item in val:
                if isinstance(item, EmailAddress):
                    self._bcc_recipients.append(item)

    def add_bcc_email_address(self, email_address, friendly_name: str = None):
        """
        Add an EmailAddress to the BCC recipient list.
        :param email_address: the email address
        :type email_address: object
        :param friendly_name: the recipients friendly name
        :type friendly_name: str
        """
        if isinstance(email_address, EmailAddress):
            self._bcc_recipients.append(email_address)

        if isinstance(email_address, str):
            self._bcc_recipients.append(EmailAddress(email_address, friendly_name))

    """
    interface properties
    """

    @property
    def subject(self):
        """
        Get the message subject.
        :return the subject
        :rtype str
        """
        return self._subject

    @subject.setter
    def subject(self, val: str):
        """
        Set the message subject.
        :param val: the subject
        :type val: str
        """
        self._subject = val

    @property
    def plain_text_body(self):
        """
        Get the plain text portion of the message body.
        (Optional) Either TextBody or HtmlBody must be used with the AmpBody or use a ApiTemplate
        :return the plain text body
        :rtype str
        """
        return self._plain_text_body

    @plain_text_body.setter
    def plain_text_body(self, val: str):
        """
        Set the plain text portion of the message body.
        (Optional) Either TextBody or HtmlBody must be used with the AmpBody or use a ApiTemplate
        :param val: the plain text body
        :type val: str
        """
        self._plain_text_body = val

    @property
    def html_body(self):
        """
        Get the HTML portion of the message body.
        (Optional) Either TextBody or HtmlBody must be used with the AmpBody or use a ApiTemplate
        :return the HTML body
        :rtype str
        """
        return self._html_body

    @html_body.setter
    def html_body(self, val: str):
        """
        Set the HTML portion of the message body.
        (Optional) Either TextBody or HtmlBody must be used with the AmpBody or use a ApiTemplate
        :param val: the HTML body
        :type val: str
        """
        self._html_body = val

    @property
    def amp_body(self):
        """
        Get the AMP portion of the message body.
        (Optional) Either TextBody or HtmlBody must be used with the AmpBody or use a ApiTemplate
        :return the AMP body
        :rtype str
        """
        return self._amp_body

    @amp_body.setter
    def amp_body(self, val: str):
        """
        Set the AMP portion of the message body.
        (Optional) Either TextBody or HtmlBody must be used with the AmpBody or use a ApiTemplate
        :param val: the AMP body
        :type val: str
        """
        self._amp_body = val

    @property
    def api_template(self):
        """
        Get the api template.
        (Optional) Either TextBody or HtmlBody must be used with the AmpBody or use a ApiTemplate
        :return the api template
        :rtype str
        """
        return self._api_template

    @api_template.setter
    def api_template(self, val: str):
        """
        Set the api template.
        (Optional) Either TextBody or HtmlBody must be used with the AmpBody or use a ApiTemplate
        :param val: the api template
        :rtype str
        """
        self._api_template = val

    @property
    def mailing_id(self):
        """
        Get the custom mailing id.
        See https://www.injectionapi.com/blog/best-practices-for-using-custom-mailingids-and-messageids/
        for more information.
        :return the mailing id
        :rtype str
        """
        return self._mailing_id

    @mailing_id.setter
    def mailing_id(self, val: str):
        """
        Set the custom mailing id.
        :param val: the mailing id
        :type val: str
        """
        self._mailing_id = val

    @property
    def message_id(self):
        """
        Get the custom message id.
        See https://www.injectionapi.com/blog/best-practices-for-using-custom-mailingids-and-messageids/
        for more information.
        :return the message id
        :rtype str
        """
        return self._message_id

    @message_id.setter
    def message_id(self, val: str):
        """
        Set the custom message id.
        :param val: the message id
        :type val: str
        """
        self._message_id = val

    @property
    def charset(self):
        """
        Get the optional character set. Default is UTF-8
        :return the character set
        :rtype str
        """
        return self._charset

    @charset.setter
    def charset(self, val: str):
        """
        Set the optional character set. Default is UTF-8
        :param val: the character set
        :type val: str
        """
        self._charset = val

    @property
    def from_email_address(self):
        """
        Get the from email address.
        :return EmailAddress
        :rtype EmailAddress
        """
        return self._from_email

    @from_email_address.setter
    def from_email_address(self, val: EmailAddress):
        """
        Set the from email address.
        :param val: EmailAddress
        :type val: EmailAddress
        """
        self._from_email = val

    @property
    def reply_to_email_address(self):
        """
        Get the optional reply to email address
        :return EmailAddress
        :rtype EmailAddress
        """
        return self._reply_to

    @reply_to_email_address.setter
    def reply_to_email_address(self, val: EmailAddress):
        """
        Set the optional reply to email address.
        :param val: EmailAddress
        :type val: EmailAddress
        """
        self._reply_to = val

    @property
    def attachments(self):
        """
        Get the list of Attachments.
        :returns: List of Attachment objects.
        :rtype list
        """
        return self._attachments

    @attachments.setter
    def attachments(self, val: list):
        """
        Set the list of Attachments.
        :param val: list of Attachment
        :type val: list
        """
        self._attachments = []
        if val is not None:
            for item in val:
                if isinstance(item, Attachment):
                    self._attachments.append(item)

    def add_attachment(self, val: Attachment):
        """
        Add an Attachment to the attachments list.
        :param val: list of Attachment
        :type val: list
        """
        self._attachments.append(val)

    @property
    def custom_headers(self):
        """
        Get the list of CustomHeaders.
        :return list of CustomHeader
        :rtype list
        """
        return self._custom_headers

    @custom_headers.setter
    def custom_headers(self, val: list):
        """
        Set the list of CustomHeaders.
        :param val: list of CustomHeader
        :type val: list
        """
        self._custom_headers = []
        if val is not None:
            for item in val:
                if isinstance(item, CustomHeader):
                    self._custom_headers.append(item)

    def add_custom_header(self, header, val: str = None):
        """
        Add a CustomHeader to the attachment
        :param header: the CustomHeader. CustomHeader, dict, and string is allowed
        :type header: CustomHeader, dict, str
        :param val: the custom header value, required if header is str
        :type val: str
        """
        if isinstance(header, CustomHeader):
            self._custom_headers.append(header)
        if isinstance(header, str):
            self._custom_headers.append(CustomHeader(header, val))
        if isinstance(header, dict):
            for name, value in header.items():
                self._custom_headers.append(CustomHeader(name, value))

    def __str__(self):
        """
        Represents the BasicMessage as a string (# of recipients & subject)
        :return the string
        :rtype str
        """
        return "Recipients: {count}, Subject: '{subject}'"\
            .format(
                count=len(self._to_recipients),
                subject=str(self._subject))
