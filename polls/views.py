from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseNotAllowed
import numpy as np
import dicom2nifti
import nibabel as nib
import nilearn as nil
import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
import os
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def _mock(request):
    print("Running the mock routine.")
    file_location = f'imaging/output_pancreas_095_{np.random.randint(0, 100)}.png'
    try:
        file_data = None
        print(file_location)
        with open(file_location, 'rb') as f:
           file_data = f.read()
        print(file_data)

        # sending response 
        response = HttpResponse(file_data, content_type='application/image/png')

    except IOError as e:
        # handle file not exist case here
        response = HttpResponseNotFound('<h1>File not exist</h1>')

    return response

@csrf_exempt
def _nifti(request):
    # Preparation
    print("Running the nifty routine.")
    DIR = "imaging/niicube"
    INAME = "48542_aligned_ct_-_test1.nii.gz"
    TNAME = "foo.png"
    LLNAME = "{0:s}/{1:s}".format(DIR, TNAME)
    
    # Load phase
    pancreas_in, pancreas_in_data = None, None
    if len(request.body) == 2:
        print("Resorting to random nifty.")
        try:
            pancreas_in = nib.load("{0:s}/{1:s}".format(DIR, INAME))
            pancreas_in_data = pancreas_in.get_fdata()
        except FileNotFoundError as e:
            return HttpResponseNotFound('<h1>Nifty file not exist</h1>')
        except Exception as e:
            return HttpResponseNotFound('<h1>Game over</h1>')
    else:
        print("Processing sent file.")
        DIR = "imaging"
        INAME = "omg.png"
        LLNAME = "zomfg.png"
        g = open("{0:s}/omg.nii.gz".format(DIR), 'wb')
        h = request.body
        print(h)
        g.write(h)
        g.close()
        try:
            pancreas_in = nib.load("{0:s}/{1:s}".format(DIR, "omg.nii.gz"))
            pancreas_in_data = pancreas_in.get_fdata()
        except FileNotFoundError as e:
            return HttpResponseBadRequest('<h1>Nifty file failed to process</h1>')
        except Exception as e:
            print(e)
            return HttpResponseNotAllowed('<h1>Game over</h1>')
        
    print(f"Input: {pancreas_in.get_fdata().shape}")
    print(pancreas_in.header)
    
    # Show phase
    fig_rows = 4
    fig_cols = 4
    n_subplots = fig_rows * fig_cols
    n_slice = pancreas_in_data.shape[2]
    step_size = n_slice // n_subplots
    plot_range = n_subplots * step_size
    start_stop = int((n_slice - plot_range) / 2)

    fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[10, 10])

    for idx, img in enumerate(range(start_stop, plot_range, step_size)):
        print(f"Slice: {img}")
        axs.flat[idx].imshow(pancreas_in_data[:, :, img])
        axs.flat[idx].axis('off')
            
    plt.tight_layout()
    plt.savefig(f"imaging/{INAME}_{idx}.png")
    plt.savefig(LLNAME)

    # # Long phase
    # fig_rows = 1
    # fig_cols = 1
    # n_slice = pancreas_in_data.shape[2]
    # fig, axs = plt.subplots(1, 1, figsize=[10, 10])
    # cube = []

    # for idx, img in enumerate(range(0, n_slice, 1)):
    #     print(f"@@ {idx} @@")
    #     print(pancreas_in_data[:, :, img])
    #     axs.imshow(pancreas_in_data[:, :, img], cmap='gray')
    #     plt.tight_layout()
    #     SLICENAME = f"imaging/{INAME}_{idx}.png"
    #     cube.append(SLICENAME)
    #     plt.savefig(f"imaging/{INAME}_{idx}.png")

    # concatenated = Image.fromarray(
    # np.concatenate(
    #     [np.array(Image.open(x).resize((96,96))) for x in cube],
    #     axis=1
    # )
    # ).save(LLNAME)

    # Return phase
    try:
        file_data = None
        print(LLNAME)
        with open(LLNAME, 'rb') as f:
           file_data = f.read()
        print(file_data)

        # sending response 
        response = HttpResponse(file_data, content_type='application/image/png')
        response['Content-Disposition'] = 'attachment; filename="foobar.png"'

    except IOError as e:
        # handle file not exist case here
        response = HttpResponseNotFound('<h1>File not exist</h1>')

    return response

