import os
import flickrapi
import urllib.request
from optparse import OptionParser

api_key = u'e81d38aba305d753bc9bb3daaa3e1375'
api_secret = u'699112c310b707df'
page = 1


def init_opts():
    """
    This function runs the different modes of our program with input in the
    command line
    """
    parser = OptionParser()
    parser.add_option("-k", '--keyword', action="store",
                      dest="keyword", help="the keyword based on which you wish to scrape flickr images from.")
    parser.add_option("-n", '--number', action="store",
                      dest="number", default=100,
                      help="The number of images to scrape. The default value is 100 images.")
    parser.add_option("-p", '--path', action="store",
                      dest="path", default='datset/',
                      help="The directory to save the image scraped")
    options, args = parser.parse_args()
    return options, args


def user_input():
    """Asks user for keyword and number of photos and return them"""
    keyword = input('What photos are you searching for: ')
    number = input('How many photos do you want to scrape: ')
    return keyword, int(number)


def save_photo(flickr, photos, file_path):
    """this functions tries to save images from Flickr in their largest sizes
    by casading a series of try-and-except starting with the largest possible
    image size. If a image is smaller than Flickr's mediu resolution,
    it will be skipped.

    :param flickr: the initiate flickrapi object
    :param photos: the object created by flickr.photos.search() method
    :param file_path: the object created by flickr.photos.search() method
    """
    for photo in photos[0]:
        photo_id = photo.get('id')
        try:
            photo_src = flickr.photos.getSizes(photo_id=photo_id)[0][10].get('source')
        except:
            try:
                photo_src = flickr.photos.getSizes(photo_id=photo_id)[0][9].get('source')
            except:
                try:
                    photo_src = flickr.photos.getSizes(photo_id=photo_id)[0][8].get('source')
                except:
                    try:
                        photo_src = flickr.photos.getSizes(photo_id=photo_id)[0][7].get('source')
                    except:
                        try:
                            photo_src = flickr.photos.getSizes(photo_id=photo_id)[0][6].get('source')
                        except:
                            try:
                                photo_src = flickr.photos.getSizes(photo_id=photo_id)[0][5].get('source')
                            except:
                                print('this image is too small')
        try:
            urllib.request.urlretrieve(photo_src, file_path+str(photo_id)+".jpg")
        except:
            print('HTTPError')


def main():
    global page
    # Initiate the command line parser
    options, args = init_opts()
    # Initiate the Flickrapi
    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    number = int(options.number)

    # Check whether the desired file path exists; if not, create it
    file_path = options.path+str(options.keyword)+"/"
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Keep downloading images from flickr until desired number of photos are reached
    while number > 500:
        photos = flickr.photos.search(text=keyword, per_page=500, sort='relevance', page=page)
        save_photo(flickr, photos, file_path)
        number -= 500
        page += 1
    photos = flickr.photos.search(text=keyword, per_page=number, sort='relevance', page=page)
    save_photo(flickr, photos, file_path)


if __name__ == "__main__":
    main()
