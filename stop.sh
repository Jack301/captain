#!/usr/bin/env bash
pgrep -f captain | xargs kill -9
pgrep -f tackle_word | xargs kill -9
pgrep -f clipboard | xargs kill -9
pgrep -f retrieve | xargs kill -9