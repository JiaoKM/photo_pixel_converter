# photo_pixel_converter

这是一款正在开发中的照片像素风转换应用，目标是经过一系列图像处理，得到可直接用于像素游戏开发或只需少量手动修改即可应用的素材。

This is a Photo to Pixel Art Converter under development. The goal is to obtain assets after a series of image processing. They can be directly used in pixel game development or can be applied with only a small amount of manual modification.

URL: https://jiaokm-photo-pixel-converter-converter-k288iy.streamlit.app/

```
conda create -n photo2pixel python=3.10
conda activate photo2pixel
git clone https://github.com/JiaoKM/photo_pixel_converter.git
cd photo_pixel_converter
pip install -r requirements.txt
streamlit run converter.py
```

## TODOs
- ~~图片自定义比例的裁剪~~
- 提供更多经典调色盘
- 背景自动去除
- 噪声点颜色修正
- 内外轮廓自动描边，多种颜色模式
- 多方向打光

## 示例 Examples

![ori](example_image\example_ori_image.jpg)

![processed](example_image\pixel_art_8_SEGA.png)