# ABF-Verwerking
A collection of automation scripts made for a Job I currently work at.

The scripts are given a UI with PyQt to make them a little more user friendly.

There are 3 main ones.

## Klasfotos:
Klasfotos, or in english Class Pitcrures. This program makes a collage image, for each image in each subdirectory in a given directory. It automatically decides the number of rows and columns needed to make each image the maximum size it can be, taking into account a constant x pad and y pad. The images (for the purpouse of the job I work at) are always in the same aspect ratio, so this was hard coded in. The collage is made on top of a template/background provided to the program. The area on the background/template that the images will be placed on is also hard coded. These two things could be made more dynamic but I saw no real reason to do this. The use of these scripts are therefore very limited outside of the scope of my job.

## Raam:
Raam is pretty simple. It takes in a png that will be pasted onto an image. A raam in english is a frame. So the consept is pretty self explanitory. The scirpt takes in as input a directory, and produces as output, another direcotry with the same structure as the original, where each jpg it encounters is framed with the process discribed. This script is straight forward deu to the fact that each image that needs to be framed is in the same aspect ratio.

One major oversight of this script is also just that. The framing process has a resizing step. So this means that when you give it an image that is not in the aspect ratio it expects it will resize that image into the constant aspect ratio of all other images, morphing it. For the most part we mitigate this by deleting those images and framing them with the old manual process we had in place before the script was in use.

## Dropbox
This does the same duplicating file structure thing as the Raam script. The only processing done on the images is compression. This makes the images smaller and easier to upload to dropbox. These programs are used by our photographers while they are far away form the office and the framed images are needed to make order forms. They use dropbox to upload these images to the cloud so we at the office can use them.
