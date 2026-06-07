from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def text_to_handwriting_local(text, save_to="handwriting.png", rgb=(0, 15, 85)):
    # 1. Choose a font path (Ink Free looks like real handwriting)
    font_path = "C:/Windows/Fonts/Inkfree.ttf"
    if not os.path.exists(font_path):
        # Fallback to Segoe Print, Comic Sans, or default
        font_path = "C:/Windows/Fonts/segoepr.ttf"
        if not os.path.exists(font_path):
            font_path = "arial.ttf"  # Default system font if all else fails

    font_size = 32
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    # 2. Text wrapping configuration
    # Left margin is 130px, right margin is 50px. Total width = 900px.
    # Text area width = 720px. 720 / 15 = ~48 characters per line.
    wrap_width = 48
    lines = []
    for paragraph in text.split('\n'):
        if not paragraph.strip():
            lines.append("")
        else:
            lines.extend(textwrap.wrap(paragraph, width=wrap_width))

    # 3. Canvas dimensions
    line_height = 45
    top_margin = 80
    bottom_margin = 80
    
    # Calculate required height based on content, with a minimum height
    num_lines = len(lines)
    min_lines = 15
    total_lines = max(num_lines, min_lines)
    img_width = 900
    img_height = top_margin + (total_lines * line_height) + bottom_margin

    # 4. Create image with ruled paper styling (cream background)
    image = Image.new("RGB", (img_width, img_height), (252, 250, 242))
    draw = ImageDraw.Draw(image)

    # Draw ruled lines (blue notebook lines)
    for i in range(total_lines + 1):
        y = top_margin + (i * line_height)
        draw.line([(0, y), (img_width, y)], fill=(200, 220, 240), width=1)
        
    # Draw vertical red margin line
    draw.line([(110, 0), (110, img_height)], fill=(235, 140, 140), width=2)

    # 5. Draw text onto the image
    current_y = top_margin + 5
    for line in lines:
        if line:
            # Draw text with dark blue "ink" color or user-defined rgb
            draw.text((130, current_y), line, font=font, fill=rgb)
        current_y += line_height

    image.save(save_to)
    print(f"Handwriting image successfully saved to: {save_to}")

if __name__ == "__main__":
    txt = input("Enter the message you want to convert into Hand Writing: ")
    if not txt.strip():
        txt = "This is a default handwriting text.\nIt runs completely offline and uses local system fonts!\n\nNo internet API needed."
    
    text_to_handwriting_local(txt, save_to="handwriting.png")
