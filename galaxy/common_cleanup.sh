#!/bin/sh

set -x

# This usually drastically reduced the container size
# at the cost of the startup time of your application
find / -name '*.pyc' -delete

find / -name '*.log' -delete
find / -name '.cache' -type d -prune -exec rm -rf '{}' +
find / -name '.npm' -type d -prune -exec rm -rf '{}' +
find / -name '.launchpadlib' -type d -prune -exec rm -rf '{}' +
rm -rf /var/lib/apt/lists/*
rm -rf /var/cache/*
rm -rf /tmp/*
rm -rf /var/tmp/*

# https://askubuntu.com/questions/266738/how-to-truncate-all-logfiles
truncate -s 0 /var/log/*log || true
truncate -s 0 /var/log/**/*log || true
