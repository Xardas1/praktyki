import pygame
from pathlib import Path
import sys

def get_input_events():
    return pygame.event.get()

def check_for_quit(Events):
    for event in Events:
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:#event.unicode == 'q':
                return True
    return False

def find_all_images(path):
    return [fn for fn in path.iterdir() if fn.is_file()]

def drawFrame(screen,frame_origin,width):
    if frame_origin is not None:
        color = (255,0,0)
        pygame.draw.rect(screen,color,(frame_origin[0],frame_origin[1],width,width),width=2)

def same_cropped_image(fn,frame_width, frame_origin, picture_scale, current_image):
    if frame_origin is not None:
        print('output filename',fn )
        frame_width_cropped = int(frame_width / picture_scale)
        crop_size = (int(frame_origin[0] / picture_scale), int(frame_origin[1] / picture_scale),frame_width_cropped,frame_width_cropped)
        cropped_image = current_image.subsurface(crop_size)
        pygame.image.save(cropped_image,fn)

def main(in_path,out_path):
    pygame.init()
    ratio = 1.5
    #ratio = 2.0
    screen_width = 1200
    screen_size = (screen_width, int(screen_width / ratio))
    screen = pygame.display.set_mode(screen_size)
    images = find_all_images(in_path)
    current_image_idx = 0
    current_image = None
    current_image_scaled = None
    origin = (0,0)
    frame_width_100pct = 224
    picture_scale = None
    frame_origin = None
    frame_width = None
    current_output_tomek = 0
    current_output_gaba = 0
    current_output_maciek = 0
    current_output_mama = 0
    out_path_tomek = out_path / 'tomek'
    out_path_gaba = out_path / 'gaba'
    out_path_maciek = out_path / 'maciek'
    out_path_mama = out_path / 'mama'
    for p in [out_path_tomek,out_path_gaba,out_path_maciek,out_path_mama]:
        if not p.exists():
            p.mkdir()
    while True:
        Events = get_input_events()
        if check_for_quit(Events) == True:
            break
        for event in Events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if current_image_idx + 1 < len(images):
                        current_image_idx = current_image_idx + 1
                        current_image = None
                elif event.key == pygame.K_LEFT:
                    if current_image_idx  >= 1:
                        current_image_idx = current_image_idx - 1
                        current_image = None
                elif event.key == pygame.K_t:
                    fn = out_path_tomek / (images[current_image_idx].stem + f'-{current_output_tomek}' +  images[current_image_idx].suffix)
                    same_cropped_image(fn,frame_width, frame_origin, picture_scale,current_image)
                elif event.key == pygame.K_m:
                    fn = out_path_maciek / (images[current_image_idx].stem + f'-{current_output_maciek}' +  images[current_image_idx].suffix)
                    same_cropped_image(fn,frame_width, frame_origin, picture_scale,current_image)
                elif event.key == pygame.K_g:
                    fn = out_path_gaba / (images[current_image_idx].stem + f'-{current_output_gaba}' +  images[current_image_idx].suffix)
                    same_cropped_image(fn,frame_width, frame_origin, picture_scale,current_image)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y = event.pos
                    frame_origin = (x - frame_width/2,y - frame_width/2)
                    
            elif event.type == pygame.MOUSEWHEEL:
                dw = event.y
                frame_width += 2*dw
                if frame_origin is not None:
                    frame_origin = (frame_origin[0]-dw, frame_origin[1]-dw)
                
        # display current_image
        if current_image is None:
            fn = images[current_image_idx]
            current_image = pygame.image.load(fn)
            im_size = current_image.get_size()
            current_image_scaled = pygame.transform.scale(current_image,screen_size)
            frame_origin = None
            picture_scale = float(screen_width) / float(im_size[0])
            frame_width = frame_width_100pct * picture_scale

        screen.blit(current_image_scaled,origin)
        drawFrame(screen,frame_origin,frame_width)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('provide path with pictures and output folder')
        exit(1)
    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    main(in_path,out_path)
