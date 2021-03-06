from typing import AsyncContextManager, Callable, Optional, Union

import yarl

from .base import ClosableResponse, EmptyResponse, Header, Method, Request, Response
from .context import get_context
from .deadline import Deadline
from .delays_provider import linear_delays
from .priority import Priority
from .response_classifier import DefaultResponseClassifier, ResponseClassifier
from .strategy import MethodBasedStrategy, RequestStrategy, SendRequestResult, parallel_strategy, sequential_strategy
from .transport import Transport


class Client:
    __slots__ = (
        "_endpoint",
        "_transport",
        "_response_classifier",
        "_request_strategy",
        "_priority",
        "_timeout",
        "_emit_system_headers",
        "_low_timeout_threshold",
        "_request_enricher",
    )

    def __init__(
        self,
        *,
        endpoint: yarl.URL,
        transport: Transport,
        response_classifier: ResponseClassifier,
        request_strategy: RequestStrategy,
        timeout: float,
        priority: Priority,
        emit_system_headers: bool,
        low_timeout_threshold: float,
        request_enricher: Optional[Callable[[Request], Request]],
    ):
        self._endpoint = endpoint
        self._transport = transport
        self._response_classifier = response_classifier
        self._request_strategy = request_strategy
        self._priority = priority
        self._timeout = timeout
        self._emit_system_headers = emit_system_headers
        self._low_timeout_threshold = low_timeout_threshold
        self._request_enricher = request_enricher

    def request(
        self,
        request: Request,
        *,
        deadline: Optional[Deadline] = None,
        priority: Optional[Priority] = None,
        strategy: Optional[RequestStrategy] = None,
    ) -> AsyncContextManager[Response]:
        if self._request_enricher is not None:
            request = self._request_enricher(request)
        context = get_context()
        return (strategy or self._request_strategy).request(
            self._send_request,
            self._endpoint,
            request,
            deadline or context.deadline or Deadline.from_timeout(self._timeout),
            self.normalize_priority(priority or self._priority, context.priority),
        )

    @staticmethod
    def normalize_priority(priority: "Priority", context_priority: Optional["Priority"]) -> "Priority":
        if context_priority is None:
            return priority

        if priority == Priority.LOW and context_priority == Priority.HIGH:
            return Priority.NORMAL

        if priority == Priority.HIGH and context_priority == Priority.LOW:
            return Priority.NORMAL

        return priority

    async def _send_request(
        self, endpoint: yarl.URL, request: Request, deadline: Deadline, priority: Priority
    ) -> SendRequestResult:
        if self._emit_system_headers:
            request = request.update_headers(
                {
                    Header.X_REQUEST_DEADLINE_AT: str(deadline),
                    Header.X_REQUEST_PRIORITY: str(priority),
                }
            )

        if deadline.expired or deadline.timeout < self._low_timeout_threshold:
            response: ClosableResponse = EmptyResponse(status=408)
        else:
            response = await self._transport.send(endpoint, request, deadline.timeout)

        return SendRequestResult(response, self._response_classifier.classify(response))


def setup(
    *,
    transport: Transport,
    endpoint: Union[str, yarl.URL],
    safe_method_attempts_count: int = 3,
    unsafe_method_attempts_count: int = 3,
    safe_method_delays_provider: Callable[[int], float] = linear_delays(delay_multiplier=0.1),
    unsafe_method_delays_provider: Callable[[int], float] = linear_delays(delay_multiplier=0.05),
    response_classifier: Optional[ResponseClassifier] = None,
    default_timeout: float = 20.0,
    default_priority: Priority = Priority.NORMAL,
    low_timeout_threshold: float = 0.005,
    emit_system_headers: bool = True,
    request_enricher: Optional[Callable[[Request], Request]] = None,
) -> Client:
    request_strategy = MethodBasedStrategy(
        {
            Method.GET: parallel_strategy(
                attempts_count=safe_method_attempts_count, delays_provider=safe_method_delays_provider
            ),
            Method.POST: sequential_strategy(
                attempts_count=unsafe_method_attempts_count, delays_provider=unsafe_method_delays_provider
            ),
            Method.PUT: sequential_strategy(
                attempts_count=unsafe_method_attempts_count, delays_provider=unsafe_method_delays_provider
            ),
            Method.DELETE: sequential_strategy(
                attempts_count=unsafe_method_attempts_count, delays_provider=unsafe_method_delays_provider
            ),
        }
    )
    return Client(
        endpoint=yarl.URL(endpoint) if isinstance(endpoint, str) else endpoint,
        transport=transport,
        response_classifier=response_classifier or DefaultResponseClassifier(),
        request_strategy=request_strategy,
        timeout=default_timeout,
        priority=default_priority,
        request_enricher=request_enricher,
        low_timeout_threshold=low_timeout_threshold,
        emit_system_headers=emit_system_headers,
    )
