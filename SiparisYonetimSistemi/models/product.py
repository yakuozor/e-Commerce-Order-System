#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ürün ile ilgili sınıfları içerir
"""

from enum import Enum

class ProductCategory(Enum):
    """Ürün kategorilerini tanımlayan enum sınıfı"""
    ELECTRONICS = "Elektronik"
    CLOTHING = "Giyim"
    FOOTWEAR = "Ayakkabı"
    BOOKS = "Kitaplar"
    COSMETICS = "Kozmetik"
    HEALTH = "Sağlık"
    HOME = "Ev Eşyası"
    OTHER = "Diğer"

class Product:
    """
    Ürün sınıfı. Sistem içindeki ürünleri temsil eder.
    """
    
    def __init__(self, product_id, name, price, category, stock_quantity):
        """
        Ürün nesnesi oluşturur.
        
        Args:
            product_id (str): Ürün ID
            name (str): Ürün adı
            price (float): Ürün fiyatı
            category (ProductCategory): Ürün kategorisi
            stock_quantity (int): Stok miktarı
        """
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__category = category
        self.__stock_quantity = stock_quantity
    
    @property
    def product_id(self):
        """Ürün ID getter"""
        return self.__product_id
    
    @property
    def name(self):
        """Ürün adı getter"""
        return self.__name
    
    @property
    def price(self):
        """Ürün fiyatı getter"""
        return self.__price
    
    @price.setter
    def price(self, value):
        """Ürün fiyatı setter"""
        if value < 0:
            raise ValueError("Ürün fiyatı negatif olamaz")
        self.__price = value
    
    @property
    def category(self):
        """Ürün kategorisi getter"""
        return self.__category
    
    @property
    def stock_quantity(self):
        """Stok miktarı getter"""
        return self.__stock_quantity
    
    @stock_quantity.setter
    def stock_quantity(self, value):
        """Stok miktarı setter"""
        if value < 0:
            raise ValueError("Stok miktarı negatif olamaz")
        self.__stock_quantity = value
    
    def decrease_stock(self, quantity):
        """
        Stok miktarını azaltır.
        
        Args:
            quantity (int): Azaltılacak miktar
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if self.__stock_quantity >= quantity:
            self.__stock_quantity -= quantity
            return True
        return False
    
    def increase_stock(self, quantity):
        """
        Stok miktarını artırır.
        
        Args:
            quantity (int): Artırılacak miktar
        """
        if quantity < 0:
            raise ValueError("Artırılacak miktar negatif olamaz")
        self.__stock_quantity += quantity
    
    def __str__(self):
        """String temsili"""
        return f"{self.__name} ({self.__category.value}) - {self.__price} TL [Stok: {self.__stock_quantity}]" 