# ManuCure
A Python library which uses the PyQt5 framework to provide a graphical and interactive interface for the manual curation of cell labels.

The manual curation functions are included in the cell_mask_curation.py script and applied in the apply_mask_curation.py script, using the matplotlib "Qt5Agg" backend.
The apply_curation function takes 4 variables:
  1. cell_masks_path (str): the path to the cell labels image (usually a .tif or .png file)
  2. mask_categories (list): a list which includes all the curation categories as strings
  3. category colors (list): a list which includes color of each label category. The index of each color should match that of the curation category in the mask_categories variable.
  4. save (bool): choose True to save a dictionary with the manually grouped cell labels in the same folder as the masked cell labels (cell_masks_path).
The cell labels that were not manually selected are grouped as "good_labels".

## User's manual
  1. To switch between categories use the keyoard keys 1, 2, 3, 4 etc, each corresponding to the first, second, third, fourth etc items in the mask_categories list.
  2. To manually apply a selected category to a cell label, left-click on the cell label.
  3. To remove an applied category, right-click around the category marker (usually shown as a cross). A radius of 5 pixels around the cross is considered.
  4. The user may use the toolbar on top of the GUI to zoom in, or return to the home view. However, before changing categories or clicking on cells, the user must ensure that the toolbar items are not selected.
  5. To finish the manual curation simply close the GUI window. 

![](https://github.com/alexSysBio/ManuCur/blob/main/example_movie.mp4)
