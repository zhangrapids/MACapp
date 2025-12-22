"""
Create application icon for Medical Health Assistant
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a 256x256 icon with medical theme
    size = 256
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a medical cross background (blue circle)
    circle_color = (33, 150, 243, 255)  # Blue
    draw.ellipse([20, 20, size-20, size-20], fill=circle_color)
    
    # Draw white cross
    cross_color = (255, 255, 255, 255)
    cross_width = 40
    center = size // 2
    
    # Vertical bar
    draw.rectangle(
        [center - cross_width//2, 60, center + cross_width//2, size-60],
        fill=cross_color
    )
    
    # Horizontal bar
    draw.rectangle(
        [60, center - cross_width//2, size-60, center + cross_width//2],
        fill=cross_color
    )
    
    # Add a heart outline in the center
    heart_color = (244, 67, 54, 255)  # Red
    heart_size = 50
    hx, hy = center, center + 10
    
    # Simple heart shape using polygon
    heart_points = [
        (hx, hy),
        (hx - heart_size//2, hy - heart_size//3),
        (hx - heart_size//2, hy - heart_size),
        (hx, hy - heart_size//2),
        (hx + heart_size//2, hy - heart_size),
        (hx + heart_size//2, hy - heart_size//3),
        (hx, hy + heart_size//2)
    ]
    draw.polygon(heart_points, fill=heart_color)
    
    # Save as ICO file
    img.save('app_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    
    # Also save as PNG for other uses
    img.save('app_icon.png', format='PNG')
    
    print("✓ Icon created successfully: app_icon.ico")
    
except ImportError:
    print("✗ PIL/Pillow not installed. Using default icon.")
    print("  Install with: pip install Pillow")
except Exception as e:
    print(f"✗ Error creating icon: {e}")
    print("  Will use default icon instead.")