from devsnets.__internal.utils.system import get_os_name
from devsnets.__internal.data import config
from devsnets.__internal.utils import log
from devsnets.__internal.utils.io import info as io_info
from devsnets.__internal.utils import system
from devsnets.computer_vision import exceptions as computer_vision_exceptions
from devsnets.__internal.utils import http
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import threading
import time
import math
import cv2
import sys




def draw_border(image, top_left_point, bottom_right_point, color, thickness, radius=5, length=5):
    x1, y1 = top_left_point
    x2, y2 = bottom_right_point
    res_scale = (image.shape[0] + image.shape[1])/2000
    radius = int(radius * res_scale)
 
    # Top left
    cv2.line(image, (x1 + radius, y1), (x2 - radius - length, y1), color, thickness, cv2.LINE_AA)
    cv2.line(image, (x1, y1 + radius), (x1, y2 - radius - length), color, thickness, cv2.LINE_AA)
    cv2.ellipse(image, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness, cv2.LINE_AA)
 
    # Top right
    cv2.line(image, (x2 - radius, y1), (x1 + radius + length, y1), color, thickness, cv2.LINE_AA)
    cv2.line(image, (x2, y1 + radius), (x2, y2 - radius - length), color, thickness, cv2.LINE_AA)
    cv2.ellipse(image, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness, cv2.LINE_AA)
 
    # Bottom left
    cv2.line(image, (x1 + radius, y2), (x2 - radius - length, y2), color, thickness, cv2.LINE_AA)
    cv2.line(image, (x1, y2 - radius), (x1, y1 + radius + length), color, thickness, cv2.LINE_AA)
    cv2.ellipse(image, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness, cv2.LINE_AA)
 
    # Bottom right
    cv2.line(image, (x2 - radius, y2), (x1 + radius + length, y2), color, thickness, cv2.LINE_AA)
    cv2.line(image, (x2, y2 - radius), (x2, y1 + radius + length), color, thickness, cv2.LINE_AA)
    cv2.ellipse(image, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness, cv2.LINE_AA)



def plot_box(image, top_left_point, bottom_right_point, width, height, label, color=(210,240,0), padding=6, font_scale=0.375, alpha=0.15):
    label = label.title()

    if alpha > 1:
        alpha = 1

    if alpha > 0:
        box_crop = image[top_left_point['y']:top_left_point['y']+height, top_left_point['x']:top_left_point['x']+width]

        colored_rect = np.ones(box_crop.shape, dtype=np.uint8)
        colored_rect[:,:,0] = color[0] - 90 if color[0] - 90 >= 0 else 0
        colored_rect[:,:,1] = color[1] - 90 if color[1] - 90 >= 0 else 0
        colored_rect[:,:,2] = color[2] - 90 if color[2] - 90 >= 0 else 0

        box_crop_weighted = cv2.addWeighted(box_crop, 1 - alpha, colored_rect, alpha, 1.0)

        image[top_left_point['y']:top_left_point['y']+height, top_left_point['x']:top_left_point['x']+width] = box_crop_weighted


    draw_border(image, (top_left_point['x'] - 1, top_left_point['y']), (bottom_right_point['x'], bottom_right_point['y']), color, thickness=1, radius=5, length=5)

    res_scale = (image.shape[0] + image.shape[1])/1600
    

    font_scale = font_scale * res_scale
    font_width, font_height = 0, 0
    font_face = cv2.FONT_HERSHEY_SIMPLEX

    text_size = cv2.getTextSize(label, font_face, fontScale=font_scale, thickness=1)[0]


    if text_size[0] > font_width:
        font_width = text_size[0]

    if text_size[1] > font_height:
        font_height = text_size[1]
    
    if top_left_point['x'] - 1 < 0:
        top_left_point['x'] = 1
    
    if top_left_point['x'] + font_width + padding*2 > image.shape[1]:
        top_left_point['x'] = image.shape[1] - font_width - padding*2

    if top_left_point['y'] - font_height - padding*2  < 0:
        top_left_point['y'] = font_height + padding*2
    

    p3 = top_left_point['x'] + font_width + padding*2, top_left_point['y'] - font_height - padding*2

    cv2.rectangle(image, (top_left_point['x'] - 1, top_left_point['y']), p3, color, -1, lineType=cv2.LINE_AA)

    x = top_left_point['x'] + padding
    y = top_left_point['y'] - padding
    
    cv2.putText(image, label, (x, y), font_face, font_scale, [0, 0, 0], thickness=1, lineType=cv2.LINE_AA)

    return image



