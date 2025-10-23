import os
import json
from flask import Blueprint, request, Response, jsonify, current_app

videos_bp = Blueprint("videos", __name__)

def _load_config():
    repo_root = os.path.abspath(os.path.join(current_app.root_path, ".."))
    web_root = os.path.join(repo_root, "WebAnnotationEngine")
    cfg_path = os.path.join(web_root, "src", "routes", "config", "videoConfig.json")
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f), web_root

def _stream_with_range(file_path):
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("Range") or request.headers.get("range")

    def file_iter(start=0, end=None, chunk_size=8192):
        with open(file_path, "rb") as f:
            f.seek(start)
            remaining = (end - start + 1) if end is not None else None
            while True:
                read_len = chunk_size if remaining is None else min(chunk_size, remaining)
                data = f.read(read_len)
                if not data:
                    break
                if remaining is not None:
                    remaining -= len(data)
                    if remaining <= 0:
                        yield data
                        break
                yield data

    headers = {
        "Accept-Ranges": "bytes",
        "Content-Type": "video/mp4",
    }

    if range_header:
        try:
            _, rng = range_header.split("=")
            start_s, end_s = rng.split("-")
            start = int(start_s) if start_s else 0
            end = int(end_s) if end_s else file_size - 1
            if start < 0: start = 0
            if end >= file_size: end = file_size - 1
            if start > end:
                start, end = 0, file_size - 1
        except Exception:
            start, end = 0, file_size - 1

        headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
        headers["Content-Length"] = str(end - start + 1)
        return Response(file_iter(start, end), status=206, headers=headers)

    headers["Content-Length"] = str(file_size)
    return Response(file_iter(), status=200, headers=headers)

@videos_bp.get("/reference/<path:filename>")
def get_reference_video(filename):
    cfg, web_root = _load_config()
    base_dir = cfg["reference_source"]
    if not os.path.isabs(base_dir):
        base_dir = os.path.join(web_root, base_dir)
    file_path = os.path.join(base_dir, filename)
    return _stream_with_range(file_path)

@videos_bp.get("/review/<batch>/<sign>/<path:filename>")
def get_review_video(batch, sign, filename):
    cfg, web_root = _load_config()
    review_root = cfg["review_source"]
    if not os.path.isabs(review_root):
        review_root = os.path.join(web_root, review_root)
    file_path = os.path.join(review_root, batch, sign, filename)
    return _stream_with_range(file_path)
