import os
import re
import tempfile
from flask import Flask, request, render_template, jsonify, send_file, make_response, flash, redirect, url_for
from flask_cors import CORS
from video_downloader.core.info import get_formats
from video_downloader.core.downloader import download
from video_downloader.utils.helpers import validate_url


def strip_ansi(text: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production")
CORS(app, origins=["https://www.shuvokamal.com", "https://shuvokamal.com"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/info", methods=["POST"])
def info():
    url = request.json.get("url", "").strip()
    # Strip playlist parameters from YouTube URLs
    if "youtube.com" in url or "youtu.be" in url:
        from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        qs.pop("list", None)
        qs.pop("index", None)
        url = urlunparse(parsed._replace(query=urlencode({k: v[0] for k, v in qs.items()})))
    try:
        validate_url(url)
        formats, title = get_formats(url)
        if not formats:
            return jsonify({"error": "No downloadable formats found for this video."}), 400
        return jsonify({"title": title, "formats": formats})
    except Exception as e:
        return jsonify({"error": strip_ansi(str(e))}), 400


@app.route("/download", methods=["POST"])
def handle_download():
    """Server-side download for formats that need audio/video merging."""
    url = request.form.get("url", "").strip()
    format_id = request.form.get("format_id", "").strip()

    if not url or not format_id:
        flash("Missing URL or format.")
        return redirect(url_for("index"))

    tmp_dir = tempfile.mkdtemp()
    try:
        download(url, output_dir=tmp_dir, format_id=format_id)
    except (ValueError, RuntimeError) as e:
        flash(strip_ansi(str(e)))
        return redirect(url_for("index"))

    files = os.listdir(tmp_dir)
    if not files:
        flash("Download completed but no file was found.")
        return redirect(url_for("index"))

    token = request.form.get("download_token", "")
    file_path = os.path.join(tmp_dir, files[0])
    response = make_response(send_file(file_path, as_attachment=True, download_name=files[0]))
    if token:
        response.set_cookie("download_token", token, max_age=60)
    return response


if __name__ == "__main__":
    app.run(debug=True)
