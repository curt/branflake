"""module: branflake

A Branflake represents a modified Flake ID, for which the time part is
microseconds since the beginning of the epoch and the rest is purely random. The
`to_int()` result is numerically increasing, and `to_hex_string()` result is
lexically increasing. A Branflake may be reconstituted by storing the `to_int()`
result and then calling the `from_int(int)` class method.

License: MIT. See LICENSE file for more details.
"""
from base64 import b16encode
from time import time, gmtime
from secrets import token_bytes
from uuid import UUID

ONE_MILLION = 1000000

class Branflake:
    """Encapsulates 128 bits of data, 64 of which correspond to microseconds
    since the beginning of the epoch, and 64 of which are random.

    microseconds: A 64-bit `int` corresponding to the time part of the
    `Branflake`. If omitted, the current time is used.

    random_bytes: A 8-byte array corresponding to the random part of the
    `Branflake`. If omitted, it is generated at random.

    Usage: # Create flake flake = Branflake()

        # Store flake as `int`
        flake_int = flake.to_int()

        # Reuse flake stored as `int`
        another_flake = Branflake.from_int(flake_int)
    """
    def __init__(self, microseconds=None, random_bytes=None):
        self._time = int(microseconds or (time() * ONE_MILLION))
        self._random_bytes = random_bytes or token_bytes(8)
        self._set_time_bytes()

    def __str__(self):
        return str(self.to_int())

    def __repr__(self):
        return '<Branflake %r>' % self.to_int()

    @classmethod
    def from_int(cls, flake_int):
        """Returns a new `Branflake` corresponding to a 128-bit `int`.

        Args:
            flake_int: A 128-bit int returned from another `Branflake`
        """
        all_bytes = flake_int.to_bytes(16, byteorder='big', signed=False)
        time_bytes = all_bytes[0:8]
        microseconds = int.from_bytes(
            time_bytes, byteorder='big', signed=False)
        random_bytes = all_bytes[8:16]
        return cls(microseconds, random_bytes)

    def to_seconds(self):
        """Returns a `float` corresponding to the epoch time in seconds
        of the Branflake."""
        return self._time / ONE_MILLION

    def to_gmtime(self):
        """Returns a time structure corresponding to the Branflake."""
        return gmtime(self.to_seconds())

    def to_microseconds(self):
        """Returns an `int` corresponding to the epoch time in microseconds
        of the Branflake."""
        return self._time

    def get_time_bytes(self):
        """Returns an 8-byte array corresponding to the time part of the
        Branflake."""
        return self._time_bytes

    def get_random_bytes(self):
        """Returns an 8-byte array corresponding to the random part of the
        Branflake."""
        return self._random_bytes

    def to_bytes(self):
        """Returns a 16-byte array corresponding to the Branflake."""
        return self.get_time_bytes() + self.get_random_bytes()

    def to_hex_bytes(self):
        """Returns a 32-byte hexidecimal-encoded array corresponding
        to the Branflake."""
        return b16encode(self.to_bytes())

    def to_int(self):
        """Returns a 128-bit `int` corresponding to the Branflake."""
        return int.from_bytes(
            self.to_bytes(), byteorder='big', signed=False)

    def to_uuid(self):
        """Returns a UUID corresponding to the Branflake."""
        return UUID(bytes=self.to_bytes())

    def to_hex_string(self):
        """Returns a 32-character hexidecimal-encoded `string`
        corresponding to the Branflake."""
        return self.to_hex_bytes().decode('utf-8').lower()

    def _set_time_bytes(self):
        self._time_bytes = self.to_microseconds().to_bytes(
            8, byteorder='big', signed=False)
