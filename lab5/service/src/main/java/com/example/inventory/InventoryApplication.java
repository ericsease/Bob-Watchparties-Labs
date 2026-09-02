package com.example.inventory;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class InventoryApplication {

    public static void main(String[] args) {
        System.out.println("===========================================");
        System.out.println("  Inventory Service (Legacy Java 8 build) ");
        System.out.println("  http://localhost:8080/api/inventory       ");
        System.out.println("===========================================");
        SpringApplication.run(InventoryApplication.class, args);
    }
}
