# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import shutil

def clear_screen():
    """Membersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Mencetak banner atau judul program dengan logo DIEAN."""
    # Menggunakan ANSI escape codes untuk warna di terminal
    cyan = "\033[1;36m"
    green = "\033[1;32m"
    yellow = "\033[1;33m"
    white = "\033[1;37m"
    reset = "\033[0m"

    banner = f"""
{cyan}
    ██████╗ ██╗ ███████╗ █████╗ ███╗   ██╗
    ██╔══██╗██║ ██╔════╝██╔══██╗████╗  ██║
    ██║  ██║██║ █████╗  ███████║██╔██╗ ██║
    ██║  ██║██║ ██╔══╝  ██╔══██║██║╚██╗██║
    ██████╔╝██║ ███████╗██║  ██║██║ ╚████║
    ╚═════╝ ╚═╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝
{reset}
{white}====================================================={reset}
{green}    Alat Untuk Unduh Video Menggunakan link {reset}
{yellow}                 by. Diean XD{reset}
{white}====================================================={reset}

{yellow}Skrip ini akan mengunduh video ke folder 'downloads' di penyimpanan internal Anda.{reset}\n
    """
    print(banner)


def check_dependencies():
    """Memeriksa apakah yt-dlp dan ffmpeg sudah terinstal."""
    # Pengecekan yt-dlp
    if not shutil.which('yt-dlp'):
        print("\033[1;31m[!] Perintah 'yt-dlp' tidak ditemukan.\033[0m")
        print("    Sepertinya yt-dlp belum terinstal.")
        print("\n    Silakan instal terlebih dahulu dengan menjalankan perintah:")
        print("    pip install yt-dlp")
        sys.exit(1)

    # --- PERBAIKAN DIMULAI DI SINI ---
    # Pengecekan ffmpeg yang penting untuk menggabungkan video dan audio
    if not shutil.which('ffmpeg'):
        print("\033[1;31m[!] Perintah 'ffmpeg' tidak ditemukan.\033[0m")
        print("    FFmpeg diperlukan untuk menggabungkan video dan audio.")
        print("\n    Silakan instal terlebih dahulu dengan menjalankan perintah:")
        print("    pkg install ffmpeg")
        sys.exit(1)
    # --- PERBAIKAN SELESAI DI SINI ---
    
    # Memeriksa folder penyimpanan bersama
    shared_storage_path = os.path.expanduser('~/storage/downloads')
    if not os.path.isdir(shared_storage_path):
        print("\033[1;31m[!] Folder penyimpanan bersama tidak ditemukan.\033[0m")
        print("    Pastikan Anda telah menjalankan perintah 'termux-setup-storage'")
        print("    dan memberikan izin akses penyimpanan untuk Termux.")
        sys.exit(1)

def download_video(url, download_path):
    """Fungsi utama untuk mengunduh video menggunakan yt-dlp."""
    try:
        # Perintah ini sudah benar, membutuhkan ffmpeg untuk opsi '--merge-output-format'
        command = [
            'yt-dlp',
            '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            '--merge-output-format', 'mp4',
            '-o', os.path.join(download_path, '%(title)s.%(ext)s'),
            url
        ]
        
        print(f"\n[*] Memulai proses unduhan untuk: {url}")
        print(f"[*] Video akan disimpan di: {download_path}")
        print("-" * 50)

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8')
        
        for line in process.stdout:
            print(line, end='')
        
        process.wait()

        if process.returncode == 0:
            print("\n" + "=" * 50)
            print("\033[1;32m[✓] Unduhan Selesai!\033[0m")
            print(f"\033[1;32m[✓] Video berhasil disimpan di folder 'downloads' Anda.\033[0m")
            print("=" * 50)
        else:
            print("\n" + "!" * 50)
            print("\033[1;31m[!] Terjadi kesalahan saat mengunduh.\033[0m")
            print("\033[1;31m[!] Periksa kembali URL atau koneksi internet Anda.\033[0m")
            print("!" * 50)
            
    except subprocess.CalledProcessError as e:
        print(f"\n[X] Gagal menjalankan proses unduhan: {e}")
    except Exception as e:
        print(f"\n[X] Terjadi kesalahan yang tidak terduga: {e}")

def main():
    """Fungsi utama program."""
    try:
        clear_screen()
        print_banner()
        check_dependencies()
        
        download_folder = os.path.expanduser('~/storage/downloads')

        while True:
            video_url = input("\n\033[1;37m[»] Masukkan URL video (atau ketik 'keluar' untuk berhenti): \n> \033[0m")
            
            if video_url.lower() == 'keluar':
                print("\nTerima kasih telah menggunakan skrip ini. Sampai jumpa!")
                break
            
            if not video_url.strip():
                print("\033[1;31m[!] URL tidak boleh kosong, silakan coba lagi.\033[0m")
                continue

            download_video(video_url.strip(), download_folder)

    except KeyboardInterrupt:
        print("\n\n[!] Program dihentikan oleh pengguna. Keluar...")
        sys.exit(0)

if __name__ == '__main__':
    main()

