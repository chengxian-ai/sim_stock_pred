import cv2
import os
from tqdm import tqdm  # 可选，用于显示进度条

def images_to_video(img_folder, output_path, fps=30, scale_factor=0.5):
    """
    将图片序列转换为视频，尺寸缩放为原来的一半
    
    参数：
    img_folder: 图片文件夹路径
    output_path: 输出视频路径（如：output.mp4）
    fps: 视频帧率
    scale_factor: 缩放比例，默认0.5（一半）
    """
    # 获取图片文件列表（按文件名排序）
    img_files = sorted([f for f in os.listdir(img_folder) 
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))])
    
    if not img_files:
        print("错误：没有找到图片文件！")
        return False
    
    # 读取第一张图片获取原始尺寸
    first_img_path = os.path.join(img_folder, img_files[0])
    first_img = cv2.imread(first_img_path)
    
    if first_img is None:
        print(f"错误：无法读取图片 {first_img_path}")
        return False
    
    # 计算缩放后的尺寸
    original_height, original_width = first_img.shape[:2]
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)
    new_size = (new_width, new_height)
    
    # import pdb; pdb.set_trace()
    # 创建视频写入器
    # 使用H.264编码（需要安装对应编码器）
    fourcc = cv2.VideoWriter_fourcc(*'avc1')  # 或 'XVID' 用于avi, 'H264' 需要额外安装
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, new_size)
    
    if not video_writer.isOpened():
        print("错误：无法创建视频写入器！")
        return False
    
    print(f"原始尺寸: {original_width}x{original_height}")
    print(f"目标尺寸: {new_width}x{new_height}")
    print(f"总帧数: {len(img_files)}")
    print(f"输出视频: {output_path}")
    
    # 处理每一张图片
    for i, img_file in enumerate(tqdm(img_files, desc="处理图片")):
        img_path = os.path.join(img_folder, img_file)
        img = cv2.imread(img_path)
        
        if img is not None:
            # 1. 调整尺寸
            resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
            
            # 2. 写入视频
            video_writer.write(resized_img)
        else:
            print(f"警告：无法读取图片 {img_file}")
    
    # 释放资源
    video_writer.release()
    cv2.destroyAllWindows()
    
    print(f"视频生成完成: {output_path}")
    return True

# 使用示例
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='将图片序列转换为视频，支持尺寸缩放')
    parser.add_argument('-i', '--input', type=str, default='/Users/chengxian/Desktop/buy_sell_images/2026-05-28/1y-1d/',
                       help='输入图片文件夹路径')
    parser.add_argument('-o', '--output', type=str, default='/Users/chengxian/Desktop/buy_sell_images/2026-05-28/1y-1d/output_video.mp4',
                       help='输出视频文件路径')
    parser.add_argument('--fps',type=int, default=25,
                       help='视频帧率，默认: 25')
    parser.add_argument('--scale', type=float, default=0.5,
                       help='缩放比例, 默认: 0.5')

    args = parser.parse_args()
    # 基本用法
    images_to_video(
        img_folder=args.input,  # 图片文件夹路径
        output_path=args.output,  # 输出视频路径
        fps=args.fps,  # 帧率
        scale_factor=args.scale  # 缩放为原来的一半
    )
    print('视频生成完成')