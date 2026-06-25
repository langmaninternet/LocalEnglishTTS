from flask import Flask, request, send_file, jsonify, after_this_request
import os
import sys
import shutil
import subprocess
import tempfile

app = Flask(__name__)
DEFAULT_MODEL = "suno/tts-en-1"

KOKORO_CMD = shutil.which("kokoro")
if not KOKORO_CMD:
    KOKORO_CMD = [sys.executable, "-m", "kokoro"]


def build_kokoro_cmd(text: str, output_path: str, model: str) -> list[str]:
    cmd = ["tts", "--model", model, "--text", text, "--output", output_path]
    if isinstance(KOKORO_CMD, str):
        return [KOKORO_CMD] + cmd
    return KOKORO_CMD + cmd


@app.route("/tts")
def tts():
    text = request.args.get("text", "").strip()
    if not text:
        return jsonify({"error": "Missing text parameter"}), 400

    model = request.args.get("model", DEFAULT_MODEL)
    output_path = tempfile.mktemp(suffix=".wav")

    try:
        cmd = build_kokoro_cmd(text, output_path, model)
        subprocess.run(cmd, check=True)

        @after_this_request
        def cleanup(response):
            try:
                os.remove(output_path)
            except OSError:
                pass
            return response

        return send_file(output_path, mimetype="audio/wav", as_attachment=True, download_name="tts.wav")
    except subprocess.CalledProcessError as exc:
        return jsonify({"error": "kokoro execution failed", "cmd": cmd, "returncode": exc.returncode}), 500
    except Exception as exc:
        return jsonify({"error": "Unexpected error", "message": str(exc)}), 500


@app.route("/")
def index():
    return jsonify({
        "message": "Local English TTS service using kokoro",
        "endpoint": "/tts?text=Hello+world",
        "default_model": DEFAULT_MODEL,
        "note": "af_heart and af_bella are not official kokoro model names. Use suno/tts-en-1 or other supported English models.",
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
