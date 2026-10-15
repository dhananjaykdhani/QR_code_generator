# QR Code Generator with Custom Logo

A Python utility to generate high-resolution QR codes with custom centered logos, customizable colors, shapes, and background padding.

## Features

- **High Native Resolution**: Generates QR codes directly at requested pixel dimensions without blurry upscaling.
- **Error Correction**: Uses high error correction (`ERROR_CORRECT_H`, ~30% redundancy) to ensure reliable scanning even with center logos.
- **Custom Logo Embedding**: Scale and position custom logos within the QR code.
- **Background Shape Options**: Support for `"none"`, `"circle"`, `"square"`, or `"rounded"` background shapes behind logos with custom padding.
- **Custom Colors**: Configure fill and background colors for both the QR code and the logo backdrop.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the script directly or import `generate_qr_with_logo`:

```python
from generate_qr import generate_qr_with_logo

generate_qr_with_logo(
    data="https://example.com",
    logo_path="path/to/logo.png",
    output_path="output_qr.png",
    qr_size=1250,
    logo_ratio=0.25,
    fill_color="black",
    back_color="white",
    logo_bg_shape="none",
)
```

Run script:

```bash
python generate_qr.py
```