def draw(image, detections, classes=None, alpha=0.15):
    image_copy = image.copy()
    
    for box in detections:
        draw_box = False
        class_name = box['class_name']
        conf = box['confidence']
        label = class_name + ' ' + str(int(conf*100)) + '%'
        width = box['width']
        height = box['height']
        
        if (classes is None) or (classes is not None and class_name in classes):
            draw_box = True

        if draw_box:
            image_copy = plot_box(image_copy, box['top_left_point'], box['bottom_right_point'], width, height, label, alpha=alpha)

    return image_copy



def show_frame(frame):
    cv2.imshow('Devsnets', frame)
    cv2.waitKey(10)



def save_frame(frame, path):
    cv2.imwrite(system.join_paths(config.outputs_folder_path, path), frame)



class URLImage:
    def __init__(self, url):
        self.url = url
        self.filename = system.get_filename_from_url(url)
        self.path = self.filename
        self.full_path = system.join_paths(config.inputs_folder_path, self.filename)
        http.download_file_from_url(url, self.full_path)


    def delete(self):
        system.delete_file(self.full_path)




class Image:
    def __init__(self, path):
        self.path = path
        self.host_path = system.join_paths(config.inputs_folder_path, path)

        if not io_info.file_exists(self.host_path):
            error = f'file {self.host_path} not found.'
            log.error(error)
            raise computer_vision_exceptions.ImageNotFound(error)

        self.image = cv2.imread(self.host_path)
        self.raw_image = self.image.copy()
        self.width = self.raw_image.shape[1]
        self.height = self.raw_image.shape[0]


    def draw(self, detections, alpha=0.15):
        self.image = draw(self.raw_image, detections, alpha=alpha)


    def erase(self):
        self.image = self.raw_image.copy()


    def show(self, detections=None):
        if detections is not None:
            self.draw(detections)

        dpi = 80
        image_width = self.image.shape[1]
        image_height = self.image.shape[0]
        figsize = image_width / float(dpi), image_height / float(dpi)
        figure = plt.figure(figsize=figsize)
        figure.canvas.set_window_title(self.path)
        ax = figure.add_axes([0, 0, 1, 1])
        ax.axis('off')
        ax.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB), cmap='gray')
        plt.show()
    

    def save(self, path):
        cv2.imwrite(system.join_paths(config.outputs_folder_path, path), self.image)
        log.info(f'{path} saved succesfully')



