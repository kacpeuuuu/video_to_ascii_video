# ASCII Video Converter

This project converts videos to ASCII

---

Initially, the plan was to use **only OpenCV (`cv2`)** for the entire conversion and text rendering.  
However, **OpenCV cannot reliably use true monospace fonts** without the `freetype` module, which is not always available.  
Therefore:

- In the current version, **ASCII text is rendered using PIL (Python Imaging Library)** to ensure proper alignment of rows and columns.  
- OpenCV is mainly used for **reading and writing video** and for converting frames to/from images.

---

## Requirements

- Python 3.9+  
- OpenCV (`opencv-python`)  
- Pillow (`PIL`)  
- NumPy  

---

## Usage

```bash

## 🚀 Usage

```bash
python ascii_video.py <input_video> [output_video] [font_size] [characters]