@csrf_exempt
def _nifti_random(request):
    # Preparation
    print("Running the nifty routine.")
    SLICEOUTPUT = f"imaging/bobby.png"
    SLICEINPUT = f"imaging/alice.png"
    # Load phase
    pancreas_in, pancreas_in_data = None, None
    if len(request.body) == 2:
        return HttpResponseBadRequest('<h1>Nifty file not exist</h1>')
    else:
        print("Processing sent file.")
        DIR = "imaging"
        INAME = "omg.png"
        LLNAME = "zomfg.png"
        g = open("{0:s}/omg.nii.gz".format(DIR), 'wb')
        h = request.body
        print(h)
        g.write(h)
        g.close()
        try:
            pancreas_in = nib.load("{0:s}/{1:s}".format(DIR, "omg.nii.gz"))
            pancreas_in_data = pancreas_in.get_fdata()
        except FileNotFoundError as e:
            return HttpResponseBadRequest('<h1>Nifty file failed to process</h1>')
        except Exception as e:
            print(e)
            return HttpResponseNotAllowed('<h1>Game over</h1>')
        
    print(f"Input: {pancreas_in.get_fdata().shape}")
    print(pancreas_in.header)
    
    # Show phase
    fig_rows = 4
    fig_cols = 4
    n_subplots = fig_rows * fig_cols
    n_slice = pancreas_in_data.shape[2]
    step_size = n_slice // n_subplots
    plot_range = n_subplots * step_size
    start_stop = int((n_slice - plot_range) / 2)

    fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[10, 10])

    for idx, img in enumerate(range(start_stop, plot_range, step_size)):
        print(f"Slice: {img}")
        axs.flat[idx].imshow(pancreas_in_data[:, :, img])
        axs.flat[idx].axis('off')
            
    plt.tight_layout()
    plt.savefig(f"imaging/alice.png")

    # # Long phase
    # fig_rows = 1
    # fig_cols = 1
    # n_slice = pancreas_in_data.shape[2]
    # fig, axs = plt.subplots(1, 1, figsize=[10, 10])
    # cube = []

    # for idx, img in enumerate(range(0, n_slice, 1)):
    #     print(f"@@ {idx} @@")
    #     print(pancreas_in_data[:, :, img])
    #     axs.imshow(pancreas_in_data[:, :, img], cmap='gray')
    #     plt.tight_layout()
    #     SLICENAME = f"imaging/{INAME}_{idx}.png"
    #     cube.append(SLICENAME)
    #     plt.savefig(f"imaging/{INAME}_{idx}.png")

    # concatenated = Image.fromarray(
    # np.concatenate(
    #     [np.array(Image.open(x).resize((96,96))) for x in cube],
    #     axis=1
    # )
    # ).save(LLNAME)

    # Randomly select a pancreas imaging
    DIR = "imaging/cube"
    images_list = os.listdir(DIR)
    INAME = images_list[np.random.randint(0, len(images_list))]
    TNAME = "foo.png"
    print(INAME)
    try:
        pancreas_in = nib.load("{0:s}/{1:s}".format(DIR, INAME))
        pancreas_in_data = pancreas_in.get_fdata()
    except FileNotFoundError as e:
        return HttpResponseBadRequest('<h1>Nifty file failed to process</h1>')
    except Exception as e:
        print(e)
        return HttpResponseNotAllowed('<h1>Game over</h1>')

    # Show phase
    fig_rows = 4
    fig_cols = 4
    n_subplots = fig_rows * fig_cols
    n_slice = pancreas_in_data.shape[2]
    step_size = n_slice // n_subplots
    plot_range = n_subplots * step_size
    start_stop = int((n_slice - plot_range) / 2)

    fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[10, 10])

    for idx, img in enumerate(range(start_stop, plot_range, step_size)):
        print(f"Slice: {img}")
        axs.flat[idx].imshow(pancreas_in_data[:, :, img], cmap='gray')
        axs.flat[idx].axis('off')
            
    plt.tight_layout()
    plt.savefig(f"imaging/bobby.png")

    # Save Phase
    background = Image.open(SLICEOUTPUT)
    overlay = Image.open(SLICEINPUT)

    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")

    new_img = Image.blend(background, overlay, 0.5)
    LLNAME = "imaging/zomfg.png"
    new_img.save(LLNAME)

    # Return phase
    try:
        file_data = None
        print(LLNAME)
        with open(LLNAME, 'rb') as f:
           file_data = f.read()
        print(file_data)

        # sending response 
        response = HttpResponse(file_data, content_type='application/image/png')
        response['Content-Disposition'] = 'attachment; filename="foobar.png"'

    except IOError as e:
        # handle file not exist case here
        response = HttpResponseNotFound('<h1>File not exist</h1>')

    return response

@csrf_exempt
def index(request):
    print(f"{request.__dir__()}")
    print(f"@@@ ${request.__repr__()} @@@")
    print(f"@@@ ${request.headers} @@@")
    print(f"@@@ ${request.body} @@@")
    return _nifti_random(request)