# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 09:12:35 2020
@author: Ajit Johnson Nirmal
Convert mcmicro output to AnnData object
"""

# Import library
import numpy as np
import anndata as ad
import pandas as pd

def mcmicro_to_scimap (image_path,remove_dna=True,remove_string_from_name=None,
                        log=True,drop_markers=None,random_sample=None, unique_CellId=True,
                        CellId='CellID',split='X_centroid',custom_imageid=None,
                        min_cells=None):
    """

    Parameters
    ----------
    image_path : list
        List of path to the image or images. Each Image should have a unique path supplied.
    remove_dna : bool, optional
        Remove the DNA channels from the final output. Looks for channels with the string 'dna' in it. The default is True.
    remove_string_from_name : string, optional
        Used to celan up channel names. If a string is given, that particular string will be removed from all marker names.
        If multiple images are passed, just use the string that appears in the first image. The default is None.
    log : bool, optional
        Log the data (log1p transformation will be applied). The default is True.
    drop_markers : list, optional
        List of markers to drop from the analysis. e.g. ["CD3D", "CD20"]. The default is None.
    random_sample : int, optional
        Randomly sub-sample the data with the desired number of cells. The default is None.
    CellId : string, optional
        Name of the column that contains the cell ID. The default is CellID.
    unique_CellId: bool, optional
        By default, the function creates a unique name for each cell/row by combining the 
        `CellId` and `imageid`. If you wish not to perform this operation please pass `False`.
        The function will use whatever is under `CellId`. In which case, please be careful to pass unique `CellId`
        especially when loading multiple datasets togeather.  
    split : string, optional
        To split the CSV into counts table and meta data, pass in the name of the column
        that immediately follows the marker quantification. The default is 'X_centroid'.
    custom_imageid: string, optional
        Pass a user defined Image ID. By default the name of the CSV file is used.
    min_cells: int, optional
        If these many cells are not in the image, the image will be dropped.
        Particulary useful when importing multiple images.

    Returns
    -------
    AnnData Object

    Example
    -------
    image_path = ['/Users/aj/whole_sections/PTCL1_450.csv',
                  '/Users/aj/whole_sections/PTCL2_552.csv']
    adata = sm.pp.mcmicro_to_scimap (image_path, drop_markers= ['CD21', 'ACTIN'], random_sample=5000)

    """
    
    # image_path list or string
    if isinstance(image_path, str):
        image_path = [image_path]

    # Import data based on the location provided
    def load_process_data (image):
        # Print the data that is being processed
        print("Loading " + str(image.rsplit('/', 1)[-1]))
        d = pd.read_csv(image)
        # If the data does not have a unique image ID column, add one.
        if 'imageid' not in d.columns:
            if custom_imageid is not None:
                imid = custom_imageid
            else:
                #imid = random.randint(1000000,9999999)
                imid = str(image.rsplit('/', 1)[-1]).replace('.csv','')
            d['imageid'] = imid
        # Unique name for the data
        if unique_CellId is True:
            d.index = d['imageid'].astype(str)+'_'+d[CellId].astype(str)
        else:
            d.index = d[CellId]
        # Drop imageid and cell ID column
        d.drop([CellId], axis=1, inplace=True)
        # Move Image ID to the last column
        cols = d.columns.tolist()
        cols.insert(len(cols), cols.pop(cols.index('imageid')))
        d = d.reindex(columns= cols)
        # If there is INF replace with zero
        d = d.replace([np.inf, -np.inf], 0)
        # Return data
        return d
    # Apply function to all images and create a master dataframe
    r_load_process_data = lambda x: load_process_data(image=x) # Create lamda function
    all_data = list(map(r_load_process_data, list(image_path))) # Apply function

    # Merge all the data into a single large dataframe
    for i in range(len(all_data)):
        all_data[i].columns = all_data[0].columns
    entire_data = pd.concat(all_data, axis=0, sort=False)
    
    # Randomly sample the data
    if random_sample is not None:
        entire_data = entire_data.sample(n=random_sample,replace=False)

    #Remove the images that contain less than a defined threshold of cells (min_cells)
    if min_cells is not None:
        to_drop = entire_data['imageid'].value_counts()[entire_data['imageid'].value_counts() < min_cells].index
        entire_data = entire_data[~entire_data['imageid'].isin(to_drop)]
        print('Removed Images that contained less than '+str(min_cells)+' cells: '+ str(to_drop.values))

    # Split the data into expression data and meta data
    # Step-1 (Find the index of the column with name Area)
    split_idx = entire_data.columns.get_loc(split)
    meta = entire_data.iloc [:,split_idx:]
    # Step-2 (select only the expression values)
    entire_data = entire_data.iloc [:,:split_idx]

    # Rename the columns of the data
    if remove_string_from_name is not None:
        entire_data.columns = entire_data.columns.str.replace(remove_string_from_name, '')

    # Save a copy of the column names in the uns space of ANNDATA
    markers = list(entire_data.columns)

    # Remove DNA channels
    if remove_dna is True:
        entire_data = entire_data.loc[:,~entire_data.columns.str.contains('dna', case=False)]

    # Drop unnecessary markers
    if drop_markers is not None:
        if isinstance(drop_markers, str):
            drop_markers = [drop_markers]
        entire_data = entire_data.drop(columns=drop_markers)

    # Create an anndata object
    adata = ad.AnnData(entire_data)
    adata.obs = meta
    adata.uns['all_markers'] = markers

    # Add log data
    if log is True:
        adata.raw = adata
        adata.X = np.log1p(adata.X)
        
    # Return data
    return adata
