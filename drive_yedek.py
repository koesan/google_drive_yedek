from __future__ import annotations

import io
import os
import sys
import zipfile
import tempfile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.table import Table
from rich.panel import Panel

# -----------------------------------------------------------
# Settings
# -----------------------------------------------------------
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "astute-citadel-453510-d7-7175b255da8d.json"
PARENT_FOLDER_ID = "1iTZTWWOuOnPxqfacRrs9awLFXOMsEtU-"

DEFAULT_DIRS = [
    "Belgeler",
    "İndirilenler",
    "Masaüstü",
    "Müzik",
    "Resimler",
    "Şablonlar",
    "Videolar",
]

console = Console()

# -----------------------------------------------------------
# Google Drive
# -----------------------------------------------------------
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build("drive", "v3", credentials=credentials, cache_discovery=False)

# -----------------------------------------------------------
# Helpers
# -----------------------------------------------------------

def _create_folder(name: str, parents: List[str] | None = None) -> str:
    body = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parents:
        body["parents"] = parents
    return (
        drive_service.files().create(body=body, fields="id").execute()["id"]
    )

def _list_children(folder_id: str) -> List[dict]:
    return (
        drive_service.files()
        .list(
            q=f"'{folder_id}' in parents and trashed=false",
            pageSize=1000,
            fields="files(id,name,mimeType,size)",
        )
        .execute()
        .get("files", [])
    )

# -----------------------------------------------------------
# Core functions
# -----------------------------------------------------------

def _gather_files(targets: List[Path]) -> List[Tuple[Path, str]]:
    """Return all files that will be uploaded together with their intended upload path."""
    uploads: List[Tuple[Path, str]] = []
    for base in targets:
        if not base.exists():
            console.print(f"[yellow]Atlandı:[/] {base} bulunamadı")
            continue
        for root, _, files in os.walk(base):
            for f in files:
                uploads.append((Path(root) / f, base.name))
    return uploads

def _human_bytes(num: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} PB"

def _compress_files(uploads: List[Tuple[Path, str]], ts: str) -> Path:
    """
    Dosyaları ZIP formatında sıkıştırır ve geçici dosyanın yolunu döndürür
    """
    # Geçici klasör oluştur
    temp_dir = Path(tempfile.mkdtemp())
    
    # Her dosyayı orijinal klasör yapısıyla geçici dizine kopyala
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        "{task.percentage:3.0f}%",
        TimeElapsedColumn(),
        console=console,
    ) as prog:
        copy_task = prog.add_task("Dosyalar kopyalanıyor", total=len(uploads))
        
        for src_file, base_name in uploads:
            # Hedef klasör yolu
            dest_folder = temp_dir / base_name / src_file.parent.relative_to(src_file.parts[0])
            dest_folder.mkdir(parents=True, exist_ok=True)
            
            # Dosyayı kopyala
            dest_file = dest_folder / src_file.name
            shutil.copy2(src_file, dest_file)
            
            prog.update(copy_task, advance=1)
    
    # ZIP dosya adı
    zip_filename = f"backup_{ts}.zip"
    zip_filepath = temp_dir / zip_filename
    
    # Dosyaları sıkıştır
    total_size = sum(f.stat().st_size for f, _ in uploads)
    
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        "{task.percentage:3.0f}%",
        TimeElapsedColumn(),
        console=console,
    ) as prog:
        zip_task = prog.add_task("Dosyalar sıkıştırılıyor", total=total_size)
        
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Geçici dizindeki her klasörü (temel klasörleri) ayrı ayrı ekle
            for folder in temp_dir.iterdir():
                if folder.is_dir() and folder.name in [base for _, base in uploads]:
                    folder_size = 0
                    for root, _, files in os.walk(folder):
                        for file in files:
                            file_path = Path(root) / file
                            folder_size += file_path.stat().st_size
                    
                    # Klasördeki dosyaları sıkıştır
                    for root, _, files in os.walk(folder):
                        for file in files:
                            file_path = Path(root) / file
                            # zipfile içindeki yolu, temp_dir'i çıkararak oluştur
                            arc_name = str(file_path.relative_to(temp_dir))
                            zipf.write(file_path, arc_name)
                            prog.update(zip_task, advance=file_path.stat().st_size)
    
    return zip_filepath

