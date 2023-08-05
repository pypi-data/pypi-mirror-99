"""
    PyJAMAS is Just A More Awesome Siesta
    Copyright (C) 2018  Rodrigo Fernandez-Gonzalez (rodrigo.fernandez.gonzalez@utoronto.ca)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import numpy
from PyQt5 import QtCore, QtGui, QtWidgets

from pyjamas.pjscore import PyJAMAS
import pyjamas.rimage as rimage
import pyjamas.rutils as rutils


class PJSEventFilter(QtCore.QObject):
    POLYLINE_MOVE_STEP = 1

    def __init__(self, ui):
        """

        :type ui: PyJAMAS
        """
        super().__init__()

        self.pjs: PyJAMAS = ui
        self.x_prev: int = -1
        self.y_prev: int = -1
        self.x: int = -1
        self.y: int = -1

    def eventFilter(self, source, event: QtCore.QEvent):
        # sourcery skip: hoist-statement-from-if, merge-nested-ifs
        """
        Returns False for events that should not be processed, and the event itself otherwise.
        :param source:
        :param event:
        :return:
        """

        # IMPORTANT!!!!! ------------
        # CAPTURE MOUSE EVENTS HERE!!! SEE BELOW (elif) FOR KEYBOARD EVENTS.
        if type(source) == QtWidgets.QWidget:
             # Event coordinates.
            #if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.type() in (QtCore.QEvent.MouseMove, QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonRelease):
                thepoint = self.pjs.gView.mapToScene(event.x(), event.y())

                # The mouse position is determined as the floor of the current floating point position
                # (using int would shift the coordinate to the one below or to the right before moving the
                # mouse into that pixel).
                self.x, self.y = (int(numpy.floor(thepoint.x())), int(numpy.floor(thepoint.y())))

                # Check for boundaries.
                if self.x < 0:
                    self.x = 0
                elif self.x >= self.pjs.width:
                    self.x = self.pjs.width - 1

                if self.y < 0:
                    self.y = 0
                elif self.y >= self.pjs.height:
                    self.y = self.pjs.height - 1

            # Mouse click: display pixel coordinates and value.
            if event.type() == QtCore.QEvent.MouseMove:
                if 0 <= self.x < self.pjs.width and 0 <= self.y < self.pjs.height:
                    self.pjs.statusbar.showMessage(
                        str(self.pjs.curslice + 1) + '/' + str(self.pjs.n_frames) + '\t(' + str(self.x) + ', ' + str(
                            self.y) + '): ' + str(self.pjs.imagedata[self.y, self.x]))
            
            # Orthogonal views tracker. 
            if self.pjs.slicetracker is not None and event.type() == QtCore.QEvent.MouseMove and event.buttons() == QtCore.Qt.LeftButton:
                self.pjs.slicetracker = (self.x, self.y)
                self.pjs.orthogonal_views.reloadViews()

            # Fiducials: add and remove.
            elif self.pjs.annotation_mode == PyJAMAS.fiducials and event.type() == QtCore.QEvent.MouseButtonPress:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self.pjs.addFiducial(self.x, self.y, self.pjs.curslice)

                elif event.buttons() == QtCore.Qt.RightButton:
                    self.pjs.removeFiducial(self.x, self.y, self.pjs.curslice)

            # Rectangles.
            elif self.pjs.annotation_mode == PyJAMAS.rectangles:
                if event.type() == QtCore.QEvent.MouseButtonPress:
                    # Store first coordinate if left click ...
                    if event.buttons() == QtCore.Qt.LeftButton:
                        self.pjs._poly_ = [self.x, self.y]

                    # ... or delete polygon if right click.
                    elif event.buttons() == QtCore.Qt.RightButton:
                        self.pjs.removePolyline(self.x, self.y,
                                                self.pjs.curslice)  # CAN WE JUST HAVE ONE removeAnnotationItem function?

                # Redraw rectangle as the user drags the cursor.
                elif event.type() == QtCore.QEvent.MouseMove and event.buttons() == QtCore.Qt.LeftButton:  # Mouse move events will occur only when a mouse button is pressed down, unless mouse tracking has been enabled with QWidget.setMouseTracking()
                    if self.pjs._agraphicsitem_:
                        self.pjs.gScene.removeItem(self.pjs._agraphicsitem_)

                    # If shift is not pressed, draw a rectangle, a square if it is pressed.
                    modifierPressed = QtWidgets.QApplication.keyboardModifiers()
                    if (modifierPressed & QtCore.Qt.ShiftModifier) != QtCore.Qt.ShiftModifier:
                        x = self.x
                        y = self.y
                    else:
                        deltaX = self.x - self.pjs._poly_[0]
                        deltaY = self.y - self.pjs._poly_[1]

                        if abs(deltaX) >= abs(deltaY):
                            x = self.x
                            y = self.pjs._poly_[1] + numpy.sign(deltaY) * abs(deltaX)
                        else:
                            y = self.y
                            x = self.pjs._poly_[0] + numpy.sign(deltaX) * abs(deltaY)

                    self.pjs._agraphicsitem_ = self.pjs.drawRectangle(self.pjs._poly_[0], self.pjs._poly_[1], x, y)
                    self.pjs.statusbar.showMessage(
                        '{0}/{1}\t({2}, {3}) -> w: {4}, h: {5}'.format(str(self.pjs.curslice + 1),
                                                                                           str(self.pjs.n_frames), str(
                                self.pjs._poly_[0]), str(
                                self.pjs._poly_[1]), str(abs(self.pjs._poly_[0] - x)+1), str(abs(self.pjs._poly_[1] - y)+1)))

                # Add rectangle as mouse button is released.
                elif event.type() == QtCore.QEvent.MouseButtonRelease and self.pjs._poly_ != []:
                    if self.pjs._agraphicsitem_:
                        self.pjs.gScene.removeItem(self.pjs._agraphicsitem_)

                    x0 = self.pjs._poly_[0]
                    y0 = self.pjs._poly_[1]

                    modifierPressed = QtWidgets.QApplication.keyboardModifiers()
                    if (modifierPressed & QtCore.Qt.ShiftModifier) != QtCore.Qt.ShiftModifier:
                        x1 = self.x
                        y1 = self.y
                    else:
                        deltaX = self.x - self.pjs._poly_[0]
                        deltaY = self.y - self.pjs._poly_[1]

                        if abs(deltaX) >= abs(deltaY):
                            x1 = self.x
                            y1 = self.pjs._poly_[1] + numpy.sign(deltaY) * abs(deltaX)
                        else:
                            y1 = self.y
                            x1 = self.pjs._poly_[0] + numpy.sign(deltaX) * abs(deltaY)

                    if x0 > x1:
                        dummy = x1
                        x1 = x0
                        x0 = dummy

                    if y0 > y1:
                        dummy = y1
                        y1 = y0
                        y0 = dummy

                    self.pjs.addPolyline([[x0, y0], [x0, y1], [x1, y1], [x1, y0], [x0, y0]], self.pjs.curslice)
                    self.pjs._poly_ = []

            # Polylines.
            elif self.pjs.annotation_mode == PyJAMAS.polylines:
                if event.type() == QtCore.QEvent.MouseButtonPress:
                    # Store coordinate if left click ...
                    if event.buttons() == QtCore.Qt.LeftButton:
                        self.pjs._poly_.append([self.x, self.y])

                        if self.pjs._agraphicsitem_:
                            self.pjs.gScene.removeItem(self.pjs._agraphicsitem_)

                        self.pjs._agraphicsitem_, _ = self.pjs.drawPath(self.pjs._poly_)

                    # Delete last point if middle click
                    elif event.buttons() == QtCore.Qt.RightButton and self.pjs._poly_ != [] and len(self.pjs._poly_) >= 2:
                        self.pjs._poly_ = self.pjs._poly_[0:-1]
                        if self.pjs._agraphicsitem_:
                            self.pjs.gScene.removeItem(self.pjs._agraphicsitem_)

                            apoly = self.pjs._poly_.copy()
                            apoly.append([self.x, self.y])

                            self.pjs._agraphicsitem_, _ = self.pjs.drawPath(apoly)
                    # ... or delete polygon if right click.
                    elif event.buttons() == QtCore.Qt.RightButton:
                        self.pjs.removePolyline(self.x, self.y, self.pjs.curslice)

                # Redraw polyline as the user moves the cursor.
                elif event.type() == QtCore.QEvent.MouseMove and self.pjs._poly_ != []:
                    if self.pjs._agraphicsitem_:
                        self.pjs.gScene.removeItem(self.pjs._agraphicsitem_)

                        apoly = self.pjs._poly_.copy()
                        apoly.append([self.x, self.y])

                        self.pjs._agraphicsitem_, _ = self.pjs.drawPath(apoly)

                # Add polyline as mouse button is released.
                elif event.type() == QtCore.QEvent.MouseButtonDblClick and self.pjs._poly_ != []:
                    if self.pjs._agraphicsitem_:
                        self.pjs.gScene.removeItem(self.pjs._agraphicsitem_)

                    # Polylines need to have at least two points.
                    if len(self.pjs._poly_) <= 1:
                        self.pjs._poly_ = []
                        return False

                    apoly = self.pjs._poly_.copy()

                    # If shift is not pressed, go back to origin.
                    modifierPressed = QtWidgets.QApplication.keyboardModifiers()
                    if (modifierPressed & QtCore.Qt.ShiftModifier) != QtCore.Qt.ShiftModifier:
                        apoly.append([self.pjs._poly_[0][0], self.pjs._poly_[0][1]])

                    self.pjs.addPolyline(apoly, self.pjs.curslice)
                    self.pjs._poly_ = []

            # Delete fiducials outside polyline.
            elif self.pjs.annotation_mode == PyJAMAS.delete_fiducials_outside_polyline:
                if event.type() == QtCore.QEvent.MouseButtonPress:
                    index = self.pjs.find_clicked_polyline(self.x, self.y)
                    if index >= 0:
                        # Delete every annotation outside.
                        self.pjs.removeFiducialsPolyline(self.pjs._poly_, False)
                    else:
                        return False

            # Delete fiducials inside polyline.
            elif self.pjs.annotation_mode == PyJAMAS.delete_fiducials_inside_polyline:
                if event.type() == QtCore.QEvent.MouseButtonPress:
                    index = self.pjs.find_clicked_polyline(self.x, self.y)
                    if index >= 0:
                        # Delete every annotation outside.
                        self.pjs.removeFiducialsPolyline(self.pjs._poly_, True)
                    else:
                        return False

            # Copy polyline.
            elif self.pjs.annotation_mode == PyJAMAS.copy_polyline:
                if event.type() == QtCore.QEvent.MouseButtonPress:
                    index = self.pjs.find_clicked_polyline(self.x, self.y)

                    # Not using self.pjs._poly_ here, as other operations on the UI will overwrite it.
                    self.pjs._copied_poly_ = self.pjs.polylines[self.pjs.curslice][index]

                    if index < 0:
                        return False

            # LiveWire.
            elif self.pjs.annotation_mode == PyJAMAS.livewire:
                if type(self.pjs._poly_) == list:
                    if event.type() == QtCore.QEvent.MouseButtonPress:
                        # Store coordinate if left click ...
                        if event.buttons() == QtCore.Qt.LeftButton:
                            if self.pjs._poly_ != []:
                                thesource = self.pjs._poly_[-1][::-1]
                                thedest = [self.y, self.x]
                                thepoints = rimage.rimcore.rimage(self.pjs.imagedata).livewire(thesource, thedest,
                                                                                               PyJAMAS.livewire_margin, xy=True)  # Make livewire a static method?
                                self.pjs._poly_.extend(
                                    thepoints)  ### CHANGE: STORE ALL COORDINATES GENERATED BY LIVEWIRE FROM LAST CLICKED POINT

                                if self.pjs._agraphicsitem_:
                                    self.pjs.gScene.removeItem(self.pjs._agraphicsitem_)

                                self.pjs._agraphicsitem_, _ = self.pjs.drawPath(self.pjs._poly_)

                            else:
                                self.pjs._poly_.append([self.x, self.y])
                                if self.pjs._agraphicsitem_:
                                    self.pjs.gScene.removeItem(self.pjs._agraphicsitem_)

                                self.pjs._agraphicsitem_, _ = self.pjs.drawPath(self.pjs._poly_)
                        # Delete last point if middle click # NOT DONE YET.
                        elif event.buttons() == QtCore.Qt.RightButton and self.pjs._poly_ != [] and len(self.pjs._poly_) >= 2:
                            self.pjs._poly_ = self.pjs._poly_[0:-1]
                            if self.pjs._agraphicsitem_:
                                self.pjs.gScene.removeItem(self.pjs._agraphicsitem_)

                                apoly = self.pjs._poly_.copy()
                                apoly.append([self.x, self.y])

                                self.pjs._agraphicsitem_, _ = self.pjs.drawPath(apoly)
                        # ... or delete polygon if right click.
                        elif event.buttons() == QtCore.Qt.RightButton:
                            self.pjs.removePolyline(self.x, self.y, self.pjs.curslice)

                    # Redraw polyline as the user moves the cursor.
                    elif event.type() == QtCore.QEvent.MouseMove and self.pjs._poly_ != []:
                        if self.pjs._agraphicsitem_:
                            self.pjs.gScene.removeItem(self.pjs._agraphicsitem_)

                            apoly = self.pjs._poly_.copy()
                            thesource = apoly.copy()[-1][::-1]
                            thedest = [self.y, self.x]
                            thepoints = rimage.rimcore.rimage(self.pjs.imagedata).livewire(thesource, thedest,
                                                                                           PyJAMAS.livewire_margin, xy=True)  # Make livewire a static method? Or make self.imagedata an RImage?
                            apoly.extend(
                                thepoints)  ### CHANGE: STORE ALL COORDINATES GENERATED BY LIVEWIRE FROM LAST CLICKED POINT

                            self.pjs._agraphicsitem_, _ = self.pjs.drawPath(apoly)
                            # self.statusbar.showMessage(str(self.curslice + 1) + '/' + str(self.n_frames) + '\t(' + str(self._poly_[0]) + ', ' + str(
                            # self._poly_[1]) + ') -> w: ' + str(abs(self._poly_[0] - self.x)) + ', h: ' + str(abs(self._poly_[1] - self.y)))

                    # Add polyline as mouse button is released.
                    elif event.type() == QtCore.QEvent.MouseButtonDblClick and self.pjs._poly_ != []:
                        if self.pjs._agraphicsitem_:
                            self.pjs.gScene.removeItem(self.pjs._agraphicsitem_)

                        if len(self.pjs._poly_) <= 2:
                            self.pjs._poly_ = []
                            return False

                        # If shift is not pressed, go back to origin.
                        modifierPressed = QtWidgets.QApplication.keyboardModifiers()
                        if (modifierPressed & QtCore.Qt.ShiftModifier) != QtCore.Qt.ShiftModifier:
                            thesource = self.pjs._poly_[-1][::-1]
                            thedest = self.pjs._poly_[0][::-1]
                            thepoints = rimage.rimcore.rimage(self.pjs.imagedata).livewire(thesource, thedest,
                                                                                           PyJAMAS.livewire_margin, xy=True)  # Make livewire a static method? Or make self.imagedata an RImage?
                            self.pjs._poly_.extend(thepoints)

                        self.pjs.addPolyline(self.pjs._poly_, self.pjs.curslice)
                        self.pjs._poly_ = []

                else:
                    self.pjs._poly_ = []
                    return False
                
            # Move polylines.
            elif self.pjs.annotation_mode == PyJAMAS.move_polyline:
                # Select polyline with the mouse.
                if event.type() == QtCore.QEvent.MouseButtonPress:
                    index = self.pjs.find_clicked_polyline(self.x, self.y)

                    if index < 0:
                        return False

                # Move with the mouse.
                # Redraw polyline as the user moves the cursor.
                elif event.type() == QtCore.QEvent.MouseMove and event.buttons() == QtCore.Qt.LeftButton and self.x_prev > -1 and self.y_prev > -1:
                    if self.pjs._agraphicsitem_:
                        #self.pjs.gScene.removeItem(self.pjs._agraphicsitem_)
                        theshift = QtCore.QPointF(self.x - self.x_prev, self.y - self.y_prev)

                        for i in range(self.pjs._poly_.size()):
                            self.pjs._poly_[i] += theshift

                        # Make sure you stay within the image: first find bounding box.
                        theboundingrect = self.pjs._poly_.boundingRect()

                        thex = theboundingrect.x()
                        they = theboundingrect.y()
                        themaxx = thex + theboundingrect.width()
                        themaxy = they + theboundingrect.height()

                        # Make sure the bounding box is within the image. If not, ...
                        if thex < 0 or they < 0 or themaxx >= self.pjs.width or themaxy >= self.pjs.height:
                            theshift = QtCore.QPointF(0, 0)

                            # Shift the X and/or Y coordinates accordingly.
                            if thex < 0:
                                theshift.setX(theshift.x() - thex)
                            if themaxx >= self.pjs.width:
                                theshift.setX(theshift.x() - (themaxx - self.pjs.width + 1))
                            if they < 0:
                                theshift.setY(theshift.y() - they)
                            if themaxy >= self.pjs.height:
                                theshift.setY(theshift.y() - (themaxy - self.pjs.height + 1))

                            # This is the shift happening!
                            for i in range(self.pjs._poly_.size()):
                                self.pjs._poly_[i] += theshift

                        #self.pjs._agraphicsitem_ = self.pjs.drawPolyline(self.pjs._poly_)
                        self.pjs._agraphicsitem_.moveBy(theshift.x(), theshift.y())

                        self.pjs.repaint()

                # Update polyline as mouse button is released.
                #elif event.type() == QtCore.QEvent.MouseButtonRelease and self.pjs._poly_ != []:
                #    self.pjs._poly_ = []


            # Export polylines associated with a fiducial.
            elif self.pjs.annotation_mode == PyJAMAS.export_fiducial_polyline:
                self.process_export_fiducial_polyline(event)

            elif event.type() == QtCore.QEvent.Resize:
                self.pjs.timeSlider.setGeometry(
                    QtCore.QRect(0, self.pjs.MainWindow.height() - 43, self.pjs.MainWindow.width(), 22))
            
            # Select polyline for cropping & process.
            elif self.pjs.annotation_mode == PyJAMAS.select_polyline_crop and event.type() == QtCore.QEvent.MouseButtonPress:
                self.process_polyline_crop(event)

            # Select polyline for exporting ROI and masks.
            elif self.pjs.annotation_mode == PyJAMAS.select_polyline_exportroi and event.type() == QtCore.QEvent.MouseButtonPress:
                self.process_polyline_exportroi(event)

            # Store current position as previous (for mouse tracking).
            if event.type() in (QtCore.QEvent.MouseMove, QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonRelease):
                self.x_prev = self.x
                self.y_prev = self.y

        # CAPTURE KEYBOARD EVENTS HERE.
        elif type(source) == QtWidgets.QGraphicsView:
            # Move with the keyboard.
            if event.type() == QtCore.QEvent.KeyPress and self.x_prev > -1 and self.y_prev > -1:
                if self.pjs._agraphicsitem_ and self.pjs._poly_ != []:
                    if event.key() == QtCore.Qt.Key_Left:
                        theshift = QtCore.QPointF(- PJSEventFilter.POLYLINE_MOVE_STEP, 0)
                    elif event.key() == QtCore.Qt.Key_Right:
                        theshift = QtCore.QPointF(PJSEventFilter.POLYLINE_MOVE_STEP, 0)
                    elif event.key() == QtCore.Qt.Key_Down:
                        theshift = QtCore.QPointF(0, PJSEventFilter.POLYLINE_MOVE_STEP)
                    elif event.key() == QtCore.Qt.Key_Up:
                        theshift = QtCore.QPointF(0, - PJSEventFilter.POLYLINE_MOVE_STEP)
                    else:
                        return False

                    for i in range(self.pjs._poly_.size()):
                        self.pjs._poly_[i] += theshift

                    # Make sure you stay within the image: first find bounding box.
                    theboundingrect = self.pjs._poly_.boundingRect()

                    thex = theboundingrect.x()
                    they = theboundingrect.y()
                    themaxx = thex + theboundingrect.width()
                    themaxy = they + theboundingrect.height()

                    # Make sure the bounding box is within the image. If not, ...
                    if thex < 0 or they < 0 or themaxx >= self.pjs.width or themaxy >= self.pjs.height:
                        theshift = QtCore.QPointF(0, 0)

                        # Shift the X and/or Y coordinates accordingly.
                        if thex < 0:
                            theshift.setX(theshift.x() - thex)
                        if themaxx >= self.pjs.width:
                            theshift.setX(theshift.x() - (themaxx - self.pjs.width + 1))
                        if they < 0:
                            theshift.setY(theshift.y() - they)
                        if themaxy >= self.pjs.height:
                            theshift.setY(theshift.y() - (themaxy - self.pjs.height + 1))

                        # This is the shift happening!
                        for i in range(self.pjs._poly_.size()):
                            self.pjs._poly_[i] += theshift

                    # self.pjs._agraphicsitem_ = self.pjs.drawPolyline(self.pjs._poly_)
                    self.pjs._agraphicsitem_.moveBy(theshift.x(), theshift.y())

                    self.pjs.repaint()

                    theboundingrect = self.pjs._poly_.boundingRect()
                    self.pjs.statusbar.showMessage(
                        '{0}/{1}\t({2}, {3}) -> w: {4}, h: {5}'.format(str(self.pjs.curslice + 1),
                                                                       str(self.pjs.n_frames), str(
                                int(theboundingrect.x())), str(
                                int(theboundingrect.y())), str(int(theboundingrect.width() + 1)),
                                                                       str(int(theboundingrect.height() + 1))))

        return QtCore.QObject.eventFilter(self.pjs, source, event)

    def process_export_fiducial_polyline(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            theClickedItem = self.pjs.findGraphicItem(self.x, self.y, QtWidgets.QGraphicsEllipseItem)

            # If you found an ellipse:
            if type(theClickedItem) == QtWidgets.QGraphicsEllipseItem:
                # Get coordinates.
                pos = theClickedItem.scenePos()
                fiducial_coords = [int(pos.x() + PyJAMAS.fiducial_radius / 2),
                                   int(pos.y() + PyJAMAS.fiducial_radius / 2)]

                self.pjs.io.export_polyline_annotations(fiducial_coords[0], fiducial_coords[1])
        return True

    def process_polyline_crop(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            item_index = self.pjs.find_clicked_polyline(self.x, self.y)

            # ItemIndex of -1 means no polyline found, in which case, exit
            if item_index == -1:
                return False
            else:
                if self.pjs.crop_tracked_polyline:  # Crop tracked polyline, input index to cbCrop
                    coords = numpy.array([item_index])
                else:  # Crop polyline on this slice, input min and max coordinates to cbCrop
                    thepolyline = self.pjs.polylines[self.pjs.curslice][item_index].boundingRect()
                    minx, miny, maxx, maxy = thepolyline.getCoords()
                    coords = numpy.array([[minx, miny], [maxx, maxy]])
                self.pjs.image.cbCrop(polyline=coords, margin_size=self.pjs.margin_size)
        return True

    def process_polyline_exportroi(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            item_index = self.pjs.find_clicked_polyline(self.x, self.y)

            # ItemIndex of -1 means no polyline found, in which case, exit
            if item_index == -1:
                return False
            else:
                thepolyline = rutils.RUtils.qpolygonf2ndarray(self.pjs.polylines[self.pjs.curslice][item_index])
                self.pjs.io.cbExportROIAndMasks(polyline=thepolyline)
        return True
