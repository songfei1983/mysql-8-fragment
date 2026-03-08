"""Run fragmentation cycles until table free space exceeds 1GB."""
import subprocess
import re
import sys

# We'll call the existing Python scripts via subprocess and parse results

def get_free_mb():
    proc = subprocess.run(['python', 'query_table_size.py'], capture_output=True, text=True)
    out = proc.stdout.strip()
    # output is a Python list representation: [(..., Decimal('XXX'), ...)]
    m = re.search(r"Decimal\('([0-9.]+)'\)\s*,\s*Decimal\('([0-9.]+)'\)\s*,\s*Decimal\('([0-9.]+)'\)\s*,\s*Decimal\('([0-9.]+)'\)\)", out)
    if m:
        # groups: total, data, index, free
        free = float(m.group(4))
        return free
    else:
        print("Could not parse output:", out)
        return None

if __name__ == '__main__':
    cycles = 0
    while True:
        cycles += 1
        print(f"--- Fragment cycle {cycles} ---")
        subprocess.run(['python', 'fragment_test.py'])
        free = get_free_mb()
        if free is None:
            print("Failed to get free space, aborting")
            sys.exit(1)
        print(f"Current free MB: {free}")
        if free >= 1024.0:
            print("Free space exceeded 1GB")
            break
    print("Done")
