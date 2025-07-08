from skimage import io
import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import matplotlib.cm as cmp
import numpy as np
import pickle
import os


def update_colormap(colormap_name, cell_mask_max):
    base_cmap = cmp.get_cmap(colormap_name)
    colors = base_cmap(np.linspace(0, 1, base_cmap.N))
    new_colors = np.vstack(([1, 1, 1, 1], colors))  # white at index 0
    new_cmap = mcol.ListedColormap(new_colors)
    norm = mcol.BoundaryNorm(boundaries=np.arange(0, cell_mask_max + 2), ncolors=new_cmap.N)
    return new_cmap, norm


def read_image(img_path):
   return io.imread(img_path)


def check_marker_in_region(groups, x,y, radius=5):
   for gid in groups:
      for idx, (mx, my, mrk, txt) in enumerate(groups[gid]):
         if abs(mx-x) <= radius and abs(my-y) <= radius:
            return gid, idx
   else:
      return 'none', 'none'
         

def get_group_dictionaries(cell_groups_list, group_color_list):
   
   groups = {}
   cell_groups_str = {}
   group_colors = {}
   event_keys = []
   for i in range(len(cell_groups_list)):
      groups[i+1] = []
      cell_groups_str[i+1] = cell_groups_list[i]
      group_colors[i+1] = group_color_list[i]
      event_keys.append(str(i+1))
   
   return groups, cell_groups_str, group_colors, event_keys


def curate_masks_gui(cell_masks_path, cell_groups_list, group_color_list, colormap='turbo'):
   
   cell_mask = read_image(cell_masks_path)
   colormap, normcolormap = update_colormap(colormap, np.max(cell_mask.ravel()))
   
   # Store coordinates for each group
   groups, cell_groups_str, group_colors, event_keys = get_group_dictionaries(cell_groups_list, group_color_list)
   current_group = [1]  # Use list for mutability in nested function

   # Click on mask coordinates
   def onclick(event):
      toolbar_mode = plt.get_current_fig_manager().toolbar.mode
      if event.button == 1 and toolbar_mode == '':
         x, y = int(event.xdata), int(event.ydata)
         z = cell_mask[y][x]
         if z > 0:
            print(f"Added point ({x}, {y}) to group {cell_groups_str[current_group[0]]}")
            marker = ax.plot(x, y, 'x', label=f'Group {current_group[0]}', 
                             color = group_colors[current_group[0]])   
            text = ax.text(x+2,y, str(current_group[0]), color = group_colors[current_group[0]], fontsize=15)
            groups[current_group[0]].append((x, y, marker, text))
         plt.draw()

      # Remove marked coordinates and text label
      elif event.button == 3 and toolbar_mode == '':
         x, y = int(event.xdata), int(event.ydata)
         z = cell_mask[y][x]
         if z > 0:
            gid, idx = check_marker_in_region(groups, x,y)
            if gid != 'none':
               _, _, marker, text = groups[gid].pop(idx)
               marker[0].remove()
               text.remove()
               print(f"Removed selection at ({x}, {y}) from group {cell_groups_str[gid]}")
               plt.draw()

   # Choose key event
   def onkey(event):   
      if event.key in event_keys:
         current_group[0] = int(event.key)
         print(f"Switched to group {current_group[0]}:{cell_groups_str[current_group[0]]}")

   # Show image
   fig, ax = plt.subplots()
   ax.imshow(cell_mask, cmap=colormap, norm=normcolormap)
   fig.canvas.mpl_connect('button_press_event', onclick)
   fig.canvas.mpl_connect('key_press_event', onkey)
   plt.title("Click to select points. Press 1, 2, 3 or 4 to change group.")
   plt.show()
   
   return groups


def store_grouped_labels(labels_dict, save_path):
   with open(save_path, 'wb') as handle:
      pickle.dump(labels_dict, handle)


def get_grouped_labels(cell_masks_path, cell_groups_list, grouped_coords, save_path):
   
   cell_masks = read_image(cell_masks_path)
   
   labels_dict = {}
   grouped_labels = []
   
   for gid in grouped_coords:
      labels_dict[cell_groups_list[gid-1]] = []
      for (x, y, _, _) in grouped_coords[gid]:
            cor_label = cell_masks[y][x]
            if cor_label not in labels_dict[cell_groups_list[gid-1]]:
               labels_dict[cell_groups_list[gid-1]].append(cor_label)
      grouped_labels += labels_dict[cell_groups_list[gid-1]]
   
   labels_dict['good labels'] = []
   for lbl in np.unique(cell_masks.ravel()):
      if lbl not in grouped_labels and lbl > 0:
         labels_dict['good labels'].append(lbl)
   
   if os.path.isdir(save_path):
      store_grouped_labels(labels_dict, save_path)
      
   return labels_dict
      


def apply_curation(cell_masks_path,
                  mask_categories= ['incorrect mask', 'cells at edge', 'stitch masks', 'stitch masks at edge'],
                  category_colors = ['red','black','blue','black'], save=False):
   
   grouped_coords = curate_masks_gui(cell_masks_path, mask_categories, category_colors)
   
   if save:
      save_path = cell_masks_path+'/'+'grouped_labels_dict'
   else:
      save_path = 'none'
   
   grouped_labels = get_grouped_labels(cell_masks_path, 
                                          mask_categories,
                                          grouped_coords, save_path)
   return grouped_labels