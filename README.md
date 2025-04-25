# Automaticli Drive Backup (Otomatik Drive Yedeklemesi)

This project provides a set of handy functions for managing files and folders on Google Drive. With it, you can list, delete, upload, and download items making routine backups to Drive quick and painless. It’s especially useful for anyone who needs a simple way to keep their data organized and safely stored in the cloud.

---

Bu proje, Google Drive'da dosya ve klasör yönetimini kolaylaştırmak için çeşitli işlevler sunar. Bu araçla dosya ve klasörleri listeleyebilir, silebilir, yükleyebilir ve indirebilirsiniz. Özellikle Google Drive üzerinde düzenli yedekleme yapmayı amaçlayanlar için oldukça kullanışlıdır.

# Requirements(Gereksinimler)

1. **Installing the Python libraries (Python kütüphanelerinin kurulması).**
   
   ```bash
   pip install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib rich
   ```

2. **Create a service account and key file (.json) in Google Cloud ( Google Cloud’ta servis hesabı ve anahtar dosyası (.json) )**
   
   - ****Create a new project or open an existing one**  
     [https://console.cloud.google.com](https://console.cloud.google.com)
   
   - In the left‑hand menu go to **APIs & Services ▸ Library**, search for **Google Drive API**, and click **Enable**.
   
   - Still in **APIs & Services**, open **Credentials** and choose **Create credentials ▸ Service account**. Give it a name and click **Done**.
   
   - On the row of the new service account, click **︙ Actions ▸ Manage keys ▸ Add key ▸ Create new key ▸ JSON**.
   
   - Copy the service account’s e‑mail address (it looks like 
     *my‑sa@my‑project.iam.gserviceaccount.com*).
     
     ---
   
   - **Proje oluşturun / mevcut projeyi açın**  
     [https://console.cloud.google.com](%5Bhttps://console.cloud.google.com%5D(https://console.cloud.google.com))
   
   - **Sol menü** - ▸ **APIs & Services - ▸ Library** - ▸ “**Google Drive API**”yi bulun, **Enable** butonuna basın.
   
   - **Sol menü** - ▸ **APIs & Services - ▸ Credentials** - ▸ **Create Credentials - ▸ Service account** - ▸ İsim verin, “**Done**”la bitirin.
   
   - Oluşan servis hesabının satırında “**︙ Actions**” - ▸ **Manage keys** - ▸ **Add key - ▸ Create new key - ▸ JSON**, indirdiğiniz dosyayı güvenli bir yerde tutun.
   
   - Servis hesabının e‑postasını kopyalayın (şu biçimde olur: *my‑sa@my‑project.iam.gserviceaccount.com*).
     
     

3. **Prepare the target (parent) folder in Drive (Drive’da hedef (parent) klasörü hazırlayın)**
   
   - [In [Google Drive](https://drive.google.com/) create the folder that will hold your backups.
   
   - Right‑click the folder and choose **Share**. Leave “General access” set to **Restricted**.
   
   - In **Add people and groups**, paste the **service account e‑mail**, give it **Editor** access, and click **Send**.
   
   - Open the folder and look at the URL, which has this form:
     
     ```
     https://drive.google.com/drive/folders/1AbC‑DeFGhijkLmNop-
     ```
     
     The final segment (“**1AbC‑DeFGhijkLmNop-**”) is the **folder ID** you’ll supply to the program.
     
     ---
   
   - [Google Drive’da](https://drive.google.com/) yedeklerin gideceği klasörü oluşturun.
   
   - Klasöre sağ tıklayıp **Paylaş** (Share) - ▸ “Genel erişim: Kısıtlı” kalsın.
   
   - **Kişi ekle** bölümüne **servis hesabı e‑postanızı** yapıştırın. ***Düzenleyici*** yetkisi verip **Gönder** deyin.
   
   - Klasörü açın, adres çubuğundaki URL şu biçimde:
     
     ```
     https://drive.google.com/drive/folders/1AbC‑DeFGhijkLmNop-
     ```
     
     Son kısım (“**1AbC‑DeFGhijkLmNop-**”) klasör ID’sidir. Programı kullanırken bu **ID'yi** girmeniz gerekecek.
     
     

**In short**, before you can run the program you need to install the required packages with **pip** and have both the **JSON key file** and the **folder ID** ready.



**Sonuç olarak** programı kullanmak için öncelikle **Pip** ile gerekli paketleri kurmanız ve elinizde **json** ve **klasör ID** bulunması gerekiyor.

---

# Usage / Kullanım

#### 1) **Backup / Yedekle**

Uploads a local folder to Google Drive. The script creates a new sub‑folder named with the current date & time, then copies everything inside.

---

Yerel bir klasörü Google Drive’a yükler. Betik, o anki tarih‑saat adında yeni bir alt klasör açar ve tüm dosyaları buraya kopyalar.

#### 2) **List Backups / Yedekleri Listele**

Shows every file and folder inside the parent backup directory on Drive, so you can see what’s already stored.

---

Drive’daki ana yedek klasörünün içindeki dosya ve klasörleri gösterir; hangi yedeklerin mevcut olduğunu görürsünüz.

#### 3) **Download Backup / Yedek İndir**

Pulls a backup (or the whole backup directory) from Drive down to your computer, preserving the original folder structure.

---

Seçtiğiniz yedeği (ya da tüm klasörü) Drive’dan bilgisayarınıza indirir, klasör yapısını bozmadan kopyalar.

#### 4) **Delete Backup / Yedek Sil**

Lets you pick individual files/folders or everything at once and remove them from Drive.

---

Tek tek dosya/klasör seçerek ya da hepsini birden Drive’dan silmenizi sağlar.
