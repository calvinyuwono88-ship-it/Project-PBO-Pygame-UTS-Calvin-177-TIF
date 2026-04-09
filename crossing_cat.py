import pygame
import random
import sys
import time
import os

LEBAR, TINGGI = 1280, 720
FPS = 60

W_TROTOAR = (200, 200, 200)
W_JALAN = (40, 40, 45)
W_PUTIH = (245, 245, 245)
W_HITAM = (20, 20, 20)
W_BAR_UI = (50, 50, 60)
W_TOMBOL = (100, 150, 200)
W_TOMBOL_SOROT = (150, 200, 250)

GRID_X = [64, 208, 316, 424, 532, 640, 748, 856, 964, 1072, 1216]

GRID_Y = [280, 320, 360, 400, 440]

class Entitas(pygame.sprite.Sprite):
    def __init__(self, x, y, lebar, tinggi):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.rect = pygame.Rect(0, 0, lebar, tinggi)
        self.rect.center = (int(self.x), int(self.y))

    def perbarui(self):
        pass

    def gambar(self, permukaan):
        pass

class Kucing(Entitas):
    def __init__(self):
        super().__init__(GRID_X[0], GRID_Y[2], 30, 30)
        self.kecepatan = 3.0
        self.hidup = True
        self.menang = False
        self.image = GAMBAR_KUCING

    def perbarui(self):
        if not self.hidup or self.menang:
            return
        
        tombol = pygame.key.get_pressed()
        if tombol[pygame.K_LEFT] and self.x > 30:
            self.x -= self.kecepatan
        if tombol[pygame.K_RIGHT] and self.x < LEBAR - 30:
            self.x += self.kecepatan
        if tombol[pygame.K_UP] and self.y > 240:
            self.y -= self.kecepatan
        if tombol[pygame.K_DOWN] and self.y < 480:
            self.y += self.kecepatan
            
        self.rect.center = (int(self.x), int(self.y))

    def gambar(self, permukaan):
        cx, cy = self.x, self.y
        rect_gambar = self.image.get_rect(center=(int(cx), int(cy)))
        permukaan.blit(self.image, rect_gambar)
        
        if not self.hidup:
            pygame.draw.line(permukaan, W_HITAM, (cx-15, cy-15), (cx+15, cy+15), 4)
            pygame.draw.line(permukaan, W_HITAM, (cx+15, cy-15), (cx-15, cy+15), 4)

class Kendaraan(Entitas):
    def __init__(self, indeks_jalur, lebar, tinggi, gambar_kendaraan, kecepatan_dasar, offset_x=0):
        x = GRID_X[indeks_jalur * 2 + 1] + offset_x
        y = TINGGI + 100
        super().__init__(x, y, lebar, tinggi)
        self.image = gambar_kendaraan
        
        pengali_kecepatan_jalur = [1.0, 1.3, 0.8, 1.5, 1.1]
        self.kecepatan = kecepatan_dasar * pengali_kecepatan_jalur[indeks_jalur]

    def perbarui(self):
        self.y -= self.kecepatan
        self.rect.centery = int(self.y)

    def gambar(self, permukaan):
        permukaan.blit(self.image, self.rect)

class Sedan(Kendaraan):
    def __init__(self, indeks_jalur):
        kecepatan = random.uniform(4.0, 6.0)
        super().__init__(indeks_jalur, 50, 90, GAMBAR_KENDARAAN['sedan'], kecepatan, offset_x=-25)

class Minibus(Kendaraan):
    def __init__(self, indeks_jalur):
        super().__init__(indeks_jalur, 60, 120, GAMBAR_KENDARAAN['minibus'], random.uniform(4.5, 5.5), offset_x=25)

class Truk(Kendaraan):
    def __init__(self, indeks_jalur):
        super().__init__(indeks_jalur, 70, 160, GAMBAR_KENDARAAN['truk'], random.uniform(5.0, 6.0), offset_x=25)

GAMBAR_KENDARAAN = {}
GAMBAR_KUCING = None
GAMBAR_POHON = None

