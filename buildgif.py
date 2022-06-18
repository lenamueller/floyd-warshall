import imageio


# Build GIF.
filenames = ["images/001.png","images/002.png","images/003.png","images/004.png",
             "images/005.png","images/006.png","images/007.png","images/008.png",
             "images/009.png","images/010.png"]

with imageio.get_writer('floyd-warshall-algorithm.gif', mode='I', duration=1) as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)