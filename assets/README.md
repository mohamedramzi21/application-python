# Assets Folder

This folder contains all game assets (images, sounds, fonts, etc.)

## 📁 Structure

```
assets/
├── images/
│   ├── rooms/      # Room images (256x256 or 512x512 PNG)
│   ├── items/      # Item icons (64x64 or 128x128 PNG)
│   └── ui/         # UI elements (backgrounds, buttons, icons)
├── sounds/         # (Future) Sound effects and music
└── fonts/          # (Future) Custom fonts
```

## 🖼️ Image Guidelines

### Rooms (`images/rooms/`)
- **Format**: PNG (with transparency support)
- **Size**: 256x256px or 512x512px (square)
- **Naming**: lowercase with underscores
  - Example: `vault.png`, `master_bedroom.png`, `green_house.png`

### Items (`images/items/`)
- **Format**: PNG (with transparency)
- **Size**: 64x64px or 128x128px
- **Naming**: lowercase with underscores
  - Example: `key.png`, `gem.png`, `apple.png`, `shovel.png`

### UI Elements (`images/ui/`)
- **Format**: PNG
- **Size**: Variable (depends on use)
- **Examples**:
  - `background.png` - Main background (1400x900px)
  - `button_normal.png`, `button_hover.png`
  - `panel.png` - UI panels
  - `icon_*.png` - Various icons

## 🎨 Art Style Recommendations

Choose ONE consistent style:
- **Pixel Art**: Retro game style (easier to create)
- **Hand-Drawn**: Artistic, unique look
- **Isometric**: Board game style (matches original)
- **Minimalist**: Clean, modern design

## 📥 Where to Get Images

1. **Create Your Own**:
   - Krita (free, professional)
   - GIMP (free)
   - Aseprite (pixel art, $20)
   - Procreate (iPad, $10)

2. **AI Generation**:
   - DALL-E, Midjourney, Stable Diffusion
   - Prompt: "isometric board game room, vault/library/garden, top-down view"

3. **Free Assets**:
   - OpenGameArt.org
   - itch.io
   - Kenney.nl (great for prototyping)

4. **Commission an Artist**:
   - Fiverr, ArtStation, DeviantArt

## 🚀 Development Phases

**Phase 1**: Use colored rectangles (current - works without images)
**Phase 2**: Add placeholder images (simple colored squares as PNG)
**Phase 3**: Replace with final art

## 📝 Current Room List

You'll need images for these rooms (~30 total):

### Blue Rooms (Common)
- vault.png, den.png, library.png, lavatory.png, drawing_room.png, 
- sitting_room.png, parlor.png, living_room.png, conservatory.png

### Green Rooms (Gardens)
- veranda.png, greenhouse.png, garden.png, patio.png

### Purple Rooms (Bedrooms)
- bedroom.png, master_bedroom.png, nursery.png, chapel.png

### Orange Rooms (Corridors)
- hallway.png, corridor.png, passage.png

### Yellow Rooms (Shops)
- shop.png, market.png, bazaar.png

### Red Rooms (Undesirable)
- trap_room.png, dark_room.png, cursed_room.png

### Special
- entrance.png, antechamber.png (exit)

## 💡 Tips

- Start with simple placeholders
- Focus on making the game work first
- Polish graphics last
- Keep file sizes reasonable (<500KB per image)
- Use consistent lighting/perspective across all images