class Permainan:
    def __init__(self):
        pygame.init()
        self.layar = pygame.display.set_mode((LEBAR, TINGGI))
        pygame.display.set_caption("Crossing Cat - PBO Pygame")
        self.jam = pygame.time.Clock()
        
        self.font_judul = pygame.font.SysFont("Courier New", 36, bold=True)
        self.font_ui    = pygame.font.SysFont("Courier New", 24, bold=True)
        self.font_besar = pygame.font.SysFont("Courier New", 64, bold=True)
        
        global GAMBAR_KUCING, GAMBAR_POHON
        
        img_kucing = pygame.image.load(os.path.join("aset", "kucing.png")).convert_alpha()
        GAMBAR_KUCING = pygame.transform.scale(img_kucing, (160, 100))
        
        img_pohon = pygame.image.load(os.path.join("aset", "pohon.png")).convert_alpha()
        GAMBAR_POHON = pygame.transform.scale(img_pohon, (70, 70))
        
        img_sedan = pygame.image.load(os.path.join("aset", "sedan.png")).convert_alpha()
        GAMBAR_KENDARAAN['sedan'] = pygame.transform.scale(img_sedan, (50, 90))
        
        img_minibus = pygame.image.load(os.path.join("aset", "minibus.png")).convert_alpha()
        GAMBAR_KENDARAAN['minibus'] = pygame.transform.scale(img_minibus, (60, 120))
        
        img_truk = pygame.image.load(os.path.join("aset", "truk.png")).convert_alpha()
        GAMBAR_KENDARAAN['truk'] = pygame.transform.scale(img_truk, (70, 160))

        pygame.mixer.music.load(os.path.join("aset", "backsound.mp3"))
        pygame.mixer.music.play(-1)

        self.tampilkan_bantuan = False
        self.reset_permainan()

    def reset_permainan(self):
        self.kucing = Kucing()
        self.daftar_kendaraan = []
        self.timer_muncul = [0] * 5
        self.waktu_mulai = time.time()
        self.waktu_akhir = 0
        self.status = "BERMAIN"

    def tangani_input(self):
        for kejadian in pygame.event.get():
            if kejadian.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if kejadian.type == pygame.MOUSEBUTTONDOWN and kejadian.button == 1:
                mx, my = kejadian.pos
                if TINGGI - 50 <= my <= TINGGI - 10:
                    if 20 <= mx <= 140:
                        self.reset_permainan()
                    if 160 <= mx <= 280:
                        self.tampilkan_bantuan = not self.tampilkan_bantuan
                    if 300 <= mx <= 420:
                        pygame.quit()
                        sys.exit()

            if kejadian.type == pygame.KEYDOWN:
                if kejadian.key == pygame.K_r:
                    self.reset_permainan()
                if self.tampilkan_bantuan and kejadian.key in [pygame.K_ESCAPE, pygame.K_SPACE]:
                    self.tampilkan_bantuan = False

    def perbarui(self):
        if self.status != "BERMAIN" or self.tampilkan_bantuan:
            return

        waktu_berjalan = time.time() - self.waktu_mulai
        self.skor = max(0, 10000 - int(waktu_berjalan * 100))

        for lane in range(5):
            self.timer_muncul[lane] += 1
            if self.timer_muncul[lane] > random.randint(60, 150):
                spawn_aman = True
                x_jalur = GRID_X[lane * 2 + 1]
                for v in self.daftar_kendaraan:
                    if v.rect.centerx == x_jalur and v.y > TINGGI - 120:
                        spawn_aman = False
                        break
                
                if spawn_aman:
                    tipe_v = random.choice([Sedan, Sedan, Minibus, Truk])
                    self.daftar_kendaraan.append(tipe_v(lane))
                    self.timer_muncul[lane] = 0

        self.kucing.perbarui()
        for v in self.daftar_kendaraan:
            v.perbarui()

        self.daftar_kendaraan = [v for v in self.daftar_kendaraan if v.y > -100]

        for v in self.daftar_kendaraan:
            if self.kucing.rect.colliderect(v.rect):
                self.kucing.hidup = False
                self.status = "GAME_OVER"
                self.waktu_akhir = waktu_berjalan
                break

        if self.kucing.x >= GRID_X[10]:
            self.kucing.menang = True
            self.status = "MENANG"
            self.waktu_akhir = waktu_berjalan

    def gambar_lingkungan(self):
        self.layar.fill(W_JALAN)
        
        pygame.draw.rect(self.layar, W_TROTOAR, (0, 0, 128, TINGGI))
        pygame.draw.rect(self.layar, W_TROTOAR, (LEBAR - 128, 0, 128, TINGGI))

        for ty in range(50, TINGGI - 50, 150):
            self.layar.blit(GAMBAR_POHON, GAMBAR_POHON.get_rect(center=(64, ty)))
            self.layar.blit(GAMBAR_POHON, GAMBAR_POHON.get_rect(center=(LEBAR - 64, ty)))

        for i in [2, 4, 6, 8]:
            x_pos = GRID_X[i]
            pygame.draw.rect(self.layar, W_PUTIH, (x_pos - 16, 0, 32, TINGGI))

        for x in range(128, LEBAR - 128, 40):
            pygame.draw.rect(self.layar, W_PUTIH, (x, 240, 20, 240))

    def gambar_antarmuka(self):
        pygame.draw.rect(self.layar, W_BAR_UI, (0, TINGGI - 60, LEBAR, 60))
        
        pos_mouse = pygame.mouse.get_pos()
        tombol_tombol = [("Restart", 20), ("Bantuan", 160), ("Keluar", 300)]
        for teks, bx in tombol_tombol:
            rect_tombol = pygame.Rect(bx, TINGGI - 50, 120, 40)
            warna = W_TOMBOL_SOROT if rect_tombol.collidepoint(pos_mouse) else W_TOMBOL
            pygame.draw.rect(self.layar, warna, rect_tombol, border_radius=5)
            
            surf_teks = self.font_ui.render(teks, True, W_HITAM)
            self.layar.blit(surf_teks, (bx + 60 - surf_teks.get_width()//2, TINGGI - 40))

        waktu_berjalan = time.time() - self.waktu_mulai if self.status == "BERMAIN" else self.waktu_akhir
        
        teks = self.font_judul.render("CROSSING CAT", True, (255, 0, 0))
        posisi = teks.get_rect(midtop=(LEBAR//2, 20))
        bingkai = posisi.inflate(40, 20)
        
        pygame.draw.rect(self.layar, (30, 30, 30), bingkai, border_radius=10)
        pygame.draw.rect(self.layar, (255, 0, 0), bingkai, 3, border_radius=10)
        self.layar.blit(teks, posisi)
        
        teks_waktu = self.font_ui.render(f"Waktu: {waktu_berjalan:.2f}s", True, W_PUTIH)
        self.layar.blit(teks_waktu, (LEBAR - 250, 20))

    def gambar_lapisan_layar(self):
        if self.tampilkan_bantuan:
            lapisan = pygame.Surface((LEBAR, TINGGI))
            lapisan.set_alpha(220)
            lapisan.fill(W_HITAM)
            self.layar.blit(lapisan, (0, 0))
            
            baris_teks = [
                "CARA BERMAIN:",
                "- Gunakan tombol Panah [KIRI] dan [KANAN] untuk menyeberang.",
                "- Gunakan tombol Panah [ATAS] dan [BAWAH] untuk naik/turun.",
                "- Hindari mobil yang melaju dari bawah.",
                "- Garis Marka Putih Solid adalah ZONA AMAN.",
                "- Semakin cepat menyeberang, Skor semakin tinggi!",
                ""
                "(Tekan SPASI untuk kembali)"
            ]
            
            for i, baris in enumerate(baris_teks):
                teks = self.font_ui.render(baris, True, W_PUTIH)
                self.layar.blit(teks, (LEBAR//2 - teks.get_width()//2, 200 + (i*40)))
                
        elif self.status == "GAME_OVER":
            teks_judul = self.font_besar.render("KUCING TERTABRAK!", True, (255, 50, 50))
            teks_info = self.font_ui.render("Tekan 'R' atau klik Restart untuk main lagi", True, (255, 0, 0))
            
            posisi_judul = teks_judul.get_rect(midtop=(LEBAR // 2, TINGGI // 2 - 50))
            posisi_info = teks_info.get_rect(midtop=(LEBAR // 2, TINGGI // 2 + 30))
            
            rect_kotak = posisi_judul.union(posisi_info).inflate(60, 40)
            
            pygame.draw.rect(self.layar, (0, 0, 0), rect_kotak, border_radius=15)
            
            self.layar.blit(teks_judul, posisi_judul)
            self.layar.blit(teks_info, posisi_info)
            
        elif self.status == "MENANG":
            teks_menang = self.font_besar.render("MENYEBERANG BERHASIL!", True, (50, 255, 50))
            posisi_menang = teks_menang.get_rect(midtop=(LEBAR // 2, TINGGI // 2 - 80))
            self.layar.blit(teks_menang, posisi_menang)
            
            teks_skor = self.font_ui.render(f"Skor Akhir: {self.skor}", True, W_PUTIH)
            posisi_skor = teks_skor.get_rect(center=(LEBAR // 2, TINGGI // 2 + 40))
            
            rect_kotak = posisi_skor.inflate(60, 30)
            
            pygame.draw.rect(self.layar, (30, 30, 30), rect_kotak, border_radius=15)
            pygame.draw.rect(self.layar, (50, 255, 50), rect_kotak, 4, border_radius=15)
            
            self.layar.blit(teks_skor, posisi_skor)

    def gambar(self):
        self.gambar_lingkungan()
        
        for v in self.daftar_kendaraan:
            v.gambar(self.layar)
            
        self.kucing.gambar(self.layar)
        
        self.gambar_antarmuka()
        self.gambar_lapisan_layar()
        
        pygame.display.flip()

    def jalankan(self):
        while True:
            self.tangani_input()
            self.perbarui()
            self.gambar()
            self.jam.tick(FPS)

if __name__ == "__main__":
    game = Permainan()
    game.jalankan()
    