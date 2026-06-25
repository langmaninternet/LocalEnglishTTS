import os
import tempfile
import unittest
from unittest.mock import patch

from tts_service import app


class TtsServiceTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_returns_service_info(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get("default_model"), "suno/tts-en-1")
        self.assertIn("Local English TTS service", data.get("message", ""))

    def test_tts_route_writes_fixed_audio_file(self):
        fixed_text = "This is a fixed text for unit test."
        output_file = os.path.join(tempfile.gettempdir(), "test_tts_service_fixed.wav")

        with open(output_file, "wb") as f:
            f.write(b"RIFF....")

        with patch("tts_service.tempfile.mktemp", return_value=output_file), patch("tts_service.subprocess.run") as mock_run:
            response = self.client.get("/tts", query_string={"text": fixed_text})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers["Content-Type"].startswith("audio/"))
        self.assertEqual(response.data, b"RIFF....")
        mock_run.assert_called_once()

        called_cmd = mock_run.call_args[0][0]
        self.assertIn("--text", called_cmd)
        self.assertIn(fixed_text, called_cmd)
        self.assertFalse(os.path.exists(output_file), "Temporary audio file should be removed after response")

    def test_tts_route_requires_text(self):
        response = self.client.get("/tts")
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data.get("error"), "Missing text parameter")


if __name__ == "__main__":
    unittest.main()
