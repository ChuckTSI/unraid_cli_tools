# Unraid CLI Tools

A small collection of practical command-line tools for Unraid.

This repository holds focused utilities that solve real operational problems on an Unraid server without requiring a full application stack.

## Tools

### `bigmove`

Moves large top-level folders from one Unraid disk to another under a shared relative path.

Source script path:

- [`boot/config/scripts/bigmove`](./boot/config/scripts/bigmove)

Install note:

- copy it from `/boot/config/scripts/bigmove` to `/usr/local/bin/bigmove`
- run `chmod +x /usr/local/bin/bigmove`
- put those commands in `/boot/config/go` for persistence across reboot

Detailed README:

- [`docs/bigmove/README.md`](./docs/bigmove/README.md)

Use the tool-specific README for:

- what the tool does
- usage and examples
- status and stop controls
- runtime file locations
- safety behavior

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
