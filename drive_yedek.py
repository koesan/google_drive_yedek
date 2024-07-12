import os
import io
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from tqdm import tqdm  # İlerleme çubuğu için tqdm kütüphanesi eklendi

# Google Drive API kapsamlarını ve servis hesap dosyasının yolunu tanımlayın
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "/home/koesan/İndirilenler/tough-diagram-429202-r2-cf3eacdab3e1.json"
parent_folder_id = "189LN6JXG9DssV9iefs-Pza4inXNLJDS8"

# Servis hesap dosyasını kullanarak kimlik bilgilerini oluşturun
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Drive servisini oluşturun
drive_service = build('drive', 'v3', credentials=credentials)

def delete_files_in_folder(folder_id):
    """Belirtilen klasördeki dosyaları ve klasörleri listeleyip kullanıcı seçimlerine göre silme işlemi yapar."""
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    items = results.get('files', [])

    if not items:
        print("Klasörde dosya veya klasör bulunamadı.")
        return

    # Tüm dosya ve klasörleri listele
    print("Klasördeki dosyalar ve klasörler:")
    for idx, item in enumerate(items, start=1):
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            print(f"{idx}. [Klasör] {item['name']} (ID: {item['id']})")
        else:
            print(f"{idx}. [Dosya] {item['name']} (ID: {item['id']})")

    print(f"{len(items) + 1}. Hepsini Sil")
    choice = int(input("Silmek istediğiniz dosya veya klasör numarasını seçin: "))

    if choice == len(items) + 1:
        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                delete_folder_contents(item['id'])
            try:
                drive_service.files().delete(fileId=item['id']).execute()
                print(f"Başarıyla silindi: ID: {item['id']}, İsim: {item['name']}")
            except Exception as e:
                print(f"Silme hatası: ID: {item['id']}, İsim: {item['name']}")
                print(f"Hata detayları: {str(e)}")
    elif 1 <= choice <= len(items):
        item_to_delete = items[choice - 1]
        if item_to_delete['mimeType'] == 'application/vnd.google-apps.folder':
            delete_folder_contents(item_to_delete['id'])
        try:
            drive_service.files().delete(fileId=item_to_delete['id']).execute()
            print(f"Başarıyla silindi: ID: {item_to_delete['id']}, İsim: {item_to_delete['name']}")
        except Exception as e:
            print(f"Silme hatası: ID: {item_to_delete['id']}, İsim: {item_to_delete['name']}")
            print(f"Hata detayları: {str(e)}")
    else:
        print("Geçersiz seçim. Hiçbir dosya veya klasör silinmedi.")

def list_files_in_folder(folder_id):
    """Belirtilen klasördeki dosyaları ve doğrudan alt klasörleri listeleyen fonksiyon."""
    # Klasördeki dosya ve klasörleri listele
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    items = results.get('files', [])

    if not items:
        print("Klasörde dosya veya klasör bulunamadı.")
        return

    print("Klasördeki dosyalar ve klasörler:")
    for idx, item in enumerate(items, start=1):
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            print(f"{idx}. [Klasör] {item['name']} (ID: {item['id']})")
        else:
            print(f"{idx}. [Dosya] {item['name']} (ID: {item['id']})")

def delete_folder_contents(folder_id):
    """Belirtilen klasördeki tüm dosyaları ve alt klasörleri recursively (özyinelemeli olarak) siler."""
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    items = results.get('files', [])

    with tqdm(total=len(items), desc="Alt klasörler ve dosyalar siliniyor", unit="öğe") as pbar:
        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                delete_folder_contents(item['id'])
            try:
                drive_service.files().delete(fileId=item['id']).execute()
                pbar.update(1)
            except Exception as e:
                pass  # Hatalar basılmıyor, yalnızca ilerleme çubuğu güncelleniyor

def create_folder(folder_name, parent_folder_id=None):
    """Google Drive'da bir klasör oluşturur ve oluşturulan klasörün ID'sini döner."""
    folder_metadata = {
        'name': folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        'parents': [parent_folder_id] if parent_folder_id else []
    }

    created_folder = drive_service.files().create(
        body=folder_metadata,
        fields='id'
    ).execute()

    print(f'Klasör oluşturuldu: ID: {created_folder["id"]}')
    return created_folder["id"]

