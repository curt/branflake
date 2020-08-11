Branflake
=========

A modified, simplified 128-bit pseudo-flake ID generator for Python.

About
-----

I recently had a need for Python code that would generate lexically and numerically increasing identifiers. However, most of the "flake ID" packages I found included a worker component and an intra-microsecond sequencing. For my needs, having a time portion with microsecond precision is more than sufficient, so long as the rest of the identifier is random enough to avoid a collision. Within any microsecond, I don't care about the sequence.

Scratching an itch, I put together a minimal library and called it __Branflake__. It combines a 64-bit microsecond time component with a 64-bit random number. For my needs, it's more than enough to keep the likelihood of a collision infinitesimal.

A Branflake can be represented either as a numerically increasing `int` or as a lexically increasing hex-coded `string`. It can be persisted in a database or shared online as an `int` or a hex-coded `string` and be reconstituted later from either.

Requirements
------------

Python >= 3.6

Installation
------------

Ideally, in a Python virtual environment.

        $ pip install branflake

Usage
-----

First, of course, import the class definition from the package.

        $ python
        >>> from branflake import Branflake

Depending on your setup, you may need to use `python3` instead of `python`.

To create a new Branflake is straightforward.

        >>> flake = Branflake()
        >>> flake
        <Branflake 29461407052892765126374337862832989>

To persist a Branflake as an `int`, use the `to_int` method.

        >>> i = flake.to_int()
        >>> i
        29461407052892765126374337862832989

To reconstitute the Branflake later from the `int`, use the `from_int` method.

        >>> reflake = Branflake.from_int(i)
        >>> reflake
        <Branflake 29461407052892765126374337862832989>

To get the `time` structure corresponding to the time part of the Branflake, use the `to_gmtime` method.

        >>> struct = reflake.to_gmtime()
        >>> struct
        time.struct_time(tm_year=2020, tm_mon=8, tm_mday=11, tm_hour=0, tm_min=34, tm_sec=36, tm_wday=1, tm_yday=224, tm_isdst=0)

Limitations
-----------

Python treats the `None` object and a zero `int` the same for true-false logic. Rather than code around this, the earliest possible valid Branflake corresponds to _one microsecond_ after the beginning of the epoch.

The earliest possible Branflake corresponds to January 1, 1970. The `int` representation has 20 digits.

        >>> min_branflake = Branflake.from_bytes(b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00')
        >>> min_branflake.to_int()
        18446744073709551616
        >>> len(str(min_branflake))
        20
        >>> min_branflake.to_gmtime()
        time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=1, tm_isdst=0)

The latest possible Branflake corresponds to January 19, 586524. The `int` representation has 39 digits.

        >>> max_branflake = Branflake.from_bytes(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
        >>> max_branflake.to_int()
        340282366920938463463374607431768211455
        >>> len(str(max_branflake))
        39
        >>> max_branflake.to_gmtime()
        time.struct_time(tm_year=586524, tm_mon=1, tm_mday=19, tm_hour=8, tm_min=1, tm_sec=49, tm_wday=2, tm_yday=19, tm_isdst=0)

Remarks
-------

The `int` representation of a Branflake is numerically increasing across the entire valid range. However, strictly speaking, it is not lexically increasing without padding it with leading zeroes to make it 39 digits. Still, even without the padding, it can be considered lexically increasing over certain ranges of time.

For example, since the year 1987, the `int` representation has had 35 digits. It will continue to have 35 digits until the year 2141.

        >>> low_branflake = Branflake.from_int(10000000000000000000000000000000000)
        >>> low_branflake.to_gmtime()
        time.struct_time(tm_year=1987, tm_mon=3, tm_mday=7, tm_hour=7, tm_min=38, tm_sec=6, tm_wday=5, tm_yday=66, tm_isdst=0)
        >>> high_branflake = Branflake.from_int(99999999999999999999999999999999999)
        >>> high_branflake.to_gmtime()
        time.struct_time(tm_year=2141, tm_mon=10, tm_mday=14, tm_hour=4, tm_min=21, tm_sec=2, tm_wday=5, tm_yday=287, tm_isdst=0)

Therefore, if you assume the time portion of a Branflake will fall inside this range, you can use the `<` and `>` operators on `int` representations even if they've been converted to `string`.

License
-------

MIT license.

Author
------

The package is written and maintained by Curt Gilman.

Name
----

Snowflake was the name of the [original project at Twitter](https://github.com/twitter-archive/snowflake) that inspired a number of implementations. For that reason, I wanted to choose a name that had _flake_ in it.

_Cornflake_ was already taken in the [Python Package Index](https://pypi.org/), so that was out. It apparently has nothing to do with flake ID generation.

_Frostedflake_ was a name that crossed my mind. It sounded delicious but was a bit of a mouthful.

_Branflake_ seemed like a good choice. It may be part of a healthy and nutritious breakfast.