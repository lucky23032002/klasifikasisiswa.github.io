from flask import Flask, render_template, request
import mysql.connector

def classify_kelas(nilai, sesi):
    if nilai <= 82.5:
        return 'D'
    elif nilai > 94.5:
        return 'A'
    elif nilai <= 89.5:
        if sesi > 58.5:
            return 'B'
        else:
            return 'C'
    elif nilai > 90.5:
        return 'B'
    else:
        return 'C'

app = Flask(__name__)

# Konfigurasi koneksi database (gunakan variabel lingkungan)
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'data_siswa'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        id_siswa = int(request.form['id_siswa'])
        nama_siswa = request.form['nama_siswa']
        jumlah_sesi = int(request.form['jumlah_sesi'])
        nilai_rata_rata = float(request.form['nilai_rata_rata'])

        # Validasi input pengguna di sini

        kelas = classify_kelas(nilai_rata_rata, jumlah_sesi)

        data_siswa = {
            'id_siswa': id_siswa,
            'nama_siswa': nama_siswa,
            'jumlah_sesi': jumlah_sesi,
            'nilai_rata_rata': nilai_rata_rata,
            'kelas': kelas
        }

        # Menggunakan context manager untuk koneksi database
        with mysql.connector.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                # Menjalankan query INSERT untuk menyimpan data siswa ke tabel
                insert_query = "INSERT INTO siswa (id_siswa, nama_siswa, jumlah_sesi, nilai_rata_rata, kelas) VALUES (%s, %s, %s, %s, %s)"
                values = (id_siswa, nama_siswa, jumlah_sesi, nilai_rata_rata, kelas)
                cursor.execute(insert_query, values)
                connection.commit()

        return render_template('result.html', data_siswa=data_siswa)
    except Exception as e:
        # Tangani kesalahan dengan memberikan tanggapan yang sesuai kepada pengguna dan mencatat kesalahan
        print("Error:", str(e))
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
