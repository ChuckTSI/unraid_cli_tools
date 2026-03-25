# Unraid CLI Tools

A small collection of practical command-line tools for Unraid.

This repository holds focused utilities that solve real operational problems on an Unraid server without requiring a full application stack.

## Tools

## Wrapper Entry Point

If the individual tool names are hard to remember, use the shared wrapper:

- [`boot/config/scripts/clitools`](./boot/config/scripts/clitools)

Examples:

- `clitools arrayheat`
- `clitools diskbrain TV 40G`
- `clitools bigmove disk1 disk2 100G TV`

Install note:

- copy `/boot/config/scripts/clitools` to `/usr/local/bin/clitools`
- run `chmod +x /usr/local/bin/clitools`
- put those commands in `/boot/config/go` for persistence across reboot

Behavior note:

- `clitools` forwards arguments directly to the selected tool
- if a tool is missing required arguments, you will see that tool's normal usage output
- `clitools --list` shows the available wrapped tools

### `bigmove`

Moves large top-level folders from one Unraid disk to another under a shared relative path.

Source script path:

- [`boot/config/scripts/bigmove`](./boot/config/scripts/bigmove)

Install note:

- copy it from `/boot/config/scripts/bigmove` to `/usr/local/bin/bigmove`
- run `chmod +x /usr/local/bin/bigmove`
- optional: install `clitools` and run it as `clitools bigmove ...`
- put those commands in `/boot/config/go` for persistence across reboot

Detailed README:

- [`docs/bigmove/README.md`](./docs/bigmove/README.md)

Use the tool-specific README for:

- what the tool does
- usage and examples
- status and stop controls
- runtime file locations
- safety behavior

### `diskbrain`

Selects the best Unraid disk for a target subfolder using free-space and fill-level scoring.

Source script path:

- [`boot/config/scripts/diskbrain`](./boot/config/scripts/diskbrain)

Install note:

- copy it from `/boot/config/scripts/diskbrain` to `/usr/local/bin/diskbrain`
- run `chmod +x /usr/local/bin/diskbrain`
- optional: install `clitools` and run it as `clitools diskbrain ...`
- put those commands in `/boot/config/go` for persistence across reboot

Detailed README:

- [`docs/diskbrain/README.md`](./docs/diskbrain/README.md)

Use the tool-specific README for:

- what the tool does
- usage and examples
- scoring behavior
- subfolder path requirements
- output details

### `arrayheat`

Shows a live one-shot disk utilization view for Unraid array disks using `iostat`, with disk names mapped from Unraid metadata.

Source script path:

- [`boot/config/scripts/arrayheat`](./boot/config/scripts/arrayheat)

Install note:

- copy it from `/boot/config/scripts/arrayheat` to `/usr/local/bin/arrayheat`
- run `chmod +x /usr/local/bin/arrayheat`
- optional: install `clitools` and run it as `clitools arrayheat`
- make sure `sysstat` is installed so `iostat` is available
- put the copy and chmod commands in `/boot/config/go` for persistence across reboot

Detailed README:

- [`docs/arrayheat/README.md`](./docs/arrayheat/README.md)

Use the tool-specific README for:

- what the tool does
- install and dependency notes
- usage and example output
- how disk name mapping works
- current limits

## Repository Direction

This repository is meant to grow into a set of simple, dependable Unraid-focused tools.

Planned conventions:

- one tool per clear operational job
- simple CLI behavior
- readable shell or Python scripts
- runtime writes kept off `/boot` unless there is a strong reason otherwise
- documentation written for direct use from GitHub

## Contributing

New tools in this repo should stay boring in the good way: direct, inspectable, and safe to run on a real Unraid box.

Preferred conventions:

- choose a name that matches the tool's real job
- keep the CLI small and obvious
- default to safe behavior over clever behavior
- avoid writing logs, state, or temp data to `/boot`
- support a status mode when the tool runs for more than a few seconds
- document stop behavior clearly if the tool changes or moves data
- keep README examples copy-paste friendly
