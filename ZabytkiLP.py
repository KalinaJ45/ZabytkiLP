# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ZabytkiLP
                                 A QGIS plugin
 da
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-02-02
        git sha              : $Format:%H$
        copyright            : (C) 2021 by dsd
        email                : dsd
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.core import *
from PyQt5.QtCore import QVariant, QFileInfo
from .object_kind import ObjectKindEnum
from .category_kind import CategoryKindEnum

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .ZabytkiLP_dialog import ZabytkiLPDialog
import os.path


class ZabytkiLP:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this cl
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ZabytkiLP_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Zabytki LP')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ZabytkiLP', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ZabytkiLP/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True
        

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Zabytki LP'),
                action)
            self.iface.removeToolBarIcon(action)

    
    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = ZabytkiLPDialog()

        # zmienne globalne
        savelayerPath=""
        openLayerPath=""
        fieldName=["NAZWA", "KATEG", "FUNKCJA", "CZY_ZESP", "DATOW","DOKUM","CZY_DZIER","CZY_DOST","UWAGI"]

        #funkcja "czyszcząca" pola formularza

        def clearForm():
            global savelayerPath
            savelayerPath=[]
            self.dlg.buttonGroup.setExclusive(False)
            self.dlg.buttonGroup_2.setExclusive(False)        
            self.dlg.polygonBtn.setChecked(False)
            self.dlg.pointBtn.setChecked(False)
            self.dlg.lineBtn.setChecked(False)
            self.dlg.createLayerBtn.setChecked(False)
            self.dlg.editBtn.setChecked(False)
            self.dlg.buttonGroup.setExclusive(True)
            self.dlg.buttonGroup_2.setExclusive(True)
            self.dlg.output.clear()
            self.dlg.input.clear()
            self.dlg.selectActionBox.setEnabled(True)
            self.dlg.createBox.setEnabled(False)
            self.dlg.selectActionBox.setEnabled(True)
            self.dlg.editBox.setEnabled(False)

        clearForm()
       

        # funkcja ustawiająca dostępność sekcji i przycisków przy wyborze opcji edycji obiektu
        def makeEnabled():
            if self.dlg.createLayerBtn.isChecked()== True:
                self.dlg.createBox.setEnabled(True)
                self.dlg.clearBtn.setEnabled(True)
                self.dlg.geometryBox.setEnabled(True)
                self.dlg.editBox.setEnabled(False)
               
            if self.dlg.editBtn.isChecked()== True:
                self.dlg.editBox.setEnabled(True)
                self.dlg.openBtn.setEnabled(False)
                self.dlg.clearBtn.setEnabled(True)
                self.dlg.createBox.setEnabled(False)
            
        
        
       
        # funkcja ustawiająca dostępność okna wyboru ścieżki zapisu pliku przy zmianie typu geometrii
        def makeEnabled_2():
            self.dlg.pathBox.setEnabled(True) 
            
       
        # funkcja tworząca listę funkcji zabytków w zależności od wyboru typu geometrii
        def funkcjaField():
            
            if (self.dlg.polygonBtn.isChecked()== True) or 'zabytki_powierzchniowe' in self.dlg.input.text():
                dictionary={object.value.funkcja: object.value.funkcja for object in ObjectKindEnum if 'POLYGON' in object.value.geometria}
            if (self.dlg.pointBtn.isChecked()== True) or 'zabytki_punktowe' in self.dlg.input.text():
                dictionary={object.value.funkcja: object.value.funkcja for object in ObjectKindEnum if 'POINT' in object.value.geometria}
            if (self.dlg.lineBtn.isChecked()== True) or 'zabytki_liniowe' in self.dlg.input.text():
                dictionary={object.value.funkcja: object.value.funkcja for object in ObjectKindEnum if 'LINE' in object.value.geometria}
            return dictionary

        # funkcja tworząca listę kategorii zabytków w zależności od wyboru typu geometrii

        def funkcjaFieldCategory():
            if self.dlg.polygonBtn.isChecked()== True:
                dictionary={object.value.kategoria: object.value.kategoria for object in CategoryKindEnum if 'POLYGON' in object.value.geometria}
            if self.dlg.pointBtn.isChecked()== True:
                dictionary={object.value.kategoria: object.value.kategoria for object in CategoryKindEnum if 'POINT' in object.value.geometria}
            if self.dlg.lineBtn.isChecked()== True:
                dictionary={object.value.kategoria: object.value.kategoria for object in CategoryKindEnum if 'LINE' in object.value.geometria}
            return dictionary

        
        # funkcja wyboru typu geometrii

        def geometryType():
            if self.dlg.polygonBtn.isChecked()== True:
                a=QgsWkbTypes.MultiPolygon
            if self.dlg.pointBtn.isChecked()== True:
                a=QgsWkbTypes.MultiPoint
            if self.dlg.lineBtn.isChecked()== True:
                a=QgsWkbTypes.MultiLineString
            return a

            
        # funkcja tworząca predefiniowaną nazwę tworzonej warstwy w zależności od wyboru typu gemetrii
              
        def nameFile():
            if self.dlg.polygonBtn.isChecked()== True or 'zabytki_powierzchniowe' in self.dlg.input.text():
                a="zabytki_powierzchniowe"
            if self.dlg.pointBtn.isChecked()== True or 'zabytki_punktowe' in self.dlg.input.text():
                a="zabytki_punktowe"
            if self.dlg.lineBtn.isChecked()== True or 'zabytki_liniowe' in self.dlg.input.text():
                a="zabytki_liniowe"
            return a

        # funkcja tworząca predefiniowaną nazwę tworzonej warstwy tymczasowej zawierajacej zestaw funkcji zabytków w zależności od wyboranego typu geometrii warstwy i wybranej kategorii zabytku

        def nameFunctionFile():
            if self.dlg.polygonBtn.isChecked()== True or 'zabytki_powierzchniowe' in self.dlg.input.text():
                a="Funkcje_zabytki_powierzchniowe"
            if self.dlg.pointBtn.isChecked()== True or 'zabytki_punktowe' in self.dlg.input.text():
                a="Funkcje_zabytki_punktowe"
            if self.dlg.lineBtn.isChecked()== True or 'zabytki_liniowe' in self.dlg.input.text():
                a="Funkcje_zabytki_liniowe"
            return a
            
        # funkcja do tworzenia ścieżki zapisu utworzonej warstwy

        def createLayerPath():

            global savelayerPath

            self.dlg.output.clear()
            savelayerPath = QFileDialog.getSaveFileName(None,"Wybierz lokalizację",nameFile(), "*.shp")

            if len(savelayerPath[0])==0:
                msg=QMessageBox.critical(None,"Wybierz lokalizację zapisu pliku",'Nie wybrano lokalizacji!')
            else:
                self.dlg.geometryBox.setEnabled(False) 
                self.dlg.createBtn.setEnabled(True)
                self.dlg.output.setText(savelayerPath[0])

        

        # funkcja ustawień typów widżetów

        def addStyleLayer(layer, memoryLayer):
            nonlocal fieldName
            
            fieldIndex = layer.fields().indexFromName('KATEG')
            editor_widget_setup = QgsEditorWidgetSetup( 'ValueMap', {'map': funkcjaFieldCategory()})
            layer.setEditorWidgetSetup( fieldIndex, editor_widget_setup )

          

            fieldIndex = layer.fields().indexFromName('FUNKCJA')
            editor_widget_setup = QgsEditorWidgetSetup( 'ValueRelation', {'AllowMulti': False, 'AllowNull': True, 'Description': '', 'FilterExpression': '"KATEG"=current_value(\'KATEG\')', 'Key': 'KATEG', 'LayerName': nameFunctionFile(), 'LayerProviderName': 'memory', 'NofColumns': 1, 'OrderByValue': True, 'UseCompleter': False, 'Value': 'FUNKCJA'})
            layer.setEditorWidgetSetup( fieldIndex, editor_widget_setup )

            
            for name in fieldName:
                fieldIndex = layer.fields().indexFromName(name)
                if name.startswith('CZY'):
                    editor_widget_setup = QgsEditorWidgetSetup( 'CheckBox', {'CheckedState': "TAK", 'UncheckedState': "NIE"} )
                    layer.setEditorWidgetSetup( fieldIndex, editor_widget_setup)
                if  fieldIndex!=8:
                    layer.setFieldConstraint(fieldIndex, QgsFieldConstraints.ConstraintNotNull)

        # funkcja tworząca warstwę tymczasową zawierającą zestaw funkcji zabytków w zależności od wyboranego typu geometrii warstwy i wybranej kategorii zabytku

        def createFunctionLayer():
            dictionary= funkcjaField()
            vl = QgsVectorLayer('None', nameFunctionFile(), 'memory')
            pr = vl.dataProvider()
            vl.startEditing()
            pr.addAttributes( [ QgsField("FUNKCJA", QVariant.String), QgsField("KATEG", QVariant.String)] )
            fet = QgsFeature()

            for object in ObjectKindEnum:
                for dict in dictionary:
                    if object.value.funkcja==dict:
                        fet.setAttributes([object.value.funkcja,object.value.kategoria])
                        pr.addFeatures( [ fet ] )

            vl.commitChanges()
            QgsProject.instance().addMapLayer(vl)

            return vl

        #funkcja tworząca aliasy nazw pól tworzonej warstwy
        def createFieldAlias(layer):
            nonlocal fieldName 
            alias=['Nazwa obiektu', 'Kategoria obiektu','Funkcja obiektu','Czy obiekt stanowi część zespołu?','Datowanie obiektu','Dokumenty dotyczące ewentualnej ochrony','Czy obiekt jest w dzierżawie?','Czy obiekt jest dostępny do zwiedzania?','Uwagi']
            for i in range (0, len(fieldName)):
                layer.setFieldAlias(i,alias[i])

        #funkcja określająca długość pól tworzonej warstwy

        def longOfField(name):
            long=None
            nonlocal fieldName
            if name.startswith('CZY'):
                long=3
            elif name==fieldName[0] or name==fieldName[5]:
                long=100
            elif name==fieldName[1] or name==fieldName[2] or name==fieldName[4]:
                long=50
            else:
                long=254
            return long


        #funkcja tworząca nową warstwę z zabytkami

        def createLayer():
            global savelayerPath
            nonlocal fieldName
            layerList = QgsProject.instance().mapLayersByName(nameFile())
            if layerList==[]:       
                fields = QgsFields()
                for name in fieldName:
                    fields.append(QgsField(name, QVariant.String, "text", longOfField(name)))
                crs = QgsCoordinateReferenceSystem('EPSG:2180')
                writer = QgsVectorFileWriter(savelayerPath[0], 'utf-8', fields,  geometryType(), crs, "ESRI Shapefile")
                del writer
                layer = QgsVectorLayer(savelayerPath[0], nameFile(), "ogr")
                createFieldAlias(layer)
                layer.setCrs(crs)
                QgsProject.instance().addMapLayers([layer])
                addStyleLayer(layer,createFunctionLayer())
                pathqml = savelayerPath[0][:-4]+'.qml'  
                layer.saveNamedStyle(pathqml)
                createBoxCleare()
            else:
                msg=QMessageBox.critical(None,"Utwórz inną warstwę",'Warstwa o wybranej geometrii jest już w projekcie!')
                createBoxCleare()
        
        #funkcja "czyszcząca" pola sekcji tworzenia warstwy
       
        def createBoxCleare():
            self.dlg.output.clear()
            self.dlg.geometryBox.setEnabled(True)
            self.dlg.createBtn.setEnabled(False)            
            savelayerPath == ""

        #funkcja wyboru istniejącej warstwy warstwy do edycji

        def openLayerPath():
            global openLayerPath
            self.dlg.input.clear()
            openLayerPath = QFileDialog.getOpenFileName(None, "Wybierz plik shapefile", "", "Shapefile (*.shp)")


            if len(openLayerPath[0])==0:
                msg=QMessageBox.critical(None,"Wybierz plik shapefile",'Nie wybrano pliku shapefile!')
            else:   
                
                self.dlg.input.setText(openLayerPath[0])
                if 'zabytki_powierzchniowe' in self.dlg.input.text() or 'zabytki_punktowe' in self.dlg.input.text() or 'zabytki_liniowe' in self.dlg.input.text():
                    self.dlg.openBtn.setEnabled(True)
                else: 
                    msg=QMessageBox.critical(None,"Wybierz prawidłowy plik shapefile",'Wybrano nieprawidłowy shapefile!')
                

        #funkcja otworzenia w projekcie istniejącej warstwy do edycji

        def openLayer():
            global openLayerPath
            layerList = QgsProject.instance().mapLayersByName(nameFile())
            if layerList==[]:
                openedLayer = QgsVectorLayer(openLayerPath[0], nameFile(), "ogr")
                crs = QgsCoordinateReferenceSystem('EPSG:2180')
                openedLayer.setCrs(crs)
                QgsProject.instance().addMapLayers([openedLayer])
                createFunctionLayer()
                self.dlg.input.clear()
                self.dlg.openBtn.setEnabled(False) 
            else:
                msg=QMessageBox.critical(None,"Wybierz inny plik shapefile",'Wybrany plik jest już otwarty w projekcie!')
                self.dlg.input.clear() 
                self.dlg.openBtn.setEnabled(False)      

       
                   

        
              

        def close():
            clearForm()
            self.dlg.close()

        #przypisanie funkcji elementom formularza

        self.dlg.createBtn.clicked.connect(createLayer)
        self.dlg.closeBtn.clicked.connect(close)
        self.dlg.outputBtn.clicked.connect(createLayerPath)
        self.dlg.clearBtn.clicked.connect(clearForm)
        self.dlg.inputBtn.clicked.connect(openLayerPath)
        self.dlg.openBtn.clicked.connect(openLayer)
        self.dlg.pointBtn.toggled.connect(makeEnabled_2)
        self.dlg.lineBtn.toggled.connect(makeEnabled_2)
        self.dlg.polygonBtn.toggled.connect(makeEnabled_2)    
        self.dlg.createLayerBtn.toggled.connect(makeEnabled)
        self.dlg.editBtn.toggled.connect(makeEnabled)
        

         # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

       
        
        
