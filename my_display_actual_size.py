# Mustafa Ghanim S021848 Department of Electrical-Electronics Engineering 

from matplotlib import pyplot as plt


def my_display_actual_size(img, str_caption = 'Image with Actual Size'):

    height= img.shape[0]
    width = img.shape[1]

    # determine a figure size big enough to accomodate an axis of xpixels by ypixels
    # as well as the ticklabels, etc.
    margin = 0.05
    dpi = 80
    figsize = (1.0+margin)*height/dpi, (1.0+margin)*width/dpi

    # define the figure
    fig = plt.figure(figsize=figsize, dpi=dpi)
    
    # make the axis the right size
    ax = fig.add_axes([margin, margin, 1 - 2*margin, 1 - 2*margin])

    # dipalya the image
    ax.imshow(img, cmap='gray', vmin=0, vmax=255, interpolation='none')
    plt.title(str_caption)
    plt.show()
    
    return