MAX_MESSAGE_SIZE: int = 64 * 1024 * 1024
"""The maximum gRPC message size."""

NANO_SECOND_PRECISION: float = 1000_000_000.0
"""Use this to convert a datetime.timestamp() floating point value to an integer with nano second precision."""

MESSAGE_OVERHEAD_SIZE = 1024
"""the message wire format takes up some bytes as well, choose a safe value here for now"""

PER_ACTION_OVERHEAD_SIZE = 8
"""overhead per buffered action, chosen a safe value again"""

MAX_CHUNK_SIZE: int = MAX_MESSAGE_SIZE - MESSAGE_OVERHEAD_SIZE - PER_ACTION_OVERHEAD_SIZE
"""an estimate of the maximum chunk size based on the MAX_MESSAGE_SIZE and message overhead"""
