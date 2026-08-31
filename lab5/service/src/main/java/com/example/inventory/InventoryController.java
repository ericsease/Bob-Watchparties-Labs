package com.example.inventory;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * REST controller for inventory management.
 *
 * TODO (modernization):
 *   - Replace raw HashMap responses with proper response DTOs or records
 *   - Use ResponseEntity<InventoryItem> instead of ResponseEntity<?>
 *   - Add proper input validation annotations
 *   - Replace null checks with Optional
 */
@RestController
@RequestMapping("/api/inventory")
public class InventoryController {

    private final InventoryService inventoryService;

    public InventoryController(InventoryService inventoryService) {
        this.inventoryService = inventoryService;
    }

    @GetMapping
    public ResponseEntity<List<InventoryItem>> getAllItems() {
        List<InventoryItem> items = inventoryService.findAll();
        return ResponseEntity.ok(items);
    }

    @PostMapping
    public ResponseEntity<?> createItem(@RequestBody InventoryItem item) {
        // TODO (modernization): validate with @Valid and BindingResult, not manual if-checks
        if (item.getName() == null || item.getName().trim().isEmpty()) {
            Map<String, String> error = new HashMap<String, String>();
            error.put("error", "Name is required");
            return ResponseEntity.badRequest().body(error);
        }
        if (item.getQuantity() < 0) {
            Map<String, String> error = new HashMap<String, String>();
            error.put("error", "Quantity cannot be negative");
            return ResponseEntity.badRequest().body(error);
        }
        InventoryItem created = inventoryService.create(item);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteItem(@PathVariable Long id) {
        boolean deleted = inventoryService.delete(id);
        if (!deleted) {
            // TODO (modernization): use a proper @ControllerAdvice exception handler
            Map<String, String> error = new HashMap<String, String>();
            error.put("error", "Item not found: " + id);
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
        }
        return ResponseEntity.noContent().build();
    }
}
