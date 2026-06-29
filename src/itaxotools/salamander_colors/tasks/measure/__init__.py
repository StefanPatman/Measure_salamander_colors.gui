from itaxotools.salamander_colors.resources import task_pixmaps_large, task_pixmaps_medium

title = "Measure Colors"
description = "Measure black and yellow pixel proportions"

pixmap = task_pixmaps_large.measure
pixmap_medium = task_pixmaps_medium.measure

long_description = (
    "Measure the proportion of black and yellow pixels in a folder of salamander images. "
    "Each image is analyzed pixel by pixel and classified as background, black, yellow, or other. "
    "Results are written to a tab-delimited text file."
)
