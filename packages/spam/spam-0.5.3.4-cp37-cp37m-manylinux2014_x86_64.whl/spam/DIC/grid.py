﻿"""
Library of SPAM functions for defining a regular grid in a reproducible way.
Copyright (C) 2020 SPAM Contributors

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import print_function

import numpy
import spam.DIC.correlate
import sys
import progressbar
if sys.version[0] == '2':
    import Queue as queue
else:
    import queue as queue


def makeGrid(imageSize, nodeSpacing):
    """
        Define a grid of correlation points.

        Parameters
        ----------
        imageSize : 3-item list
            Size of volume to spread the grid inside

        nodeSpacing : 3-item list or int
            Spacing between nodes

        Returns
        -------
        nodePositions : nPointsx3 numpy.array
            Array containing Z, Y, X positions of each point in the grid
    """

    if len(imageSize) != 3:
        print("\tgrid.makeGrid(): imageSize doesn't have three dimensions, exiting")
        return

    if type(nodeSpacing) == int or type(nodeSpacing) == float:
        nodeSpacing = [nodeSpacing] * 3
    elif len(nodeSpacing) != 3:
        print("\tgrid.makeGrid(): nodeSpacing is not an int or float and doesn't have three dimensions, exiting")
        return

    if imageSize[0] == 1:
        twoD = True
    else:
        twoD = False

    # Note: in this cheap node spacing, the first node is always at a distance of --nodeSpacing-- from the origin
    # The following could just be done once in principle...
    nodesMgrid = numpy.mgrid[nodeSpacing[0]:imageSize[0]:nodeSpacing[0],
                             nodeSpacing[1]:imageSize[1]:nodeSpacing[1],
                             nodeSpacing[2]:imageSize[2]:nodeSpacing[2]]

    # If twoD then overwrite nodesMgrid
    if twoD:
        nodesMgrid = numpy.mgrid[0: 1: 1,
                                 nodeSpacing[1]:imageSize[1]:nodeSpacing[1],
                                 nodeSpacing[2]:imageSize[2]:nodeSpacing[2]]

    nodesDim = (nodesMgrid.shape[1], nodesMgrid.shape[2], nodesMgrid.shape[3])

    numberOfNodes = int(nodesMgrid.shape[1] * nodesMgrid.shape[2] * nodesMgrid.shape[3])

    nodePositions = numpy.zeros((numberOfNodes, 3))

    nodePositions[:, 0] = nodesMgrid[0].ravel()
    nodePositions[:, 1] = nodesMgrid[1].ravel()
    nodePositions[:, 2] = nodesMgrid[2].ravel()

    return nodePositions, nodesDim


def pixelSearchOnGrid(im1, im2, nodePositions, halfWindowSize, searchRange, PhiField=None, minMaskCoverage=0.5, im1mask=None, greyThreshold=[-numpy.inf, numpy.inf], mpi=False):
    """
    This function handles grid-based local correlation, offering an initial rough dispalcement-only guess.
    At the moment matching of windows is done with a Normalised-Correlation-Coefficient approach.

    Parameters
    ----------
        im1 : 3D numpy array
            A 3D image of greylevels defining a reference configuration for the pixel search

        im2 : 3D numpy array
            A deformed 3D image of greylevels

        nodePositions : nPoints*3 numpy array
            Array containing Z, Y, X positions of each point in the grid, as returned by ``makeGrid`` for example
            defined at im1

        halfWindowSize : 3-item list or int
            Size of subvolumes to perform the image correlation on, as a data range taken either side of the voxel on which the node is placed.
            The subvolume will be 2*halfWindowSize + 1 pixels on each side.
            A general recommendation is to make this half the node spacing

        searchRange : dictionary
            Search range as a dictionary containing 3 keys: 'zRange', 'yRange', and 'xRange',
            Each of which contains a list with two items

        PhiField : nPoints*4*4 numpy array, optional
            Optional field of ``F`` transformation operators defined for each node.
            Currently, only the translational components of F will be taken into account.
            Default = No displacement

        minMaskCoverage : float, optional
            Minimum number of pixels in a subvolume for it to be correlated (only considered in the case of im1mask).
            Default = 0.5

        im1mask : 3D boolean numpy array, optional
            A mask for im1 which is true in the zones to correlate.
            Default = None

        greyThreshold : list of two floats, optional
            Threshold for the mean greylevel in each im1 subvolume.
            If the mean is below the first value or above the second value, the grid point is not correlated.
            Default = [ -inf, inf ]

        mpi : bool, optional (default = False)
            Are we being called by an MPI run?

    Returns
    -------
        Dictionary containing:

        Keys
            PhiField : nNodes*4*4 numpy array of floats
                For each node, the measured transformatio operator (displacement only)

            pixelSearchCC : nNodes numpy array of floats
                For each node, the NCC score obtained
    """

    def getImagettes(nodeNumber, nodePositions, PhiField, searchRange, halfWindowSize, im1, im2, minMaskVolume, greyThreshold):
        returnStatus = 2

        initialDisplacement = PhiField[nodeNumber, 0:3, 3].astype(int)

        # Add initial displacement guess to search range
        searchRangeForThisNode = {'zRange': [searchRange['zRange'][0] + initialDisplacement[0], searchRange['zRange'][1] + initialDisplacement[0]],
                                  'yRange': [searchRange['yRange'][0] + initialDisplacement[1], searchRange['yRange'][1] + initialDisplacement[1]],
                                  'xRange': [searchRange['xRange'][0] + initialDisplacement[2], searchRange['xRange'][1] + initialDisplacement[2]]}

        # point in im2 that we are searching around
        searchCentre = [halfWindowSize[0] - searchRangeForThisNode['zRange'][0],
                        halfWindowSize[1] - searchRangeForThisNode['yRange'][0],
                        halfWindowSize[2] - searchRangeForThisNode['xRange'][0]]

        # 2020-09-25 OS and EA: Prepare startStop array for imagette 1 to be extracted with new slicePadded
        PhiNoDisp = PhiField[nodeNumber]
        PhiNoDisp[0:3,-1] = 0.0

        # If F is not the identity, create a pad to be able to apply F to imagette 1
        if numpy.allclose(PhiNoDisp, numpy.eye(4)):
            applyPhiPad = 0
        else:
            # 2020-10-06 OS and EA: Add a pad to each dimension of 25% of max(halfWindowSize) to allow space to apply F (no displacement) to imagette1
            applyPhiPad = int(0.25*numpy.ceil(max(halfWindowSize)))

        startStopIm1 = [int(nodePositions[nodeNumber, 0] - halfWindowSize[0] - applyPhiPad), int(nodePositions[nodeNumber, 0] + halfWindowSize[0] + applyPhiPad + 1),
                        int(nodePositions[nodeNumber, 1] - halfWindowSize[1] - applyPhiPad), int(nodePositions[nodeNumber, 1] + halfWindowSize[1] + applyPhiPad + 1),
                        int(nodePositions[nodeNumber, 2] - halfWindowSize[2] - applyPhiPad), int(nodePositions[nodeNumber, 2] + halfWindowSize[2] + applyPhiPad + 1)]
        # In either case, extract imagette1, now guaranteed to be the right size
        imagette1padded = spam.helpers.slicePadded(im1, startStopIm1)

        # If F is not the identity, apply F and undo crop
        if numpy.allclose(PhiNoDisp, numpy.eye(4)):
            # In this case there is is no padding (despite the name) and we can just keep going
            imagette1def = imagette1padded
        else:
            # apply F to imagette 1 padded
            imagette1paddedDef = spam.DIC.applyPhi(imagette1padded, PhiNoDisp)
            # undo padding
            imagette1def = imagette1paddedDef[applyPhiPad:-applyPhiPad,
                                              applyPhiPad:-applyPhiPad,
                                              applyPhiPad:-applyPhiPad]

        # Make sure imagette is not 0-dimensional in any dimension
        if numpy.all(numpy.array(imagette1def.shape) > 0):
            if numpy.nanmean(imagette1def) > greyThreshold[0] and numpy.nanmean(imagette1def) < greyThreshold[1] and len(imagette1def.ravel()) > minMaskVolume:
                # Slice for image 2
                ## 2020-09-25 OS and EA: Prepare startStop array for imagette 2 to be extracted with new slicePadded
                ## Extract it...
                startStopIm2 = [int(nodePositions[nodeNumber, 0] - halfWindowSize[0] + searchRangeForThisNode['zRange'][0]),
                                int(nodePositions[nodeNumber, 0] + halfWindowSize[0] + searchRangeForThisNode['zRange'][1] + 1),
                                int(nodePositions[nodeNumber, 1] - halfWindowSize[1] + searchRangeForThisNode['yRange'][0]),
                                int(nodePositions[nodeNumber, 1] + halfWindowSize[1] + searchRangeForThisNode['yRange'][1] + 1),
                                int(nodePositions[nodeNumber, 2] - halfWindowSize[2] + searchRangeForThisNode['xRange'][0]),
                                int(nodePositions[nodeNumber, 2] + halfWindowSize[2] + searchRangeForThisNode['xRange'][1] + 1)]
                imagette2 = spam.helpers.slicePadded(im2, startStopIm2)

            # Failed minMaskVolume or greylevel condition
            else:
                returnStatus = -5
                imagette1def = None
                imagette2 = None

        # Failed 0-dimensional imagette test
        else:
            returnStatus = -5
            imagette1def = None
            imagette2 = None

        return {'imagette1': imagette1def,
                'imagette2': imagette2,
                'returnStatus': returnStatus,
                'initialDisplacement': initialDisplacement,
                'searchRangeForThisNode': searchRangeForThisNode,
                'searchCentre': searchCentre}

    if mpi:
        import mpi4py.MPI

        mpiComm = mpi4py.MPI.COMM_WORLD
        mpiSize = mpiComm.Get_size()
        mpiRank = mpiComm.Get_rank()
        mpiStatus = mpi4py.MPI.Status()

        boss = mpiSize - 1

        numberOfWorkers = mpiSize - 1
        workersActive = numpy.zeros(numberOfWorkers)
    else:
        # not mpi
        numberOfWorkers = 1
        workersActive = numpy.array([0])

    # start setting up
    numberOfNodes = nodePositions.shape[0]

    # Check input sanity
    if type(halfWindowSize) == int or type(halfWindowSize) == float:
        halfWindowSize = [halfWindowSize] * 3

        # Check minMaskVolume
    minMaskVolume = int(minMaskCoverage * (1+halfWindowSize[0]*2)*
                                          (1+halfWindowSize[1]*2)*
                                          (1+halfWindowSize[2]*2))

    # Check F field
    if PhiField is None:
        PhiField = numpy.zeros((numberOfNodes, 4, 4))
        for nodeNumber in range(numberOfNodes):
            PhiField[nodeNumber] = numpy.eye(4)

    # Create pixelSearchCC vector
    pixelSearchCC = numpy.zeros((numberOfNodes))

    # Add nodes to a queue -- mostly useful for MPI
    q = queue.Queue()
    for node in range(numberOfNodes):
        q.put(node)
    finishedNodes = 0

    writeReturns = False

    print("\n\tStarting Pixel search")
    widgets = [progressbar.FormatLabel(''), ' ', progressbar.Bar(), ' ', progressbar.AdaptiveETA()]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=numberOfNodes)
    pbar.start()
    while finishedNodes != numberOfNodes:
        # If there are workers not working, satify their requests...
        #   Note: this condition is alyas true if we are not in MPI and there are jobs to do
        if workersActive.sum() < numberOfWorkers and not q.empty():
            worker = numpy.where(workersActive == False)[0][0]
            # Get the next node off the queue
            nodeNumber = q.get()

            imagetteReturns = getImagettes(nodeNumber, nodePositions, PhiField, searchRange, halfWindowSize, im1, im2, minMaskVolume, greyThreshold)

            if imagetteReturns['returnStatus'] == 2:
                if mpi:
                    # build message for pixel search worker
                    m = {'nodeNumber': nodeNumber,
                         'im1': imagetteReturns['imagette1'],
                         'im2': imagetteReturns['imagette2'],
                         'searchRangeForThisNode': imagetteReturns['searchRangeForThisNode'],
                         'searchCentre': imagetteReturns['searchCentre'],
                         'initialDisplacement': imagetteReturns['initialDisplacement']
                         }

                    # print "\tBoss: sending node {} to worker {}".format( nodeNumber, worker )
                    mpiComm.send(m, dest=worker, tag=1)

                    # Mark this worker as working
                    workersActive[worker] = True

                    # NOTE: writeReturns is defined later when receiving messages

                else:  # Not MPI
                    returns = spam.DIC.correlate.pixelSearch(imagetteReturns['imagette1'],
                                                             imagetteReturns['imagette2'],
                                                             searchRange=imagetteReturns['searchRangeForThisNode'],
                                                             searchCentre=imagetteReturns['searchCentre'])
                    initialDisplacement = imagetteReturns['initialDisplacement']
                    writeReturns = True

            else:  # Regardless of MPI or single proc
                # Failed to extract imagettes or something
                pixelSearchCC[nodeNumber] = 0.0
                finishedNodes += 1
                PhiField[nodeNumber, 0:3, 0:3] = numpy.eye(3)
                PhiField[nodeNumber, 0:3, 3] = numpy.nan

        # Otherwise spend time looking waiting for replies from workers
        elif mpi:
            message = mpiComm.recv(source=mpi4py.MPI.ANY_SOURCE, tag=2, status=mpiStatus)
            tag = mpiStatus.Get_tag()
            if tag == 2:
                worker = message[0]
                nodeNumber = message[1]
                returns = message[2]
                initialDisplacement = message[3]
                # print "\tBoss: received node {} from worker {}".format( nodeNumber, worker )
                workersActive[worker] = False
                writeReturns = True
            else:
                print("\tBoss: Don't recognise tag ", tag)

        # If we have new DVC returns, save them in our output matrices
        if writeReturns:
            finishedNodes += 1
            writeReturns = False
            # set translation for this node
            PhiField[nodeNumber, 0:3, 3] = numpy.array(returns['transformation']['t'])

            pixelSearchCC[nodeNumber] = returns['cc']
            widgets[0] = progressbar.FormatLabel("  CC={:0>7.5f} ".format(pixelSearchCC[nodeNumber]))
            pbar.update(finishedNodes)

    pbar.finish()
    print("\n")

    return {'PhiField': PhiField,
            'pixelSearchCC': pixelSearchCC}


def registerOnGrid(im1, im2, nodePositions, halfWindowSize, PhiField=None, margin=None, maxIterations=None, deltaPhiMin=None, updateGradient=None, interpolationOrder=None, minMaskCoverage=0.5, im1mask=None, greyThreshold=[-numpy.inf, numpy.inf], mpi=False, killWorkersWhenDone=True):
    """
    This function handles grid-based local correlation, performing a "register" subpixel refinement.
    Here we minimise a residual which is the difference between im1 and im2.

    Parameters
    ----------
        im1 : 3D numpy array
            A 3D image of greylevels defining a reference configuration for the pixel search

        im2 : 3D numpy array
            A deformed 3D image of greylevels

        nodePositions : nPoints*3 numpy array
            Array containing Z, Y, X positions of each point in the grid, as returned by ``makeGrid`` for example

        halfWindowSize : 3-item list or int
            Size of subvolumes to perform the image correlation on, as a data range taken either side of the voxel on which the node is placed.
            The subvolume will be 2*halfWindowSize + 1 pixels on each side.
            A general recommendation is to make this half the node spacing

        PhiField : nPoints*4*4 numpy array, optional
            Optional field of Phi deformation functions defined for each node
            Default = None

        margin : int or list, optional
            Margin to extract for subpixel interpolation
            Default = None (use ``register``'s default)

        maxIterations : int, optional (default = None (use ``register``'s default))
            Number of iterations for subpixel refinement

        deltaPhiMin : float, optional
            Stop iterating when norm of F gets below this value
            Default = None (use ``register``'s default)
            
        updateGradient : bool, optional
            Should the gradient of the image be computed (and updated) on the deforming im2?
            Default = None (use ``register``'s default)

        interpolationOrder : int, optional
            Greyscale interpolation order
            Default = None (use ``register``'s default)

        minMaskCoverage : float, optional
            Minimum number of pixels in a subvolume for it to be correlated (only considered in the case of im1mask).
            Default = 0.5

        im1mask : 3D boolean numpy array, optional
            A mask for the whole of im1 which is true in the zones to correlate.
            This is NOT used to mask the image, but to detect subvolumes that
            Fall inside the mask (see minMaskVolume for proportion)
            Default = None

        greyThreshold : list of two floats, optional
            Threshold for the mean greylevel in each im1 subvolume.
            If the mean is below the first value or above the second value, the grid point is not correlated.
            Default = [ -inf, inf ]

        mpi : bool, optional (default = False)
            Are we being called by an MPI run?

    Returns
    --------
        Dictionary containing:
            PhiField
            error
            iterations
            returnStatus
            deltaPhiNorm
    """

    # Check input sanity
    if type(margin) == int or type(margin) == float:
        margin = [margin] * 3

    # Detect unpadded 2D image first:
    if len(im1.shape) == 2:
        # pad them
        im1 = im1[numpy.newaxis, ...]
        im2 = im2[numpy.newaxis, ...]

    # Detect 2D images
    if im1.shape[0] == 1:
        twoD = True
    else:
        twoD = False

    if interpolationOrder == 1:
        interpolator = 'C'
    else:
        interpolator = 'python'
    # Override interpolator for python in 2D
    if twoD:
        interpolator = 'python'

    numberOfNodes = nodePositions.shape[0]

    def getImagettes(nodeNumber, im1, im2, PhiField, nodePositions, margin, halfWindowSize, greyThreshold, im1mask, minMaskVolume, twoD=False):
        # We don't have many single letter variable names, but this is one to keep things aligned
        # This variable is =0 in 2D and =1 in 3D
        if twoD: m = 0
        else:    m = 1
        # Initialise defaults
        imagette1mask = None
        PhiInit = None
        nodeDisplacement = None

        # Make sure all components of F are real numbers
        if numpy.isfinite(PhiField[nodeNumber]).sum() == 16:
            nodeDisplacement = numpy.round(PhiField[nodeNumber][0:3, -1])

            # prepare slice for imagette 1 -- this is fixed +1 for the margin which is always 1
            # 2020-09-25 OS and EA: Prepare startStop array for imagette 1 to be extracted with new slicePadded
            #subVolSlice1 = (slice(int(nodePositions[nodeNumber, 0] - halfWindowSize[0] - 1), int(nodePositions[nodeNumber, 0] + halfWindowSize[0] + 1 + 1)),
                            #slice(int(nodePositions[nodeNumber, 1] - halfWindowSize[1] - 1), int(nodePositions[nodeNumber, 1] + halfWindowSize[1] + 1 + 1)),
                            #slice(int(nodePositions[nodeNumber, 2] - halfWindowSize[2] - 1), int(nodePositions[nodeNumber, 2] + halfWindowSize[2] + 1 + 1)))
            #imagette1 = im1[subVolSlice1].copy()
            startStopIm1 = [int(nodePositions[nodeNumber, 0] - halfWindowSize[0] - m), int(nodePositions[nodeNumber, 0] + halfWindowSize[0] + 1 + m),
                            int(nodePositions[nodeNumber, 1] - halfWindowSize[1] - 1), int(nodePositions[nodeNumber, 1] + halfWindowSize[1] + 1 + 1),
                            int(nodePositions[nodeNumber, 2] - halfWindowSize[2] - 1), int(nodePositions[nodeNumber, 2] + halfWindowSize[2] + 1 + 1)]
            imagette1, imagette1mask = spam.helpers.slicePadded(im1, startStopIm1, createMask=True)


            # If there is a mask defined for im1, compute the coverage of this correlation window
            # Check Mask volume condition
            if im1mask is not None:
                # AND masks together, the one coming from the im1mask -- i.e., allowed correlation zones
                # and the imagette1sliceMask indicating whether we've gone outside the volume
                imagette1mask = numpy.logical_and(imagette1mask, spam.helpers.slicePadded(im1mask, startStopIm1))
            maskVolCondition = imagette1mask.sum() > minMaskVolume

            # Make sure imagette is not 0-dimensional in any dimension
            if numpy.all(numpy.array(imagette1.shape) > 0):
                # Check if out extracted imagette 1 is above grey threshold, if there is enough under the mask if defined, and that dispalcements are not NaN
                if numpy.nanmean(imagette1) > greyThreshold[0] and numpy.nanmean(imagette1) < greyThreshold[1] and maskVolCondition:

                    # Prepare im2 imagette
                    # start from nodePosition in im1 and move it according to the nodeDisplacement
                    # and move it + 1 for the margin which is always 1
                    # 2020-09-25 OS and EA: Prepare startStop array for imagette 2 to be extracted with new slicePadded
                    #subVolSlice2 = (slice(int(nodePositions[nodeNumber, 0] - halfWindowSize[0] + nodeDisplacement[0] - margin[0] - 1), int(nodePositions[nodeNumber, 0] + halfWindowSize[0] + nodeDisplacement[0] + margin[0] + 1 + 1)),
                                    #slice(int(nodePositions[nodeNumber, 1] - halfWindowSize[1] + nodeDisplacement[1] - margin[1] - 1), int(nodePositions[nodeNumber, 1] + halfWindowSize[1] + nodeDisplacement[1] + margin[1] + 1 + 1)),
                                    #slice(int(nodePositions[nodeNumber, 2] - halfWindowSize[2] + nodeDisplacement[2] - margin[2] - 1), int(nodePositions[nodeNumber, 2] + halfWindowSize[2] + nodeDisplacement[2] + margin[2] + 1 + 1)))
                    ## Extract it
                    #imagette2 = im2[subVolSlice2].copy()
                    startStopIm2 = [int(nodePositions[nodeNumber, 0] - halfWindowSize[0] + nodeDisplacement[0] - margin[0] - m), int(nodePositions[nodeNumber, 0] + halfWindowSize[0] + nodeDisplacement[0] + margin[0] + m + 1),
                                    int(nodePositions[nodeNumber, 1] - halfWindowSize[1] + nodeDisplacement[1] - margin[1] - 1), int(nodePositions[nodeNumber, 1] + halfWindowSize[1] + nodeDisplacement[1] + margin[1] + 1 + 1),
                                    int(nodePositions[nodeNumber, 2] - halfWindowSize[2] + nodeDisplacement[2] - margin[2] - 1), int(nodePositions[nodeNumber, 2] + halfWindowSize[2] + nodeDisplacement[2] + margin[2] + 1 + 1)]
                    imagette2 = spam.helpers.slicePadded(im2, startStopIm2, padValue=numpy.nan)
                    ## 2020-09-25 OS and EA: overwrite 0-padding with NaN-padding
                    #imagette2[~imagette2mask] = numpy.nan

                    # Extract initial F for correlation, remove int() part of displacement since it's already used to extract imagette2
                    PhiInit = PhiField[nodeNumber].copy()
                    PhiInit[0:3, -1] -= nodeDisplacement.copy()
                    # print "PhiInit:\n", PhiInit, '\n'
                    #PhiInit = numpy.eye(4)

                    if (numpy.array(imagette2.shape) - numpy.array(imagette1.shape) == numpy.array(margin) * 2).all():
                        returnStatus = 2

                    # Failed innermost condition -- im1 and im2 margin alignment -- this is a harsh condition
                    else:
                        returnStatus = -4
                        imagette1 = None
                        imagette2 = None

                # Failed mask or greylevel condition
                else:
                    returnStatus = -5
                    imagette1 = None
                    imagette2 = None

            # Failed 0-dimensional imagette test
            else:
                returnStatus = -5
                imagette1 = None
                imagette2 = None

        # Failed non-NaN components in F
        else:
            returnStatus = -6
            imagette1 = None
            imagette2 = None

        return {'imagette1': imagette1, 'imagette2': imagette2,
                'imagette1mask': imagette1mask,
                'returnStatus': returnStatus,
                'PhiInit': PhiInit,
                'nodeDisplacement': nodeDisplacement}

    if mpi:
        import mpi4py.MPI

        mpiComm = mpi4py.MPI.COMM_WORLD
        mpiSize = mpiComm.Get_size()
        mpiRank = mpiComm.Get_rank()
        mpiStatus = mpi4py.MPI.Status()

        boss = mpiSize - 1

        numberOfWorkers = mpiSize - 1
        workersActive = numpy.zeros(numberOfWorkers)
    else:
        numberOfWorkers = 1
        workersActive = numpy.array([0])

    # Check input sanity
    if type(halfWindowSize) == int or type(halfWindowSize) == float:
        halfWindowSize = [halfWindowSize] * 3

    # Check minMaskVolume
    minMaskVolume = int(minMaskCoverage * (1+halfWindowSize[0]*2)*
                                          (1+halfWindowSize[1]*2)*
                                          (1+halfWindowSize[2]*2))

    # Check F field
    if PhiField is None:
        PhiField = numpy.zeros((numberOfNodes, 4, 4))
        for nodeNumber in range(numberOfNodes):
            PhiField[nodeNumber] = numpy.eye(4)

    # Add nodes to a queue -- mostly useful for MPI
    q = queue.Queue()
    for node in range(numberOfNodes):
        q.put(node)
    finishedNodes = 0

    subpixelError = numpy.zeros((numberOfNodes))
    subpixelIterations = numpy.zeros((numberOfNodes))
    subpixelReturnStatus = numpy.zeros((numberOfNodes))
    subpixelDeltaFnorm = numpy.zeros((numberOfNodes))

    writeReturns = False

    print("\n\tStarting Correlation")
    widgets = [progressbar.FormatLabel(''), ' ', progressbar.Bar(), ' ', progressbar.AdaptiveETA()]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=numberOfNodes)
    pbar.start()
    while finishedNodes != numberOfNodes:
        # If there are workers not working, satify their requests...
        #   Note: this condition is alyas true if we are not in MPI and there are jobs to do
        if workersActive.sum() < numberOfWorkers and not q.empty():
            worker = numpy.where(workersActive == False)[0][0]
            # Get the next node off the queue
            nodeNumber = q.get()

            imagetteReturns = getImagettes(nodeNumber, im1, im2, PhiField, nodePositions, margin, halfWindowSize, greyThreshold, im1mask, minMaskVolume, twoD)

            if imagetteReturns['returnStatus'] == 2:
                if mpi:
                    # build message for lukas kanade worker
                    m = {'nodeNumber': nodeNumber,
                         'im1': imagetteReturns['imagette1'],
                         'im2': imagetteReturns['imagette2'],
                         'im1mask': imagetteReturns['imagette1mask'],
                         'PhiInit': imagetteReturns['PhiInit'],
                         # 'PhiInitBinRatio' : PhiInitBinRatio,
                         'margin': 1,  # see top of this file for compensation
                         'maxIterations': maxIterations,
                         'deltaPhiMin': deltaPhiMin,
                         'updateGradient': updateGradient,
                         'interpolationOrder': interpolationOrder,
                         'interpolator': interpolator,
                         'nodeDisplacement': imagetteReturns['nodeDisplacement']
                         }

                    # print "\tBoss: sending node {} to worker {}".format( nodeNumber, worker )
                    mpiComm.send(m, dest=worker, tag=3)

                    # Mark this worker as working
                    workersActive[worker] = True

                    # NOTE: writeReturns is defined later when receiving messages

                else:  # Not MPI
                    returns = spam.DIC.correlate.register(imagetteReturns['imagette1'],
                                                          imagetteReturns['imagette2'],
                                                          im1mask=imagetteReturns['imagette1mask'],
                                                          PhiInit=imagetteReturns['PhiInit'],
                                                          margin=1,  # see top of this file for compensation
                                                          maxIterations=maxIterations,
                                                          deltaPhiMin=deltaPhiMin,
                                                          updateGradient=updateGradient,
                                                          interpolationOrder=interpolationOrder,
                                                          verbose=False,
                                                          imShowProgress=False)
                    nodeDisplacement = imagetteReturns['nodeDisplacement']
                    writeReturns = True

            else:  # Regardless of MPI or single proc
                # Failed to extract imagettes or something
                subpixelError[nodeNumber] = numpy.inf
                subpixelIterations[nodeNumber] = 0
                subpixelReturnStatus[nodeNumber] = imagetteReturns['returnStatus']
                subpixelDeltaFnorm[nodeNumber] = numpy.inf
                PhiField[nodeNumber, 0:3, 0:3] = numpy.eye(3)
                PhiField[nodeNumber, 0:3, 3] = numpy.nan
                finishedNodes += 1

        # Otherwise spend time looking waiting for replies from workers
        elif mpi:
            message = mpiComm.recv(source=mpi4py.MPI.ANY_SOURCE, tag=4, status=mpiStatus)
            tag = mpiStatus.Get_tag()
            if tag == 4:
                worker = message[0]
                nodeNumber = message[1]
                returns = message[2]
                nodeDisplacement = message[3]
                # print "\tBoss: received node {} from worker {}".format( nodeNumber, worker )
                workersActive[worker] = False
                writeReturns = True
            else:
                print("\tBoss: Don't recognise tag ", tag)

        # If we have new DVC returns, save them in our output matrices
        if writeReturns:
            finishedNodes += 1
            writeReturns = False
            # Overwrite transformation operator for this node
            PhiField[nodeNumber] = returns['Phi']
            # Add back in the translation from the initial guess
            PhiField[nodeNumber, 0:3, 3] += nodeDisplacement

            subpixelError[nodeNumber] = returns['error']
            subpixelIterations[nodeNumber] = returns['iterations']
            subpixelReturnStatus[nodeNumber] = returns['returnStatus']
            subpixelDeltaFnorm[nodeNumber] = returns['deltaPhiNorm']

            #widgets[0] = progressbar.FormatLabel("err={:0>7.03f}\tit={:0>3d}\tdFnorm={:0>5.03f}\trs={:+1d}".format( returns['error'], returns['iterationNumber'], returns['deltaFnorm'], returns['returnStatus'] ))
            widgets[0] = progressbar.FormatLabel("  it={:0>3d}  dPhiNorm={:0>6.4f}  rs={:+1d} ".format(returns['iterations'], returns['deltaPhiNorm'], returns['returnStatus']))
            pbar.update(finishedNodes)
            #print("\r\t\tCorrelating node {:04d} of {:04d}".format( nodeNumber+1, numberOfNodes ), end='' )
            #print("\terror={:05.0f}\titerations={:02d}\tdeltaFnorm={:0.5f}\treturnStat={:+1d}".format( returns['error'], returns['iterationNumber'], returns['deltaFnorm'], returns['returnStatus'] ), end='')

    pbar.finish()
    print("\n")

    return {"PhiField": PhiField,
            "error": subpixelError,
            "iterations": subpixelIterations,
            "returnStatus": subpixelReturnStatus,
            "deltaPhiNorm": subpixelDeltaFnorm,
            }
