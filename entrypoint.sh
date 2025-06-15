#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

readonly cmd="$*"

###########################
alembic upgrade head
###########################

# shellcheck disable=SC2086
exec $cmd
