"""
Backend API untuk prediksi harga HP bekas
============================================
Membungkus price_model_v2.joblib jadi REST API yang bisa dipanggil
dari website (frontend HTML/JS apapun, tidak harus buatan Claude).

Endpoint:
  POST /predict
    Body (JSON), salah satu dari 2 mode:

    Mode 1 -- cari otomatis dari katalog:
      {"model": "Galaxy A53 5G", "storage": "128GB", "kota": "jakarta", "kondisi": "Bekas"}

    Mode 2 -- input manual:
      {"manual": true, "brand": "Samsung", "ram": 8, "storage": 128,
       "battery": 5000, "display": 6.5, "tahun": 2022, "nfc": 1,
       "network": "5G", "kota": "surabaya", "kondisi": "Bekas"}

  GET /search?q=<nama model>
    Cari model di katalog (untuk autocomplete di frontend)

Usage lokal:
  pip install flask flask-cors
  python app.py
  -> server jalan di http://localhost:5000

Deploy ke internet (opsi umum, pilih salah satu):
  - Render.com / Railway.app (gratis untuk trafik kecil, paling mudah)
  - PythonAnywhere
  - VPS sendiri (DigitalOcean, dll) + gunicorn/nginx

PENTING: --debug HARUS dimatikan (debug=False) kalau sudah live di
internet, dan cek CORS_ORIGINS supaya cuma domain website kamu yang
boleh akses API ini.
"""

import re
import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

MODEL_PATH = 'price_model_v2.joblib'
SPECS_PATH = 'gsmarena_specs.csv'

app = Flask(__name__)
# GANTI "*" dengan domain website kamu yang sebenarnya sebelum live,
# mis. CORS(app, origins=["https://situskamu.com"])
CORS(app, origins="*")

print("Memuat model...")
BUNDLE = joblib.load(MODEL_PATH)
SPECS = pd.read_csv(SPECS_PATH)
print(f"Model dimuat. Katalog: {len(SPECS)} baris spesifikasi.")


def parse_gb(val):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return np.nan
    val = str(val).upper().strip()
    m = re.match(r'([\d.]+)\s*(GB|TB)?', val)
    if not m:
        return np.nan
    num = float(m.group(1))
    unit = m.group(2) or 'GB'
    return num * 1024 if unit == 'TB' else num


def build_input_row(brand, ram_gb, storage_gb, battery_mah, display_inch,
                     release_year, has_nfc, network_type, kota, kondisi):
    rare_kota_list = BUNDLE.get('rare_kota_list', [])
    current_year = BUNDLE.get('current_year', 2026)

    kota_norm = str(kota).lower().strip() if kota else '(tidak diketahui)'
    if kota_norm in rare_kota_list:
        kota_norm = 'lainnya'

    row = {
        'ram_numeric': parse_gb(ram_gb),
        'storage_numeric': parse_gb(storage_gb),
        'battery_mah': float(battery_mah),
        'display_inch': float(display_inch),
        'release_year': int(release_year),
        'umur_tahun': current_year - int(release_year),
        'has_nfc': int(has_nfc),
        'brand': brand,
        'network_type': network_type or '4G',
        'kota_norm': kota_norm,
        'condition': kondisi or 'Tidak Diketahui',
        'kondisi_resmi_ibox': False, 'kondisi_inter': False,
        'kondisi_second': False, 'kondisi_fullset': False,
        'kondisi_ada_minus': False, 'kondisi_cicilan': False,
        'kondisi_bnib_baru': False, 'kondisi_garansi': False,
    }
    return pd.DataFrame([row])


def run_prediction(X: pd.DataFrame):
    model = BUNDLE['model']
    feature_num = BUNDLE['feature_num']
    feature_cat = BUNDLE['feature_cat']
    for col in feature_num + feature_cat:
        if col not in X.columns:
            X[col] = 0 if col in feature_num else 'unknown'
    X = X[feature_num + feature_cat]

    pred_log = model.predict(X)
    pred = float(np.expm1(pred_log)[0])
    mape = BUNDLE.get('cv_mape_mean', 0.20)
    return {
        'harga_estimasi': round(pred),
        'harga_min': round(pred * (1 - mape)),
        'harga_max': round(pred * (1 + mape)),
        'mape_model': round(mape * 100, 1),
    }


@app.route('/search', methods=['GET'])
def search():
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify([])
    matches = SPECS[SPECS['model_name'].str.contains(q, case=False, na=False, regex=False)]
    results = (
        matches[['model_name', 'ram_gb', 'storage_gb']]
        .drop_duplicates()
        .head(20)
        .to_dict('records')
    )
    return jsonify(results)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)

    try:
        if data.get('manual'):
            required = ['brand', 'ram', 'storage', 'battery', 'display', 'tahun']
            missing = [f for f in required if data.get(f) is None]
            if missing:
                return jsonify({'error': f'Field wajib kosong: {missing}'}), 400

            X = build_input_row(
                data['brand'], data['ram'], data['storage'], data['battery'],
                data['display'], data['tahun'], data.get('nfc', 0),
                data.get('network', '4G'), data.get('kota'), data.get('kondisi')
            )
            model_desc = f"{data['brand']} (spek manual)"

        else:
            model_query = data.get('model', '').strip()
            if not model_query:
                return jsonify({'error': "Field 'model' kosong. Isi nama model atau pakai mode manual."}), 400

            candidates = SPECS[SPECS['model_name'].str.contains(model_query, case=False, na=False, regex=False)]
            if len(candidates) == 0:
                return jsonify({'error': f"Model '{model_query}' tidak ditemukan di katalog."}), 404

            storage_gb = parse_gb(data.get('storage'))
            if storage_gb is not None and not pd.isna(storage_gb):
                filtered = candidates[candidates['storage_gb'].apply(parse_gb) == storage_gb]
                if len(filtered) > 0:
                    candidates = filtered

            row = candidates.iloc[0]
            X = build_input_row(
                row['brand'], row['ram_gb'], row['storage_gb'], row['battery_mah'],
                row['display_inch'], row['release_year'], row['has_nfc'],
                row['network_type'] if pd.notna(row['network_type']) else '4G',
                data.get('kota'), data.get('kondisi')
            )
            model_desc = f"{row['model_name']} ({row['ram_gb']}/{row['storage_gb']})"

        result = run_prediction(X)
        result['model'] = model_desc
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'katalog_size': len(SPECS)})


if __name__ == '__main__':
    import os
    # Railway (dan hosting lain) assign PORT lewat environment variable,
    # bukan selalu 5000. debug=False wajib untuk produksi.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)