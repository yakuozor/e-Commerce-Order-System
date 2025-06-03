#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sipariş oluşturma sınıfı.
Factory Method Design Pattern kullanılmıştır.
"""

from models.order import Order, OrderStatus
from models.shipping import ShippingFactory
from services.notification_service import NotificationService

class OrderFactory:
    """
    Sipariş nesneleri oluşturan fabrika sınıfı.
    Factory Method pattern'i uygulanmıştır.
    """
    
    def __init__(self, notification_service=None):
        self.__notification_service = notification_service or NotificationService()
    
    def create_order(self, customer, products_with_quantities, select_shipping=True, shipping_method=None, notes=None):
        """
        Yeni bir sipariş oluşturur.
        
        Args:
            customer: Müşteri nesnesi
            products_with_quantities: (ürün, miktar) tuple'larının listesi
            select_shipping: Kargo yöntemini otomatik seçme
            shipping_method: Elle belirtilen kargo yöntemi
            notes: Sipariş notu
            
        Returns:
            Order or None: Başarılıysa sipariş nesnesi, değilse None
        """
        # Yeni bir sipariş oluştur
        order = Order(customer)
        
        # Ürünleri siparişe ekle
        for product, quantity in products_with_quantities:
            if not order.add_item(product, quantity):
                # Stok yeterli değilse siparişi iptal et
                # Siparişi iptal ederken önceden eklenen ürünlerin stoklarını geri iade et
                for item in order.items:
                    item.product.increase_stock(item.quantity)
                return None
        
        # Sipariş notunu ayarla
        if notes:
            order.notes = notes
        
        # Kargo yöntemini ayarla
        if shipping_method:
            order.shipping_method = shipping_method
        elif select_shipping:
            # Otomatik kargo seçimi
            optimal_shipping = ShippingFactory.get_optimal_shipping_method(order)
            order.shipping_method = optimal_shipping
        
        # Siparişi müşterinin geçmişine ekle
        customer.add_order_to_history(order)
        
        # Bildirim gönder
        if self.__notification_service:
            self.__notification_service.send_order_notification(order, "Siparişiniz başarıyla oluşturuldu!")
        
        return order
    
    def update_order_status(self, order, new_status):
        """
        Sipariş durumunu günceller ve ilgili bildirim ve işlemleri yapar.
        
        Args:
            order: Güncellenecek sipariş
            new_status: OrderStatus enum değeri
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if not isinstance(new_status, OrderStatus):
            return False
        
        # Durum güncellemesi
        old_status = order.status
        order.status = new_status
        
        # Yeni duruma göre ek işlemler
        if new_status == OrderStatus.SHIPPED:
            # Kargo yola çıktığında takip numarası oluştur
            if not order.tracking_number and order.shipping_method:
                order.tracking_number = order.shipping_method.generate_tracking_number()
            
            # Tahmini teslimat tarihini hesapla
            if order.shipping_method:
                order.delivery_date = order.shipping_method.estimate_delivery_time(order)
        
        # Bildirim gönder
        if self.__notification_service:
            message = f"Siparişinizin durumu '{old_status.value}' -> '{new_status.value}' olarak güncellendi."
            
            if new_status == OrderStatus.SHIPPED and order.tracking_number:
                message += f" Takip numaranız: {order.tracking_number}"
                
            if new_status == OrderStatus.SHIPPED and order.delivery_date:
                delivery_str = order.delivery_date.strftime("%d.%m.%Y %H:%M")
                message += f" Tahmini teslimat: {delivery_str}"
                
            self.__notification_service.send_order_notification(order, message)
        
        return True 