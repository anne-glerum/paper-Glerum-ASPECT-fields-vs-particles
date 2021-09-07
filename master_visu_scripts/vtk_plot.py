"""
Functions for plotting data from VTU/PVTU files.
"""
import os
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv
from tqdm import tqdm
from cmcrameri import cm

def plot(file,field,bounds,ax=None,contours=False,
         cfields=['crust_upper','crust_lower','mantle_lithosphere'],
         null_field='asthenosphere',plot_scalar_bar=True,**kwargs):
    """
    Plot 2D ASPECT results using Pyvista.

    Parameters
    ----------
    file : VTU or PVTU file to plot
    field : Field to use for color.
    bounds : Bounds by which to clip the plot.
    ax: Matplotlib axes on which to plot results. The default is None.
    contours : Boolean for whether to add temperature contours. 
        The default is False.
    cfields : Names of compositional fields to use if field is 'comp_field.' 
        The default is ['crust_upper','crust_lower','mantle_lithosphere'].
    null_field : Null field if field is 'comp_field.'
        The default is 'asthenosphere'.

    Returns
    -------
    ax: Matplotlib axes with results plotted.

    """
    
    mesh = pv.read(file)
    
    km2m = 1000
    bounds_m = [bound*km2m for bound in bounds] # Convert bounds to m
    bounds_3D = bounds_m + [0,0]
    mesh = mesh.clip_box(bounds=bounds_3D,invert=False)
    
    if field=='comp_field':
        mesh = comp_field_vtk(mesh,fields=cfields,null_field=null_field)
    
    if contours==True:
        cntrs = add_contours(mesh)
    
    # Format text 
    pv.set_plot_theme("document")
    pv.global_theme.font.family = 'arial'
    pv.global_theme.font.size = 12
    pv.global_theme.font.title_size = 14
    pv.global_theme.font.label_size = 10
    pv.global_theme.font.fmt = '%1.2-e'

    # Format color bar
    pv.global_theme.colorbar_horizontal.height = 0.2
    pv.global_theme.colorbar_horizontal.position_x = 0.21
    pv.global_theme.colorbar_horizontal.position_y = 0.01

    color_bar_args = dict(
        title_font_size=12,
        label_font_size=10,
        shadow=False,
        n_labels=3,
        italic=False,
        fmt="%1.1e",
        font_family="arial",
    )

    plotter = pv.Plotter(off_screen=True)

    # Select color map and color bar title for each field.
    # Also set the min/max limits for the color bar, change as needed.
    #TODO write powers as superscript as required by Solid Earth
    if field=='ve_stress_xx':
        #TODO convert to MPa and write symbol sigma
        clim = [0, 250e6]
        color_map = cm.batlow_r
        color_bar_args["title"] = "sigma_xx [Pa]"
    elif field=='ve_stress_xy':
        clim = [0, 250e6]
        color_map = cm.batlow_r
        color_bar_args["title"] = "sigma_xy [Pa]"
    elif field=='ve_stress_yy':
        clim = [0, 250e6]
        color_map = cm.batlow_r
        color_bar_args["title"] = "sigma_yy [Pa]"
    elif field=='density':
        clim = [2500, 3500]
        color_map = cm.devon_r
        color_bar_args["title"] = "Density [kg/m3]"
    elif field=='T':
        clim = [273, 1873]
        color_map = cm.lajolla
        color_bar_args["title"] = "Temperature [K]"
    elif field=='viscosity':
        clim = [1e19, 1e25]
        color_map = cm.bilbao
        color_bar_args["title"] = "Viscosity [Pa s]"
    elif field=='p':
        clim = [0, 2e9]
        color_map = cm.imola_r
        color_bar_args["title"] = "Pressure [Pa]"
    elif field=='strain_rate':
        clim = [1e-20, 1e-14]
        color_map = cm.grayC
        color_bar_args["title"] = "Strain rate [1/s]"
    elif field=='velocity':
        clim = [0, 0.1]
        color_map = cm.davos_r
        color_bar_args["title"] = "Velocity magnitude [m/yr]"
    #TODO how to specify a component of the velocity?
    #elif field=='velocity_x':
    #    clim = [0, 0.1]
    #    color_map = cm.cork
    #    color_bar_args["title"] = "X-velocity [m/yr]"
    else:
        print("This field variable is not recognized")

    plotter.add_mesh(mesh,scalars=field,clim=clim,scalar_bar_args=color_bar_args,cmap=color_map,**kwargs)

    # Whether or not to plot the color bar in each subplot.
    #TODO plot bar only in one subplot.
    if plot_scalar_bar == False:
        plotter.remove_scalar_bar()
    
    # Plot temperature contours
    if contours == True:
        plotter.add_mesh(cntrs,color='black',line_width=5)
    
    plotter.view_xy()
    
    # Calculate Camera Position from Bounds
    bounds_array = np.array(bounds_m)
    xmag = float(abs(bounds_array[1] - bounds_array[0]))
    ymag = float(abs(bounds_array[3] - bounds_array[2]))
    aspect_ratio = ymag/xmag
    
    plotter.window_size = (1024,int(1024*aspect_ratio))
    
    xmid = xmag/2 + bounds_array[0] # X midpoint
    ymid = ymag/2 + bounds_array[2] # Y midpoint
    zoom = xmag*aspect_ratio*1.875 # Zoom level - not sure why 1.875 works

    position = (xmid,ymid,zoom)
    focal_point = (xmid,ymid,0)
    viewup = (0,1,0)
    
    camera = [position,focal_point,viewup]
    
    plotter.camera_position = camera
    plotter.camera_set = True
    
    # Create image
    img = plotter.screenshot(transparent_background=True,
                             return_img=True)
    
    # Plot using imshow
    if ax is None:
        ax = plt.gca()
    
    ax.imshow(img,aspect='equal',extent=bounds)
    
    return(ax)


