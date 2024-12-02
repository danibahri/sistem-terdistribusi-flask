# Aplikasi Pemrosesan Sentimen Terdistribusi

Aplikasi ini digunakan untuk menganalisis sentimen dari komentar atau ulasan yang diberikan oleh pengguna di berbagai platform (media sosial, forum, dll.) dengan menggunakan analisis sentimen berbasis model pre-trained. Aplikasi ini dibangun dengan menggunakan Flask sebagai API server, RabbitMQ sebagai message broker untuk komunikasi antar komponen, dan model pre-trained untuk analisis sentimen.

## Fitur Utama
- **Master Node**: Menerima permintaan untuk menganalisis komentar dan mendistribusikannya ke worker nodes.
- **Worker Node**: Memproses komentar menggunakan model analisis sentimen dan mengirimkan hasil kembali ke master node.
- **RabbitMQ**: Message broker yang mendistribusikan tugas dan menerima hasil analisis.

## Teknologi yang Digunakan
- **Flask**: Framework web untuk API Master Node.
- **RabbitMQ**: Message broker untuk mendistribusikan tugas dan menerima hasil.
- **Transformers**: Untuk model analisis sentimen (misalnya BERT).
- **Python**: Bahasa pemrograman utama untuk implementasi.
- **TensorFlow**: Untuk menjalankan model deep learning (opsional, tergantung pada model yang digunakan).

## Prasyarat
Sebelum menjalankan aplikasi, pastikan Anda sudah menginstal:
- **Python 3.6+**
- **RabbitMQ** (terpasang dan berjalan di localhost)
- **Pip** (untuk mengelola dependensi Python)

## Persiapan dan Instalasi

### 1. Clone Repository
Pertama, clone repository ini ke dalam direktori lokal Anda:
```bash
git clone https://github.com/username/repository-name.git
cd repository-name

### 2. Membuat Virtual Environment
Disarankan untuk menggunakan virtual environment agar dependensi proyek terisolasi.

python -m venv env
Aktifkan virtual environment:

Windows:
.\env\Scripts\activate
macOS/Linux:
source env/bin/activate

### 3. Install Dependensi
Install semua dependensi yang diperlukan menggunakan pip:

pip install -r requirements.txt

### 4. Menjalankan RabbitMQ
Pastikan RabbitMQ sudah terinstal dan berjalan di sistem Anda. Jika belum, Anda dapat mengunduh dan menginstalnya di situs resmi RabbitMQ.

Setelah RabbitMQ terpasang, jalankan server RabbitMQ:

rabbitmq-server

### 5. Menyiapkan API Master Node
Master node akan menjalankan API menggunakan Flask. Anda dapat menjalankan aplikasi ini di server lokal.

Untuk menjalankan master node, gunakan perintah berikut:

python app.py --mode master
API Master Node akan berjalan di http://localhost:5000.

### 6. Menjalankan Worker Node
Setelah master node berjalan, Anda dapat menjalankan satu atau lebih worker node untuk memproses tugas secara paralel.

Untuk menjalankan worker node, gunakan perintah berikut di terminal terpisah:

python app.py --mode worker
Anda dapat menjalankan beberapa instance worker dengan membuka terminal baru dan menjalankan perintah yang sama.

### Cara Menggunakan Aplikasi
#### 1. Mengirimkan Tugas untuk Analisis Sentimen
Untuk mengirim komentar atau ulasan yang ingin dianalisis, gunakan endpoint API POST /distribute di master node. Anda dapat menggunakan alat seperti Postman atau curl untuk mengirim permintaan HTTP.

Contoh permintaan dengan curl:

curl -X POST http://localhost:5000/distribute \
     -H "Content-Type: application/json" \
     -d '{
           "comments": [
               "I love this product!",
               "This is the worst service I have ever experienced."
           ]
         }'
Jika berhasil, Anda akan menerima respons seperti ini:

{
  "message": "Tasks distributed successfully."
}

#### 2. Mendapatkan Hasil Analisis
Setelah worker nodes selesai memproses komentar, Anda dapat mendapatkan hasil analisis menggunakan endpoint GET /results di master node.

Contoh permintaan menggunakan curl:

curl http://localhost:5000/results
Respons yang Anda terima akan berisi hasil analisis sentimen untuk setiap komentar:

[
  {
    "comment": "I love this product!",
    "sentiment": {
      "label": "POSITIVE",
      "score": 0.9992
    }
  },
  {
    "comment": "This is the worst service I have ever experienced.",
    "sentiment": {
      "label": "NEGATIVE",
      "score": 0.9987
    }
  }
]
Struktur Proyek
/project-root
│
├── app.py                # File utama aplikasi (Master & Worker Node)
├── requirements.txt      # Daftar dependensi Python
├── README.md             # Dokumentasi proyek ini
└── /models               # Folder untuk model pre-trained
Menghentikan Aplikasi
Untuk menghentikan aplikasi:

Tekan Ctrl+C di terminal tempat Anda menjalankan Flask server (master node).
Tekan Ctrl+C di terminal tempat Anda menjalankan worker nodes.
Troubleshooting
RabbitMQ tidak berjalan: Pastikan RabbitMQ telah berjalan dengan benar. Anda dapat memverifikasi statusnya dengan membuka URL http://localhost:15672 (management interface RabbitMQ).

Kesalahan dependensi: Pastikan semua dependensi diinstal dengan benar menggunakan pip install -r requirements.txt. Jika ada masalah, coba untuk menginstal ulang dependensi.

Masalah koneksi ke RabbitMQ: Pastikan RabbitMQ berjalan di localhost dan port 5672 tidak diblokir oleh firewall.