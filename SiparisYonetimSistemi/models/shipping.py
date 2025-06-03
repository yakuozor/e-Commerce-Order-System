#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kargo yöntemleri ile ilgili sınıfları içerir.
Strategy Design Pattern kullanılmıştır.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import random
import string

class ShippingMethod(ABC):
    """
    Kargo yöntemi için soyut temel sınıf.
    Strategy pattern'deki Strategy arayüzü rolünü üstlenir.
    """
    
    @abstractmethod
    def calculate_cost(self, order):
        """
        Kargo maliyetini hesaplar.
        
        Args:
            order (Order): Sipariş nesnesi
            
        Returns:
            float: Hesaplanan kargo maliyeti
        """
        pass
    
    @abstractmethod
    def estimate_delivery_time(self, order):
        """
        Tahmini teslimat süresini hesaplar.
        
        Args:
            order (Order): Sipariş nesnesi
            
        Returns:
            datetime: Tahmini teslimat tarihi
        """
        pass
    
    def generate_tracking_number(self):
        """
        Kargo takip numarası oluşturur.
        
        Returns:
            str: Oluşturulan takip numarası
        """
        # 2 harf + 8 rakam şeklinde takip numarası oluştur
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        numbers = ''.join(random.choices(string.digits, k=8))
        return f"{letters}{numbers}"


class FastShipping(ShippingMethod):
    """
    Hızlı kargo yöntemi.
    Strategy pattern'deki ConcreteStrategy rolünü üstlenir.
    """
    
    def calculate_cost(self, order):
        """
        Hızlı kargo maliyetini hesaplar.
        Baz ücret + ürün başına ek ücret + toplam ağırlık ücreti.
        
        Args:
            order (Order): Sipariş nesnesi
            
        Returns:
            float: Hesaplanan kargo maliyeti
        """
        base_cost = 50  # Hızlı kargo için baz ücret
        per_item_cost = 5  # Ürün başına ek ücret
        
        # Ürün sayısı bazlı ek ücret
        item_count = sum(item.quantity for item in order.items)
        
        # Toplam maliyet
        total_cost = base_cost + (per_item_cost * item_count)
        
        # Toplam sipariş tutarı 1000 TL üzerindeyse indirim
        if order.get_subtotal() > 1000:
            total_cost *= 0.9  # %10 indirim
            
        return total_cost
    
    def estimate_delivery_time(self, order):
        """
        Hızlı kargo için tahmini teslimat süresini hesaplar (1-2 gün).
        
        Args:
            order (Order): Sipariş nesnesi
            
        Returns:
            datetime: Tahmini teslimat tarihi
        """
        # Rastgele 1-2 gün teslimat süresi
        days = random.randint(1, 2)
        return datetime.now() + timedelta(days=days)
    
    def __str__(self):
        """String temsili"""
        return "Hızlı Kargo (1-2 gün)"


class EconomicShipping(ShippingMethod):
    """
    Ekonomik kargo yöntemi.
    Strategy pattern'deki ConcreteStrategy rolünü üstlenir.
    """
    
    def calculate_cost(self, order):
        """
        Ekonomik kargo maliyetini hesaplar.
        Düşük sabit ücret.
        
        Args:
            order (Order): Sipariş nesnesi
            
        Returns:
            float: Hesaplanan kargo maliyeti
        """
        base_cost = 20  # Ekonomik kargo için baz ücret
        
        # Toplam sipariş tutarı 500 TL üzerindeyse ücretsiz kargo
        if order.get_subtotal() > 500:
            return 0
            
        return base_cost
    
    def estimate_delivery_time(self, order):
        """
        Ekonomik kargo için tahmini teslimat süresini hesaplar (3-5 gün).
        
        Args:
            order (Order): Sipariş nesnesi
            
        Returns:
            datetime: Tahmini teslimat tarihi
        """
        # Rastgele 3-5 gün teslimat süresi
        days = random.randint(3, 5)
        return datetime.now() + timedelta(days=days)
    
    def __str__(self):
        """String temsili"""
        return "Ekonomik Kargo (3-5 gün)"


class DroneShipping(ShippingMethod):
    """
    Drone ile kargo yöntemi.
    Strategy pattern'deki ConcreteStrategy rolünü üstlenir.
    """
    
    def calculate_cost(self, order):
        """
        Drone kargo maliyetini hesaplar.
        Yüksek sabit ücret + ağırlık bazlı ek ücret.
        
        Args:
            order (Order): Sipariş nesnesi
            
        Returns:
            float: Hesaplanan kargo maliyeti
        """
        base_cost = 100  # Drone kargo için baz ücret
        per_item_cost = 10  # Ürün başına ek ücret
        
        # Ürün sayısı bazlı ek ücret
        item_count = sum(item.quantity for item in order.items)
        
        # Toplam ücret
        return base_cost + (per_item_cost * item_count)
    
    def estimate_delivery_time(self, order):
        """
        Drone kargo için tahmini teslimat süresini hesaplar (aynı gün veya ertesi gün).
        
        Args:
            order (Order): Sipariş nesnesi
            
        Returns:
            datetime: Tahmini teslimat tarihi
        """
        # Rastgele 0-1 gün teslimat süresi (0: bugün, 1: yarın)
        days = random.randint(0, 1)
        
        # Eğer bugünse, birkaç saat içinde
        if days == 0:
            hours = random.randint(1, 6)
            return datetime.now() + timedelta(hours=hours)
        
        return datetime.now() + timedelta(days=days)
    
    def __str__(self):
        """String temsili"""
        return "Drone ile Teslimat (Aynı gün veya ertesi gün)"


class ShippingFactory:
    """
    Kargo stratejisini belirleyen fabrika sınıfı.
    Factory Method pattern'i uygular.
    """
    
    @staticmethod
    def get_optimal_shipping_method(order):
        """
        Sipariş için en uygun kargo yöntemini belirler.
        
        Args:
            order (Order): Sipariş nesnesi
            
        Returns:
            ShippingMethod: Seçilen kargo yöntemi
        """
        # Toplam ürün miktarı
        total_quantity = sum(item.quantity for item in order.items)
        
        # Toplam sipariş tutarı
        subtotal = order.get_subtotal()
        
        # Stratejik seçim
        if subtotal > 2000:
            # Yüksek değerli siparişler için drone ile teslimat
            return DroneShipping()
        elif subtotal > 1000 or total_quantity <= 2:
            # Orta değerli siparişler veya az ürünlü siparişler için hızlı kargo
            return FastShipping()
        else:
            # Diğer siparişler için ekonomik kargo
            return EconomicShipping() 