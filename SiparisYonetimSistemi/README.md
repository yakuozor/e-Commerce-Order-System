# Sipariş Yönetim Sistemi

Bu proje, bir e-ticaret platformu için sipariş, ürün, müşteri ve kargo süreçlerini yöneten nesne yönelimli bir yazılım sistemidir.

## Proje Özellikleri

- **Ürün Yönetimi:** Yeni ürün ekleme, listeleme ve stok bilgisi tutma, filtreleme
- **Müşteri İşlemleri:** Müşteri kaydı ve profil oluşturma, sipariş geçmişi görüntüleme
- **Sipariş Sistemi:** Sepete ürün ekleme, sipariş oluşturma, sipariş durumu güncelleme
- **Kargo Stratejileri:** Farklı kargo stratejileri (hızlı, ekonomik, drone) ve otomatik seçim
- **Bildirim Mekanizması:** Sipariş durum değişikliklerinde bildirim gönderme
- **Stok Takibi:** Siparişle birlikte stok güncelleme, stok kontrolü

## Kullanılan Tasarım Desenleri

1. **Strategy Pattern:** Farklı kargo yöntemlerinin (Hızlı, Ekonomik, Drone) dinamik seçimi 
2. **Observer Pattern:** Sipariş durumu değiştiğinde müşterilere bildirim gönderilmesi
3. **Factory Method Pattern:** Sipariş oluşturma ve kargo stratejisi belirleme
4. **Singleton Pattern:** Stok yönetiminin merkezi kontrolü

## Proje Yapısı

- **models/** - Veri modelleri
  - product.py - Ürün ve kategori sınıfları
  - customer.py - Müşteri sınıfı
  - order.py - Sipariş ve sipariş durumu sınıfları
  - shipping.py - Kargo stratejileri
- **services/** - İş mantığı servisleri
  - inventory_manager.py - Stok yönetimi (Singleton)
  - notification_service.py - Bildirim sistemi (Observer)
  - order_factory.py - Sipariş oluşturma (Factory Method)
- **ui/** - Kullanıcı arayüzü
  - terminal_ui.py - Terminal kullanıcı arayüzü
- **main.py** - Ana program

## Kurulum ve Çalıştırma

1. Python 3.6 veya üzeri gereklidir.
2. Ek paket kurulumu gerekmez, sadece Python standart kütüphanesi kullanılmıştır.
3. Terminalde şu komutu çalıştırın:

```bash
python main.py
```

## Kullanım

Program başlatıldığında terminalde bir menü gösterilir. Aşağıdaki işlemler yapılabilir:

1. Ürünlere göz atma ve sepete ekleme
2. Sepeti görüntüleme ve düzenleme
3. Sipariş oluşturma ve kargo seçimi
4. Sipariş geçmişini görüntüleme
5. Sipariş durumlarını takip etme

## Ekran Görüntüleri

(Demo sırasında eklenecek)

## Yapımcılar

Bu proje yazılım tasarımı dersi ödevidir.