from inkml2png import inkml2png
from png2bb import png2bb

# Dataset conversion
#inkml2png('FCinkML')  # Converts the inkml files in the specified folder to png images; folder must be in the same directory as the inkml2png.py script
#inkml2png('NeoSmartpenM1_demo')

# Bounding box drawing
png2bb('FCinkML', save_bb=True)
