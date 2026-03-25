# `diskbrain`

`diskbrain` picks the best Unraid disk for a target subfolder based on free space and fill level.

It is designed for cases like:

- choosing a destination disk before moving media
- keeping new data on disks that still have healthy free space
- restricting selection to disks that already contain the requested subfolder path

Source script path:

- [`boot/config/scripts/diskbrain`](../../boot/config/scripts/diskbrain)

## Install On Unraid

Do not run the tool directly from `/boot`.

Keep the source file on the flash drive, then copy it into a runnable location at boot:

```bash
cp /boot/config/scripts/diskbrain /usr/local/bin/diskbrain
chmod +x /usr/local/bin/diskbrain
```

Put those commands in `/boot/config/go` so the install persists across reboot.

If you also install the shared wrapper, you can run the same tool as:

```bash
clitools diskbrain TV 40G
```

## What `diskbrain` Does

Given:

- a subfolder path, such as `TV` or `media/shows`
- an optional minimum required size

`diskbrain` will:

1. scan mounted `/mnt/disk*` array disks
2. keep only disks that already contain the requested subfolder path
3. skip disks under the configured minimum free-space threshold
4. skip disks that do not have enough free space for the requested size
5. score the remaining disks and choose the best candidate

The current scoring weights are:

- free space: `70`
- fill level headroom: `30`

## Usage

```bash
diskbrain [SUBFOLDER] [SIZE]
diskbrain [SUBFOLDER] [SIZE] --quiet
```

## Examples

Choose the best disk for `TV` with at least `40G` free for the request:

```bash
/usr/local/bin/diskbrain TV 40G
```

Choose the best disk for `Movies` with no explicit size requirement beyond the built-in free-space floor:

```bash
/usr/local/bin/diskbrain Movies
```

Return only the selected disk name:

```bash
/usr/local/bin/diskbrain TV 40G --quiet
```

## Output

Normal output shows:

- disk name
- used percent
- free space
- score
- evaluated subfolder path

Then it prints the selected disk and score.

`--quiet` currently still prints the table and selected line before echoing the disk name, so it is not fully machine-clean output yet.

## Path Requirement

`diskbrain` only considers disks where the requested subfolder path already exists.

Example:

If you run:

```bash
/usr/local/bin/diskbrain TV 40G
```

the script only scores disks that already contain:

- `/mnt/disk1/TV`
- `/mnt/disk2/TV`
- and so on

If no eligible disk has that path, the script returns:

```text
No suitable disk found
```

## Current Limits

Current version notes:

- size parsing expects uppercase `M`, `G`, or `T`
- invalid size input falls back poorly and should be improved in a later revision
- `usage()` exists in the script but is not wired into argument validation yet
- `--quiet` is useful for humans but still needs cleaner machine-readable behavior
