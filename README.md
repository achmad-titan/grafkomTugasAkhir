# 🧩 3D & 2D Graphics Demo with PyOpenGL & Pygame

Proyek ini merupakan kumpulan **demo grafika komputer interaktif**, baik **2D** maupun **3D**, yang dibangun menggunakan **Python**, **Pygame**, dan **PyOpenGL**.

## 📦 Isi Proyek

- 🔷 **3D Graphics Demo**: Visualisasi objek 3D (Kubus & Piramida) dengan kontrol kamera dan pencahayaan.
- 🔶 **2D Graphics Editor**: Editor grafis 2D interaktif yang mendukung transformasi objek dan clipping window.

---

# 🎲 3D Graphics Demo with PyOpenGL & Pygame

Visualisasi interaktif objek 3D (Kubus dan Piramida) menggunakan **PyOpenGL** dan **Pygame**. Aplikasi ini mendukung pencahayaan (Phong), kontrol kamera, translasi dan rotasi objek melalui keyboard dan mouse.

## 🎮 Fitur Utama

- Visualisasi objek 3D: **Cube** dan **Pyramid**
- Transformasi objek: translasi (WASD) & rotasi (panah/mouse)
- Kamera dinamis (zoom in/out)
- Lighting interaktif (on/off)
- Wireframe & shading dengan Gouraud Lighting
- Render simultan dua objek

## 🖼️ Preview

Tampilan akan muncul dalam jendela OpenGL saat program dijalankan. Objek dapat digerakkan dan diputar secara interaktif.

## 🛠️ Instalasi

Pastikan Python 3.x telah terpasang, lalu install dependensi:

```bash
pip install PyOpenGL PyOpenGL_accelerate pygame

🚀 Menjalankan Aplikasi
bash
Salin
Edit
python namafile.py
Gantilah namafile.py dengan nama file Python Anda (misalnya main_3d.py).

🎮 Kontrol
Tombol	Fungsi
W, A, S, D	Translasi objek (atas/kiri/bawah/kanan)
Panah (↑↓←→)	Rotasi objek
Mouse Drag	Rotasi objek dengan mouse
Q, E	Zoom kamera masuk / keluar
1	Tampilkan objek Cube
2	Tampilkan objek Pyramid
3	Tampilkan keduanya
L	Toggle lighting
ESC	Keluar dari aplikasi

🧱 Struktur Kode
Object3D : Kelas dasar objek 3D

Cube, Pyramid : Turunan dari Object3D

Camera : Mengatur perspektif dan posisi kamera

Lighting : Setup ambient, diffuse, dan specular lighting

Graphics3D : Kelas utama untuk rendering dan kontrol

⚙️ Teknologi
PyOpenGL

Pygame

📋 Catatan Tambahan
Lighting menggunakan Phong model

Shading menggunakan Gouraud

Normal vector dihitung per face untuk efek pencahayaan realistis

✏️ 2D Graphics Editor with PyOpenGL & Pygame
Editor grafis 2D interaktif yang memungkinkan pengguna menggambar dan memanipulasi objek-objek 2D menggunakan OpenGL.

✨ Fitur
Gambar objek 2D:

Titik (Point)

Garis (Line)

Persegi (Rectangle)

Elips (Ellipse)

Transformasi objek:

Translasi

Rotasi

Skala

Window Clipping (Cohen-Sutherland)

Warna & ketebalan garis dinamis

Interaksi objek (pilih, hapus, transformasi)

🚀 Menjalankan Editor
bash
Salin
Edit
python editor2d.py
🎮 Kontrol Lengkap
Mode Gambar
Tombol	Mode
F1	Titik
F2	Garis
F3	Persegi
F4	Elips

Interaksi Objek
Tombol	Aksi
Klik Kiri	Menentukan titik gambar
C	Ganti warna
T	Ganti ketebalan garis
TAB	Pilih objek berikutnya
DELETE	Hapus objek terpilih

Transformasi
Tombol	Aksi
W, A, S, D	Geser objek
Q, E	Rotasi objek
Z, X	Perbesar / perkecil objek

Clipping Window
Tombol	Aksi
V	Aktifkan mode pembuatan window
Klik (2x)	Tentukan sudut kiri bawah & kanan atas
Panah	Geser window kliping
+ / -	Zoom window kliping
B	Hapus window kliping

Keluar
ESC untuk keluar

⚠️ Catatan Penting
🛠 Beberapa konstruktor ditulis dengan salah (_init_) → harus diganti menjadi __init__ agar aplikasi berjalan normal!

💡 Teknologi yang Digunakan
Python 3.x

Pygame

PyOpenGL

🧪 Visual
Objek di dalam clipping window ditandai dengan warna hijau terang

Transformasi dilakukan terhadap titik pivot tiap objek
