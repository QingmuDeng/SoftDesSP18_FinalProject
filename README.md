# [Paletteful](http://paletteful.herokuapp.com/)
### Get Inspiration From Your Favorite Images

<span style="color:red">On our website</span>, you can generate color palettes from inputted images using color theory, color quantization, and k means clustering. Our goal is to extract usefulness from your favorite images by providing user-friendly tools, such as downloadable color palettes and image sentiment analysis. We want to make it easier for everyone to be amazing designers and artists. This is the final project for Software Design Spring 2018 at Olin College.

## Authors

* [**Hwei-shin Harriman**](https://github.com/hsharriman)
* [**Cassandra Overney**](https://github.com/coverney)
* [**Enmo Ren**](https://github.com/Enmoren)
* [**Qingmu Deng**](https://github.com/QingmuDeng)

## Getting Started

This program is developed with _Python_ in _Ubuntu 16.4 LTS_. To download the repository as a zip or use the following command in the terminal.
```
git clone https://github.com/QingmuDeng/SoftDesSP18_FinalProject.git
```
Fourteen different Python packages need to be installed to run the full functionality of this repository. The name of the packages can be in [requirement.txt](https://github.com/QingmuDeng/SoftDesSP18_FinalProject/blob/master/requirements.txt). To install all the packages, issue the following command in the terminal for running this program locally:
```
sudo pip3 install -r requirements_local.txt
```

## Usage

### Heroku
To start generating color palettes online, just go to the home page hosted on Heroku by either entering [`http://paletteful.herokuapp.com/`](http://paletteful.herokuapp.com/) in your browser or clicking on the main leaf icon on any of _Paletteful_ pages. At the home page, upload an image of your choice via the “upload” and “submit” buttons. After selecting an image, a new page will load with the generated color palettes. From there you can use the crop tool to generate additional color palettes. More features can be accessed from the toolbar that appears when hovering over the leaf icon. The penguin icon links to this page while the search icon links to the image sentiment analysis feature. However, currently, the image sentiment analysis is separate from the rest of the application and will be integrated in the future. You can also view a video demo of using the website by clicking below.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=YOUTUBE_VIDEO_ID_HERE
" target="_blank"><img src="http://img.youtube.com/vi/YOUTUBE_VIDEO_ID_HERE/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>

### Local 
To run the program locally, first navigate to the repo directory cloned to your local machine and go into the flask_local folder with the command. Type in
```
cd /Path/To/Repo/SoftDesSP18_FinalProject/flask_local
```
Then, enter the following command in the terminal to launch the Flask App. Once the local address of the website shows up in the terminal, open the website in your browser by just clicking the address.
```
python3 app.py
```
![alt text](https://github.com/QingmuDeng/SoftDesSP18_FinalProject/blob/master/assignments/run_local.gif "Run Locally")

To scrape data from Flickr with our `scrape.py`, navitage to the `/vector quantization` folder and run `scrape.py`. The command line option parser is supported and required.
```
cd /Path/To/Repo/SoftDesSP18_FinalProject/vector\ quantization/
python scrape.py
Options:
  -h, --help            show this help message and exit
  -k KEYWORD, --keyword=KEYWORD
                        the keyword based on which you wish to scrape flickr
                        images from.
  -n NUMBER, --number=NUMBER
                        The number of images to scrape. The default value is
                        100 images.
  -p PATH, --path=PATH  The directory to save the images scraped
```
To run the machine learning file in this directory, simply do `python dense.py`. However, to prepare the dataset to run with `dense.py` would require configuring and running `ml_utils.py` where all the necessary functions are already defined in an object-oriented way and free to be tweaked.

To run the machine learning file in `CNN` folder, please do `python cnnImage.py`. Preparing the dataset would require using `resize.py` in the same directory.

## Built With

* [TensorFlow](https://www.tensorflow.org/) - Open Source Machine Learning Library
* [Amazon Web Services](https://aws.amazon.com/) - Cloud Data Storage
* [Boto](https://www.heroku.com/) - Python SDK for AWS
* [Heroku](https://www.heroku.com/) - Web Application Deployment
* [Flask](http://flask.pocoo.org/) - Python Backend Handling

## How to Contribute

1. Fork this repository
2. After navigating to your desire directory in the terminal, type in 
```
git clone https://github.com/USER_NAME/SoftDesSP18_FinalProject.git
```
3. Make a new branch on your local machine using command
```git checkout -b feature-boo```
4. Edit _feature boo_ on your local machine
5. Push the branch you worked on to your Github Fork using 
```git push origin HEAD```
6. Submit a pull request to us on GitHub

One area of suggested improvements would include exporting the trained TensorFlow models and integrating the feature with the web application. You are also welcomed to submit new issues through GitHub to report bugs or provide suggestions.
## Implementation Details

### Color Palette Generation
There are currently three main types of color palettes that Paletteful can generate from a given image. All three types utilize clustering techniques and color theory concepts. The classic color palette finds the dominant colors within an image using a modified median cut algorithm, which repeatedly divides the image colorspace into clusters by using the medians of the clusters as partition points. The dominant/accent color palette type selects the five palette colors by using K means clustering to search for the dominant and accent colors within an image. Three of the five colors are varying shades of the dominant color, while the other two colors are bright accents that pop out in the image. A palette containing dominant and accent colors is often useful when designing eye-catching webpages and presentations. The analogous color palette type consists of colors that lie close to each other on the color wheel. It is generated from various shades of the image’s dominant color that is found using K means clustering. We also experimented with generating a complementary color palette type, which consists of colors that lie opposite each other on the color wheel. To generate this type of color palette, the dominant color of the image is matched with its complement. 
The color theory behind this palette still needs to be refined before publishing it to Paletteful. 

For the dominant/accent and analogous color palettes, finding the dominant colors by K means clustering is an important concept. K means clustering finds K groups within an image’s RGB data. The algorithm works iteratively to assign each data point to one of K groups based on the color values that are provided. The centroids of the K clusters can then be labe

More information regarding modified median cut quantization can be found [here](http://www.leptonica.com/color-quantization.html). To generate the palettes we find the median colors for 11 clusters. The final five colors are determined by taking the four most dominant colors and the most saturated color from the remaining seven. 

### Color Symbolism
To further explore the realm of colors, we decided to look at the colors within a given image and tried to look at how certain colors can be associated with certain sentiments and emotions.

There are two main methods of classification we identified: 1. A Convolutional Neural Network (CNN) that performs convolution, feature extractions of images by sweeping a given set of kernels across an image, and downsampling in all three of the RGB channels. Then, the dimension reduced RGB arrays would be flattened and fed into a dense, or fully-connected/hidden, layer before giving out a final list of activations for each sentiment category. The one with the highest activation would be the program’s classification of the image. 2. A neural network solely composed of dense layers. 16 RGB values have been determined by K Means Clustering over a large number of images at the same time. Those 16 RGB values would then serve as the fixed cluster centers for any images regardless of their color schemes. Provided with an image, by counting how many pixels are the closest to each of the 16 RGB values and dividing the counts by the total number of pixels, we would receive a normalized array of 16 percentages that would be the inputs for the neural network. As before, the category with the highest activation would be the program’s classification.

## License

This project is licensed under the MIT License. Please see the [LICENSE.md](https://github.com/QingmuDeng/SoftDesSP18_FinalProject/blob/master/LICENSE) file for details.

## Acknowledgments
We are appreciative of the inspirtations and resources the following sources provide:
* [HTML5 UP](https://html5up.net/) for HTML templates
* [CodyHouse](https://github.com/CodyHouse/morphing-modal-window) for A call-to-action button that animates and turns into a full-size modal window
* [Paul Kinzett](http://paulkinzett.github.io/toolbar/) for tooltip style toolbars in web applications
* [Allan Bishop](https://github.com/AllanBishop/ImageCropper) for an image cropper for HTML5
* [Vasavi Gajarla and Aditi Gupta](https://www.cc.gatech.edu/~hays/7476/projects/Aditi_Vasavi.pdf) for inspiring the machine learning to classify images based on sentiments
* [Vitaly Bezgachev](https://towardsdatascience.com/how-to-deploy-machine-learning-models-with-tensorflow-part-1-make-your-model-ready-for-serving-776a14ec3198) for the series of blogs on deploying TensorFlow models
* [Shipeng Feng](https://github.com/fengsp/color-thief-py) and [Lokesh Dhakar](https://github.com/lokesh/color-thief) for their ColorThief library. The original algorithm is created by  the [Leptonica Library](http://www.leptonica.com/color-quantization.html)

Last but not least, we would like to thank the Olin College of Engineering Software Design instructors and NINJAS for their help during our project. Special thanks to [Paul Ruvolo](https://github.com/paulruvolo) for providing tremendous computing powers to our machine learning endeavors and [Vicky McDermott](https://github.com/vickymmcd) for the support through the difficult web application process.

## Software Design Course Deliverables
##### The Initial Proposal can be found [here](https://github.com/QingmuDeng/SoftDesSP18_FinalProject/blob/master/assignments/Initial%20Proposal.md).
##### The Architectural Review Preparation Document can be found [here](https://github.com/QingmuDeng/SoftDesSP18_FinalProject/blob/master/assignments/AR%20Preparation%20and%20Framing.md).
##### The Architectural Review Reflection Document can be found [here](https://github.com/QingmuDeng/SoftDesSP18_FinalProject/blob/master/assignments/AR%20Reflection.md).
##### The Architectural Review 2 Preparation Document can be found [here](https://github.com/QingmuDeng/SoftDesSP18_FinalProject/blob/master/assignments/AR2%20Preparation%20and%20Framing.md).
##### The Architectural Review 2 Reflection Document can be found [here](https://github.com/QingmuDeng/SoftDesSP18_FinalProject/blob/master/assignments/AR2%20Reflection.md).
##### Our system architectural diagram can be viewed [here](https://github.com/QingmuDeng/SoftDesSP18_FinalProject/blob/master/assignments/System%20architecture%20diagram.jpg).
##### Our system architectural diagram can be viewed [here](https://github.com/QingmuDeng/SoftDesSP18_FinalProject/blob/master/assignments/poster.pdf).
