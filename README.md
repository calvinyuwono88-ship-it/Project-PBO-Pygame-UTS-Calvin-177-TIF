# 🐾 Crossing Cat - Project PBO Pygame

**Crossing Cat** adalah game *arcade* sederhana bergenre *survival/crossing* yang dikembangkan menggunakan bahasa pemrograman Python dan library Pygame. Dalam game ini, pemain mengendalikan seekor kucing yang harus menyeberangi jalan raya yang sibuk tanpa tertabrak oleh berbagai jenis kendaraan yang melintas. Semakin cepat kucing menyeberang, semakin tinggi skor yang didapatkan!

---

## 📋 Pemenuhan Ketentuan Project

Game ini dikembangkan untuk memenuhi kriteria tugas Pemrograman Berorientasi Objek (PBO) dengan rincian sebagai berikut:

- [x] **Dibuat menggunakan Python dan Pygame**: Game berjalan sepenuhnya menggunakan engine Pygame.
- [x] **Menerapkan konsep PBO (Class dan Object)**: Struktur kode dibagi menjadi beberapa *class* seperti `Entitas`, `Kucing`, `Kendaraan`, dan `Permainan`.
- [x] **Menggunakan konsep Inheritance (Pewarisan)**: Telah diterapkan lebih dari satu kali. Contohnya, class `Kucing` dan `Kendaraan` mewarisi properti dari class induk `Entitas`. Selain itu, class `Sedan`, `Minibus`, dan `Truk` mewarisi class `Kendaraan`.
- [x] **Berjalan tanpa error**: Kode telah distrukturisasi sedemikian rupa dengan penanganan loop dan event yang aman.
- [x] **Memiliki Player/Karakter Utama**: Pemain mengendalikan objek **Kucing**.
- [x] **Memiliki Objek Lain (Rintangan)**: Terdapat berbagai rintangan berupa kendaraan bermotor (Sedan, Minibus, Truk) yang melaju dengan kecepatan bervariasi.
- [x] **Struktur kode rapi dan mudah dipahami**: Variabel konstan dipisahkan, logika pembaruan (*update*) dan penggambaran (*draw*) dienkapsulasi dengan baik di dalam masing-masing class.
- [x] **Tema bebas dan kreatif**: Mengambil tema *animal crossing* (kucing menyeberang jalan) dengan visual pixel/kartun yang menarik.

---

## 🎮 Fitur Game

1. **Mekanik Pergerakan**: Karakter utama dapat bergerak ke 4 arah (Atas, Bawah, Kiri, Kanan) menggunakan tombol Panah (*Arrow Keys*).
2. **Sistem Rintangan Dinamis**: Kendaraan muncul secara acak dari bawah layar pada jalur (*lane*) yang berbeda dengan kecepatan yang bervariasi.
3. **Deteksi Tabrakan (Collision Detection)**: Jika kucing menyentuh kendaraan, game akan masuk ke status *Game Over*.
4. **Sistem Skor & Waktu**: Terdapat *timer* yang menghitung seberapa cepat pemain menyelesaikan level. Semakin cepat sampai ke zona aman (garis finish), skor akhir akan semakin besar (Maksimal skor: 10.000).
5. **Zona Aman (Trotoar & Marka)**: Pemain dapat beristirahat sejenak di area trotoar atau marka jalan putih.
6. **Antarmuka Interaktif (UI)**: Tersedia tombol interaktif yang bisa diklik menggunakan *mouse* untuk **Restart**, membuka menu **Bantuan**, dan **Keluar** dari game.
7. **Audio/BGM**: Dilengkapi dengan *backsound* yang berputar terus-menerus selama permainan berlangsung untuk menambah keseruan.

---

## 🧩 Struktur Kode & Konsep PBO

Proyek ini sangat mengandalkan paradigma *Object-Oriented Programming*. Berikut adalah arsitektur *class* di dalam kode:

* **`Entitas` (Base Class)**: Class dasar untuk semua objek fisik di dalam game. Menyimpan posisi koordinat (`x`, `y`) dan *bounding box* (`pygame.Rect`) untuk keperluan *collision*.
    * **`Kucing` (Inherits from `Entitas`)**: Class untuk karakter pemain. Memiliki metode tambahan untuk membaca input *keyboard* dan membatasi pergerakan agar tidak keluar layar.
    * **`Kendaraan` (Inherits from `Entitas`)**: Class dasar untuk rintangan. Mengatur logika pergerakan maju secara otomatis.
        * **`Sedan`, `Minibus`, `Truk` (Inherits from `Kendaraan`)**: Class turunan spesifik yang mendefinisikan ukuran (*hitbox*), *sprite* gambar, dan variasi kecepatan dari masing-masing tipe kendaraan.
* **`Permainan` (Main Controller)**: Mengelola *game loop*, inisialisasi Pygame, memuat aset (gambar & suara), mendeteksi *event* (input UI), mengatur *spawn* musuh, dan menggambar (render) seluruh objek ke layar.

---

## 🚀 Cara Menjalankan Game

**Prasyarat:**
Pastikan kamu sudah menginstal Python 3.x dan library Pygame di komputermu. Jika belum memiliki Pygame, instal menggunakan pip:
```bash
pip install pygame
