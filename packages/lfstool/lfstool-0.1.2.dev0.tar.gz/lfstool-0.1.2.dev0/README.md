# LFSTool

A command line utility to sync local folder with a remote LittleFS partition. 

It communicates with the ROM bootloader in Espressif ESP8266 & ESP32 microcontrollers only. 

Internally lfstool.py uses esptool when communicating with microcontrollers.

The lfstool.py project is hosted on github: https://github.com/iotctl/lfstool

Installation
------------

lfstool can be installed via pip:

  $ pip install lfstool -U

lfstool supports Python 3.5 or newer.

lfstool supports both ESP8266 & ESP32.

## Installation / dependencies

### Easy Installation

You will need [Python 3.5 or newer](https://www.python.org/downloads/) installed on your system.

The latest stable lfstool.py release can be installed from [pypi](http://pypi.python.org/pypi/lfstool) via pip:

```
$ pip install lfstool
```

With some Python installations this may not work and you'll receive an error, try `python -m pip install lfstool`

[Setuptools](https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html) is also a requirement which is not available on all systems by default. You can install it by a package manager of your operating system, or by `pip install setuptools`.

After installing, you will have `lfstool.py` installed into the default Python executables directory and you should be able to run it with the command `lfstool.py` or `python -m lfstool`. Please note that probably only `python -m lfstool` will work for Pythons installed from Windows Store.

### Development Mode Installation

Development mode allows you to run the latest development version from this repository.

```
$ git clone https://github.com/iotctl/lfstool.git
$ cd lfstool
$ pip install --user -e .
# When using virtualenv:
$ pip install -e .
```

This will install lfstool's dependencies and create some executable script wrappers in the user's `bin` directory. The wrappers will run the scripts found in the git working directory directly, so any time the working directory contents change it will pick up the new versions.

It's also possible to run the scripts directly from the working directory with this Development Mode installation.

(Note: if you actually plan to do development work with esptool itself, see the CONTRIBUTING.md file.)

## Usage:

```console
lfstool.py  --help
usage: lfstool.py [-h] [--source SOURCE] [--local_mirror LOCAL_MIRROR] [--create] [--no-stub] [--block_size BLOCK_SIZE] [--block_count BLOCK_COUNT] [--read_size READ_SIZE] [--prog_size PROG_SIZE] [--lookahead_size LOOKAHEAD_SIZE] [--chip {auto,esp32,esp32s2,esp32s3beta2,esp32c3}] [--baud BAUD] [--port PORT]
                  [--before {default_reset,no_reset,esp32r1,no_reset_no_sync}] [--after {hard_reset,soft_reset,no_reset}] [--address ADDRESS] [--compress | --no-compress] [--erase-all] [--flash_freq {keep,40m,26m,20m,80m}] [--flash_mode {keep,qio,qout,dio,dout}] [--flash_size FLASH_SIZE]
                  [--spi-connection SPI_CONNECTION] [--verify] [--verbose] [--force]

LFSTool

optional arguments:
  -h, --help            show this help message and exit
  --source SOURCE, -s SOURCE
                        Source path to update from
  --local_mirror LOCAL_MIRROR, -t LOCAL_MIRROR
                        Local mirror of the remote FS
  --create              Create local mirror fs if the file does not exist
  --no-stub             Disable launching the flasher stub, only talk to ROM bootloader. Some features will not be available.
  --block_size BLOCK_SIZE, -bs BLOCK_SIZE
                        Block size
  --block_count BLOCK_COUNT, -bc BLOCK_COUNT
                        Block count
  --read_size READ_SIZE, -rs READ_SIZE
                        Read size buffer
  --prog_size PROG_SIZE, -ps PROG_SIZE
                        Prog size buffer
  --lookahead_size LOOKAHEAD_SIZE, -ls LOOKAHEAD_SIZE
                        Look ahead size
  --chip {auto,esp32,esp32s2,esp32s3beta2,esp32c3}, -c {auto,esp32,esp32s2,esp32s3beta2,esp32c3}
                        Target chip type
  --baud BAUD, -b BAUD  Serial port baud rate used when flashing/reading
  --port PORT, -p PORT  Serial port device, could be taken from env ESPTOOL_PORT, if not default to /dev/ttyUSB0
  --before {default_reset,no_reset,esp32r1,no_reset_no_sync}
                        What to do before connecting to the chip
  --after {hard_reset,soft_reset,no_reset}, -a {hard_reset,soft_reset,no_reset}
                        What to do after esptool.py is finished
  --address ADDRESS     Data partition start address
  --compress, -z        Compress data in transfer (default unless --no-stub is specified)
  --no-compress, -u     Disable data compression during transfer (default if --no-stub is specified)
  --erase-all, -e       Erase all regions of flash (not just write areas) before programming
  --flash_freq {keep,40m,26m,20m,80m}, -ff {keep,40m,26m,20m,80m}
                        SPI Flash frequency
  --flash_mode {keep,qio,qout,dio,dout}, -fm {keep,qio,qout,dio,dout}
                        SPI Flash mode
  --flash_size FLASH_SIZE, -fs FLASH_SIZE
                        SPI Flash size in MegaBytes (1MB, 2MB, 4MB, 8MB, 16M) plus ESP8266-only (256KB, 512KB, 2MB-c1, 4MB-c1), detect, or keep
  --spi-connection SPI_CONNECTION, -sc SPI_CONNECTION
                        ESP32-only argument. Override default SPI Flash connection. Value can be SPI, HSPI or a comma-separated list of 5 I/O numbers to use for SPI flash (CLK,Q,D,HD,CS).
  --verify              Verify just-written data on flash (mostly superfluous, data is read back during flashing)
  --verbose, -v         Enable verbose logging
  --force               Delete local mirror and sync all files to remote again.
```

## Example

### Sync the current working directory to a remote LittleFS partition:
```console
lfstool.py -p /dev/cu.usbserial-1410 --create
```
### Sync only changes in the working directory to a remote LittleFS partition:
```console
lfstool.py -p /dev/cu.usbserial-1410
```
### Resync the whole current working directory to a remote LittleFS partition:
```console
lfstool.py -p /dev/cu.usbserial-1410 --force
```