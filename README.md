# Unraid CLI Tools

A small collection of practical command-line tools for Unraid.

This repository is intended to hold focused utilities that solve real operational problems on an Unraid server without requiring a full application stack.

## Current Tools

### `bigmove`

`bigmove` moves large top-level folders from one Unraid disk to another under a shared relative path.

It is designed for cases like:

- rebalancing media folders across array disks
- moving large show folders from one disk to another
- stopping cleanly when a maintenance window or shutdown is needed

Script path:

- [`boot/config/scripts/bigmove`](./boot/config/scripts/bigmove)

## What `bigmove` Does

Given:

- a source disk
- a destination disk
- a minimum size threshold
- a relative path under both disks

`bigmove` will:

1. scan the top-level folders under the source path
2. copy only folders at or above the requested size
3. verify source and destination folder sizes match
4. delete the source folder only after a successful verified copy

The unit of work is the next top-level folder under the path you provide.

Example:

If the path is `TV`, `bigmove` will process folders like:

- `/mnt/disk1/TV/Show Name`
- `/mnt/disk1/TV/Another Show`

It does not treat deeper nested folders as separate move units unless the script is changed to do that.

## Usage

```bash
bigmove <diskSRC> <diskDEST> <SIZE> <PATH> [--foreground]
bigmove --status
bigmove --stop
bigmove --stop-now
```

## Examples

Move show folders in `TV` from `disk1` to `disk2` when they are at least `100G`:

```bash
/boot/config/scripts/bigmove disk1 disk2 100G TV
```

Move folders under a nested path:

```bash
/boot/config/scripts/bigmove disk1 disk2 500G media/shows
```

Run in the foreground:

```bash
/boot/config/scripts/bigmove disk1 disk2 100G TV --foreground
```

## Status And Stop Controls

Check status:

```bash
/boot/config/scripts/bigmove --status
```

Graceful stop after the next top-level folder finishes copying successfully:

```bash
/boot/config/scripts/bigmove --stop
```

Faster stop that interrupts the active `rsync`, leaves partial destination data in place, and does not delete the current source folder:

```bash
/boot/config/scripts/bigmove --stop-now
```

## Runtime Files

By default, `bigmove` avoids writing runtime state to the Unraid USB boot device.

Default paths:

- state: `/var/tmp/bigmove`
- log: `/var/log/bigmove.log`

Optional overrides:

- `BIGMOVE_STATE_DIR`
- `BIGMOVE_LOG_FILE`

Example:

```bash
BIGMOVE_STATE_DIR=/mnt/cache/appdata/bigmove \
BIGMOVE_LOG_FILE=/mnt/cache/appdata/bigmove/bigmove.log \
/boot/config/scripts/bigmove disk1 disk2 100G TV
```

## Safety Model

`bigmove` is intentionally conservative:

- it only deletes source data after a completed copy and a matching size check
- `--stop` waits for the current top-level folder to finish cleanly
- `--stop-now` stops faster by interrupting the current transfer without deleting the source
- partial destination data from `--stop-now` can be resumed on the next run through `rsync --partial --append-verify`

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

- choose a name that matches the tool’s real job
- keep the CLI small and obvious
- default to safe behavior over clever behavior
- avoid writing logs, state, or temp data to `/boot`
- support a status mode when the tool runs for more than a few seconds
- document stop behavior clearly if the tool changes or moves data
- keep README examples copy-paste friendly

When a tool uses secrets:

- inspect key names when possible
- avoid printing secret values
- keep runtime use of secrets limited to the minimum needed

## Tool Template

Use this checklist when adding a new tool:

1. Create the script in a location that matches how it will be used on Unraid.
2. Pick a single tool name and use it consistently in filenames, usage text, logs, and state paths.
3. Keep runtime files off `/boot` unless persistence there is truly required.
4. Add clear `--help` or usage output with one-line examples.
5. Add status and stop controls if the tool can run long enough for operators to care.
6. Define the safety model clearly before adding destructive behavior.
7. Document the tool in this README with purpose, usage, examples, and caveats.

Suggested doc block for each new tool:

````md
### `toolname`

Short description of what it does.

Script path:

- [`path/to/tool`](./path/to/tool)

Usage:

```bash
toolname ...
```

Examples:

```bash
toolname ...
```

Notes:

- safety behavior
- runtime files
- stop/status behavior
````
