#!/bin/bash

set -euo pipefail

# Commands:
#
#   install         -- create initial installation
#   download        -- download data
#   exec            -- Execute arbitrary commands

if [[ "$1" == install ]]; then
  cd $APP_DIR
elif [[ "$1" == download ]]; then
  cd $APP_DIR
else
  shift
  cd $APP_DIR
  exec "$@"
fi

exit $?
