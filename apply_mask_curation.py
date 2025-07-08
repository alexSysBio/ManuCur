import cell_mask_curation as cur
import matplotlib
matplotlib.use("Qt5Agg")

cell_masks_path = 'example_labels.tif'
cur.apply_curation(cell_masks_path,
                  mask_categories= ['incorrect mask', 'cells at edge', 'stitch masks', 'stitch masks at edge'],
                  category_colors = ['black','black','black','black'], save=False)
   