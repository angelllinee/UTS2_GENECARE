from flask import Flask, render_template, request, redirect, url_for
from aws_kms_manager import AWSKMSManager
from encryptor import AESEncryptor
import mysql.connector
from recommendation_engine import generate_recommendations  # Pastikan file ini ada

# Konfigurasi AWS KMS
KMS_KEY_ID = 'arn:aws:kms:ap-southeast-1:842675983344:key/6f237dba-aa62-4e37-b814-5e72eedf7f22'
REGION_NAME = 'ap-southeast-1'

app = Flask(__name__)
kms = AWSKMSManager(key_id=KMS_KEY_ID, region_name=REGION_NAME)

# Fungsi koneksi MySQL
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='genecare'
    )

# Simpan DNA terbaru untuk dianalisis di global
last_uploaded_dna = ""

@app.route('/')
def home():
    return redirect(url_for('upload_dna'))

@app.route('/upload_dna', methods=['GET', 'POST'])
def upload_dna():
    global last_uploaded_dna

    if request.method == 'POST':
        dna_content = request.form['dna_sequence']
        last_uploaded_dna = dna_content  # Simpan untuk generate rekomendasi nanti
        user_id = 1
        file_name = 'dna_sequence.txt'

        key_info = kms.generate_data_key()
        encryptor = AESEncryptor(key_info['data_key_plain'])
        encrypted = encryptor.encrypt(dna_content.encode())
        encrypted_blob = encrypted['nonce'] + encrypted['tag'] + encrypted['ciphertext']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO dna_tests (user_id, file_name, encrypted_data, encrypted_data_key)
            VALUES (%s, %s, %s, %s)
        ''', (user_id, file_name, encrypted_blob, key_info['data_key_encrypted']))
        conn.commit()
        conn.close()

        return redirect(url_for('recommendations'))

    return render_template('upload_dna.html')

@app.route('/recommendations')
def recommendations():
    global last_uploaded_dna
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT notes FROM medical_records WHERE user_id = %s', (1,))
    medical_records = c.fetchall()
    conn.close()

    # Buat rekomendasi berdasarkan last_uploaded_dna
    recommendations = generate_recommendations(last_uploaded_dna) if last_uploaded_dna else []

    return render_template('recommendation.html', medical_records=medical_records, recommendations=recommendations)

@app.route('/medical_records', methods=['GET', 'POST'])
def medical_records():
    user_id = 1

    if request.method == 'POST':
        notes = request.form['notes']

        key_info = kms.generate_data_key()
        encryptor = AESEncryptor(key_info['data_key_plain'])
        encrypted = encryptor.encrypt(notes.encode())
        encrypted_blob = encrypted['nonce'] + encrypted['tag'] + encrypted['ciphertext']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO medical_records (user_id, notes, encrypted_data)
            VALUES (%s, %s, %s)
        ''', (user_id, notes, encrypted_blob))
        conn.commit()
        conn.close()

        # Kirim hanya catatan yang baru saja dimasukkan
        return render_template('medical_records.html', medical_records=[(notes,)])

    # GET request: ambil satu catatan terakhir dari database
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT notes FROM medical_records WHERE user_id = %s ORDER BY id DESC LIMIT 1', (user_id,))
    medical_records = c.fetchall()
    conn.close()

    return render_template('medical_records.html', medical_records=medical_records)

if __name__ == '__main__':
    app.run(debug=True)
