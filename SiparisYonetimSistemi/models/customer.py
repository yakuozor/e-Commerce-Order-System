#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Müşteri ile ilgili sınıfları içerir
"""

class Customer:
    """
    Müşteri sınıfı. Sistemdeki müşterileri temsil eder.
    """
    
    def __init__(self, customer_id, name, email, address, phone=None):
        """
        Müşteri nesnesi oluşturur.
        
        Args:
            customer_id (str): Müşteri ID
            name (str): Müşteri adı
            email (str): E-posta adresi
            address (str): Teslimat adresi
            phone (str, optional): Telefon numarası
        """
        self.__customer_id = customer_id
        self.__name = name
        self.__email = email
        self.__address = address
        self.__phone = phone
        self.__order_history = []  # Sipariş geçmişi listesi
    
    @property
    def customer_id(self):
        """Müşteri ID getter"""
        return self.__customer_id
    
    @property
    def name(self):
        """Müşteri adı getter"""
        return self.__name
    
    @name.setter
    def name(self, value):
        """Müşteri adı setter"""
        self.__name = value
    
    @property
    def email(self):
        """E-posta adresi getter"""
        return self.__email
    
    @email.setter
    def email(self, value):
        """E-posta adresi setter"""
        # Basit e-posta doğrulama
        if "@" not in value:
            raise ValueError("Geçersiz e-posta adresi")
        self.__email = value
    
    @property
    def address(self):
        """Teslimat adresi getter"""
        return self.__address
    
    @address.setter
    def address(self, value):
        """Teslimat adresi setter"""
        self.__address = value
    
    @property
    def phone(self):
        """Telefon numarası getter"""
        return self.__phone
    
    @phone.setter
    def phone(self, value):
        """Telefon numarası setter"""
        self.__phone = value
    
    @property
    def order_history(self):
        """Sipariş geçmişi getter"""
        return self.__order_history
    
    def add_order_to_history(self, order):
        """
        Müşterinin sipariş geçmişine yeni bir sipariş ekler.
        
        Args:
            order: Sipariş nesnesi
        """
        self.__order_history.append(order)
    
    def get_order_by_id(self, order_id):
        """
        Belirli bir sipariş ID'sine sahip siparişi döndürür.
        
        Args:
            order_id (str): Sipariş ID
            
        Returns:
            Order or None: Sipariş bulunursa sipariş nesnesi, bulunamazsa None
        """
        for order in self.__order_history:
            if order.order_id == order_id:
                return order
        return None
    
    def __str__(self):
        """String temsili"""
        return f"{self.__name} (ID: {self.__customer_id}) - E-posta: {self.__email}" 