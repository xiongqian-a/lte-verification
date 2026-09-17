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

run_privileged() {
    if [ "$(id -u 2>/dev/null || printf '1')" -eq 0 ]; then
        "$@"
    elif command -v sudo >/dev/null 2>&1; then
        sudo "$@"
    else
        echo "Administrator privileges are required to install Python, but sudo is unavailable." >&2
        return 1
    fi
}

install_python() {
    if command -v apt-get >/dev/null 2>&1; then
        echo "Python 3.10+ is missing; installing it with apt-get..."
        run_privileged apt-get update
        run_privileged apt-get install -y python3
    elif command -v dnf >/dev/null 2>&1; then
        echo "Python 3.10+ is missing; installing it with dnf..."
        run_privileged dnf install -y python3
    elif command -v yum >/dev/null 2>&1; then
        echo "Python 3.10+ is missing; installing it with yum..."
        run_privileged yum install -y python3
    elif command -v apk >/dev/null 2>&1; then
        echo "Python 3.10+ is missing; installing it with apk..."
        run_privileged apk add --no-cache python3
    elif command -v pacman >/dev/null 2>&1; then
        echo "Python 3.10+ is missing; installing it with pacman..."
        run_privileged pacman -Sy --noconfirm python
    elif command -v zypper >/dev/null 2>&1; then
        echo "Python 3.10+ is missing; installing it with zypper..."
        run_privileged zypper --non-interactive install python3
    elif command -v brew >/dev/null 2>&1; then
        echo "Python 3.10+ is missing; installing it with Homebrew..."
        brew install python
    else
        echo "Python 3.10+ is missing and no supported package manager was found." >&2
        echo "Install Python 3.10+ manually, then rerun ./bootstrap.sh." >&2
        return 1
    fi
}

python_cmd="$(find_python || true)"
if [ -z "$python_cmd" ]; then
    install_python
    python_cmd="$(find_python || true)"
fi

if [ -z "$python_cmd" ]; then
    version="$(python3 --version 2>&1 || python --version 2>&1 || true)"
    echo "Python 3.10+ was not found after installation. Current interpreter: ${version:-not found}" >&2
    echo "Install Python 3.10+ yourself, or use a current distribution/container, then rerun ./bootstrap.sh." >&2
    exit 1
fi

entry_point="./run_official_suite.py"
case "${1:-}" in
    --colleague-replay)
        entry_point="./runners/colleague_replay_verification.py"
        shift
        ;;
esac

exec "$python_cmd" -X utf8 "$entry_point" "$@"