class Video:
    def __init__(self, path):
        self.path = path
        self.host_path = system.join_paths(config.inputs_folder_path, path)
       
        if not io_info.file_exists(self.host_path):
            error = f'file {self.host_path} not found.'
            log.error(error)
            raise computer_vision_exceptions.VideoNotFound(error)

        self.video = cv2.VideoCapture(self.host_path)
        self.width  = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.video.get(cv2.CAP_PROP_FPS))
        self.save = False
        self.cache = []
        self.video_ended = False
        self.show_progress = False
        self.draw_update_time = 0
        self.frame_number = 1
        self.frames_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.callback = None
        self.drawing_thread = threading.Thread(target=self.draw_from_cache, daemon=True)


    def start(self, field_name, subfield_name, algorithm_name, output_path, show_progress, alpha):
        self.drawing_alpha = alpha
        self.field_name = field_name
        self.subfield_name = subfield_name
        self.algorithm_name = algorithm_name
        self.output_path = output_path
        self.frames_since_last_tracking = 0
        self.tracking_interval = 1
        self.last_tracking_time = time.time()

        if output_path is not None:
            self.save = True
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            self.output = cv2.VideoWriter(system.join_paths(config.outputs_folder_path, output_path), fourcc, self.fps, (self.width, self.height))
        
        self.show_progress = show_progress

        if self.show_progress:
            print()
            ascii_bar = True if get_os_name() == 'Windows' else False
            self.pbar = tqdm(total=self.frames_count, ascii=ascii_bar, unit=' frames', dynamic_ncols=True, file=sys.stdout)
        
        self.drawing_thread.start()


    def set_callback(self, callback):
        self.callback = callback


    def __reload_video(self):
        self.video = cv2.VideoCapture(self.host_path)
        self.width  = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = math.ceil(self.video.get(cv2.CAP_PROP_FPS))
        self.save = False
        self.cache = []
        self.video_ended = False
        self.show_progress = False
        self.draw_update_time = 0
        self.frame_number = 1
        self.frames_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.callback = None
        del self.drawing_thread
        self.drawing_thread = threading.Thread(target=self.draw_from_cache, daemon=True)


    def abort(self):
        self.video_ended = True

        if self.show_progress:
            self.pbar.close()
            print()

        if self.drawing_thread.is_alive():
            self.drawing_thread.join()
        
        if self.save:
            self.output.release()

        self.video.release()
        self.__reload_video()

        
    def close(self):
        self.video_ended = True

        if self.show_progress:
            self.pbar.update(self.frames_count - self.pbar.n)
            self.pbar.close()
            print()
        
        if self.drawing_thread.is_alive():
            self.drawing_thread.join()
        
        if self.save:
            self.output.release()

        self.video.release()
        self.__reload_video()


    def draw_from_cache(self):
        while not self.video_ended or len(self.cache) > 0:
            if len(self.cache) > 0:
                detections = self.cache.pop(0)
                
                if self.video.isOpened():
                    ok, frame = self.video.read()

                    if ok:
                        detected_frame = draw(frame, detections, alpha=self.drawing_alpha)

                        if self.callback is not None:
                            self.callback(frame, detected_frame, detections, self.frame_number, self.frames_count)

                        if self.save:
                            self.output.write(detected_frame)

                        if self.show_progress:
                            self.pbar.update(1)
                        
                    self.frame_number += 1
                    self.frames_since_last_tracking += 1

                time_since_last_tracking = time.time() - self.last_tracking_time

                if time_since_last_tracking >= self.tracking_interval:
                    self.last_tracking_time = time.time()
                    self.frames_since_last_tracking = 0


    def draw(self, detections):
        self.cache.append(detections)
    

    def process(self, detections, alpha, draw_detections=False):
        result = {}

        if self.video.isOpened():
            ok, frame = self.video.read()
            
            if ok:
                result['frame'] = frame
                
                if draw_detections:
                    detected_frame = draw(frame, detections, alpha=alpha)
                    result['detected_frame'] = detected_frame
                
                result['detections'] = detections
                result['frame_number'] = self.frame_number
                result['frames_count'] = self.frames_count
            
            self.frame_number += 1
    
        return result




class ObjectDetectionWebsocketLogger:
    def __init__(self, sio):
        self.sio = sio
    

    def info(self, message):
        self.sio.emit('new_info', message)
    

    def detected(self, detections):
        self.sio.emit('detected', detections)


    def metrics(self, data):
        self.sio.emit('new_metrics', data)


    def finished_training(self):
        self.sio.emit('finished_training')


    def video_loaded(self):
        self.sio.emit('video_loaded')


    def video_ended(self):
        self.sio.emit('video_ended')


    def error(self, message):
        self.sio.emit('error_ocurred', message)
