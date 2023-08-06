Sanskrit
========

For usage of this library, and for other tasks such as `sandhi` joining/splitting,
sentence parsing, etc., please see the
[sanskrit_parser](https://github.com/kmadathil/sanskrit_parser/) library.

The `sandhi` and `sounds` modules are not fully featured currently,
and are unlikely to be developed due to the availability of better maintained packages.

## Original description:

This is a general-purpose package for dealing with Sanskrit data of any kind.
It currently operates at and below the word level and below, with modules like:

- `query`, for accessing linguistic data
- `sandhi`, for applying and undoing sandhi changes
- `sounds`, for testing sounds and getting the meter of a phrase

Soon the package will move up to the word and sentence levels. Once there, it
will provide tools for inflecting, analyzing, tagging, and parsing Sanskrit.
