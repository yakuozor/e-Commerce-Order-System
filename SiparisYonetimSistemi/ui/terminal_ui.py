#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Terminal kullanıcı arayüzü sınıfı
"""

import os
import getpass
from models.product import ProductCategory
from models.customer import Customer
from models.order import OrderStatus
from models.shipping import FastShipping, EconomicShipping, DroneShipping

class TerminalUI:
    """
    Terminal tabanlı kullanıcı arayüzü.
    Kullanıcı ile etkileşim için basit bir CLI sağlar.
    """
    
    def __init__(self, inventory_manager, order_factory, notification_service):
        """
        Terminal arayüzü oluşturur.
        
        Args:
            inventory_manager: Stok yöneticisi
            order_factory: Sipariş fabrikası
            notification_service: Bildirim servisi
        """
        self.__inventory_manager = inventory_manager
        self.__order_factory = order_factory
        self.__notification_service = notification_service
        self.__current_customer = None
        self.__shopping_cart = []  # (ürün, miktar) çiftleri
        self.__registered_customers = {}  # email -> customer eşleşmesi
    
    def clear_screen(self):
        """Terminali temizler"""
        import os

        def safe_clear():
            try:
                os.system("clear")  # Linux/macOS
            except:
                pass

    def display_header(self, title):
        """
        Başlık gösterir.
        
        Args:
            title: Gösterilecek başlık
        """
        self.clear_screen()
        print("\n" + "=" * 60)
        print(f"{title}".center(60))
        print("=" * 60 + "\n")
    
    def display_menu(self, options):
        """
        Menü seçeneklerini gösterir.
        
        Args:
            options: Seçenek listesi
            
        Returns:
            int: Seçilen seçeneğin indeksi
        """
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        print("\n0. Geri")
        
        while True:
            try:
                choice = int(input("\nSeçiminiz: "))
                if 0 <= choice <= len(options):
                    return choice
                print("Geçersiz seçim. Lütfen tekrar deneyin.")
            except ValueError:
                print("Lütfen bir sayı girin.")
    
    def prompt(self, message):
        """
        Kullanıcıdan giriş ister.
        
        Args:
            message: Giriş mesajı
            
        Returns:
            str: Kullanıcının girişi
        """
        return input(f"{message}: ")
        
    def prompt_password(self, message):
        """
        Kullanıcıdan şifre ister (göstermeden).
        
        Args:
            message: Giriş mesajı
            
        Returns:
            str: Kullanıcının girdiği şifre
        """


        return input(message + ": ")  # Şifre görünür ama çalışır

    def wait_for_enter(self):
        """Kullanıcının Enter tuşuna basmasını bekler"""
        input("\nDevam etmek için Enter tuşuna basın...")
    
    def register_customer(self):
        """
        Yeni müşteri kaydı oluşturur.
        
        Returns:
            Customer: Oluşturulan müşteri nesnesi
        """
        self.display_header("MÜŞTERİ KAYDI")
        
        customer_id = f"C{str(id(self))[-4:]}"  # Benzersiz ID oluştur
        name = self.prompt("Adınız ve soyadınız")
        
        while True:
            email = self.prompt("E-posta adresiniz")
            if "@" not in email:
                print("Geçersiz e-posta adresi. Lütfen tekrar deneyin.")
                continue
                
            # E-posta zaten kayıtlı mı kontrol et
            if email in self.__registered_customers:
                print("Bu e-posta adresi zaten kayıtlı. Lütfen giriş yapın veya farklı bir e-posta kullanın.")
                return None
            break
        
        # Şifre ekleniyor
        password = self.prompt_password("Şifreniz")
        confirm_password = self.prompt_password("Şifrenizi tekrar girin")
        
        if password != confirm_password:
            print("Şifreler eşleşmiyor. Lütfen tekrar deneyin.")
            self.wait_for_enter()
            return None
        
        address = self.prompt("Teslimat adresiniz")
        phone = self.prompt("Telefon numaranız (isteğe bağlı)")
        
        if not phone.strip():
            phone = None
        
        customer = Customer(customer_id, name, email, address, phone)
        # Şifreyi burada bir sözlükte saklamak basit bir çözüm
        # Gerçek bir uygulamada şifreler hashlenerek saklanmalıdır
        self.__registered_customers[email] = {"customer": customer, "password": password}
        
        print(f"\nHoş Geldiniz, {name}! Müşteri kaydınız oluşturuldu.")
        
        self.wait_for_enter()
        return customer
    
    def login_customer(self):
        """
        Müşteri girişi sağlar.
        
        Returns:
            Customer: Giriş yapan müşteri nesnesi veya None
        """
        self.display_header("MÜŞTERİ GİRİŞİ")
        
        email = self.prompt("E-posta adresiniz")
        password = self.prompt_password("Şifreniz")
        
        # Kullanıcı kayıtlı mı ve şifre doğru mu kontrol et
        if email in self.__registered_customers and self.__registered_customers[email]["password"] == password:
            customer = self.__registered_customers[email]["customer"]
            print(f"\nHoş Geldiniz, {customer.name}!")
            self.wait_for_enter()
            return customer
        else:
            print("\nHatalı e-posta veya şifre. Lütfen tekrar deneyin.")
            self.wait_for_enter()
            return None
    
    def logout_customer(self):
        """
        Mevcut müşteri oturumunu kapatır.
        """
        if self.__current_customer:
            name = self.__current_customer.name
            self.__current_customer = None
            self.__shopping_cart = []  # Sepeti temizle
            print(f"\n{name}, oturumunuz başarıyla kapatıldı.")
            self.wait_for_enter()
    
    def display_product_list(self, products, show_details=False):
        """
        Ürün listesini gösterir.
        
        Args:
            products: Gösterilecek ürünler listesi
            show_details: Detayları gösterme seçeneği
        """
        if not products:
            print("Gösterilecek ürün bulunamadı.")
            return
        
        for i, product in enumerate(products, 1):
            if show_details:
                print(f"{i}. {product}")
            else:
                print(f"{i}. {product.name} - {product.price} TL")
    
    def display_categories(self):
        """
        Ürün kategorilerini gösterir ve seçilen kategoriyi döndürür.
        
        Returns:
            ProductCategory or None: Seçilen kategori veya None
        """
        self.display_header("KATEGORİLER")
        
        categories = list(ProductCategory)
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.value}")
        
        print("\n0. Tümünü Göster")
        
        while True:
            try:
                choice = int(input("\nKategori seçin: "))
                if choice == 0:
                    return None
                elif 1 <= choice <= len(categories):
                    return categories[choice - 1]
                print("Geçersiz seçim. Lütfen tekrar deneyin.")
            except ValueError:
                print("Lütfen bir sayı girin.")
    
    def browse_products(self):
        """
        Ürünleri listeler ve kullanıcının ürün seçmesini sağlar.
        
        Returns:
            tuple(Product, int) or None: Seçilen ürün ve miktar veya None
        """
        # Kategori seçimi
        category = self.display_categories()
        
        # Ürünleri al
        if category:
            products = self.__inventory_manager.get_products_by_category(category)
            title = f"KATEGORİ: {category.value}"
        else:
            products = self.__inventory_manager.get_all_products()
            title = "TÜM ÜRÜNLER"
        
        # Ürünleri göster
        self.display_header(title)
        self.display_product_list(products, show_details=True)
        
        if not products:
            self.wait_for_enter()
            return None
        
        print("\n0. Geri")
        
        # Ürün seçimi
        while True:
            try:
                choice = int(input("\nÜrün seçin (0: Geri): "))
                if choice == 0:
                    return None
                elif 1 <= choice <= len(products):
                    selected_product = products[choice - 1]
                    
                    # Stok kontrolü
                    if selected_product.stock_quantity <= 0:
                        print("Bu ürün stokta kalmadı.")
                        self.wait_for_enter()
                        return None
                    
                    # Miktar seçimi
                    while True:
                        try:
                            quantity = int(input(f"Miktar (max {selected_product.stock_quantity}): "))
                            if 1 <= quantity <= selected_product.stock_quantity:
                                return (selected_product, quantity)
                            else:
                                print("Geçersiz miktar. Lütfen tekrar deneyin.")
                        except ValueError:
                            print("Lütfen bir sayı girin.")
                    
                print("Geçersiz seçim. Lütfen tekrar deneyin.")
            except ValueError:
                print("Lütfen bir sayı girin.")
    
    def view_cart(self):
        """
        Sepeti görüntüler ve yönetir.
        
        Returns:
            bool: Değişiklik yapıldıysa True, değilse False
        """
        while True:
            self.display_header("SEPETİNİZ")
            
            if not self.__shopping_cart:
                print("Sepetiniz boş.")
                self.wait_for_enter()
                return False
            
            # Sepet içeriğini göster
            total = 0
            for i, (product, quantity) in enumerate(self.__shopping_cart, 1):
                subtotal = product.price * quantity
                total += subtotal
                print(f"{i}. {product.name} - {quantity} adet x {product.price} TL = {subtotal} TL")
            
            print(f"\nToplam: {total} TL")
            
            # Seçenekleri göster
            options = ["Alışverişi tamamla", "Ürün çıkar", "Sepeti boşalt"]
            choice = self.display_menu(options)
            
            if choice == 0:
                return False
            elif choice == 1:  # Alışverişi tamamla
                return True
            elif choice == 2:  # Ürün çıkar
                self.remove_from_cart()
            elif choice == 3:  # Sepeti boşalt
                self.__shopping_cart = []
                print("Sepet boşaltıldı.")
                self.wait_for_enter()
    
    def remove_from_cart(self):
        """Sepetten ürün çıkarır"""
        self.display_header("SEPETTEN ÜRÜN ÇIKAR")
        
        for i, (product, quantity) in enumerate(self.__shopping_cart, 1):
            print(f"{i}. {product.name} - {quantity} adet")
        
        print("\n0. Geri")
        
        while True:
            try:
                choice = int(input("\nÇıkarılacak ürünü seçin: "))
                if choice == 0:
                    return
                elif 1 <= choice <= len(self.__shopping_cart):
                    self.__shopping_cart.pop(choice - 1)
                    print("Ürün sepetten çıkarıldı.")
                    self.wait_for_enter()
                    return
                print("Geçersiz seçim. Lütfen tekrar deneyin.")
            except ValueError:
                print("Lütfen bir sayı girin.")
    
    def select_shipping_method(self):
        """
        Kargo yöntemi seçimi.
        
        Returns:
            ShippingMethod or None: Seçilen kargo yöntemi veya None (otomatik)
        """
        self.display_header("KARGO YÖNTEMİ SEÇİMİ")
        
        options = [
            "Otomatik seçim (en uygun kargo)",
            "Hızlı Kargo (1-2 gün)",
            "Ekonomik Kargo (3-5 gün)",
            "Drone ile Teslimat (aynı gün)"
        ]
        
        choice = self.display_menu(options)
        
        if choice == 0 or choice == 1:
            return None  # Otomatik seçim
        elif choice == 2:
            return FastShipping()
        elif choice == 3:
            return EconomicShipping()
        elif choice == 4:
            return DroneShipping()
    
    def complete_order(self):
        """
        Siparişi tamamlar.
        
        Returns:
            bool: Sipariş başarılıysa True, değilse False
        """
        self.display_header("SİPARİŞİ TAMAMLA")
        
        if not self.__shopping_cart:
            print("Sepetiniz boş. Sipariş oluşturulamadı.")
            self.wait_for_enter()
            return False
        
        # Müşteri kontrolü
        if not self.__current_customer:
            print("Sipariş vermeden önce giriş yapmanız gerekmektedir.")
            self.display_login_register_menu()
            if not self.__current_customer:
                print("\nGiriş yapmadan sipariş veremezsiniz.")
                self.wait_for_enter()
                return False
        
        # Sipariş notları
        notes = self.prompt("Sipariş notu (isteğe bağlı)")
        if not notes.strip():
            notes = None
        
        # Kargo yöntemi seçimi
        shipping_method = self.select_shipping_method()
        
        # Siparişi oluştur
        products_with_quantities = self.__shopping_cart.copy()
        order = self.__order_factory.create_order(
            self.__current_customer,
            products_with_quantities,
            select_shipping=(shipping_method is None),
            shipping_method=shipping_method,
            notes=notes
        )
        
        if order:
            print("\nSiparişiniz başarıyla oluşturuldu!")
            print(f"Sipariş No: {order.order_id}")
            print(f"Toplam Tutar: {order.get_total()} TL")
            print(f"Durum: {order.status.value}")
            
            if order.shipping_method:
                print(f"Kargo: {order.shipping_method}")
                
            self.__shopping_cart = []  # Sepeti temizle
            self.wait_for_enter()
            return True
        else:
            print("\nSipariş oluşturulurken bir hata oluştu.")
            print("Bir veya daha fazla ürün stokta bulunmuyor olabilir.")
            self.wait_for_enter()
            return False
    
    def view_orders(self):
        """Müşterinin sipariş geçmişini gösterir"""
        if not self.__current_customer:
            print("Sipariş geçmişini görüntülemek için giriş yapmanız gerekmektedir.")
            self.display_login_register_menu()
            if not self.__current_customer:
                return
        
        while True:
            self.display_header("SİPARİŞ GEÇMİŞİ")
            
            orders = self.__current_customer.order_history
            if not orders:
                print("Henüz bir sipariş vermediniz.")
                self.wait_for_enter()
                return
            
            # Siparişleri göster
            for i, order in enumerate(orders, 1):
                print(f"{i}. {order}")
            
            print("\n0. Geri")
            
            # Sipariş seçimi
            while True:
                try:
                    choice = int(input("\nSipariş detayları için sipariş seçin: "))
                    if choice == 0:
                        return
                    elif 1 <= choice <= len(orders):
                        self.display_order_details(orders[choice - 1])
                        break
                    print("Geçersiz seçim. Lütfen tekrar deneyin.")
                except ValueError:
                    print("Lütfen bir sayı girin.")
    
    def display_order_details(self, order):
        """
        Sipariş detaylarını gösterir.
        
        Args:
            order: Gösterilecek sipariş
        """
        self.display_header(f"SİPARİŞ #{order.order_id} DETAYLARI")
        
        print(f"Durum: {order.status.value}")
        print(f"Tarih: {order.create_date.strftime('%d.%m.%Y %H:%M')}")
        print(f"Müşteri: {order.customer.name}\n")
        
        print("ÜRÜNLER:")
        for item in order.items:
            print(f"• {item}")
        
        print(f"\nToplam (kargo hariç): {order.get_subtotal()} TL")
        
        if order.shipping_method:
            print(f"Kargo: {order.shipping_method} - {order.shipping_cost} TL")
            
            if order.tracking_number:
                print(f"Takip No: {order.tracking_number}")
                
            if order.delivery_date:
                print(f"Tahmini Teslim: {order.delivery_date.strftime('%d.%m.%Y %H:%M')}")
        
        print(f"TOPLAM: {order.get_total()} TL")
        
        if order.notes:
            print(f"\nSipariş Notu: {order.notes}")
        
        # Admin için ek seçenekler (gösterim amaçlı)
        print("\n--- Admin Seçenekleri ---")
        options = ["Sipariş durumunu güncelle"]
        choice = self.display_menu(options)
        
        if choice == 1:
            self.update_order_status(order)
    
    def update_order_status(self, order):
        """
        Sipariş durumunu günceller.
        
        Args:
            order: Güncellenecek sipariş
        """
        self.display_header(f"SİPARİŞ #{order.order_id} DURUMU GÜNCELLE")
        
        statuses = list(OrderStatus)
        current_index = statuses.index(order.status)
        
        print(f"Mevcut Durum: {order.status.value}")
        print("\nYeni durum seçin:")
        
        for i, status in enumerate(statuses, 1):
            print(f"{i}. {status.value}")
        
        print("\n0. İptal")
        
        while True:
            try:
                choice = int(input("\nSeçiminiz: "))
                if choice == 0:
                    return
                elif 1 <= choice <= len(statuses):
                    new_status = statuses[choice - 1]
                    self.__order_factory.update_order_status(order, new_status)
                    print(f"Sipariş durumu '{new_status.value}' olarak güncellendi.")
                    self.wait_for_enter()
                    return
                print("Geçersiz seçim. Lütfen tekrar deneyin.")
            except ValueError:
                print("Lütfen bir sayı girin.")
    
    def admin_menu(self):
        """Admin menüsü (gösterim amaçlı)"""
        while True:
            self.display_header("YÖNETİCİ PANELİ")
            
            options = [
                "Tüm Kullanıcıları Listele"
            ]
            
            choice = self.display_menu(options)
            
            if choice == 0:
                return
            elif choice == 1:
                self.list_all_customers()
    
    def list_all_customers(self):
        """Tüm kayıtlı müşterileri listeler (admin için)"""
        self.display_header("KAYITLI KULLANICILAR")
        
        if not self.__registered_customers:
            print("Henüz kayıtlı müşteri bulunmamaktadır.")
            self.wait_for_enter()
            return
            
        print(f"Toplam {len(self.__registered_customers)} kayıtlı müşteri:\n")
        
        for email, data in self.__registered_customers.items():
            customer = data["customer"]
            print(f"• {customer.name} ({email})")
            
        self.wait_for_enter()
    
    def display_login_register_menu(self):
        """
        Giriş ve kayıt menüsünü gösterir.
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        while True:
            self.display_header("GİRİŞ / KAYIT MENÜSÜ")
            
            options = ["Giriş Yap", "Yeni Kayıt Oluştur"]
            choice = self.display_menu(options)
            
            if choice == 0:
                return False
            elif choice == 1:  # Giriş Yap
                customer = self.login_customer()
                if customer:
                    self.__current_customer = customer
                    return True
            elif choice == 2:  # Yeni Kayıt
                customer = self.register_customer()
                if customer:
                    self.__current_customer = customer
                    return True
    
    def main_menu(self):
        """Ana menüyü gösterir ve kullanıcı seçimlerini işler"""
        while True:
            title = "SİPARİŞ YÖNETİM SİSTEMİ"
            if self.__current_customer:
                title += f" - Hoş Geldiniz, {self.__current_customer.name}"
            
            self.display_header(title)
            
            # Temel seçenekler
            options = [
                "Ürünlere Göz At",
                "Sepeti Görüntüle",
                "Siparişlerimi Görüntüle"
            ]
            
            # Kullanıcı giriş/çıkış seçenekleri
            if not self.__current_customer:
                options.append("Giriş Yap / Kaydol")
            else:
                options.append("Çıkış Yap")
            
            # Admin paneli
            options.append("Yönetici Paneli")
            
            choice = self.display_menu(options)
            
            if choice == 0:
                if self.prompt("Programdan çıkmak istediğinize emin misiniz? (e/h)").lower() == 'e':
                    self.display_header("TEŞEKKÜRLER")
                    print("Sipariş Yönetim Sistemini kullandığınız için teşekkür ederiz!")
                    print("Güle güle!")
                    break
            elif choice == 1:  # Ürünlere Göz At
                product_info = self.browse_products()
                if product_info:
                    self.__shopping_cart.append(product_info)
                    print(f"\n{product_info[0].name} sepete eklendi.")
                    
                    if self.prompt("Sepeti görüntülemek ister misiniz? (e/h)").lower() == 'e':
                        proceed = self.view_cart()
                        if proceed:
                            self.complete_order()
                    else:
                        self.wait_for_enter()
            elif choice == 2:  # Sepeti Görüntüle
                proceed = self.view_cart()
                if proceed:
                    self.complete_order()
            elif choice == 3:  # Siparişlerimi Görüntüle
                self.view_orders()
            elif choice == 4 and not self.__current_customer:  # Giriş Yap / Kaydol
                self.display_login_register_menu()
            elif choice == 4 and self.__current_customer:  # Çıkış Yap
                self.logout_customer()
            elif choice == 5:  # Yönetici Paneli
                self.admin_menu()
    
    def start(self):
        """Uygulamayı başlatır"""
        # Demo için örnek müşteri ekleme
        demo_customer = Customer("C1234", "Demo Kullanıcı", "demo@example.com", "Demo Adres", "5551234567")
        self.__registered_customers["demo@example.com"] = {"customer": demo_customer, "password": "123456"}
        
        self.main_menu()