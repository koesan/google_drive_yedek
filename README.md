<div align="center">

# Google Drive Backup Manager

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Google Drive API](https://img.shields.io/badge/Google%20Drive-API-green.svg)](https://developers.google.com/drive)
[![Rich](https://img.shields.io/badge/Rich-Terminal-orange.svg)](https://github.com/Textualize/rich)

☁️ **Professional-grade Google Drive backup and file management solution**

[🇬🇧 English](#english) | [🇹🇷 Türkçe](#türkçe)

</div>

---

## English

## 🇬🇧 

### About This Project

Google Drive Backup Manager is a comprehensive toolkit designed for seamless file and folder management on Google Drive. This professional solution transforms routine backup operations into quick, painless, and reliable processes. Built with enterprise-grade error handling and user-friendly interfaces, it's perfect for individuals and organizations requiring consistent data protection.

The application leverages Google's official Drive API to provide secure, authenticated access to your cloud storage. Whether you need to backup important documents, organize existing files, or maintain synchronized archives, this tool delivers reliable performance with intuitive operation.

### ✨ Core Features

**📤 Intelligent Upload System**
- Bulk file and folder uploading with progress tracking
- Automatic directory structure preservation
- Resume capability for interrupted transfers
- Smart duplicate detection and handling

**📥 Advanced Download Manager**
- Selective file and folder downloading
- Batch download operations with progress indicators
- Maintain original folder hierarchies during downloads
- Bandwidth optimization for large transfers

**📋 Comprehensive File Listing**
- Detailed file and folder inventory with metadata
- Sorting and filtering capabilities
- File size, creation date, and modification tracking
- Easy navigation through complex directory structures

**🗑️ Secure Deletion Operations**
- Safe file and folder removal with confirmation prompts
- Bulk deletion with preview capabilities
- Trash management and recovery options
- Protection against accidental data loss

### 🔧 Installation & Setup

#### Prerequisites
- **Python 3.8+** with pip package manager
- **Google Cloud Platform account** for API access
- **Google Drive account** for storage operations

#### Required Dependencies
```bash
pip install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib rich
```

#### Google Cloud Setup

**Step 1: Create a Google Cloud Project**
1. Navigate to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Enable billing for the project (required for API access)

**Step 2: Enable Google Drive API**
1. Go to **APIs & Services → Library**
2. Search for "Google Drive API"
3. Click **Enable** to activate the service

**Step 3: Create Service Account**
1. Navigate to **APIs & Services → Credentials**
2. Click **Create Credentials → Service Account**
3. Provide a descriptive name and click **Done**

**Step 4: Generate API Key**
1. On the service account row, click **Actions (⋮) → Manage keys**
2. Click **Add Key → Create new key → JSON**
3. Download and securely store the JSON key file

**Step 5: Setup Drive Folder**
1. Create a dedicated folder in [Google Drive](https://drive.google.com/)
2. Right-click the folder and select **Share**
3. Add the service account email (from the JSON file) as **Editor**
4. Copy the folder ID from the URL (the part after `/folders/`)

### 🚀 Usage Guide

#### Basic Operations Menu
When you run the application, you'll see an intuitive menu with these options:

**1. 📤 Backup Files**
Upload local folders to Google Drive with automatic organization by date and time.

**2. 📋 List Drive Contents**  
Display all files and folders in your backup directory with detailed information.

**3. 📥 Download Backups**
Retrieve specific backups or entire directories to your local machine.

**4. 🗑️ Delete Backups**
Remove unwanted files or folders with safety confirmations.

#### Command Examples

**Upload a Local Folder:**
The system will prompt you for:
- Local folder path to backup
- Target Drive folder ID
- JSON service account key file location

**Download from Drive:**
Select from available backups and specify:
- Source folder/file in Drive
- Local destination directory
- Download preferences (files only, folders only, or both)

**List Drive Contents:**
View detailed information including:
- File/folder names and types
- Creation and modification dates
- File sizes and storage usage
- Sharing permissions and access levels

### 💡 Advanced Tips

**Folder Organization:** The tool automatically creates timestamped subfolders for each backup, making it easy to track when backups were created.

**Batch Operations:** Take advantage of bulk operations to handle multiple files and folders efficiently.

**Recovery Planning:** Regular use of the list function helps you understand your backup structure and plan recovery strategies.

**Automation Ready:** The tool can be integrated into shell scripts or scheduled tasks for automated backup workflows.

---

## Türkçe

## 🇹🇷 

### Proje Hakkında

Google Drive Yedek Yöneticisi, Google Drive'da sorunsuz dosya ve klasör yönetimi için tasarlanmış kapsamlı bir araç setidir. Bu profesyonel çözüm, rutin yedekleme işlemlerini hızlı, acısız ve güvenilir süreçlere dönüştürür. Kurumsal seviye hata işleme ve kullanıcı dostu arayüzlerle oluşturulan bu araç, tutarlı veri koruması gerektiren bireyler ve organizasyonlar için mükemmeldir.

Uygulama, bulut depolama alanınıza güvenli, kimlik doğrulamalı erişim sağlamak için Google'ın resmi Drive API'sini kullanır. Önemli belgeleri yedeklemeniz, mevcut dosyaları düzenlemeniz veya senkronize arşivler korumanız gerekip gerekmediği fark etmez, bu araç sezgisel işlemle güvenilir performans sunar.

### ✨ Temel Özellikler

**📤 Akıllı Yükleme Sistemi**
- İlerleme takibi ile toplu dosya ve klasör yükleme
- Otomatik dizin yapısı korunması
- Kesintiye uğrayan aktarımlar için devam etme yeteneği
- Akıllı kopya algılama ve işleme

**📥 Gelişmiş İndirme Yöneticisi**
- Seçici dosya ve klasör indirme
- İlerleme göstergeleri ile toplu indirme işlemleri
- İndirmeler sırasında orijinal klasör hiyerarşilerini koruma
- Büyük aktarımlar için bant genişliği optimizasyonu

**📋 Kapsamlı Dosya Listeleme**
- Meta verilerle detaylı dosya ve klasör envanteri
- Sıralama ve filtreleme yetenekleri
- Dosya boyutu, oluşturma tarihi ve değişiklik takibi
- Karmaşık dizin yapılarında kolay gezinme

**🗑️ Güvenli Silme İşlemleri**
- Onay istekleri ile güvenli dosya ve klasör kaldırma
- Önizleme yetenekleri ile toplu silme
- Çöp kutusu yönetimi ve kurtarma seçenekleri
- Yanlışlıkla veri kaybına karşı koruma

### 🔧 Kurulum ve Ayarlar

#### Ön Gereksinimler
- **Python 3.8+** ve pip paket yöneticisi
- **Google Cloud Platform hesabı** API erişimi için
- **Google Drive hesabı** depolama işlemleri için

#### Gerekli Bağımlılıklar
```bash
pip install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib rich
```

#### Google Cloud Kurulumu

**Adım 1: Google Cloud Projesi Oluşturma**
1. [Google Cloud Console](https://console.cloud.google.com)'a gidin
2. Yeni bir proje oluşturun veya mevcut olanı seçin
3. Proje için faturalamayı etkinleştirin (API erişimi için gerekli)

**Adım 2: Google Drive API'yi Etkinleştirme**
1. **APIs & Services → Library**'ye gidin
2. "Google Drive API" aratın
3. Hizmeti etkinleştirmek için **Enable**'a tıklayın

**Adım 3: Servis Hesabı Oluşturma**
1. **APIs & Services → Credentials**'a gidin
2. **Create Credentials → Service Account**'a tıklayın
3. Açıklayıcı bir isim verin ve **Done**'a tıklayın

**Adım 4: API Anahtarı Üretme**
1. Servis hesabı satırında **Actions (⋮) → Manage keys**'e tıklayın
2. **Add Key → Create new key → JSON**'a tıklayın
3. JSON anahtar dosyasını indirin ve güvenli bir şekilde saklayın

**Adım 5: Drive Klasörü Kurulumu**
1. [Google Drive](https://drive.google.com/)'da özel bir klasör oluşturun
2. Klasöre sağ tıklayın ve **Share**'i seçin
3. Servis hesabı e-postasını (JSON dosyasından) **Editor** olarak ekleyin
4. URL'den klasör ID'sini kopyalayın (`/folders/` sonrası kısım)

### 🚀 Kullanım Kılavuzu

#### Temel İşlemler Menüsü
Uygulamayı çalıştırdığınızda, şu seçenekleri içeren sezgisel bir menü göreceksiniz:

**1. 📤 Dosyaları Yedekle**
Yerel klasörleri tarih ve saat ile otomatik organizasyonla Google Drive'a yükleyin.

**2. 📋 Drive İçeriğini Listele**
Yedek dizininizdeki tüm dosya ve klasörleri detaylı bilgilerle görüntüleyin.

**3. 📥 Yedekleri İndir**
Belirli yedekleri veya tüm dizinleri yerel makinenize alın.

**4. 🗑️ Yedekleri Sil**
Güvenlik onaylarıyla istenmeyen dosya veya klasörleri kaldırın.

#### Komut Örnekleri

**Yerel Klasör Yükleme:**
Sistem sizden şunları isteyecek:
- Yedeklenecek yerel klasör yolu
- Hedef Drive klasör ID'si
- JSON servis hesabı anahtar dosya konumu

**Drive'dan İndirme:**
Mevcut yedekler arasından seçim yapın ve belirtin:
- Drive'daki kaynak klasör/dosya
- Yerel hedef dizini
- İndirme tercihleri (sadece dosyalar, sadece klasörler veya her ikisi)

**Drive İçeriğini Listeleme:**
Şunları içeren detaylı bilgileri görüntüleyin:
- Dosya/klasör adları ve türleri
- Oluşturma ve değişiklik tarihleri
- Dosya boyutları ve depolama kullanımı
- Paylaşım izinleri ve erişim seviyeleri

### 💡 Gelişmiş İpuçları

**Klasör Organizasyonu:** Araç her yedekleme için otomatik olarak zaman damgalı alt klasörler oluşturur, yedeklemelerin ne zaman oluşturulduğunu takip etmeyi kolaylaştırır.

**Toplu İşlemler:** Birden fazla dosya ve klasörü verimli bir şekilde işlemek için toplu işlemlerden faydalanın.

**Kurtarma Planlaması:** Liste fonksiyonunun düzenli kullanımı, yedek yapınızı anlamanıza ve kurtarma stratejileri planlamanıza yardımcı olur.

**Otomasyon Için Hazır:** Araç, otomatik yedekleme iş akışları için shell scriptlerine veya zamanlanmış görevlere entegre edilebilir.

---

### 📄 License

This project is open source and available under the MIT License.
