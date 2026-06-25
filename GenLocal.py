from __future__ import annotations
import os
import shutil
import subprocess
import sys
from pathlib import Path

FIXED_TEXT = (
    "Hello from GenLocal. This text is fixed inside the script and will be converted "
    "to English speech using kokoro."
)
DEFAULT_MODEL = "suno/tts-en-1"
OUTPUT_FILENAME = "genlocal_output.wav"


def find_kokoro_command() -> list[str]:
    kokoro_exe = shutil.which("kokoro")
    if kokoro_exe:
        return [kokoro_exe]
    return [sys.executable, "-m", "kokoro"]


def build_tts_command(text: str, output_path: str, model: str = DEFAULT_MODEL) -> list[str]:
    command = find_kokoro_command()
    return command + ["tts", "--model", model, "--text", text, "--output", output_path]


def generate_tts_to_file(text: str, output_path: str, model: str = DEFAULT_MODEL) -> None:
    cmd = build_tts_command(text, output_path, model)
    print("Running kokoro TTS command:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print("TTS audio generated to:", output_path)


def main() -> int:
    output_path = Path(OUTPUT_FILENAME).resolve()
    if output_path.exists():
        output_path.unlink()

    try:
        generate_tts_to_file(FIXED_TEXT, str(output_path), DEFAULT_MODEL)
        print("Finished successfully.")
        return 0
    except FileNotFoundError:
        print(
            "kokoro command not found. Please install kokoro in the current Python environment,"
            " or make sure kokoro is on PATH."
        )
        return 1
    except subprocess.CalledProcessError as exc:
        print("kokoro failed with return code", exc.returncode)
        return exc.returncode
    except Exception as exc:
        print("Unexpected error:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
