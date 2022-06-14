import os
import shutil
import cv2
import random
import numpy as np
import filetype

from PIL import Image

COLORS = [
    (81, 114, 255),
    (116, 205, 255),
]

def findFontLocate(s_txt, font_face, font_thick, cv_bgd):
    best_scale = 1.0
    bgd_w = cv_bgd.shape[1]
    bgd_h = cv_bgd.shape[0]
    txt_rect_w = 0
    txt_rect_h = 0
    baseline = 0
    for scale in np.arange(1.0, 6.0, 0.2):
        (ret_w, ret_h), tmp_bsl = cv2.getTextSize(
            s_txt, font_face, scale, font_thick)
        tmp_w = ret_w + 2 * font_thick
        tmp_h = ret_h + 2 * font_thick + tmp_bsl
        if tmp_w >= bgd_w or tmp_h >= bgd_h:
            break
        else:
            baseline = tmp_bsl
            txt_rect_w = tmp_w
            txt_rect_h = tmp_h
            best_scale = scale
    lt_x, lt_y = round(bgd_w/2-txt_rect_w/2), round(bgd_h/2-txt_rect_h/2)
    rb_x, rb_y = round(bgd_w/2+txt_rect_w/2), round(bgd_h/2+txt_rect_h/2)-baseline
    return (lt_x, lt_y, rb_x, rb_y), best_scale, (txt_rect_w, txt_rect_h)


def preprocess_images(dir, text_list):
    if not os.path.exists(dir):
        return

    c_text_list = text_list.copy()
    photos =  os.listdir(dir)
    if len(photos) == 0:
        return
    
    if os.path.exists("./_photos"):
        shutil.rmtree("./_photos")
        
    os.mkdir("_photos")

    for photo in photos:
        path = os.path.join(dir, photo)
        t = random.choice(c_text_list)
        c = random.choice(COLORS)
        mark_image(path, t, c, os.path.join("_photos", photo))
        c_text_list.remove(t)

        if len(c_text_list) == 0:
            c_text_list = text_list.copy()

def calc_hanging_letter(text):
    hanging_letters = ["g", "j", "y"]
    adjust_px_size = 50

    for letter in hanging_letters:
        if letter in text:
            return adjust_px_size

    return 20


def mark_image(filename, text, color, output_path):
    if filename[-3:] == "txt":
        return

    try:
        img = cv2.imread(filename) 
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    except Exception as e:
        print(e, filename)
        return

    h, _, _ = img.shape

    text_size = 0
    if h > 1000:
        text_size = 10
    else:
        text_size = len(str(h))

    (lt_x, lt_y, rb_x, rb_y), best_scale, (text_w, text_h) = findFontLocate(text, cv2.FONT_HERSHEY_TRIPLEX, text_size, img)
    y_value = h-(rb_y//4)
    alpha = 0.4
    hanging_letter_correction = calc_hanging_letter(text)
    big_image_correction = + text_h + round(best_scale) - 1
    if (y_value + text_h) > h:
        print("Images too big for text, not adding text")
        print(f"Make height greater than {y_value+text_h}")

    overlay = img.copy()
    cv2.rectangle(overlay, (lt_x, y_value+hanging_letter_correction), (lt_x + text_w, y_value+text_h+hanging_letter_correction), (0, 0, 0), -1)
    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
    cv2.putText(img, text, (lt_x, y_value+big_image_correction), cv2.FONT_HERSHEY_TRIPLEX, best_scale, color, text_size, cv2.LINE_AA)
    cv2.imwrite(output_path, img)


def handle_deletions():
    try:
        os.remove("photos/.DS_STORE")
        os.remove("_videos/.DS_STORE")
    except Exception as _:
        print("No Deletions Required")

def clean_photos(dir):

    if os.path.exists(os.path.join(dir, "file_keep.txt")):
        print("File Deletion Avioded (you can also insert this file for force start)")
        return 

    images = os.listdir(dir)
    for image in images:
        filename = os.path.join(dir, image)

        if filename[-3:].lower() == "jpg":
            continue

        if not filetype.is_image(filename):
            print(f"Removed: {filename}")
            os.remove(filename)
            continue
        try:
            pillow_image = Image.open(filename)
        except Exception as _:
            print("Image format unsupported")
        pillow_image = pillow_image.convert("RGB")
        # print(filename.split("."))
        # print(filename.split(".")[1] + ".jpg")
        pillow_image.save("." + filename.split(".")[1] + ".jpg")
        os.remove(filename)