def backup(target: Path | None):
    targets = [target] if target else [Path.home() / d for d in DEFAULT_DIRS]

    # ------------------------------------------------------------------
    # 1️ Scan phase
    # ------------------------------------------------------------------
    console.print(Panel("[bold cyan]Dosyalar taranıyor...[/]", expand=False))
    uploads = _gather_files(targets)
    total_size = sum(f.stat().st_size for f, _ in uploads)
    console.print(
        f"[green]Bulunan dosya:[/] {len(uploads)} | [green]Toplam boyut:[/] {_human_bytes(total_size)}"
    )

    if not uploads:
        console.print("[red]Yedeklenecek dosya bulunamadı!")
        return

    # Timestamp oluştur
    ts = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d_%H-%M-%S")
    
    # ------------------------------------------------------------------
    # 2️ Compress phase
    # ------------------------------------------------------------------
    console.print(Panel("[bold cyan]Dosyalar sıkıştırılıyor...[/]", expand=False))
    zip_file = _compress_files(uploads, ts)
    
    console.print(f"[green]Sıkıştırılmış dosya:[/] {zip_file.name} | [green]Boyut:[/] {_human_bytes(zip_file.stat().st_size)}")
    
    # ------------------------------------------------------------------
    # 3️ Upload phase
    # ------------------------------------------------------------------
    console.print(Panel("[bold cyan]Yükleme başlıyor...[/]", expand=False))
    
    # Drive'da klasör oluştur
    backup_root_id = _create_folder(ts, [PARENT_FOLDER_ID])
    
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        "{task.percentage:3.0f}%",
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as prog:
        task = prog.add_task("ZIP dosyası yükleniyor", total=zip_file.stat().st_size)
        
        # ZIP dosyasını yükle
        meta = {"name": zip_file.name, "parents": [backup_root_id]}
        media = MediaFileUpload(str(zip_file), resumable=True)
        req = drive_service.files().create(body=meta, media_body=media)
        
        response = None
        while response is None:
            status, response = req.next_chunk()
            if status:
                prog.update(task, advance=status.resumable_progress)
                
        # Finalize any leftover
        prog.update(task, advance=media.size() - prog.tasks[0].completed)
    
    # Geçici dosyaları temizle
    try:
        shutil.rmtree(zip_file.parent)
        console.print("[cyan]Geçici dosyalar temizlendi[/]")
    except Exception as e:
        console.print(f"[yellow]Geçici dosyalar temizlenirken hata: {e}[/]")
    
    console.print("[bold green]✔ Yedekleme tamamlandı")

def list_backups() -> List[dict]:
    backups = sorted(_list_children(PARENT_FOLDER_ID), key=lambda x: x["name"], reverse=True)
    table = Table(title="Mevcut Yedekler")
    table.add_column("#", justify="right")
    table.add_column("ID")
    table.add_column("Ad")
    for i, item in enumerate(backups, 1):
        table.add_row(str(i), item["id"], item["name"])
    console.print(table)
    return backups

def _download_file(fid: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    request = drive_service.files().get_media(fileId=fid)
    with io.FileIO(dest, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                pass  # Could add progress here if desired

def _download_folder(fid: str, dest: Path):
    for item in _list_children(fid):
        if item["mimeType"].endswith("folder"):
            _download_folder(item["id"], dest / item["name"])
        else:
            _download_file(item["id"], dest / item["name"])

def download(backup_id: str):
    dest = Path("downloads") / backup_id
    console.print(f"[cyan]İndiriliyor →[/] {dest}")
    _download_folder(backup_id, dest)
    console.print("[bold green]✔ İndirme tamamlandı")

def delete(backup_id: str):
    drive_service.files().delete(fileId=backup_id).execute()
    console.print("[red]❌ Yedek silindi")

# -----------------------------------------------------------
# Menu loop
# -----------------------------------------------------------

def main():
    while True:
        console.print("\n[bold]Google Drive Yedek Aracı[/]")
        console.print("1) Yedekle\n2) Yedekleri Listele\n3) Yedek İndir\n4) Yedek Sil\nq) Çık")
        choice = Prompt.ask("Seçiminiz", choices=["1", "2", "3", "4", "q"], default="q")

        if choice == "1":
            path_str = Prompt.ask(
                "Yedeklenecek dizin (boş ⇒ varsayılan klasörler)", default=""
            )
            
            backup(Path(path_str).expanduser() if path_str else None)
        
        elif choice == "2":            
            list_backups()

        elif choice == "3":
            backups = list_backups()
            idx = Prompt.ask("İndirilecek # veya ID", default="")
            bid = backups[int(idx) - 1]["id"] if idx.isdigit() else idx
            download(bid)

        elif choice == "4":
            backups = list_backups()
            idx = Prompt.ask("Silinecek # veya ID", default="")
            bid = backups[int(idx) - 1]["id"] if idx.isdigit() else idx
            delete(bid)
        
        else:  # q
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[red]İptal edildi[/]")