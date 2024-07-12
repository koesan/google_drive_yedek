# google_drive_yedek

Bu proje, Google Drive'da dosya ve klasör yönetimini kolaylaştırmak için çeşitli işlevler sunar. Bu araçla dosya ve klasörleri listeleyebilir, silebilir, yükleyebilir ve indirebilirsiniz. Özellikle Google Drive üzerinde düzenli yedekleme yapmayı amaçlayanlar için oldukça kullanışlıdır.

* Gereksinimler

` pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client tqdm `


* Kullanım

Bu kod, Google Drive üzerinde çeşitli dosya yönetim işlemleri yapmanıza olanak tanır:

Yedekleri Listele
Klasördeki dosyaları ve klasörleri listeler.
Yedek Sil
Klasördeki dosya ve klasörleri kullanıcı seçimlerine göre siler.
Yedek Al
Yerel bir dizini Google Drive'a yükler ve mevcut tarih ve saati kullanarak bir klasör oluşturur.
Yedeği İndir
Belirtilen klasördeki dosyaları ve alt klasörleri yerel bir klasöre indirir.
Dosya veya Klasör Seçip İndir
Klasördeki dosya ve klasörleri listeler ve kullanıcıdan seçim yaparak indirir.
Kod Açıklaması
delete_files_in_folder(folder_id): Belirtilen klasördeki dosya ve klasörleri listeler ve kullanıcı seçimlerine göre silme işlemi yapar.
list_files_in_folder(folder_id): Belirtilen klasördeki dosya ve doğrudan alt klasörleri listeler.
delete_folder_contents(folder_id): Belirtilen klasördeki tüm dosyaları ve alt klasörleri özyinelemeli olarak siler.
create_folder(folder_name, parent_folder_id=None): Google Drive'da bir klasör oluşturur ve oluşturulan klasörün ID'sini döner.
upload_directory(local_directory, parent_folder_id): Bir yerel dizini ve içeriğini Google Drive'a yükler.
download_files_from_folder(folder_id, local_folder_path): Belirtilen Google Drive klasöründeki dosyaları ve alt klasörleri yerel bir klasöre indirir.
select_and_download_item(folder_id, local_folder_path): Belirtilen Google Drive klasöründeki dosya ve klasörleri listeleyip, kullanıcıdan seçim yaparak indirir.
Kodu Çalıştırma
Ana Python dosyasını çalıştırmadan önce aşağıdaki adımları tamamlayın:

Gerekli değişkenleri doldurun:

SERVICE_ACCOUNT_FILE: Servis hesap dosyasının yolu
parent_folder_id: Üst klasör ID'si
Path: Yedeklemek istediğiniz yerel klasör yolu
