# PredictPhoneApi

API untuk memprediksi estimasi harga smartphone berdasarkan spesifikasi perangkat, lokasi, jaringan, dan kondisi barang.

Project ini menggunakan Machine Learning untuk menghasilkan **estimasi harga** serta **rentang harga wajar** dari smartphone yang dimasukkan oleh pengguna.

## Tentang Project

`PredictPhoneApi` merupakan REST API berbasis Python dan Flask yang menggunakan model Machine Learning untuk melakukan prediksi harga smartphone.

Pengguna dapat memberikan informasi seperti:

* Merek smartphone
* RAM
* Storage
* Kapasitas baterai
* Ukuran layar
* Tahun rilis
* NFC
* Jenis jaringan
* Kota
* Kondisi smartphone

API kemudian memproses data tersebut dan menghasilkan estimasi harga.

## Teknologi

Project ini menggunakan beberapa teknologi berikut:

| Teknologi    | Kegunaan                           |
| ------------ | ---------------------------------- |
| Python       | Bahasa pemrograman utama           |
| Flask        | Framework untuk membuat REST API   |
| Pandas       | Pengolahan data                    |
| NumPy        | Operasi numerik                    |
| Scikit-learn | Preprocessing dan Machine Learning |
| XGBoost      | Model prediksi                     |
| Joblib       | Penyimpanan dan pemuatan model     |
| Railway      | Deployment API                     |

## Struktur Project

```text
PredictPhoneApi/
│
├── app.py
├── predict_final_test.py
├── price_model_v2.joblib
├── gsmarena_specs.csv
├── requirements.txt
├── Procfile
└── README.md
```

### Penjelasan File

**`app.py`**

File utama yang menjalankan Flask API dan menangani request dari pengguna.

**`predict_final_test.py`**

Script untuk melakukan pengujian prediksi secara lokal melalui command line.

**`price_model_v2.joblib`**

Model Machine Learning yang telah dilatih dan digunakan untuk melakukan prediksi harga.

**`gsmarena_specs.csv`**

Dataset spesifikasi smartphone yang digunakan sebagai katalog untuk membantu melengkapi informasi perangkat.

**`requirements.txt`**

Berisi daftar library Python yang diperlukan untuk menjalankan project.

**`Procfile`**

Berisi perintah yang digunakan oleh platform deployment untuk menjalankan aplikasi.

## Cara Menjalankan Secara Lokal

### 1. Clone Repository

```bash
git clone https://github.com/DimasHizkiawan/PredictPhoneApi.git
cd PredictPhoneApi
```

### 2. Buat Virtual Environment

Windows:

```bash
py -m venv venv
```

Aktifkan:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan API

```bash
python app.py
```

Jika berhasil, Flask akan menjalankan server secara lokal.

Contoh:

```text
http://127.0.0.1:5000
```

## Cara Kerja Sistem

```text
Input Pengguna
      |
      v
Informasi Smartphone
      |
      v
Pencarian Spesifikasi
      |
      v
Preprocessing Data
      |
      v
Machine Learning Model
      |
      v
Prediksi Harga
      |
      v
Estimasi + Rentang Harga
```

Model menerima beberapa fitur numerik dan kategorikal, kemudian memprosesnya melalui preprocessing sebelum digunakan oleh model Machine Learning.

### Fitur Numerik

* RAM
* Storage
* Kapasitas baterai
* Ukuran layar
* Tahun rilis
* Umur perangkat
* NFC

### Fitur Kategorikal

* Brand
* Network type
* Kota
* Kondisi

## Status Project

Project masih dalam tahap pengembangan.

Fitur yang direncanakan untuk dikembangkan lebih lanjut:

* Peningkatan kualitas dataset
* Peningkatan akurasi model
* Penambahan fitur kondisi perangkat
* Perbaikan pencarian spesifikasi smartphone
* Pengembangan endpoint API
* Pengembangan interface untuk pengguna

## Author

**Dimas Hizkiawan**

Project pembelajaran Machine Learning dan pengembangan REST API.
