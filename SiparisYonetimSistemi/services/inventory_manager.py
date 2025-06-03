#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Stok yönetimi için singleton sınıf.
Singleton Design Pattern kullanılmıştır.
"""

class InventoryManager:
    """
    Stok yönetimi için singleton sınıf.
    Tüm ürünlerin stok durumlarını merkezi olarak yönetir.
    """
    
    # Singleton örneği
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """
        Singleton örneğini döndürür, yoksa oluşturur.
        
        Returns:
            InventoryManager: Singleton örneği
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """
        Stok yöneticisi oluşturur.
        """
        # Eğer zaten bir örnek oluşturulmuşsa hata fırlat
        if InventoryManager._instance is not None:
            raise Exception("Bu sınıf bir Singleton'dır. get_instance() metodunu kullanın.")
            
        self.__products = {}  # Ürün ID'si -> Ürün nesnesi eşleşmesi
    
    def add_product(self, product):
        """
        Sisteme yeni bir ürün ekler veya var olan ürünün bilgilerini günceller.
        
        Args:
            product: Eklenecek veya güncellenecek ürün
        """
        self.__products[product.product_id] = product
    
    def remove_product(self, product_id):
        """
        Sistemden bir ürünü çıkarır.
        
        Args:
            product_id: Çıkarılacak ürünün ID'si
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if product_id in self.__products:
            del self.__products[product_id]
            return True
        return False
    
    def get_product(self, product_id):
        """
        Ürün ID'sine göre ürünü döndürür.
        
        Args:
            product_id: Ürün ID'si
            
        Returns:
            Product or None: Ürün bulunursa ürün nesnesi, bulunamazsa None
        """
        return self.__products.get(product_id)
    
    def get_all_products(self):
        """
        Tüm ürünleri döndürür.
        
        Returns:
            list: Tüm ürün nesnelerinin listesi
        """
        return list(self.__products.values())
    
    def get_products_by_category(self, category):
        """
        Belirli bir kategorideki ürünleri döndürür.
        
        Args:
            category: ProductCategory enum değeri
            
        Returns:
            list: Kategorideki ürün nesnelerinin listesi
        """
        return [product for product in self.__products.values() if product.category == category]
    
    def check_stock(self, product_id, quantity):
        """
        Belirli bir ürünün stok durumunu kontrol eder.
        
        Args:
            product_id: Ürün ID'si
            quantity: Kontrol edilecek miktar
            
        Returns:
            bool: Stok yeterliyse True, değilse False
        """
        product = self.get_product(product_id)
        if product is None:
            return False
        return product.stock_quantity >= quantity
    
    def update_stock(self, product_id, delta):
        """
        Belirli bir ürünün stok miktarını günceller.
        
        Args:
            product_id: Ürün ID'si
            delta: Stok miktarı değişimi (pozitif artış, negatif azalış)
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        product = self.get_product(product_id)
        if product is None:
            return False
            
        if delta < 0 and product.stock_quantity < abs(delta):
            # Eğer azalış miktarı mevcut stoktan fazlaysa hata
            return False
            
        if delta < 0:
            product.decrease_stock(abs(delta))
        else:
            product.increase_stock(delta)
            
        return True 