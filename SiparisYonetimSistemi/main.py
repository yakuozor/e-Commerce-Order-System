#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sipariş Yönetim Sistemi - Ana Program
"""

from models.product import Product, ProductCategory
from models.customer import Customer
from models.order import Order, OrderStatus
from models.shipping import ShippingMethod, FastShipping, EconomicShipping, DroneShipping
from services.inventory_manager import InventoryManager
from services.notification_service import NotificationService
from services.order_factory import OrderFactory
from ui.terminal_ui import TerminalUI

def main():
    # Sistem başlatma
    inventory = InventoryManager.get_instance()
    notification_service = NotificationService()
    order_factory = OrderFactory()
    
    # Örnek ürünleri ekle
    inventory.add_product(Product("P001", "iPhone 15", 25000, ProductCategory.ELECTRONICS, 10))
    inventory.add_product(Product("P002", "Samsung Galaxy S23", 20000, ProductCategory.ELECTRONICS, 15))
    inventory.add_product(Product("P003", "AirPods Pro", 4500, ProductCategory.ELECTRONICS, 20))
    inventory.add_product(Product("P004", "Levi's 501 Jean", 1200, ProductCategory.CLOTHING, 30))
    inventory.add_product(Product("P005", "Nike Air Max", 2500, ProductCategory.FOOTWEAR, 12))
    inventory.add_product(Product("P006", "Harry Potter Set", 750, ProductCategory.BOOKS, 5))
    inventory.add_product(Product("P007", "Protein Tozu", 800, ProductCategory.HEALTH, 25))
    
    # Terminal kullanıcı arayüzünü başlat
    ui = TerminalUI(inventory, order_factory, notification_service)
    ui.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram sonlandırıldı.")
    except Exception as e:
        print(f"\nBir hata oluştu: {e}")