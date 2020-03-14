from inkml2png import inkml2png
from png2bb import png2bb
from bb_test import bb_test

# Dataset conversion
inkml2png('FCinkML')  # Convert the inkml files in the specified folder to png images; folder must be in the same directory as the inkml2png.py script
inkml2png('NeoSmartpenM1_demo')

# Bounding box pixel coordinates
png2bb('FCinkML', save_bb=True)  # Draw bounding boxes over the previously created png files and saves their pixel coordinates to a text file when done

# Bounding box drawing (test csv file)
bb_test('annotation.txt')
