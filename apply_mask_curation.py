import cell_mask_curation as cur
import matplotlib
matplotlib.use("Qt5Agg")

cell_masks_path = '/Volumes/Data_01/Alex Papagiannakis/Microscopy/muNS/LL37/10262021_4umLL37_CJW6723_M9GlyCAAT/10262021_phase_tif/20211026_113318_567_tif/Point0002_ChannelTrans_Seq0008_mask.tif'
cur.apply_curation(cell_masks_path,
                  mask_categories= ['incorrect mask', 'cells at edge', 'stitch masks', 'stitch masks at edge'],
                  category_colors = ['black','black','black','black'], save=False)
   