#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"

find_python() {
    for candidate in python3 python; do
        if command -v "$candidate" >/dev/null 2>&1; then
            version="$("$candidate" --version 2>&1 || true)"
            case "$version" in
                Python\ 3.*)
                    minor="$(printf '%s' "$version" | sed -n 's/^Python 3\.\([0-9][0-9]*\).*/\1/p')"
                    if [ -n "$minor" ] && [ "$minor" -ge 10 ]; then
                        printf '%s\n' "$candidate"
                        return 0
                    fi
                    ;;
            esac
        fi
    done
    return 1
}

python_cmd="$(find_python || true)"
if [ -z "$python_cmd" ]; then
    if command -v brew >/dev/null 2>&1; then
        echo "Python 3.10+ is missing; installing it with Homebrew..."
        brew install python
    elif command -v apt-get >/dev/null 2>&1; then
        echo "Python 3.10+ is missing; installing it with apt-get..."
        sudo apt-get update
        sudo apt-get install -y python3
    else
        echo "Python 3.10+ is missing. Install it, then rerun ./bootstrap.sh." >&2
        exit 1
    fi
    python_cmd="$(find_python || true)"
fi

if [ -z "$python_cmd" ]; then
    echo "Python was not found after installation. Open a new shell and rerun ./bootstrap.sh." >&2
    exit 1
fi

exec "$python_cmd" -X utf8 ./run_official_suite.py "$@"
