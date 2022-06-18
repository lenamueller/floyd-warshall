import imageio

filenames = []
for i in range(22):
    a = str(i+1).zfill(3)
    filenames.append(f"images/{a}.png")
    
with imageio.get_writer('gifs/floyd-warshall-algorithm4.gif', mode='I', duration=0.5) as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)