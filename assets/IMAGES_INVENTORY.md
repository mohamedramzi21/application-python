# 🖼️ Images Inventory

Last updated: 6 November 2025

## ✅ Available Images

### 🏠 Rooms (15 images)
All room images are PNG format, ready to use:

- ✅ Antechamber_Icon.png
- ✅ Chapel_Icon.png
- ✅ Commissary_Icon.png
- ✅ Courtyard_Icon.png
- ✅ Dining_Room_Icon.png
- ✅ Entrance_Hall_Icon.png
- ✅ Garage_Icon.png
- ✅ Library_Icon.png
- ✅ Mail_Room_Icon.png
- ✅ Music_Room_Icon.png
- ✅ Observatory_Icon.png
- ✅ Rumpus_Room_Icon.png
- ✅ Security_Icon.png
- ✅ The_Pool_Icon.png
- ✅ Veranda_Icon.png

### 🎒 Items (5 images)
All item images are PNG format, ready to use:

- ✅ Gem.png
- ✅ Gold.png
- ✅ Key.png
- ✅ Shovel.png
- ✅ steps.png

## 📝 Notes

- All WebP files have been converted to PNG for maximum compatibility
- Images are stored in:
  - `assets/images/rooms/` for room images
  - `assets/images/items/` for item icons
- Naming convention uses underscores and capital letters (e.g., `Entrance_Hall_Icon.png`)

## 🔄 Image Mapping for Code

When implementing image loading, map these files to room/item names:

### Room Name → Image File
```python
room_images = {
    "Antechamber": "Antechamber_Icon.png",
    "Chapel": "Chapel_Icon.png",
    "Commissary": "Commissary_Icon.png",
    "Courtyard": "Courtyard_Icon.png",
    "Dining Room": "Dining_Room_Icon.png",
    "Entrance Hall": "Entrance_Hall_Icon.png",
    "Garage": "Garage_Icon.png",
    "Library": "Library_Icon.png",
    "Mail Room": "Mail_Room_Icon.png",
    "Music Room": "Music_Room_Icon.png",
    "Observatory": "Observatory_Icon.png",
    "Rumpus Room": "Rumpus_Room_Icon.png",
    "Security": "Security_Icon.png",
    "The Pool": "The_Pool_Icon.png",
    "Veranda": "Veranda_Icon.png",
}
```

### Item Name → Image File
```python
item_images = {
    "Gem": "Gem.png",
    "Gold": "Gold.png",
    "Key": "Key.png",
    "Shovel": "Shovel.png",
    "Steps": "steps.png",
}
```

## ❌ Missing Images

You may want to add images for:

### Additional Rooms (from catalog.py)
- Vault, Den, Lavatory, Drawing Room, Sitting Room, Parlor
- Living Room, Conservatory, Greenhouse, Garden, Patio
- Bedroom, Master Bedroom, Nursery, Hallway, Corridor, Passage
- Shop, Market, Bazaar, Trap Room, Dark Room, Cursed Room

### Additional Items
- Apple, Banana, Cake, Sandwich, Meal (food items)
- Hammer, Lockpick Kit, Metal Detector, Rabbit Foot (permanent items)
- Chest, Dig Spot, Locker (interactive objects)
- Dice (consumable)

## 🎯 Priority

Since you have 15/30+ rooms, consider:
1. Use available images first
2. Create placeholders for missing rooms (colored rectangles)
3. Add more images gradually
