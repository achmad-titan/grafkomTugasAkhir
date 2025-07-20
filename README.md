# 3D Graphics Demo with PyOpenGL & Pygame

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

Menjalankan Aplikasi
Jalankan file Python utama:

bash
Salin
Edit
python namafile.py
Gantilah namafile.py dengan nama file yang Anda gunakan (misalnya main.py).

🎮 Kontrol
Tombol	Fungsi
W, A, S, D	Translasi objek (naik/kiri/turun/kanan)
Panah (↑↓←→)	Rotasi objek
Mouse Drag	Rotasi objek menggunakan mouse
Q, E	Zoom kamera masuk / keluar
1	Tampilkan objek Cube
2	Tampilkan objek Pyramid
3	Tampilkan keduanya
L	Aktifkan / Nonaktifkan lighting
ESC	Keluar dari aplikasi

🧱 Struktur Kode
Object3D : Kelas dasar untuk objek 3D

Cube dan Pyramid : Turunan dari Object3D

Camera : Mengatur perspektif dan posisi kamera

Lighting : Setup ambient, diffuse, dan specular lighting

Graphics3D : Kelas utama pengatur tampilan, kontrol, dan render

⚙️ Teknologi
PyOpenGL

Pygame

📋 Catatan Tambahan
Lighting menggunakan model Phong.

Shading menggunakan Gouraud shading (smooth).

Normal vector dihitung per face untuk pencahayaan realistis.

📧 Kontak
Jika Anda memiliki pertanyaan, silakan hubungi [email@example.com] atau ajukan issue di repositori ini.

Selamat bereksplorasi dalam dunia grafika komputer 3D! 🎉

yaml
Salin
Edit

---

Jika kamu ingin saya bantu membuat versi dalam bahasa Inggris atau langsung dalam file `.md`, tinggal bilang saja!
