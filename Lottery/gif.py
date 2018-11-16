import imageio  # 引入合成gif的库

import os
os.chdir(r'C:\Users\GWT9\Desktop')  # 存放图片的路径
namelist = ['%s_ssq.jpg' % dd for dd in range(1, 10)]

#  合成一个gif图片
def create_gif(image_list, gif_name='SSQ.gif'):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=3)  # duration控制动态图中每张图片的显示时间

create_gif(namelist)