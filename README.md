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

## Pengujian Prediksi

Prediksi juga dapat dilakukan menggunakan script `predict_final_test.py`.

Contoh:

```bash
py predict_final_test.py --model "Apple iPhone 17" --storage 256GB --kota Bandung --kondisi Bekas
```

Contoh untuk kondisi baru:

```bash
py predict_final_test.py --model "Apple iPhone 17" --storage 256GB --kota Bandung --kondisi Baru
```

Output akan memberikan informasi seperti:

```text
Model              : Apple iPhone 17
Estimasi harga     : Rp 13,375,070
Rentang harga      : Rp 10,795,536 — Rp 15,954,604
MAPE               : ±19.3%
```

## Cara Kerja Sistem

Secara sederhana, proses prediksi berjalan seperti berikut:

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

Beberapa fitur numerik yang digunakan antara lain:

* RAM
* Storage
* Kapasitas baterai
* Ukuran layar
* Tahun rilis
* Umur perangkat
* NFC

### Fitur Kategorikal

Beberapa fitur kategorikal meliputi:

* Brand
* Network type
* Kota
* Kondisi

## Rentang Harga

Selain menghasilkan satu nilai prediksi, sistem juga memberikan rentang harga.

Rentang tersebut dihitung berdasarkan nilai prediksi dan nilai MAPE model.

Secara sederhana:

```text
Harga minimum = Prediksi × (1 - MAPE)

Harga maksimum = Prediksi × (1 + MAPE)
```

Contohnya, apabila model menghasilkan:

```text
Prediksi = Rp10.000.000
MAPE     = 20%
```

maka rentang yang diberikan adalah:

```text
Rp8.000.000 — Rp12.000.000
```

Rentang ini merupakan estimasi berdasarkan performa model, bukan jaminan harga pasar sebenarnya.

## Model Machine Learning

Model disimpan dalam:

```text
price_model_v2.joblib
```

Model menggunakan preprocessing untuk menangani fitur numerik dan kategorikal sebelum melakukan prediksi.

Pipeline secara umum:

```text
Raw Input
    |
    v
Data Preprocessing
    |
    +---- Numerical Features
    |
    +---- Categorical Features
    |
    v
XGBoost Regressor
    |
    v
Predicted Price
```

## API Endpoint

Aplikasi Flask menyediakan endpoint untuk melakukan prediksi harga.

Contoh request:

```http
POST /predict/
```

Data dapat dikirim melalui form sesuai dengan field yang disediakan oleh aplikasi.

Contoh konsep request:

```text
model       = Apple iPhone 17
storage     = 256GB
kota        = Bandung
kondisi     = Bekas
```

API kemudian mengembalikan hasil prediksi harga.

## Deployment

Project ini dapat dijalankan secara online menggunakan platform deployment seperti Railway.

Konfigurasi utama deployment:

```text
Procfile
requirements.txt
app.py
price_model_v2.joblib
```

Procfile:

```text
web: python app.py
```

`requirements.txt` digunakan untuk meng-install seluruh dependency yang diperlukan oleh aplikasi.

## Tujuan Project

Project ini dibuat sebagai implementasi Machine Learning untuk mempelajari bagaimana model prediksi dapat digunakan dalam sebuah aplikasi nyata.

Tujuan utama project:

1. Mengolah data spesifikasi smartphone.
2. Melakukan preprocessing data.
3. Melatih model Machine Learning.
4. Mengintegrasikan model ke dalam Flask API.
5. Menghasilkan estimasi harga smartphone.
6. Melakukan deployment API agar dapat diakses secara online.

## Catatan

Hasil prediksi merupakan **estimasi dari model Machine Learning** dan tidak dapat dianggap sebagai harga jual pasti.

Harga smartphone sebenarnya dapat dipengaruhi oleh berbagai faktor lain seperti:

* Kondisi fisik
* Battery health
* Kelengkapan perangkat
* Garansi
* Riwayat penggunaan
* Kredibilitas penjual
* Kondisi pasar
* Waktu penjualan

Oleh karena itu, hasil API sebaiknya digunakan sebagai **referensi estimasi harga**, bukan sebagai satu-satunya dasar dalam menentukan harga jual atau beli.

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
