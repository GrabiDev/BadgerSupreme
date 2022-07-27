# BadgerSupreme
This projects leverages Pimoroni's [BadgerOS](https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/examples/badger2040)
for [Badger 2040](https://shop.pimoroni.com/products/badger-2040). As the
original BadgerOS, it is also written in *MicroPython*.

It replaces the original Badger app in BadgerOS with an enhanced version.
It allows for storing multiple badges, which can be switched using the
arrow buttons, and adding contact details in form of QR codes using the
bottom A/B/C buttons.

E.g.: You can switch between your work badge and a hobby badge. Your work
badge can have a QR code for your work email address under A and your work
GitHub profile under B. A different QR code for your private email and
private GitHub profile can be attached to the other badge.

# Setup
Replace information in `badge.json` with what you desire to see in your
badges. The sample file contains two badges, but feel free to add more or
less by adding another object (limited by braces) within the list (limited
by square brackets) using the pattern provided.

Download [MicroPython image for Badger 2040](https://github.com/pimoroni/pimoroni-pico/releases)
from Pimoroni's GitHub and flash it onto your badger.
Use [instructions](https://learn.pimoroni.com/article/getting-started-with-badger-2040#installing-badger-flavoured-micropython) provided.

I have not tested this with the Badger 2040 release without the launcher,
though I am looking forward to! For now, *use the image with BadgerOS*.
As of release 1.19.6, they appear to be the same file size anyway.

Once image is flashed, copy all `.py` and `.json` files onto your badger
using a tool like [Thonny](https://thonny.org/). You may check
[Pimoroni's tutorial](https://learn.pimoroni.com/article/getting-started-with-badger-2040#programming-badger-with-thonny)
for further reference or when lost.

Once ready, plug it off from your computer, power on, launch the Badger app
and enjoy showing all your identities!
