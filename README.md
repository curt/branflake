Branflake
=========

A modified, simplified 128-bit flake ID generator for Python.

Motivation
----------

I recently had a need for Python code that would generate lexically and numerically increasing identifiers. However, most of the "flake ID" packages I found included a data center component and an intra-microsecond sequencing. For my needs, having a time portion with microsecond precision was sufficient, so long as the rest of the identifier was random enough to avoid a collision. Within any microsecond, sequence was irrelevant.

In response, I wrote __Branflake__. It combines a 64-bit microsecond time component with a 64-bit random number. For my needs, it's more than enough to make likelihood of a collision infinitesimal. A Branflake can be represented either as a numerically increasing `int` or optionally as a lexically increasing hex-coded `string`. It can be stored as an `int` and reconstituted later.

Requirements
------------

Python version should be at least 3.6.

Usage
-----

To create a new Branflake is straightforward.

        >>> from branflake import Branflake
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


License
-------

MIT license.

Author
------

The package is written and maintained by Curt Gilman.

Name
----

Snowflake would have been too obvious. Cornflake was already taken in the [Python Package Index](https://pypi.org/). Branflake seemed like a good alternative.