
import cv2
import numpy as np

class Denoiser:

    @staticmethod
    def gaussian(image:np.ndarray, ksize:int=5)->np.ndarray:
        return cv2.GaussianBlur(image,(ksize,ksize),0)

    @staticmethod
    def median(image:np.ndarray, ksize:int=5)->np.ndarray:
        return cv2.medianBlur(image,ksize)

    @staticmethod
    def bilateral(image:np.ndarray,d:int=9,sigma_color:int=75,sigma_space:int=75)->np.ndarray:
        return cv2.bilateralFilter(image,d,sigma_color,sigma_space)

    @staticmethod
    def nl_means(image:np.ndarray)->np.ndarray:
        if image.ndim==2:
            return cv2.fastNlMeansDenoising(image)
        return cv2.fastNlMeansDenoisingColored(image)

    @staticmethod
    def apply(image:np.ndarray, method:str="bilateral")->np.ndarray:
        method=method.lower()
        if method=="gaussian":
            return Denoiser.gaussian(image)
        if method=="median":
            return Denoiser.median(image)
        if method=="nlmeans":
            return Denoiser.nl_means(image)
        return Denoiser.bilateral(image)