def add_contours(mesh,field='T',values=np.arange(500,1700,200)):
    """
    Add contours to mesh in Pyvista.

    Parameters
    ----------
    mesh : Pyvista mesh object.
    field : Scalar in Pyvista mesh object to use for contours. The default is
        T.
    values : Values for the contours. The default is np.arange(500,1700,200).

    Returns
    -------
    cntrs: Pyvista mesh containing the contours.

    """
    contour_mesh = mesh.copy()
    cntrs = contour_mesh.contour(isosurfaces=values,scalars=field)
    return(cntrs)
    

def comp_field_vtk(mesh,fields=['crust_upper','crust_lower','mantle_lithosphere'],
               null_field='asthenosphere'):
    """
    Calculate compositional field from Pyvista VTK mesh.
    
    Uses input fields to assign value based on when fields are >0.9. Any point
    lacking a field >0.9 is assigned to the null field.

    Parameters
    ----------
    mesh : Pyvista mesh
    fields : Names of compositional fields that are scalars in the mesh.
        The default is ['crust_upper','crust_lower','mantle_lithosphere'].
    null_field : Name of field for points not included in compositional fields.
        The default is 'asthenosphere'.

    Returns
    -------
    mesh: Pyvista mesh with 'comp_field' added as a scalar.
    
    """

    # Create empty np array
    output = np.zeros(shape=mesh.point_arrays[fields[0]].shape)
    for x in range(len(fields)):
        array = mesh.point_arrays[fields[x]]
        output = np.where(array>0.5,x+1,output)
    
    mesh.point_arrays['comp_field'] = output
    return(mesh)


def particle_trace(meshes,timesteps,point,y_field,x_field='time',
                   bounds=None,plot_path=False):
    """
    Get single particle path over multiple timesteps from meshes generated
    by load_particle_meshes.
    
    By default, gets values for a single field over time. Can specify a 
    second field (x_field) to plot two parameters over time.
    
    Parameters
    ----------
    meshes: MultiBlock object from laod_particle_meshes function
    timesteps: NumPy array of timesteps to pull
    point: ID of particle to trace
    y_field: Particle property for y-axis
    x_field: Particle property for x-axis.
    bounds: List of bounds to clip model [xmin,xmax,ymin,ymax,zmin,zmax].
        Note that 0 indicates bottom
    plot_path: Whether to plot the x-field and y-field
    
    Returns
    -------
    point_df: Pandas dataframe with timesteps, y-field, and x-field if
        applicable.
    """
    
    x_point = []
    y_point = []
    
    # Get first and last values of timesteps
    first = timesteps[0]
    last = timesteps[-1]
    
    # Loop over files
    
    for mesh in meshes[first:last+1]:
        
        # Clip mesh if needed
        if bounds is not None:
            mesh = mesh.clip_box(bounds=bounds,invert=False)
        
        ids = pv.point_array(mesh,'id') # Get particle ids
        y_vals = pv.point_array(mesh,y_field) # Get y field values
        
        if y_field=='position': # If y array is 3D position
            x_vals = y_vals[:,0] # Get x coordinates
            y_vals = y_vals[:,1] # Get y coordinates

            # Rename fields if plotting 2D position
            if (x_field == 'position') & (y_field == 'position'):
                x_field = 'x'
                y_field = 'y' 
                df = pd.DataFrame(
                {x_field:x_vals,y_field:y_vals},index=ids.astype(int))
        
        # Get x field values if not plotting timesteps or 2D position
        elif x_field!='time':
            x_vals = pv.point_array(mesh,x_field)
            df = pd.DataFrame(
                {x_field:x_vals,y_field:y_vals},index=ids.astype(int))
        else:
            df = pd.DataFrame({y_field:y_vals},index=ids.astype(int))
        
        # Extract values for specific points and add to lists
        point_vals = df.loc[point,:]
        y = point_vals[y_field]
        if x_field!='time':
            x = point_vals[x_field]
            x_point.append(x)
        y_point.append(y)
        
        # Reset position fields if needed
        if (x_field == 'x') & (y_field == 'y'):
            x_field = 'position'
            y_field = 'position' 

    
    # Convert lists to dataframe
            
    # Rename fields if plotting 2D position
    if (x_field == 'position') & (y_field == 'position'):
        x_field = 'x'
        y_field = 'y'
    
    if x_field!='time':
        point_df = pd.DataFrame({x_field:x_point,y_field:y_point},index=timesteps)
    else:
        point_df = pd.DataFrame({y_field:y_point},index=timesteps)
   
       
    if plot_path is True:  
        if x_field!='time':
            point_df.plot(x_field,y_field)
            plt.xlabel(x_field)
            
            # Label timesteps
            for n in point_df.index:
                plt.text(x=point_df.loc[n,x_field],y=point_df.loc[n,y_field],
                     s=str(n))
        else:
            plt.plot(point_df.index,point_df[y_field])
            plt.xlabel('Timestep')
        plt.ylabel(y_field)
        plt.annotate('ID: '+str(point),xy=(0.1,0.9),xycoords='axes fraction')
        
        
    return(point_df)

