from qgis.PyQt import QtGui
from qgis.core import QgsProject
from PyQt5.QtCore import QFileInfo

# start a project
project = QgsProject.instance()
project_path = "/Users/yangshining/Desktop/internnnnn/IFC_summer_intern/IFC_intern_Shining/mapping_project/IDH project/Pyqgis code scripts/alb.qgz"

## load vector layer - admin boundary
uri1 = "/Users/yangshining/Desktop/internnnnn/IFC_summer_intern/IFC_intern_Shining/mapping_project/Albania/2 Raw Data/Administrative Boundaries/alb_admbnda_adm0_2019c.shp"
vec_layer = QgsVectorLayer(uri1, "countrys", "ogr") # layer name and provider name 
single_symbol_renderer = vec_layer.renderer()
symbol = single_symbol_renderer.symbol()
#Set fill colour
symbol.setColor(QColor.fromRgb(255,255,255))
QgsProject.instance().addMapLayer(vec_layer)
#Refresh
vec_layer.triggerRepaint()
iface.layerTreeView().refreshLayerSymbology(vec_layer.id())


## add csv file

# set file name
filename = "Albania_final_data_2022_0706_1km.csv"

# set file path
filepath = "/Users/yangshining/Desktop/internnnnn/IFC_summer_intern/IFC_intern_Shining/mapping_project/Albania/3 Output Data/"

# combine file path and name, prepare for uri
combine = "file:///"+filepath+filename

# build uri
uri2 = combine + "?encoding=%s&delimiter=%s&xField=%s&yField=%s&crs=%s" % ("UTF-8",",", "longitud", "lat","epsg:4326")

csv_layer = QgsVectorLayer(uri2, "final_data", "delimitedtext")

if not vec_layer.isValid():
    print ("Layer not loaded")
    
QgsProject.instance().addMapLayer(csv_layer)
# set the points invisible
QgsProject.instance().layerTreeRoot().findLayer(csv_layer).setItemVisibilityChecked(False)

## create square buffer around output points

inputfile = "final_data"
outputfile = "/Users/yangshining/Desktop/internnnnn/IFC_summer_intern/IFC_intern_Shining/mapping_project/IDH project/Pyqgis code scripts/bufferzone.shp"
bufferDist = 0.00415
Data = QgsProject.instance().mapLayersByName(inputfile)
layer = Data[0]
fields = layer.fields()
writer = QgsVectorFileWriter(outputfile, 'UTF-8', fields, QgsWkbTypes.Polygon, layer.sourceCrs(), 'ESRI Shapefile')
for f in layer.getFeatures():
    geom = f.geometry()
    buffer = geom.buffer(bufferDist, 1, QgsGeometry.CapSquare, QgsGeometry.JoinStyleMiter, 2.0)
    f.setGeometry(buffer)
    writer.addFeature(f)
    print("done")

# iface.addVectorLayer(outputfile, "GDP (PPP) per capita (percentiles)", "ogr")
del(writer)
# iface.addVectorLayer(outputfile, "GDP (PPP) percentiles", "ogr")
# iface.addVectorLayer(outputfile, "Population (percentiles)", "ogr")

