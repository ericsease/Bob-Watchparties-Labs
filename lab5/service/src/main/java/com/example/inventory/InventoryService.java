package com.example.inventory;

import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 * Inventory business logic service.
 *
 * TODO (modernization):
 *   - Replace ArrayList iteration with Stream API
 *   - Replace java.util.Date with java.time.LocalDateTime
 *   - Use Optional<> for nullable returns instead of null checks
 *   - Replace manual ID counter with a proper sequence
 */
@Service
public class InventoryService {

    // TODO (modernization): Use a proper repository (Spring Data JPA)
    private final List<InventoryItem> items = new ArrayList<InventoryItem>();
    private Long nextId = 1L;

    public InventoryService() {
        // Seed data — hardcoded for demo purposes
        items.add(new InventoryItem(nextId++, "Laptop Pro 15\"", 42, 1299.99));
        items.add(new InventoryItem(nextId++, "Mechanical Keyboard", 150, 89.95));
        items.add(new InventoryItem(nextId++, "USB-C Hub 7-Port", 78, 34.50));
        items.add(new InventoryItem(nextId++, "27\" 4K Monitor", 23, 449.00));
        items.add(new InventoryItem(nextId++, "Ergonomic Mouse", 200, 59.99));
    }

    public List<InventoryItem> findAll() {
        // TODO (modernization): return List.copyOf(items) — immutable defensive copy
        List<InventoryItem> result = new ArrayList<InventoryItem>();
        for (InventoryItem item : items) {
            result.add(item);
        }
        return result;
    }

    public InventoryItem findById(Long id) {
        // TODO (modernization): return items.stream().filter(i -> i.getId().equals(id)).findFirst()
        for (int i = 0; i < items.size(); i++) {
            InventoryItem item = items.get(i);
            if (item.getId() != null && item.getId().equals(id)) {
                return item;
            }
        }
        return null;
    }

    public InventoryItem create(InventoryItem item) {
        item.setId(nextId++);
        item.setLastUpdated(new Date());
        items.add(item);
        return item;
    }

    public boolean delete(Long id) {
        // TODO (modernization): items.removeIf(i -> i.getId().equals(id))
        for (int i = 0; i < items.size(); i++) {
            if (items.get(i).getId() != null && items.get(i).getId().equals(id)) {
                items.remove(i);
                return true;
            }
        }
        return false;
    }
}
