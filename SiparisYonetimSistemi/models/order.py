#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sipariş ile ilgili sınıfları içerir
"""

from enum import Enum
from datetime import datetime
import uuid

class OrderStatus(Enum):
    """Sipariş durumlarını tanımlayan enum sınıfı"""
    CREATED = "Oluşturuldu"
    PROCESSING = "Hazırlanıyor"
    SHIPPED = "Yola Çıktı"
    DELIVERED = "Teslim Edildi"
    CANCELLED = "İptal Edildi"

class OrderItem:
    """
    Sipariş öğesi sınıfı. Bir siparişte yer alan belirli bir ürünü ve miktarını temsil eder.
    """
    
    def __init__(self, product, quantity):
        """
        Sipariş öğesi oluşturur.
        
        Args:
            product (Product): Ürün nesnesi
            quantity (int): Sipariş miktarı
        """
        self.__product = product
        self.__quantity = quantity
        self.__item_price = product.price  # Sipariş anındaki fiyatı sabitler
    
    @property
    def product(self):
        """Ürün getter"""
        return self.__product
    
    @property
    def quantity(self):
        """Miktar getter"""
        return self.__quantity
    
    @property
    def item_price(self):
        """Ürün birim fiyatı getter"""
        return self.__item_price
    
    def get_subtotal(self):
        """Öğenin toplam fiyatını hesaplar"""
        return self.__item_price * self.__quantity
    
    def __str__(self):
        """String temsili"""
        return f"{self.__product.name} x {self.__quantity} ({self.__item_price} TL/adet)"


class Order:
    """
    Sipariş sınıfı. Bir müşterinin yaptığı siparişi temsil eder.
    """
    
    def __init__(self, customer, shipping_method=None):
        """
        Sipariş nesnesi oluşturur.
        
        Args:
            customer (Customer): Müşteri nesnesi
            shipping_method (ShippingMethod, optional): Kargo yöntemi
        """
        self.__order_id = str(uuid.uuid4())[:8].upper()  # Rastgele sipariş ID
        self.__customer = customer
        self.__items = []  # Sipariş öğeleri listesi
        self.__status = OrderStatus.CREATED
        self.__create_date = datetime.now()
        self.__shipping_method = shipping_method
        self.__shipping_cost = 0
        self.__delivery_date = None
        self.__tracking_number = None
        self.__notes = None
    
    @property
    def order_id(self):
        """Sipariş ID getter"""
        return self.__order_id
    
    @property
    def customer(self):
        """Müşteri getter"""
        return self.__customer
    
    @property
    def items(self):
        """Öğeler listesi getter"""
        return self.__items
    
    @property
    def status(self):
        """Durum getter"""
        return self.__status
    
    @status.setter
    def status(self, value):
        """Durum setter"""
        if not isinstance(value, OrderStatus):
            raise ValueError("Durum bir OrderStatus enum değeri olmalıdır")
        self.__status = value
    
    @property
    def create_date(self):
        """Oluşturma tarihi getter"""
        return self.__create_date
    
    @property
    def shipping_method(self):
        """Kargo yöntemi getter"""
        return self.__shipping_method
    
    @shipping_method.setter
    def shipping_method(self, value):
        """Kargo yöntemi setter"""
        self.__shipping_method = value
        if value:
            self.__shipping_cost = value.calculate_cost(self)
    
    @property
    def shipping_cost(self):
        """Kargo maliyeti getter"""
        return self.__shipping_cost
    
    @property
    def delivery_date(self):
        """Teslimat tarihi getter"""
        return self.__delivery_date
    
    @delivery_date.setter
    def delivery_date(self, value):
        """Teslimat tarihi setter"""
        self.__delivery_date = value
    
    @property
    def tracking_number(self):
        """Takip numarası getter"""
        return self.__tracking_number
    
    @tracking_number.setter
    def tracking_number(self, value):
        """Takip numarası setter"""
        self.__tracking_number = value
    
    @property
    def notes(self):
        """Notlar getter"""
        return self.__notes
    
    @notes.setter
    def notes(self, value):
        """Notlar setter"""
        self.__notes = value
    
    def add_item(self, product, quantity):
        """
        Siparişe yeni bir ürün ekler.
        
        Args:
            product (Product): Eklenecek ürün
            quantity (int): Ürün miktarı
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if quantity <= 0:
            raise ValueError("Miktar pozitif bir değer olmalıdır")
            
        # Stok kontrolü
        if not product.decrease_stock(quantity):
            return False
            
        # Ürün zaten siparişteyse miktarını artır
        for item in self.__items:
            if item.product.product_id == product.product_id:
                # Stok düşürüldüğü için miktar güncellemeye gerek kalmadı
                return True
                
        # Yeni ürün ekle
        self.__items.append(OrderItem(product, quantity))
        return True
    
    def remove_item(self, product_id):
        """
        Belirli bir ürünü siparişten çıkarır ve stok miktarını günceller.
        
        Args:
            product_id (str): Çıkarılacak ürünün ID'si
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        for i, item in enumerate(self.__items):
            if item.product.product_id == product_id:
                # Stok miktarını geri ekle
                item.product.increase_stock(item.quantity)
                # Öğeyi listeden çıkar
                self.__items.pop(i)
                return True
        return False
    
    def get_subtotal(self):
        """
        Siparişin ara toplamını hesaplar (kargo ücreti hariç).
        
        Returns:
            float: Sipariş ara toplamı
        """
        return sum(item.get_subtotal() for item in self.__items)
    
    def get_total(self):
        """
        Siparişin toplam tutarını hesaplar (kargo ücreti dahil).
        
        Returns:
            float: Sipariş toplam tutarı
        """
        return self.get_subtotal() + self.__shipping_cost
    
    def __str__(self):
        """String temsili"""
        status_text = self.__status.value
        items_count = len(self.__items)
        total = self.get_total()
        return f"Sipariş #{self.__order_id} ({status_text}) - {items_count} ürün, Toplam: {total} TL" 