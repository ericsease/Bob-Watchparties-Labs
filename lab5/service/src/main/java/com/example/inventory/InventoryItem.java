package com.example.inventory;

import java.util.Date;

/**
 * Plain old Java object representing an inventory item.
 *
 * TODO (modernization): Replace with a Java 16+ record:
 *   public record InventoryItem(Long id, String name, int quantity, double price, LocalDateTime lastUpdated) {}
 *
 * Current state: 80 lines of boilerplate for 5 fields.
 */
public class InventoryItem {

    private Long id;
    private String name;
    private int quantity;
    private double price;
    // TODO (modernization): Replace java.util.Date with java.time.LocalDateTime
    private Date lastUpdated;

    public InventoryItem() {
    }

    public InventoryItem(Long id, String name, int quantity, double price) {
        this.id = id;
        this.name = name;
        this.quantity = quantity;
        this.price = price;
        this.lastUpdated = new Date();
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public Date getLastUpdated() {
        return lastUpdated;
    }

    public void setLastUpdated(Date lastUpdated) {
        this.lastUpdated = lastUpdated;
    }

    @Override
    public String toString() {
        return "InventoryItem{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", quantity=" + quantity +
                ", price=" + price +
                ", lastUpdated=" + lastUpdated +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        InventoryItem that = (InventoryItem) o;
        if (id == null) return false;
        return id.equals(that.id);
    }

    @Override
    public int hashCode() {
        return id != null ? id.hashCode() : 0;
    }
}
