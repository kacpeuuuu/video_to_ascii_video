import cv2
from PIL import Image, ImageFont, ImageDraw
import sys
import os
import numpy as np

class ASCII_CONVERTER:
    def __init__(self, width, height, font_size=10, characters="@#=-. "):
        self.characters = characters
        self.width = width
        self.height = height
        self.font_size = font_size



    def pick_character(self, gray_rgb_val):
        index = gray_rgb_val * int(len(self.characters)-1) // 256
        return self.characters[index]

    def img_to_ascii(self, image):
        font = ImageFont.truetype("COUR.TTF", self.font_size)
        # char_width = font.getlength("a")
        # characters_horizontal = int(self.width // char_width)

        img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).convert("L")
        
        char_width = font.getlength("M")
        ascent, descent = font.getmetrics()
        char_height = ascent + descent

        chars_width = int(self.width // char_width)
        chars_height = int(self.height // char_height)  
        img = img.resize((chars_width, chars_height))


        pixels = img.load()

        lines = ""
        for y in range(chars_height):
            for x in range(chars_width):
                gray = pixels[x,y]
                lines += self.pick_character(gray)
            lines += "\n"

        return lines


    def ascii_to_img(self, ascii_text):
        font = ImageFont.truetype("COUR.TTF", self.font_size)
        lines = ascii_text.splitlines()

        char_width = font.getlength("a")
        ascent, descent = font.getmetrics()
        char_height = ascent + descent
        
        max_width = int(len(lines[0]) * char_width)
        max_height = int(len(lines) * char_height)

        img = Image.new("L", (max_width, max_height), color=255)
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), ascii_text, font=font, fill=0)


        img = img.resize((self.width, self.height))

        img_np = np.array(img)
        # cv2.imwrite("bleble.png", img_bgr) #for debugging purposes only


        return img_np

    

def video_slicer(path_to_video, path_to_output="output.mp4", font_size=10, characters="@#=-. "):
    captured_video = cv2.VideoCapture(path_to_video)
    width  = int(captured_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(captured_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(captured_video.get(cv2.CAP_PROP_FPS))
    total_frames = int(captured_video.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter(path_to_output, fourcc, fps, (width, height), isColor=False) 

    converter = ASCII_CONVERTER(width, height, font_size, characters)

    
    i = 0
    while True:
        print(f'progress: {i}/{total_frames}')
        ret, frame = captured_video.read()
        if not ret:
            break
        img_to_ascii = converter.img_to_ascii(frame)
        img_to_ascii = converter.img_to_ascii(frame)
        ascii_to_img = converter.ascii_to_img(img_to_ascii)
        out.write(ascii_to_img)
        i += 1
    out.release()
    captured_video.release()



def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ascii_video.py <input_video> [output_video] [font_size] [characters]")
        print("  ***characters should be arranged from dark to white")
        print("\nExamples:")
        print("  python ascii_video.py input.mp4")
        print("  python ascii_video.py input.mp4 output.mp4 12 \"@#*:. \"")
        sys.exit(1)

    path_to_video = sys.argv[1]
    path_to_output = sys.argv[2] if len(sys.argv) > 2 else "output.mp4"
    font_size = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    characters = sys.argv[4] if len(sys.argv) > 4 else "@#=-. "

    if not os.path.exists(path_to_video):
        print(f"Error: input video '{path_to_video}' does not exist.")
        sys.exit(1)

    print(f"Converting '{path_to_video}' → '{path_to_output}'")
    print(f"Font size: {font_size}, Characters: \"{characters}\"")

    video_slicer(path_to_video, path_to_output, font_size, characters)


if __name__ == "__main__":
    main()