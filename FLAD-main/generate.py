import os
import random
from multiprocessing import Process, freeze_support
import utils

select_cnt = 50
audio_root = 'I:\Uni-Git\Master\Tutorial\Unzipped_Data_Picture\final_test'
ds_root = './dataset'
ds_noise = f'{ds_root}/noise'
ds_test = f'{ds_root}/origin'
ext = ['flac', 'opus', 'aac', 'mp3']
cls = ['LL', 'OPUS', 'AAC', 'MP3']


def do(src_path, dst_path, idx, noise=True):
    y_s = utils.get_side(src_path)
    if noise:
        utils.get_spectrum(y_s, idx, dst_path, noise=[0.001, 0.01])
    else:
        utils.get_spectrum(y_s, idx, dst_path)


def generate():

    target_list = utils.get_file_list(audio_root, 'flac')
    random.shuffle(target_list)
    target_list = target_list[:select_cnt]
    
    for i in cls:
        os.makedirs(f'{ds_noise}/{i}', exist_ok=True)
        os.makedirs(f'{ds_test}/{i}', exist_ok=True)
    
    for idx, i in enumerate(target_list):
        o_path = i.replace('\\', '/')
        os.system(f'ffmpeg -i "{o_path}" -map 0:a -af aresample=resampler=soxr -ar 44100 "{ds_root}/temp.flac"')
        for i in ext[1:]:
            os.system(f'ffmpeg -i "{ds_root}/temp.flac" -b:a 128k "{ds_root}/temp.{i}"')
        
        job = []
        for i in range(len(ext)):
            job.append(Process(target=do, args=(f'{ds_root}/temp.{ext[i]}', f'{ds_noise}/{cls[i]}', idx,)))
            job.append(Process(target=do, args=(f'{ds_root}/temp.{ext[i]}', f'{ds_test}/{cls[i]}', idx, True,)))
        
        for i in job:
            i.start()
        for i in job:
            i.join()
        
        for i in ext:
            os.remove(f'{ds_root}/temp.{i}')


if __name__ == '__main__':
    freeze_support()
    generate()
