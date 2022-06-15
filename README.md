## 代码使用说明：

1 安装requirements.txt的包

```
pip install git+https://github.com/JoHof/lungmask
```

2 代码

```
|--mytest.py 为测试代码
|--ckpt为训练模型
```

## 数据说明：

```python
|-- data（dicom格式的数据集，一个.IMA后缀的文件代表一个切片，整个文件夹为一个患者的dicom序列）
|--result（输出格式为.nii格式的三维数据，与data文件夹一起，使用itk-snap软件打开）

示例数据和结果链接：
链接：https://pan.baidu.com/s/1OhBs-47xtQ4dVQl-RKoQ0Q 
提取码：9ccp
```

## 网络：

- U-net(R231): This model was trained on a large and diverse dataset that covers a wide range of visual variabiliy. The model performs segmentation on individual slices, extracts right-left lung seperately includes airpockets, tumors and effusions. The trachea will not be included in the lung segmentation. https://doi.org/10.1186/s41747-020-00173-2

- U-net(LTRCLobes): This model was trained on a subset of the [LTRC](https://ltrcpublic.com) dataset. The model performs segmentation of individual lung-lobes but yields limited performance when dense pathologies are present or when fissures are not visible at every slice. 

- U-net(LTRCLobes_R231): This will run the R231 and LTRCLobes model and fuse the results. False negatives from LTRCLobes will be filled by R231 predictions and mapped to a neighbor label. False positives from LTRCLobes will be removed. The fusing process is computationally intensive and can, depdending on the data and results, take up to several minutes per volume.

- [U-net(R231CovidWeb)](#COVID-19-Web)

## 论文：

## Referencing and citing
If you use this code or one of the trained models in your work please refer to:

>Hofmanninger, J., Prayer, F., Pan, J. et al. Automatic lung segmentation in routine imaging is primarily a data diversity problem, not a methodology problem. Eur Radiol Exp 4, 50 (2020). https://doi.org/10.1186/s41747-020-00173-2

This paper contains a detailed description of the dataset used, a thorough evaluation of the U-net(R231) model, and a comparison to reference methods.

## Installation
```
pip install git+https://github.com/JoHof/lungmask
```
On Windows, depending on your setup, it may be necessary to install torch beforehand: https://pytorch.org

## Runtime and GPU support
Runtime between CPU-only and GPU supported inference varies greatly. Using the GPU, processing a volume takes only several seconds, using the CPU-only will take several minutes. To make use of the GPU make sure that your torch installation has CUDA support. In case of cuda out of memory errors reduce the batchsize to 1 with the optional argument ```--batchsize 1```

## Usage
### As a command line tool:
```
lungmask INPUT OUTPUT
```
If INPUT points to a file, the file will be processed. If INPUT points to a directory, the directory will be searched for DICOM series. The largest volume found (in terms of number of voxels) will be used to compute the lungmask. OUTPUT is the output filename. All ITK formats are supported.

Choose a model: <br/>
The U-net(R231) will be used as default. However, you can specify an alternative model such as LTRCLobes...

```
lungmask INPUT OUTPUT --modelname LTRCLobes
```

For additional options type:
```
lungmask -h
```

### As a python module:

```
from lungmask import mask
import SimpleITK as sitk

input_image = sitk.ReadImage(INPUT)
segmentation = mask.apply(input_image)  # default model is U-net(R231)
```
input_image has to be a SimpleITK object.

Load an alternative model like so:
```
model = mask.get_model('unet','LTRCLobes')
segmentation = mask.apply(input_image, model)
```

To use the model fusing capability for LTRCLobes_R231 use:
```
segmentation = mask.apply_fused(input_image)
```

