# `bigmove`

`bigmove` moves large top-level folders from one Unraid disk to another under a shared relative path.

It is designed for cases like:

- rebalancing media folders across array disks
- moving large show folders from one disk to another
- stopping cleanly when a maintenance window or shutdown is needed

Source script path:

- [`boot/config/scripts/bigmove`](../../boot/config/scripts/bigmove)

## Install On Unraid

Do not run the tool directly from `/boot`.

Keep the source file on the flash drive, then copy it into a runnable location at boot:

```bash
cp /boot/config/scripts/bigmove /usr/local/bin/bigmove
chmod +x /usr/local/bin/bigmove
```

Put those commands in `/boot/config/go` so the install persists across reboot.

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
/usr/local/bin/bigmove disk1 disk2 100G TV
```

Move folders under a nested path:

```bash
/usr/local/bin/bigmove disk1 disk2 500G media/shows
```

Run in the foreground:

```bash
/usr/local/bin/bigmove disk1 disk2 100G TV --foreground
```

## Status And Stop Controls

Check status:

```bash
/usr/local/bin/bigmove --status
```

Graceful stop after the next top-level folder finishes copying successfully:

```bash
/usr/local/bin/bigmove --stop
```

Faster stop that interrupts the active `rsync`, leaves partial destination data in place, and does not delete the current source folder:

```bash
/usr/local/bin/bigmove --stop-now
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
/usr/local/bin/bigmove disk1 disk2 100G TV
```

## Safety Model

`bigmove` is intentionally conservative:

- it only deletes source data after a completed copy and a matching size check
- `--stop` waits for the current top-level folder to finish cleanly
- `--stop-now` stops faster by interrupting the current transfer without deleting the source
- partial destination data from `--stop-now` can be resumed on the next run through `rsync --partial --append-verify`
