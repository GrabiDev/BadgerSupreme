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

If you want to replace the default badger image with your own, check [Custom images](#custom-images) section below.

Once ready, plug it off from your computer, power on, launch the Badge app
and enjoy showing all your identities!

# Custom images
You can replace the default badger image with your own.
First, use your favourite photo editor to convert your image of choice
to a two colours (1-bit graphics) PNG file and resize it to precisely 104x128 pixels. Please do not convert it to any other grayscale. The display is able only to represent two colours.

You may want to play with the settings of your photo editing software to achieve a black and white image that looks best to you.

Once you are happy with the image, convert it to a binary format using
[a script provided by Pimoroni](https://github.com/pimoroni/pimoroni-pico/blob/main/examples/badger2040/image_converter/convert.py).


## Installing Pillow
The script requires [Pillow](https://python-pillow.org/) to be installed on your system or virtual environment. If you do not have it, you can install it using a command:

`python3 -m pip install --upgrade Pillow`

If you encounter problems during installation, make sure you have Pillow's
dependencies installed. This appears to be a required step on
[macOS](https://pillow.readthedocs.io/en/stable/installation.html#building-on-macos). Fortunately all requirements can be satisfied
through [Homebrew](https://brew.sh/).

## Using the image conversion script
Run the script locally using a command:

`python3 convert.py --binary badge-image.png`

Once the image is converted, upload it to the badge in the same way as you
did with with code and data files.
