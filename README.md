# [Paletteful](http://paletteful.herokuapp.com/)
### Get Creativity From Your Favorite Images

<span style="color:red">On our website</span>, you can generate color palettes from inputted images using color theory, color quantization, and k means clustering. Our goal is to extract usefulness from your favorite images by providing user-friendly tools, such as downloadable color palettes and image sentiment analysis. We want to make it easier for everyone to be amazing designers and artists. This is the final project for Software Design Spring 2018 at Olin College.

## Authors

* [**Hwei-shin Harriman**](https://github.com/hsharriman)
* [**Cassandra Overney**](https://github.com/coverney)
* [**Enmo Ren**](https://github.com/Enmoren)
* [**Qingmu Deng**](https://github.com/QingmuDeng)

## Getting Started

This program is developed with _Python_ in _Ubuntu 16.4 LTS_. To download the repository as a zip or use the following command in the terminal.
```
git clone https://github.com/USER_NAME/SoftDesSP18_FinalProject.git
```
Fourteen different Python packages need to be installed to run the full functionality of this repository. The name of the packages can be in [requirement.txt](https://github.com/QingmuDeng/SoftDesSP18_FinalProject/blob/master/requirements.txt). To install all the packages, issue the following command in the terminal:
```
sudo pip3 install -r requirements.txt
```
While we exclude OpenCV from the requirements list since it would cause build problems on Heroku, OpenCV is also needed in some of the machine learning scirpts not deployed to Heroku. To install OpenCV, use the following command in the terminal:
```
sudo pip3 install python-opencv
```

## Usage

### Heroku

### Local


## Built With

* [TensorFlow](https://www.tensorflow.org/) - Open Source Machine Learning Library
* [Amazon Web Services](https://aws.amazon.com/) - Cloud Data Storage
* [Boto](https://www.heroku.com/) - Python SDK for AWS
* [Heroku](https://www.heroku.com/) - Web Application Deployment
* [Flask](http://flask.pocoo.org/) - Python Backend Handling

## How to Contribute

1. Fork this repository
2. After navigating to your desire directory in the terminal, type in `git clone https://github.com/USER_NAME/SoftDesSP18_FinalProject.git`

## Implementation Details

### Color Palette Generation
There are currently three main types of color palettes that Paletteful can generate from a given image. All three types utilize K means clustering and color theory concepts. The default color palette type selects the five palette colors by searching for the dominant and accent colors within an image. Three of the five colors are varying shades of the dominant color, while the other two colors are accents that pop out in the image. A palette containing dominant and accent colors is often useful when designing eye-catching webpages and presentations. The complementary color palette type consists of colors that lie opposite each other on the color wheel. To generate this type of color palette, the dominant color of the image is matched with its complement. Complementary palettes offer a sense of balance. The analogous color palette type consists of colors that lie close to each other on the color wheel. It is generated from various shades of the image’s dominant color.

### Color Symbolism
To further explore the realm of colors, we decided to look at the colors within a given image and tried to look at how certain colors can be associated with certain sentiments and emotions.

There are two main methods of classification we identified: 1. A Convolutional Neural Network (CNN) that performs convolution, feature extractions of images by sweeping a given set of kernels across an image, and downsampling in all three of the RGB channels. Then, the greatly dimension reduced RGB arrays would be flattened and fed into a dense, or fully-connected/hidden, layer before giving out a final list of activations for each sentiment category. The one with the highest activation would be the program’s classification of the image. 2. A neural network solely composed of dense layers. 16 RGB values has been determined by K Means Clustering over a large number of images at the same time. Those 16 RGB values would then serve as the fixed cluster centers for any images regardless of their color schemes. Provided with an images, by counting how many pixels are the closest to each of the 16 RGB values and dividing the counts by the total number of pixels, we would receive a normalized array of  16 percentages that would be the inputs for the neural network. As before, the category with the highest activation in the end would be the program’s classification.


## License

This project is licensed under the MIT License。 Please see the [LICENSE.md](https://github.com/QingmuDeng/SoftDesSP18_FinalProject/blob/master/LICENSE) file for details.

## Acknowledgments
We are appreciative of the inspirtations and resources the following sources provide:
* [HTML5 UP](https://html5up.net/) for HTML templates
* [CodyHouse](https://github.com/CodyHouse/morphing-modal-window) for A call-to-action button that animates and turns into a full-size modal window
* [Paul Kinzett](http://paulkinzett.github.io/toolbar/) for tooltip style toolbars in web applications
* [Allan Bishop](https://github.com/AllanBishop/ImageCropper) for an image cropper for HTML5
* [Vasavi Gajarla and Aditi Gupta](https://www.cc.gatech.edu/~hays/7476/projects/Aditi_Vasavi.pdf) for inspiring the machine learning to classify images based on sentiments
* [Vitaly Bezgachev](https://towardsdatascience.com/how-to-deploy-machine-learning-models-with-tensorflow-part-1-make-your-model-ready-for-serving-776a14ec3198) for the series of blogs on deploying TensorFlow models
* []() 

## Software Design Course Deliverables
##### The Initial Proposal can be found [here](https://github.com/QingmuDeng/SoftDesSP18_FinalProject/blob/master/assignments/Initial%20Proposal.md).
##### The Architectural Review Preparation Document can be found [here](https://github.com/QingmuDeng/SoftDesSP18_FinalProject/blob/master/assignments/AR%20Preparation%20and%20Framing.md).
##### The Architectural Review Reflection Document can be found [here](https://github.com/QingmuDeng/SoftDesSP18_FinalProject/blob/master/assignments/AR%20Reflection.md).
