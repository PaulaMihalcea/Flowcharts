from inkml2png import inkml2png
from png2bb import png2bb
from bb_test import bb_test
from divide_annotations import divide_annotations
from divide_dataset import divide_dataset
from crop import crop

# Dataset conversion
inkml2png('FCinkML')  # Convert the inkml files in the specified folder to png images; folder must be in the same directory as the inkml2png.py script
inkml2png('NeoSmartpenM1_demo')

# Bounding box pixel coordinates
png2bb('FCinkML', save_bb=True)  # Draw bounding boxes over the previously created png files and saves their pixel coordinates to a text file when done

# Bounding box drawing (test csv file)
bb_test('./FCinkML_png/', 'annotation.txt', 'bb_test')

# Train and test annotations generation from the file list in the original dataset
divide_annotations('annotation.csv', './FCinkML/listInkML_Train.txt', './FCinkML/listInkML_Test.txt')

# Dataset
divide_dataset('./FCinkML_png', './FCinkML/listInkML_Train.txt', './FCinkML/listInkML_Test.txt')

# Create cropped images (data augmentation)
crop('FCinkML_png')
