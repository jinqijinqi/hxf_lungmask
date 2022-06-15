from lungmask import mask
from lungmask import utils
import SimpleITK as sitk


# INPUT = "./data/1.IMA"
# input_image = sitk.ReadImage(INPUT) # 读一个图

INPUT = "./data/"
input_image = utils.get_input_image(INPUT)# 读一个序列
model = mask.get_model('unet','LTRCLobes')
segmentation = mask.apply(input_image, model)
segmentation = mask.apply_fused(input_image)
out = sitk.GetImageFromArray(segmentation)
sitk.WriteImage(out, "./result/3.nii")







