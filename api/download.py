from flask import Flask, request, jsonify
import requests
import re
import os

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    session = requests.Session()
    headers_utama = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        'Referer': "https://sfile.mobi/",
        'Accept-Language': "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    response_utama = session.get(url, headers=headers_utama)
    match = re.search(r'<a class="w3-button w3-blue w3-round" id="download" href="([^"]+)"', response_utama.text)

    if not match:
        return jsonify({"error": "Download link not found"}), 404

    link_download_awal = match.group(1)

    headers_hasil = {
        "User-Agent": headers_utama["User-Agent"],
        "Referer": url
    }
    response_hasil = session.get(link_download_awal, headers=headers_hasil)
    match_hasil = re.search(r'<a class="w3-button w3-blue w3-round" id="download" href="([^"]+)"', response_hasil.text)
    match_k = re.search(r'onclick="location.href=this.href\+\'&k=\'\+\'([^\']+)\'', response_hasil.text)

    if not match_hasil or not match_k:
        return jsonify({"error": "Failed to extract final download link"}), 500

    link_download_final = f"{match_hasil.group(1)}&k={match_k.group(1)}"
    
    return jsonify({"download_url": link_download_final})

if __name__ == "__main__":
    app.run(debug=True)
  
