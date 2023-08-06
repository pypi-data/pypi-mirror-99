import sys
from typing import TYPE_CHECKING

import trio
from trio._util import ConflictDetector
from trio._windows_pipes import PipeSendStream, _HandleHolder, DEFAULT_RECEIVE_SIZE
from trio.abc import SendChannel, ReceiveChannel
from ._windows_cffi import ErrorCodes, peek_pipe_message_left

assert sys.platform == "win32" or not TYPE_CHECKING


class PipeSendChannel(SendChannel[bytes]):
    """Represents a message stream over a pipe object."""

    def __init__(self, handle: int) -> None:
        self._pss = PipeSendStream(handle)
        # needed for "detach" via _handle_holder.handle = -1
        self._handle_holder = self._pss._handle_holder

    async def send(self, value: bytes):
        # Works just fine if the pipe is message-oriented
        await self._pss.send_all(value)

    async def aclose(self):  # pragma: no cover
        await self._handle_holder.aclose()


class PipeReceiveChannel(ReceiveChannel[bytes]):
    """Represents a message stream over a pipe object."""

    def __init__(self, handle: int) -> None:
        self._handle_holder = _HandleHolder(handle)
        self._conflict_detector = ConflictDetector(
            "another task is currently using this pipe"
        )

    async def receive(self) -> bytes:
        with self._conflict_detector:
            buffer = bytearray(DEFAULT_RECEIVE_SIZE)
            try:
                received = await self._receive_some_into(buffer)
            except OSError as e:
                if e.winerror != ErrorCodes.ERROR_MORE_DATA:
                    raise  # pragma: no cover
                left = peek_pipe_message_left(self._handle_holder.handle)
                # preallocate memory to avoid an extra copy of very large messages
                newbuffer = bytearray(DEFAULT_RECEIVE_SIZE + left)
                with memoryview(newbuffer) as view:
                    view[:DEFAULT_RECEIVE_SIZE] = buffer
                    with trio.CancelScope(shield=True):
                        await self._receive_some_into(view[DEFAULT_RECEIVE_SIZE:])
                return newbuffer
            else:
                del buffer[received:]
                return buffer

    async def _receive_some_into(self, buffer) -> bytes:
        if self._handle_holder.closed:  # pragma: no cover
            raise trio.ClosedResourceError("this pipe is already closed")
        try:
            return await trio.lowlevel.readinto_overlapped(
                self._handle_holder.handle, buffer
            )
        except BrokenPipeError:
            if self._handle_holder.closed:  # pragma: no cover
                raise trio.ClosedResourceError(
                    "another task closed this pipe"
                ) from None

            # Windows raises BrokenPipeError on one end of a pipe
            # whenever the other end closes, regardless of direction.
            # Convert this to EndOfChannel.
            #
            # Do we have to checkpoint manually? Copied from PipeReceiveStream
            await trio.lowlevel.checkpoint()
            raise trio.EndOfChannel

    async def aclose(self):  # pragma: no cover
        await self._handle_holder.aclose()
