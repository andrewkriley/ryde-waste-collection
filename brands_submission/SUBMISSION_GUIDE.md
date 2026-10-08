# Home Assistant Brands Submission Guide

## Overview
Your brand icons are ready to submit to the official Home Assistant Brands repository.

## Your Icon Details
- **Domain**: `ryde_waste_collection`
- **Icon Files Ready**: 
- ✅ `icon.png` (256x256)
    - ✅ `icon@2x.png` (512x512)
    - ✅ `dark_icon.png` (256x256)
    - ✅ `dark_icon@2x.png` (512x512)

## Files Location
All files are in: `brands_submission/ryde_waste_collection/`

## Submission Steps

### 1. Fork the Brands Repository
Go to: https://github.com/home-assistant/brands
Click "Fork" in the top right

### 2. Clone Your Fork
```bash
git clone https://github.com/YOUR_USERNAME/brands.git
cd brands
```

### 3. Create Branch
```bash
git checkout -b add-ryde-waste-collection-icon
```

### 4. Add Your Icons
```bash
# Copy your icons to the custom_integrations folder
mkdir -p custom_integrations/ryde_waste_collection
cp /home/andreril/ryde-waste-collection/brands_submission/ryde_waste_collection/*.png custom_integrations/ryde_waste_collection/
```

### 5. Verify Files
```bash
ls -lh custom_integrations/ryde_waste_collection/
# Should show:
# icon.png (256x256)
# icon@2x.png (512x512)
# dark_icon.png (256x256)
# dark_icon@2x.png (512x512)
```

### 6. Commit and Push
```bash
git add custom_integrations/ryde_waste_collection/
git commit -m "Add Ryde Waste Collection custom integration icons"
git push origin add-ryde-waste-collection-icon
```

### 7. Create Pull Request
1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Title: "Add Ryde Waste Collection custom integration icons"
4. Description:
   ```
   Add icons for Ryde Waste Collection custom integration.
   
   Integration repository: https://github.com/andrewkriley/ryde-waste-collection
   Domain: ryde_waste_collection
   
   Files included:
   - icon.png (256x256)
   - icon@2x.png (512x512)
   - dark_icon.png (256x256)
   - dark_icon@2x.png (512x512)
   ```
5. Submit the PR

## Requirements Met ✅
- ✅ Icon is exactly 256x256 pixels
- ✅ Icon@2x is exactly 512x512 pixels
- ✅ Dark icon is exactly 256x256 pixels
- ✅ Dark icon@2x is exactly 512x512 pixels
- ✅ All icons are PNG files
- ✅ All icons are optimized
- ✅ Domain matches integration manifest.json domain
- ✅ Icons are in custom_integrations folder

## After Approval
Once your PR is merged, your icons will be available at:
- `https://brands.home-assistant.io/ryde_waste_collection/icon.png`
- `https://brands.home-assistant.io/ryde_waste_collection/icon@2x.png`
- `https://brands.home-assistant.io/ryde_waste_collection/dark_icon.png`
- `https://brands.home-assistant.io/ryde_waste_collection/dark_icon@2x.png`

Home Assistant will automatically use the appropriate icon based on the user's theme!

## Notes
- The brands repository uses PNG images (not SVG)
- Icon must be square (1:1 aspect ratio)
- Standard size is 256x256, hDPI version is 512x512
- Custom integrations go in `custom_integrations/` folder
- Dark theme variants are optimized for dark mode display
- If dark variants are missing, HA falls back to regular icons

## Icon Details
- **Regular icons**: Optimized for light themes
- **Dark icons**: Slightly brightened (10%) for better visibility on dark backgrounds