def get_pvtu(directory,timesteps,kind='solution'):
    """
    Get list of .pvtu files from directory and timesteps.
    
    Assumes files are named according to ASPECT output conventions and in a
    single directory. Can be used for standard solution or particle naming
    schemes.
    
    Parameters
    ----------
    directory: Path to directory contaning ASPECT pvtu files.
    timesteps: Integer or NumPy array of timesteps to pull
    kind: Whether to pull standard solution or particles.
    
    Returns
    -------
    files: List of file paths
    """    
    # Set up directory building blocks
    main = directory
    if kind=='solution':
        prefix = 'solution-00'
    if kind == 'particles':
        prefix = 'particles-00'
    suffix = '.pvtu'
    
    # Get file paths for all timesteps
    if type(timesteps)==int:
        timesteps_str = str(timesteps).zfill(3)
        files = os.path.join(main,prefix+timesteps_str+suffix)
    else:
        timesteps_str = [str(x).zfill(3) for x in timesteps.tolist()]
        files = [os.path.join(main,prefix+x+suffix) for x in timesteps_str]
    

    return(files)

def particle_positions(meshes,timestep,bounds=None):
    """
    Get ids and positions of all particles in a particular timestep.
    
    Parameters
    ----------
    meshes: MultiBlock object from load_particle_meshes
    timestep: Timestep from which to pull positions.
    
    Returns
    -------
    ids: NumPy array of particle ids
    positions: NumPy array of particle positions (X,Y,Z)
    """

    mesh = meshes[timestep]
    
    if bounds is not None:
        mesh = mesh.clip_box(bounds=bounds,invert=False)
    
    ids = pv.point_array(mesh,'id')
    positions = pv.point_array(mesh,'position')
    return(ids,positions)

def load_particle_meshes(directory,timesteps,filename='meshes.vtm',bounds=None):
    """
    Load particle meshes, clip, and save to avoid duplicate computation. This is
    computationally intensive for large meshes and may be preferred to do on 
    Stampede2.
    
    Parameters
    ----------
    directory: Path to directory contaning ASPECT pvtu files.
    timesteps: Integer or NumPy array of timesteps to pull.
    filename: Name of file to save clipped meshes to.
    bounds: Bounds by which to clip the model box
    
    Returns
    -------
    meshes: MultiBlock object of clipped meshes for each timestep.
    """
    
    # Set timer for computation
    startTime = datetime.now()
    
    # Set up directory building blocks
    files=get_pvtu(directory,timesteps,kind='particles')
    
    # Setup multiblock
    meshes = pv.MultiBlock()
    
    for file in tqdm(files):
        mesh = pv.read(file) # Major computation to load this.
    
        # Clip mesh to save space
        if bounds is not None:
            mesh = mesh.clip_box(bounds=bounds,invert=False)
        
        meshes.append(mesh)
        
    # Save clipped meshes as smaller file to work with
    meshes.save(filename)
    
    # Print computation time
    print(datetime.now()-startTime)
    
    return(meshes)
        
        
        
