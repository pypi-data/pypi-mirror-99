# FS Tool

The command line tool to merge any local directory with LittleFS file

## Usage:

```console
./fs_tool.py --help
usage: fs_tool.py [-h] --source SOURCE --target TARGET [--create] [--no-stub] --block_size BLOCK_SIZE --block_count BLOCK_COUNT [--read_size READ_SIZE] [--prog_size PROG_SIZE]
                  [--lookahead_size LOOKAHEAD_SIZE] [--chip {auto,esp32,esp32s2,esp32s3beta2,esp32c3}] [--baud BAUD] [--port PORT]
                  [--before {default_reset,no_reset,esp32r1,no_reset_no_sync}] [--after {hard_reset,soft_reset,no_reset}] [--address ADDRESS] [--compress | --no-compress] [--erase-all]
                  [--flash_freq {keep,40m,26m,20m,80m}] [--flash_mode {keep,qio,qout,dio,dout}] [--flash_size FLASH_SIZE] [--spi-connection SPI_CONNECTION] [--verify] [--verbose]

FS tool

optional arguments:
  -h, --help            show this help message and exit
  --source SOURCE, -s SOURCE
                        Source path to update from
  --target TARGET, -t TARGET
                        Target fs file to be updated
  --create              Create target file if the file does not exist
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
  --port PORT, -p PORT  Serial port device
  --before {default_reset,no_reset,esp32r1,no_reset_no_sync}
                        What to do before connecting to the chip
  --after {hard_reset,soft_reset,no_reset}, -a {hard_reset,soft_reset,no_reset}
                        What to do after esptool.py is finished
  --address ADDRESS     Data partition address
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
```

## Example

```console
./fs_tool.py -s /source/path -t /target/fs.bin --block_size=4096 --block_count 512 --prog_size 4096 --create -p /dev/cu.usbserial-1410 -b 460800 --flash_size 4MB --before default_reset --after hard_reset  --no-compress --spi-connection=6,17,8,11,16 --address=0x10000
```