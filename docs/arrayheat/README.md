# `arrayheat`

`arrayheat` shows a quick utilization snapshot for Unraid array disks using `iostat`.

It is designed for cases like:

- spotting which array disk is hottest right now
- checking read and write activity without opening the web UI
- mapping Linux device names like `sdb` back to Unraid disk names like `disk2`

Source script path:

- [`boot/config/scripts/arrayheat`](../../boot/config/scripts/arrayheat)

## Install On Unraid

Do not run the tool directly from `/boot`.

Keep the source file on the flash drive, then copy it into a runnable location at boot:

```bash
cp /boot/config/scripts/arrayheat /usr/local/bin/arrayheat
chmod +x /usr/local/bin/arrayheat
```

Put those commands in `/boot/config/go` so the install persists across reboot.

If you also install the shared wrapper, you can run the same tool as:

```bash
clitools arrayheat
```

`arrayheat` requires `iostat`, which is provided by `sysstat`.

If `iostat` is missing, the script exits with:

```text
ERROR: install sysstat
```

## What `arrayheat` Does

`arrayheat` will:

1. read `/var/local/emhttp/disks.ini`
2. build a map from Linux device names like `sdb` to Unraid names like `disk2`
3. run `iostat -dx 1 1`
4. keep rows for `sd*` block devices
5. print disk name, utilization percent, read rate, write rate, and a fixed-width heat bar
6. sort the final output by utilization percent descending

The heat bar is scaled to a width of `20`.

## Usage

```bash
arrayheat
```

## Example Output

```text
DISK       UTIL%  READ     WRITE    HEAT
disk3      91     12.4     144.8    [██████████████████  ]
disk1      47     8.1      31.5     [█████████           ]
disk2      4      0.0      1.2      [                    ]
```

## Notes

- the output is a single snapshot, not a continuous live monitor
- the script uses the final `%util` field from `iostat`
- read and write values are taken directly from the current `iostat -dx` column positions used by the script
- if a device is not found in `disks.ini`, the raw device name is shown instead

## Current Limits

Current version notes:

- it only matches devices whose names start with `sd`
- NVMe devices such as `nvme0n1` are not included
- the script assumes the current `iostat -dx` column layout used on the target system
- `INTERVAL` and `BAR_WIDTH` are fixed in the script and are not CLI options yet
