#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bildirim sistemi sınıfları.
Observer Design Pattern kullanılmıştır.
"""

from abc import ABC, abstractmethod
from datetime import datetime

class NotificationObserver(ABC):
    """
    Bildirim gözlemcisi için soyut sınıf.
    Observer pattern'deki Observer rolünü üstlenir.
    """
    
    @abstractmethod
    def update(self, order, message):
        """
        Yeni bir bildirim geldiğinde çağrılır.
        
        Args:
            order: Bildirimle ilgili sipariş
            message: Bildirim mesajı
        """
        pass


class EmailNotification(NotificationObserver):
    """
    E-posta bildirimi sınıfı.
    """
    
    def update(self, order, message):
        """
        E-posta bildirimi gönderir.
        
        Args:
            order: Bildirimle ilgili sipariş
            message: Bildirim mesajı
        """
        customer = order.customer
        print(f"📧 E-posta gönderiliyor: {customer.email} - Konu: Sipariş #{order.order_id} Güncelleme")
        print(f"   İçerik: {message}")


class SMSNotification(NotificationObserver):
    """
    SMS bildirimi sınıfı.
    """
    
    def update(self, order, message):
        """
        SMS bildirimi gönderir.
        
        Args:
            order: Bildirimle ilgili sipariş
            message: Bildirim mesajı
        """
        customer = order.customer
        if customer.phone:
            print(f"📱 SMS gönderiliyor: {customer.phone}")
            print(f"   İçerik: Sipariş #{order.order_id} - {message}")


class PushNotification(NotificationObserver):
    """
    Mobil uygulama push bildirimi sınıfı.
    """
    
    def update(self, order, message):
        """
        Push bildirimi gönderir.
        
        Args:
            order: Bildirimle ilgili sipariş
            message: Bildirim mesajı
        """
        customer = order.customer
        print(f"📲 Push bildirimi gönderiliyor: Kullanıcı #{customer.customer_id}")
        print(f"   İçerik: Sipariş #{order.order_id} - {message}")


class NotificationService:
    """
    Bildirim servisi.
    Observer pattern'deki Subject rolünü üstlenir.
    """
    
    def __init__(self):
        """
        Bildirim servisi oluşturur.
        """
        self.__observers = []
        
        # Varsayılan gözlemcileri ekle
        self.add_observer(EmailNotification())
        self.add_observer(SMSNotification())
    
    def add_observer(self, observer):
        """
        Bildirim gözlemcisi ekler.
        
        Args:
            observer: Eklenecek gözlemci
        """
        if observer not in self.__observers:
            self.__observers.append(observer)
    
    def remove_observer(self, observer):
        """
        Bildirim gözlemcisini çıkarır.
        
        Args:
            observer: Çıkarılacak gözlemci
        """
        if observer in self.__observers:
            self.__observers.remove(observer)
    
    def send_order_notification(self, order, message):
        """
        Sipariş ile ilgili bildirim gönderir.
        
        Args:
            order: Sipariş nesnesi
            message: Bildirim mesajı
        """
        # Bildirim gönderme zamanı
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        
        # Bildirim mesajını genişlet
        full_message = f"[{timestamp}] {message}"
        
        # Tüm gözlemcilere bildir
        for observer in self.__observers:
            observer.update(order, full_message)
    
    def notify_all(self, order, status_message):
        """
        Tüm bildirim kanallarına durum değişikliği mesajı gönderir.
        
        Args:
            order: Sipariş nesnesi
            status_message: Durum değişikliği mesajı
        """
        self.send_order_notification(order, status_message) 