import cv2
import os
import sys
import numpy as np
import random
import moviepy.editor as mp

from util import clean_photos, handle_deletions, preprocess_images
from moviepy.audio.fx.audio_fadeout import audio_fadeout

DESCRIPTIONS = [
    "Delicious",
    "Too Good",
    "Absolutely Profound",
    "Amazing",
    "Wonderful"
]

def import_files(dir_path):
    if not os.path.exists(dir_path):
        return False

    return len(os.listdir(dir_path))

def create_base_video(path, dims, duration):
    
    preprocess_images(path, DESCRIPTIONS)
    edited_photo_path = "./_photos"

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # define video stream
    video = cv2.VideoWriter('video.mp4', fourcc, 1, dims)
    contents = os.listdir(edited_photo_path)

    for i in range(len(contents)):
        p = contents[i]
        img = cv2.imread(os.path.join(edited_photo_path, p))
        for _ in range(duration):
            video.write(img)
            
    cv2.destroyAllWindows()
    video.release()

    print("Base Video Created!")


def create_final_video(path, num_pics):
    # import file into moviepy
    try:
        video = mp.VideoFileClip(path)
    except:
        return

    logo = (mp.ImageClip("logo.png")
          .set_duration(video.duration)
          .resize(height=10**3) # if you need to resize...
          .set_pos(("right","top")))

    end = (mp.ImageClip("logo.png")
          .set_duration(3)
          .resize(height=10**3.25)) # if you need to resize...

    final = mp.CompositeVideoClip([video, logo])
    music_choices = os.listdir("music")
    audioclip = mp.AudioFileClip(os.path.join("music", random.choice(music_choices)))
    final = mp.concatenate_videoclips([final, end], method="compose")
    new_audioclip = mp.CompositeAudioClip([audioclip]).set_duration(final.duration)
    final = final.set_audio(new_audioclip)
    final = audio_fadeout(final, 3)
    final.write_videofile("final.mp4", codec='libx264', 
                     audio_codec='aac', 
                     temp_audiofile='temp-audio.m4a', 
                     remove_temp=True,
                     threads=10)
    


def normalize_size(photo_dir):
    #### THROW ERROR THAT NOT ALL FILES ARE IN SAME ORIENTATION ####
    ### DELETE FILES THAT ARE ###
    photos = os.listdir(photo_dir)
    resolutions = []

    if os.path.exists(os.path.join(photo_dir, "file_keep.txt")):
        print("All file resolutions match through log/force check!")
        return

    for photo in photos:
        p = os.path.join(photo_dir, photo)
        try:
            image = cv2.imread(p)
        except Exception as e:
            print(e)
            continue
        
        if image is None:
            continue

        w, h, _ = image.shape
        resolutions.append(((w, h), p))
    

    common_resolutions = {}
    total = 0
    for resolution in resolutions:
        if resolution[0] not in common_resolutions:
            common_resolutions[resolution[0]] = [resolution[1]]
        else:
            common_resolutions[resolution[0]].append(resolution[1])
        total += 1


    sorted_resolutions = list(sorted(common_resolutions.items(), key=lambda item: len(item[1]), reverse=True))
    
    if len(sorted_resolutions) != 1:
        #print(sorted_resolutions[1])
        for _ in range(len(sorted_resolutions) - 1):
            #print(sorted_resolutions[1])
            for img in sorted_resolutions[1][1]:
                os.remove(img)

        print("Sorry, but some of your files didn't match image resolutions, so we removed them :(")
    else:
        print("All file resolutions match!")

    with open(os.path.join(photo_dir, "file_keep.txt"), "w") as _:
        pass

def get_image_size(image_path):
    try:
        image = cv2.imread(image_path)
    except Exception as e:
        print(e)
        return False

    h, w, _ = image.shape
    return (w,h)

def main():
    dir_path = "./photos/"
    file_count = import_files(dir_path)

    if not file_count:
        print("File Import Failed")
        sys.exit(1)

    handle_deletions()
    clean_photos(dir_path)
    normalize_size(dir_path)
    
    first_image = os.path.join(dir_path, os.listdir(dir_path)[0])
    create_base_video(dir_path, get_image_size(first_image), 5)
    create_final_video("video.mp4", len(os.listdir("_photos")))
    sys.exit(0)

if __name__ == "__main__":
    main()