def upload_directory(local_directory, parent_folder_id):
    """Bir yerel dizini ve içeriğini Google Drive'a yükler."""
    # Güncel tarih ve saati al
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Güncel tarih ve saati kullanarak bir klasör oluştur
    date_folder_id = create_folder(current_datetime, parent_folder_id)
    
    files_to_upload = []
    for root, dirs, files in os.walk(local_directory):
        # Google Drive'da karşılık gelen klasörü oluştur
        relative_path = os.path.relpath(root, local_directory)
        drive_folder_id = date_folder_id

        if relative_path != ".":
            # Google Drive'da bir alt klasör oluştur
            drive_folder_id = create_folder(relative_path, date_folder_id)

        # Mevcut dizindeki dosyaları toplama
        for file_name in files:
            files_to_upload.append((os.path.join(root, file_name), drive_folder_id, file_name))

    # Yükleme ilerleme çubuğunu başlat
    with tqdm(total=len(files_to_upload), desc="Dosyalar yükleniyor", unit="dosya") as pbar:
        for file_path, folder_id, file_name in files_to_upload:
            file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }
            media = MediaFileUpload(file_path)
            try:
                drive_service.files().create(body=file_metadata, media_body=media).execute()
                pbar.update(1)
            except Exception as e:
                print(f"Yükleme hatası: {file_name}")
                print(f"Hata detayları: {str(e)}")

def download_files_from_folder(folder_id, local_folder_path):
    """Belirtilen Google Drive klasöründeki dosyaları ve alt klasörleri yerel bir klasöre indirir."""
    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)

    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    items = results.get('files', [])

    if not items:
        print("Klasörde dosya veya klasör bulunamadı.")
        return

    with tqdm(total=len(items), desc="Dosyalar ve alt klasörler indiriliyor", unit="öğe") as pbar:
        for item in items:
            file_id = item['id']
            file_name = item['name']
            file_path = os.path.join(local_folder_path, file_name)

            if item['mimeType'] == 'application/vnd.google-apps.folder':
                # Alt klasörü indir
                download_files_from_folder(file_id, file_path)
            else:
                # Dosyayı indir
                request = drive_service.files().get_media(fileId=file_id)
                with io.FileIO(file_path, 'wb') as fh:
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                pbar.update(1)

def select_and_download_item(folder_id, local_folder_path):
    """Belirtilen Google Drive klasöründeki dosya ve klasörleri listeleyip, kullanıcıdan seçim yaparak indirir."""
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    items = results.get('files', [])

    if not items:
        print("Klasörde dosya veya klasör bulunamadı.")
        return

    # Klasör ve dosyaları listele
    print("Klasördeki dosyalar ve klasörler:")
    for idx, item in enumerate(items, start=1):
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            print(f"{idx}. [Klasör] {item['name']} (ID: {item['id']})")
        else:
            print(f"{idx}. [Dosya] {item['name']} (ID: {item['id']})")

    print(f"{len(items) + 1}. Hepsini İndir")
    choice = int(input("İndirmek istediğiniz dosya veya klasör numarasını seçin: "))

    if choice == len(items) + 1:
        # Tüm dosya ve klasörleri indir
        download_files_from_folder(folder_id, local_folder_path)
    elif 1 <= choice <= len(items):
        item_to_download = items[choice - 1]
        item_id = item_to_download['id']
        item_name = item_to_download['name']
        item_path = os.path.join(local_folder_path, item_name)

        if item_to_download['mimeType'] == 'application/vnd.google-apps.folder':
            # Seçilen klasörü indir
            download_files_from_folder(item_id, item_path)
        else:
            # Seçilen dosyayı indir
            request = drive_service.files().get_media(fileId=item_id)
            with io.FileIO(item_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
            print(f"Dosya indirildi: {item_name}")

    else:
        print("Geçersiz seçim. Hiçbir dosya veya klasör indirilmedi.")

if __name__ == '__main__':

    print("1.Yedekleri Listele")
    print("2.Yedek Sil")
    print("3.Yedek Al")
    print("4.Yedeği İndir")
    print("5.Dosya veya Klasör Seçip İndir")
    choice = input("Yapılacak İşlem:")

    if choice=="1":
        list_files_in_folder(parent_folder_id)
    elif choice =="2":
        delete_files_in_folder(parent_folder_id)
    elif choice =="3":
        upload_directory("/home/koesan/Müzik", parent_folder_id)
    elif choice == "4":
        select_and_download_item(parent_folder_id,"/home/koesan/İndirilenler")
    else:
        print("Geçersiz seçim.")
