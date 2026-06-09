# Offline Text-to-Handwriting Converter

A local, private Python utility that transforms typed text into a realistic handwriting image. Unlike online API-based alternatives, this tool runs completely offline, rendering text onto a custom-styled, ruled digital notebook page using local system fonts.

---

## Features

- **100% Offline & Private:** No external API calls are made. Your text stays entirely on your local machine.
- **Realistic Ruled Notebook Style:** Generates a cream-colored paper background (`#FCFAF2`) with horizontal light-blue lines and a vertical pink/red margin boundary.
- **Dynamic Height Adjustment:** Automatically scales the image height depending on the length of your text, ensuring short or long texts fit perfectly.
- **Automatic Text Wrapping:** Intelligent word wrapping prevents sentences from overflowing the notebook margins.
- **Font Fallback:** Searches for realistic pre-installed Windows handwriting fonts (`Ink Free` or `Segoe Print`), with standard system fallbacks.
- **Customizable Ink:** Default royal-blue ink color (`rgb(0, 15, 85)`), which is fully customizable in the code.

---

## How It Works

1. **Font Detection:** The script checks `C:/Windows/Fonts/` for `Inkfree.ttf` (a highly realistic handwriting font) or `segoepr.ttf`. If neither is found, it falls back to standard Arial.
2. **Text Wrapping:** The standard library `textwrap` module splits paragraphs into individual lines that fit within the 720px text area.
3. **Canvas Drawing:** 
   - A clean cream canvas is created using **Pillow (PIL)**.
   - Blue horizontal rules are drawn at regular line-height intervals (`45px`).
   - A red vertical line is drawn at `x=110px` to represent a notebook margin.
4. **Text Rendering:** The text is overlaid in dark blue ink with offsets to align perfectly between the notebook lines.
5. **Saving:** The finished product is saved as a high-quality `.png` image.

---

## Installation & Setup

### 1. Prerequisites
- Python 3.x

### 2. Install Pillow
The tool relies on the Pillow library for image generation. Install it via pip:
```bash
pip install Pillow
```

---

## Usage Instructions

1. Open your terminal or command prompt.
2. Navigate to the project directory:
   ```bash
   cd "C:\Users\DELL\OneDrive\Desktop\Python Projects\03-Text-to-HandWriting"
   ```
3. Run the script:
   ```bash
   python main.py
   ```
4. Enter the text you want to convert. Press `Enter`. (If you leave it blank, default demo text will be used).
5. The output image will be saved as **`handwriting.png`** in the same folder.

---

## Customization Tips

You can easily modify variables in [main.py](file:///c:/Users/DELL/OneDrive/Desktop/Python%20Projects/03-Text-to-HandWriting/main.py) to change the look:

- **Ink Color:** Modify the `rgb` tuple parameter in `text_to_handwriting_local()`.
  - Black ink: `rgb=(0, 0, 0)`
  - Blue ink: `rgb=(0, 15, 85)` (default)
- **Font Size:** Change `font_size = 32` on line 14.
- **Line Spacing:** Adjust `line_height = 45` on line 32.
- **Margin Width:** Adjust the horizontal values (e.g., `130` for text start, `110` for red line).
