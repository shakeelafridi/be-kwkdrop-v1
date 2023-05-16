# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import serialize
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page
from twilio.rest.api.v2010.account.call.event import EventList
from twilio.rest.api.v2010.account.call.feedback import FeedbackList
from twilio.rest.api.v2010.account.call.feedback_summary import FeedbackSummaryList
from twilio.rest.api.v2010.account.call.notification import NotificationList
from twilio.rest.api.v2010.account.call.payment import PaymentList
from twilio.rest.api.v2010.account.call.recording import RecordingList


class CallList(ListResource):

    def __init__(self, version, account_sid):
        """
        Initialize the CallList

        :param Version version: Version that contains the resource
        :param account_sid: The SID of the Account that created this resource

        :returns: twilio.rest.api.v2010.account.call.CallList
        :rtype: twilio.rest.api.v2010.account.call.CallList
        """
        super(CallList, self).__init__(version)

        # Path Solution
        self._solution = {'account_sid': account_sid, }
        self._uri = '/Accounts/{account_sid}/Calls.json'.format(**self._solution)

        # Components
        self._feedback_summaries = None

    def create(self, to, from_, method=values.unset, fallback_url=values.unset,
               fallback_method=values.unset, status_callback=values.unset,
               status_callback_event=values.unset,
               status_callback_method=values.unset, send_digits=values.unset,
               timeout=values.unset, record=values.unset,
               recording_channels=values.unset,
               recording_status_callback=values.unset,
               recording_status_callback_method=values.unset,
               sip_auth_username=values.unset, sip_auth_password=values.unset,
               machine_detection=values.unset,
               machine_detection_timeout=values.unset,
               recording_status_callback_event=values.unset, trim=values.unset,
               caller_id=values.unset,
               machine_detection_speech_threshold=values.unset,
               machine_detection_speech_end_threshold=values.unset,
               machine_detection_silence_timeout=values.unset,
               async_amd=values.unset, async_amd_status_callback=values.unset,
               async_amd_status_callback_method=values.unset, byoc=values.unset,
               call_reason=values.unset, call_token=values.unset,
               recording_track=values.unset, time_limit=values.unset,
               url=values.unset, twiml=values.unset, application_sid=values.unset):
        """
        Create the CallInstance

        :param unicode to: Phone number, SIP address, or client identifier to call
        :param unicode from_: Twilio number from which to originate the call
        :param unicode method: HTTP method to use to fetch TwiML
        :param unicode fallback_url: Fallback URL in case of error
        :param unicode fallback_method: HTTP Method to use with fallback_url
        :param unicode status_callback: The URL we should call to send status information to your application
        :param list[unicode] status_callback_event: The call progress events that we send to the `status_callback` URL.
        :param unicode status_callback_method: HTTP Method to use with status_callback
        :param unicode send_digits: The digits to dial after connecting to the number
        :param unicode timeout: Number of seconds to wait for an answer
        :param bool record: Whether to record the call
        :param unicode recording_channels: The number of channels in the final recording
        :param unicode recording_status_callback: The URL that we call when the recording is available to be accessed
        :param unicode recording_status_callback_method: The HTTP method we should use when calling the `recording_status_callback` URL
        :param unicode sip_auth_username: The username used to authenticate the caller making a SIP call
        :param unicode sip_auth_password: The password required to authenticate the user account specified in `sip_auth_username`.
        :param unicode machine_detection: Enable machine detection or end of greeting detection
        :param unicode machine_detection_timeout: Number of seconds to wait for machine detection
        :param list[unicode] recording_status_callback_event: The recording status events that will trigger calls to the URL specified in `recording_status_callback`
        :param unicode trim: Set this parameter to control trimming of silence on the recording.
        :param unicode caller_id: The phone number, SIP address, or Client identifier that made this call. Phone numbers are in E.164 format (e.g., +16175551212). SIP addresses are formatted as `name@company.com`.
        :param unicode machine_detection_speech_threshold: Number of milliseconds for measuring stick for the length of the speech activity
        :param unicode machine_detection_speech_end_threshold: Number of milliseconds of silence after speech activity
        :param unicode machine_detection_silence_timeout: Number of milliseconds of initial silence
        :param unicode async_amd: Enable asynchronous AMD
        :param unicode async_amd_status_callback: The URL we should call to send amd status information to your application
        :param unicode async_amd_status_callback_method: HTTP Method to use with async_amd_status_callback
        :param unicode byoc: BYOC trunk SID (Beta)
        :param unicode call_reason: Reason for the call (Branded Calls Beta)
        :param unicode call_token: A token string needed to invoke a forwarded call with a caller-id recieved on a previous incoming call
        :param unicode recording_track: Which track(s) to record
        :param unicode time_limit: The maximum duration of the call in seconds.
        :param unicode url: The absolute URL that returns TwiML for this call
        :param unicode twiml: TwiML instructions for the call
        :param unicode application_sid: The SID of the Application resource that will handle the call

        :returns: The created CallInstance
        :rtype: twilio.rest.api.v2010.account.call.CallInstance
        """
        data = values.of({
            'To': to,
            'From': from_,
            'Url': url,
            'Twiml': twiml,
            'ApplicationSid': application_sid,
            'Method': method,
            'FallbackUrl': fallback_url,
            'FallbackMethod': fallback_method,
            'StatusCallback': status_callback,
            'StatusCallbackEvent': serialize.map(status_callback_event, lambda e: e),
            'StatusCallbackMethod': status_callback_method,
            'SendDigits': send_digits,
            'Timeout': timeout,
            'Record': record,
            'RecordingChannels': recording_channels,
            'RecordingStatusCallback': recording_status_callback,
            'RecordingStatusCallbackMethod': recording_status_callback_method,
            'SipAuthUsername': sip_auth_username,
            'SipAuthPassword': sip_auth_password,
            'MachineDetection': machine_detection,
            'MachineDetectionTimeout': machine_detection_timeout,
            'RecordingStatusCallbackEvent': serialize.map(recording_status_callback_event, lambda e: e),
            'Trim': trim,
            'CallerId': caller_id,
            'MachineDetectionSpeechThreshold': machine_detection_speech_threshold,
            'MachineDetectionSpeechEndThreshold': machine_detection_speech_end_threshold,
            'MachineDetectionSilenceTimeout': machine_detection_silence_timeout,
            'AsyncAmd': async_amd,
            'AsyncAmdStatusCallback': async_amd_status_callback,
            'AsyncAmdStatusCallbackMethod': async_amd_status_callback_method,
            'Byoc': byoc,
            'CallReason': call_reason,
            'CallToken': call_token,
            'RecordingTrack': recording_track,
            'TimeLimit': time_limit,
        })

        payload = self._version.create(method='POST', uri=self._uri, data=data, )

        return CallInstance(self._version, payload, account_sid=self._solution['account_sid'], )

    def stream(self, to=values.unset, from_=values.unset,
               parent_call_sid=values.unset, status=values.unset,
               start_time_before=values.unset, start_time=values.unset,
               start_time_after=values.unset, end_time_before=values.unset,
               end_time=values.unset, end_time_after=values.unset, limit=None,
               page_size=None):
        """
        Streams CallInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param unicode to: Phone number or Client identifier of calls to include
        :param unicode from_: Phone number or Client identifier to filter `from` on
        :param unicode parent_call_sid: Parent call SID to filter on
        :param CallInstance.Status status: The status of the resources to read
        :param datetime start_time_before: Only include calls that started on this date
        :param datetime start_time: Only include calls that started on this date
        :param datetime start_time_after: Only include calls that started on this date
        :param datetime end_time_before: Only include calls that ended on this date
        :param datetime end_time: Only include calls that ended on this date
        :param datetime end_time_after: Only include calls that ended on this date
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.call.CallInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(
            to=to,
            from_=from_,
            parent_call_sid=parent_call_sid,
            status=status,
            start_time_before=start_time_before,
            start_time=start_time,
            start_time_after=start_time_after,
            end_time_before=end_time_before,
            end_time=end_time,
            end_time_after=end_time_after,
            page_size=limits['page_size'],
        )

        return self._version.stream(page, limits['limit'])

    def list(self, to=values.unset, from_=values.unset,
             parent_call_sid=values.unset, status=values.unset,
             start_time_before=values.unset, start_time=values.unset,
             start_time_after=values.unset, end_time_before=values.unset,
             end_time=values.unset, end_time_after=values.unset, limit=None,
             page_size=None):
        """
        Lists CallInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param unicode to: Phone number or Client identifier of calls to include
        :param unicode from_: Phone number or Client identifier to filter `from` on
        :param unicode parent_call_sid: Parent call SID to filter on
        :param CallInstance.Status status: The status of the resources to read
        :param datetime start_time_before: Only include calls that started on this date
        :param datetime start_time: Only include calls that started on this date
        :param datetime start_time_after: Only include calls that started on this date
        :param datetime end_time_before: Only include calls that ended on this date
        :param datetime end_time: Only include calls that ended on this date
        :param datetime end_time_after: Only include calls that ended on this date
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.call.CallInstance]
        """
        return list(self.stream(
            to=to,
            from_=from_,
            parent_call_sid=parent_call_sid,
            status=status,
            start_time_before=start_time_before,
            start_time=start_time,
            start_time_after=start_time_after,
            end_time_before=end_time_before,
            end_time=end_time,
            end_time_after=end_time_after,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, to=values.unset, from_=values.unset,
             parent_call_sid=values.unset, status=values.unset,
             start_time_before=values.unset, start_time=values.unset,
             start_time_after=values.unset, end_time_before=values.unset,
             end_time=values.unset, end_time_after=values.unset,
             page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of CallInstance records from the API.
        Request is executed immediately

        :param unicode to: Phone number or Client identifier of calls to include
        :param unicode from_: Phone number or Client identifier to filter `from` on
        :param unicode parent_call_sid: Parent call SID to filter on
        :param CallInstance.Status status: The status of the resources to read
        :param datetime start_time_before: Only include calls that started on this date
        :param datetime start_time: Only include calls that started on this date
        :param datetime start_time_after: Only include calls that started on this date
        :param datetime end_time_before: Only include calls that ended on this date
        :param datetime end_time: Only include calls that ended on this date
        :param datetime end_time_after: Only include calls that ended on this date
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of CallInstance
        :rtype: twilio.rest.api.v2010.account.call.CallPage
        """
        data = values.of({
            'To': to,
            'From': from_,
            'ParentCallSid': parent_call_sid,
            'Status': status,
            'StartTime<': serialize.iso8601_datetime(start_time_before),
            'StartTime': serialize.iso8601_datetime(start_time),
            'StartTime>': serialize.iso8601_datetime(start_time_after),
            'EndTime<': serialize.iso8601_datetime(end_time_before),
            'EndTime': serialize.iso8601_datetime(end_time),
            'EndTime>': serialize.iso8601_datetime(end_time_after),
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(method='GET', uri=self._uri, params=data, )

        return CallPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of CallInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of CallInstance
        :rtype: twilio.rest.api.v2010.account.call.CallPage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return CallPage(self._version, response, self._solution)

    @property
    def feedback_summaries(self):
        """
        Access the feedback_summaries

        :returns: twilio.rest.api.v2010.account.call.feedback_summary.FeedbackSummaryList
        :rtype: twilio.rest.api.v2010.account.call.feedback_summary.FeedbackSummaryList
        """
        if self._feedback_summaries is None:
            self._feedback_summaries = FeedbackSummaryList(
                self._version,
                account_sid=self._solution['account_sid'],
            )
        return self._feedback_summaries

    def get(self, sid):
        """
        Constructs a CallContext

        :param sid: The SID of the Call resource to fetch

        :returns: twilio.rest.api.v2010.account.call.CallContext
        :rtype: twilio.rest.api.v2010.account.call.CallContext
        """
        return CallContext(self._version, account_sid=self._solution['account_sid'], sid=sid, )

    def __call__(self, sid):
        """
        Constructs a CallContext

        :param sid: The SID of the Call resource to fetch

        :returns: twilio.rest.api.v2010.account.call.CallContext
        :rtype: twilio.rest.api.v2010.account.call.CallContext
        """
        return CallContext(self._version, account_sid=self._solution['account_sid'], sid=sid, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.CallList>'


class CallPage(Page):

    def __init__(self, version, response, solution):
        """
        Initialize the CallPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param account_sid: The SID of the Account that created this resource

        :returns: twilio.rest.api.v2010.account.call.CallPage
        :rtype: twilio.rest.api.v2010.account.call.CallPage
        """
        super(CallPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of CallInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.api.v2010.account.call.CallInstance
        :rtype: twilio.rest.api.v2010.account.call.CallInstance
        """
        return CallInstance(self._version, payload, account_sid=self._solution['account_sid'], )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.CallPage>'


class CallContext(InstanceContext):

    def __init__(self, version, account_sid, sid):
        """
        Initialize the CallContext

        :param Version version: Version that contains the resource
        :param account_sid: The SID of the Account that created the resource(s) to fetch
        :param sid: The SID of the Call resource to fetch

        :returns: twilio.rest.api.v2010.account.call.CallContext
        :rtype: twilio.rest.api.v2010.account.call.CallContext
        """
        super(CallContext, self).__init__(version)

        # Path Solution
        self._solution = {'account_sid': account_sid, 'sid': sid, }
        self._uri = '/Accounts/{account_sid}/Calls/{sid}.json'.format(**self._solution)

        # Dependents
        self._recordings = None
        self._notifications = None
        self._feedback = None
        self._events = None
        self._payments = None

    def delete(self):
        """
        Deletes the CallInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete(method='DELETE', uri=self._uri, )

    def fetch(self):
        """
        Fetch the CallInstance

        :returns: The fetched CallInstance
        :rtype: twilio.rest.api.v2010.account.call.CallInstance
        """
        payload = self._version.fetch(method='GET', uri=self._uri, )

        return CallInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            sid=self._solution['sid'],
        )

    def update(self, url=values.unset, method=values.unset, status=values.unset,
               fallback_url=values.unset, fallback_method=values.unset,
               status_callback=values.unset, status_callback_method=values.unset,
               twiml=values.unset):
        """
        Update the CallInstance

        :param unicode url: The absolute URL that returns TwiML for this call
        :param unicode method: HTTP method to use to fetch TwiML
        :param CallInstance.UpdateStatus status: The new status to update the call with.
        :param unicode fallback_url: Fallback URL in case of error
        :param unicode fallback_method: HTTP Method to use with fallback_url
        :param unicode status_callback: The URL we should call to send status information to your application
        :param unicode status_callback_method: HTTP Method to use to call status_callback
        :param unicode twiml: TwiML instructions for the call

        :returns: The updated CallInstance
        :rtype: twilio.rest.api.v2010.account.call.CallInstance
        """
        data = values.of({
            'Url': url,
            'Method': method,
            'Status': status,
            'FallbackUrl': fallback_url,
            'FallbackMethod': fallback_method,
            'StatusCallback': status_callback,
            'StatusCallbackMethod': status_callback_method,
            'Twiml': twiml,
        })

        payload = self._version.update(method='POST', uri=self._uri, data=data, )

        return CallInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            sid=self._solution['sid'],
        )

    @property
    def recordings(self):
        """
        Access the recordings

        :returns: twilio.rest.api.v2010.account.call.recording.RecordingList
        :rtype: twilio.rest.api.v2010.account.call.recording.RecordingList
        """
        if self._recordings is None:
            self._recordings = RecordingList(
                self._version,
                account_sid=self._solution['account_sid'],
                call_sid=self._solution['sid'],
            )
        return self._recordings

    @property
    def notifications(self):
        """
        Access the notifications

        :returns: twilio.rest.api.v2010.account.call.notification.NotificationList
        :rtype: twilio.rest.api.v2010.account.call.notification.NotificationList
        """
        if self._notifications is None:
            self._notifications = NotificationList(
                self._version,
                account_sid=self._solution['account_sid'],
                call_sid=self._solution['sid'],
            )
        return self._notifications

    @property
    def feedback(self):
        """
        Access the feedback

        :returns: twilio.rest.api.v2010.account.call.feedback.FeedbackList
        :rtype: twilio.rest.api.v2010.account.call.feedback.FeedbackList
        """
        if self._feedback is None:
            self._feedback = FeedbackList(
                self._version,
                account_sid=self._solution['account_sid'],
                call_sid=self._solution['sid'],
            )
        return self._feedback

    @property
    def events(self):
        """
        Access the events

        :returns: twilio.rest.api.v2010.account.call.event.EventList
        :rtype: twilio.rest.api.v2010.account.call.event.EventList
        """
        if self._events is None:
            self._events = EventList(
                self._version,
                account_sid=self._solution['account_sid'],
                call_sid=self._solution['sid'],
            )
        return self._events

    @property
    def payments(self):
        """
        Access the payments

        :returns: twilio.rest.api.v2010.account.call.payment.PaymentList
        :rtype: twilio.rest.api.v2010.account.call.payment.PaymentList
        """
        if self._payments is None:
            self._payments = PaymentList(
                self._version,
                account_sid=self._solution['account_sid'],
                call_sid=self._solution['sid'],
            )
        return self._payments

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.CallContext {}>'.format(context)


class CallInstance(InstanceResource):

    class Event(object):
        INITIATED = "initiated"
        RINGING = "ringing"
        ANSWERED = "answered"
        COMPLETED = "completed"

    class Status(object):
        QUEUED = "queued"
        RINGING = "ringing"
        IN_PROGRESS = "in-progress"
        COMPLETED = "completed"
        BUSY = "busy"
        FAILED = "failed"
        NO_ANSWER = "no-answer"
        CANCELED = "canceled"

    class UpdateStatus(object):
        CANCELED = "canceled"
        COMPLETED = "completed"

    def __init__(self, version, payload, account_sid, sid=None):
        """
        Initialize the CallInstance

        :returns: twilio.rest.api.v2010.account.call.CallInstance
        :rtype: twilio.rest.api.v2010.account.call.CallInstance
        """
        super(CallInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'sid': payload.get('sid'),
            'date_created': deserialize.rfc2822_datetime(payload.get('date_created')),
            'date_updated': deserialize.rfc2822_datetime(payload.get('date_updated')),
            'parent_call_sid': payload.get('parent_call_sid'),
            'account_sid': payload.get('account_sid'),
            'to': payload.get('to'),
            'to_formatted': payload.get('to_formatted'),
            'from_': payload.get('from'),
            'from_formatted': payload.get('from_formatted'),
            'phone_number_sid': payload.get('phone_number_sid'),
            'status': payload.get('status'),
            'start_time': deserialize.rfc2822_datetime(payload.get('start_time')),
            'end_time': deserialize.rfc2822_datetime(payload.get('end_time')),
            'duration': payload.get('duration'),
            'price': payload.get('price'),
            'price_unit': payload.get('price_unit'),
            'direction': payload.get('direction'),
            'answered_by': payload.get('answered_by'),
            'annotation': payload.get('annotation'),
            'api_version': payload.get('api_version'),
            'forwarded_from': payload.get('forwarded_from'),
            'group_sid': payload.get('group_sid'),
            'caller_name': payload.get('caller_name'),
            'queue_time': payload.get('queue_time'),
            'trunk_sid': payload.get('trunk_sid'),
            'uri': payload.get('uri'),
            'subresource_uris': payload.get('subresource_uris'),
        }

        # Context
        self._context = None
        self._solution = {'account_sid': account_sid, 'sid': sid or self._properties['sid'], }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: CallContext for this CallInstance
        :rtype: twilio.rest.api.v2010.account.call.CallContext
        """
        if self._context is None:
            self._context = CallContext(
                self._version,
                account_sid=self._solution['account_sid'],
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def sid(self):
        """
        :returns: The unique string that identifies this resource
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def date_created(self):
        """
        :returns: The RFC 2822 date and time in GMT that this resource was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The RFC 2822 date and time in GMT that this resource was last updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def parent_call_sid(self):
        """
        :returns: The SID that identifies the call that created this leg.
        :rtype: unicode
        """
        return self._properties['parent_call_sid']

    @property
    def account_sid(self):
        """
        :returns: The SID of the Account that created this resource
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def to(self):
        """
        :returns: The phone number, SIP address or Client identifier that received this call. Phone numbers are in E.164 format (e.g., +16175551212). SIP addresses are formatted as `name@company.com`. Client identifiers are formatted `client:name`.
        :rtype: unicode
        """
        return self._properties['to']

    @property
    def to_formatted(self):
        """
        :returns: The phone number, SIP address or Client identifier that received this call. Formatted for display.
        :rtype: unicode
        """
        return self._properties['to_formatted']

    @property
    def from_(self):
        """
        :returns: The phone number, SIP address or Client identifier that made this call. Phone numbers are in E.164 format (e.g., +16175551212). SIP addresses are formatted as `name@company.com`. Client identifiers are formatted `client:name`.
        :rtype: unicode
        """
        return self._properties['from_']

    @property
    def from_formatted(self):
        """
        :returns: The calling phone number, SIP address, or Client identifier formatted for display.
        :rtype: unicode
        """
        return self._properties['from_formatted']

    @property
    def phone_number_sid(self):
        """
        :returns: If the call was inbound, this is the SID of the IncomingPhoneNumber resource that received the call. If the call was outbound, it is the SID of the OutgoingCallerId resource from which the call was placed.
        :rtype: unicode
        """
        return self._properties['phone_number_sid']

    @property
    def status(self):
        """
        :returns: The status of this call.
        :rtype: CallInstance.Status
        """
        return self._properties['status']

    @property
    def start_time(self):
        """
        :returns: The start time of the call. Null if the call has not yet been dialed.
        :rtype: datetime
        """
        return self._properties['start_time']

    @property
    def end_time(self):
        """
        :returns: The end time of the call. Null if the call did not complete successfully.
        :rtype: datetime
        """
        return self._properties['end_time']

    @property
    def duration(self):
        """
        :returns: The length of the call in seconds.
        :rtype: unicode
        """
        return self._properties['duration']

    @property
    def price(self):
        """
        :returns: The charge for this call, in the currency associated with the account. Populated after the call is completed. May not be immediately available.
        :rtype: unicode
        """
        return self._properties['price']

    @property
    def price_unit(self):
        """
        :returns: The currency in which `Price` is measured.
        :rtype: unicode
        """
        return self._properties['price_unit']

    @property
    def direction(self):
        """
        :returns: A string describing the direction of the call. `inbound` for inbound calls, `outbound-api` for calls initiated via the REST API or `outbound-dial` for calls initiated by a `Dial` verb.
        :rtype: unicode
        """
        return self._properties['direction']

    @property
    def answered_by(self):
        """
        :returns: Either `human` or `machine` if this call was initiated with answering machine detection. Empty otherwise.
        :rtype: unicode
        """
        return self._properties['answered_by']

    @property
    def annotation(self):
        """
        :returns: The annotation provided for the call
        :rtype: unicode
        """
        return self._properties['annotation']

    @property
    def api_version(self):
        """
        :returns: The API Version used to create the call
        :rtype: unicode
        """
        return self._properties['api_version']

    @property
    def forwarded_from(self):
        """
        :returns: The forwarding phone number if this call was an incoming call forwarded from another number (depends on carrier supporting forwarding). Otherwise, empty.
        :rtype: unicode
        """
        return self._properties['forwarded_from']

    @property
    def group_sid(self):
        """
        :returns: The Group SID associated with this call. If no Group is associated with the call, the field is empty.
        :rtype: unicode
        """
        return self._properties['group_sid']

    @property
    def caller_name(self):
        """
        :returns: The caller's name if this call was an incoming call to a phone number with caller ID Lookup enabled. Otherwise, empty.
        :rtype: unicode
        """
        return self._properties['caller_name']

    @property
    def queue_time(self):
        """
        :returns: The wait time in milliseconds before the call is placed.
        :rtype: unicode
        """
        return self._properties['queue_time']

    @property
    def trunk_sid(self):
        """
        :returns: The (optional) unique identifier of the trunk resource that was used for this call.
        :rtype: unicode
        """
        return self._properties['trunk_sid']

    @property
    def uri(self):
        """
        :returns: The URI of this resource, relative to `https://api.twilio.com`
        :rtype: unicode
        """
        return self._properties['uri']

    @property
    def subresource_uris(self):
        """
        :returns: A list of related subresources identified by their relative URIs
        :rtype: unicode
        """
        return self._properties['subresource_uris']

    def delete(self):
        """
        Deletes the CallInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    def fetch(self):
        """
        Fetch the CallInstance

        :returns: The fetched CallInstance
        :rtype: twilio.rest.api.v2010.account.call.CallInstance
        """
        return self._proxy.fetch()

    def update(self, url=values.unset, method=values.unset, status=values.unset,
               fallback_url=values.unset, fallback_method=values.unset,
               status_callback=values.unset, status_callback_method=values.unset,
               twiml=values.unset):
        """
        Update the CallInstance

        :param unicode url: The absolute URL that returns TwiML for this call
        :param unicode method: HTTP method to use to fetch TwiML
        :param CallInstance.UpdateStatus status: The new status to update the call with.
        :param unicode fallback_url: Fallback URL in case of error
        :param unicode fallback_method: HTTP Method to use with fallback_url
        :param unicode status_callback: The URL we should call to send status information to your application
        :param unicode status_callback_method: HTTP Method to use to call status_callback
        :param unicode twiml: TwiML instructions for the call

        :returns: The updated CallInstance
        :rtype: twilio.rest.api.v2010.account.call.CallInstance
        """
        return self._proxy.update(
            url=url,
            method=method,
            status=status,
            fallback_url=fallback_url,
            fallback_method=fallback_method,
            status_callback=status_callback,
            status_callback_method=status_callback_method,
            twiml=twiml,
        )

    @property
    def recordings(self):
        """
        Access the recordings

        :returns: twilio.rest.api.v2010.account.call.recording.RecordingList
        :rtype: twilio.rest.api.v2010.account.call.recording.RecordingList
        """
        return self._proxy.recordings

    @property
    def notifications(self):
        """
        Access the notifications

        :returns: twilio.rest.api.v2010.account.call.notification.NotificationList
        :rtype: twilio.rest.api.v2010.account.call.notification.NotificationList
        """
        return self._proxy.notifications

    @property
    def feedback(self):
        """
        Access the feedback

        :returns: twilio.rest.api.v2010.account.call.feedback.FeedbackList
        :rtype: twilio.rest.api.v2010.account.call.feedback.FeedbackList
        """
        return self._proxy.feedback

    @property
    def events(self):
        """
        Access the events

        :returns: twilio.rest.api.v2010.account.call.event.EventList
        :rtype: twilio.rest.api.v2010.account.call.event.EventList
        """
        return self._proxy.events

    @property
    def payments(self):
        """
        Access the payments

        :returns: twilio.rest.api.v2010.account.call.payment.PaymentList
        :rtype: twilio.rest.api.v2010.account.call.payment.PaymentList
        """
        return self._proxy.payments

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.CallInstance {}>'.format(context)
