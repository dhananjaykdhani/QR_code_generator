"""
QR Code Generator with Custom Logo
Generates a QR code with a logo embedded in the center.
"""

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import SquareModuleDrawer
from PIL import Image, ImageDraw
import os


def generate_qr_with_logo(
    data: str,
    logo_path: str,
    output_path: str = "qr_with_logo.png",
    qr_size: int = 13800,
    logo_ratio: float = 0.25,
    border: int = 4,
    fill_color: str = "black",
    back_color: str = "white",
    logo_bg_shape: str = "none",  # "circle", "square", "rounded", or "none"
    logo_bg_color: str = "white",
    logo_padding: int = 1,
):
    """
    Generate a QR code with a custom logo in the center.

    Args:
        data:           The URL or text to encode in the QR code.
        logo_path:      Path to the logo image file (PNG with transparency works best).
        output_path:    Where to save the final QR code image.
        qr_size:        Size of the output image in pixels (square).
        logo_ratio:     How much of the QR code the logo should cover (0.20–0.30 recommended).
        border:         Quiet-zone border size in modules.
        fill_color:     QR module color.
        back_color:     QR background color.
        logo_bg_shape:  Shape of the white background behind the logo.
        logo_bg_color:  Background color behind the logo.
        logo_padding:   Extra padding around the logo inside the background shape.
    """

    # --- 1. Create the QR code with high error correction ---
    # First pass: determine the number of modules
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 30% redundancy (needed for logo)
        box_size=1,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    module_count = qr.modules_count + border * 2

    # Calculate box_size so the image is generated natively at (or above) qr_size
    optimal_box_size = max(1, qr_size // module_count)

    # Regenerate at the optimal native resolution — no blurry upscale
    qr2 = qrcode.QRCode(
        version=qr.version,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=optimal_box_size,
        border=border,
    )
    qr2.add_data(data)
    qr2.make(fit=True)

    qr_img = qr2.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")
    # Only resize if the native size doesn't match exactly (uses NEAREST to keep pixels sharp)
    if qr_img.size[0] != qr_size:
        qr_img = qr_img.resize((qr_size, qr_size), Image.NEAREST)

    # --- 2. Load and resize the logo ---
    logo = Image.open(logo_path).convert("RGBA")

    max_logo_size = int(qr_size * logo_ratio)
    logo.thumbnail((max_logo_size, max_logo_size), Image.LANCZOS)
    logo_w, logo_h = logo.size

    # --- 3. Create a background shape behind the logo ---
    bg_size = max(logo_w, logo_h) + logo_padding * 2

    if logo_bg_shape != "none":
        bg = Image.new("RGBA", (bg_size, bg_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bg)

        if logo_bg_shape == "circle":
            draw.ellipse([0, 0, bg_size - 1, bg_size - 1], fill=logo_bg_color)
        elif logo_bg_shape == "square":
            draw.rectangle([0, 0, bg_size - 1, bg_size - 1], fill=logo_bg_color)
        elif logo_bg_shape == "rounded":
            radius = bg_size // 5
            draw.rounded_rectangle([0, 0, bg_size - 1, bg_size - 1], radius=radius, fill=logo_bg_color)

        # Center the logo on the background shape
        logo_x = (bg_size - logo_w) // 2
        logo_y = (bg_size - logo_h) // 2
        bg.paste(logo, (logo_x, logo_y), logo)

        # Paste background+logo onto the QR code center
        pos_x = (qr_size - bg_size) // 2
        pos_y = (qr_size - bg_size) // 2
        qr_img.paste(bg, (pos_x, pos_y), bg)
    else:
        # No background shape — paste logo directly
        pos_x = (qr_size - logo_w) // 2
        pos_y = (qr_size - logo_h) // 2
        qr_img.paste(logo, (pos_x, pos_y), logo)

    # --- 4. Save ---
    qr_img = qr_img.convert("RGB")
    qr_img.save(output_path, quality=95)
    print(f"QR code saved to: {os.path.abspath(output_path)}")


# ──────────────────────────────────────────────
# Example usage — edit these values and run!
# ──────────────────────────────────────────────
if __name__ == "__main__":
    output_dir = "aditya_builds"
    os.makedirs(output_dir, exist_ok=True)
    generate_qr_with_logo(
        data="https://www.adityabuilds.co.in/",       # <-- your URL or text
        logo_path="/Users/dhananjaykdhani/Drive P/QR/logo-og.png",             # <-- path to your logo image
        output_path=os.path.join(output_dir, "aditya_builds_qr_white_bg.png"),   # <-- output file
        qr_size=1250,                      # <-- image size in pixels
        logo_ratio=0.269,                  # <-- logo covers ~25% of QR width
        fill_color="black",               # <-- QR module color
        back_color="white",               # <-- QR background color
        logo_bg_shape="none",             # <-- "circle", "square", "rounded", or "none"
        logo_bg_color="white",            # <-- background color behind logo
        logo_padding=1,                  # <-- padding around logo
    )
