
Audio
=====

The current music timers do a decent job reporting the current time,
but more work needs to be done to find better alternative for
accurate audio playback.

We separate playback libraries in two types based on their capabilities.

1) Accurate reporting of current time
2) Accurate reporting of current time and fast and accurate time seeking

These capabilites should also ideally work across the tree main platforms:
Linux, OS X and Windows.

We have decent type 1 timers, but more work needs to be done to
find better type 2 libraries. This is important when working with
timing tools such as rocket and when jumping around in the timeline.

Some of the current timers also work inconsistenly between platforms.
A lot more research and work is needed.

.. Note:: Contributions in any form on this topic is greatly appreciated.
