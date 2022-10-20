#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET 
import xml.dom.minidom


# ## Prueba de librería

# In[2]:


ide = 'ssf_LP_2021'
identifier = 'VOLCAN_LP_2021'
name = 'Misión Volcan La Palma Tajogaite, 2021 (mar, aire)'
point_id = 'p_LP_2021'
coor = '28.59590091661069 -17.927096990855635'
output = 'foi.xml'


# In[3]:


def createXML_FOI(ide, identifier, name, point_id, coor):
    '''
    inputs:
        ide: ID del foi
        identifier: identificador del foi
        name: Nombre de la Misión
        point_id: ID del punto del foi
        coor: coordenada del punto del foi
    output:
        root: objeto que contiene la estructura XML del foi
    '''
    
    #Namespaces
    ET.register_namespace('ifoi',"http://www.opengis.net/ifoi/1.0")
    ET.register_namespace('gml',"http://www.opengis.net/gml/3.2")
    ET.register_namespace('xlink',"http://www.w3.org/1999/xlink") 
    ET.register_namespace('om',"http://www.opengis.net/om/2.0") 
    ET.register_namespace('sams',"http://www.opengis.net/samplingSpatial/2.0")
    ET.register_namespace('sf',"http://www.opengis.net/sampling/2.0")
    ET.register_namespace('xsi',"http://www.w3.org/2001/XMLSchema-instance")

    #Primera etiqueta
    root = ET.Element("{http://www.opengis.net/ifoi/1.0}InsertFeatureOfInterest")
    root.set('service', "SOS")
    root.set('version', "2.0.0")
    root.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation', "http://www.opengis.net/ifoi/1.0 http://52north.org/schema/ifoi/1.0/InsertFeatureOfInterest.xsd http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd http://www.opengis.net/samplingSpatial/2.0 http://schemas.opengis.net/samplingSpatial/2.0/spatialSamplingFeature.xsd http://www.opengis.net/sampling/2.0 http://schemas.opengis.net/sampling/2.0/samplingFeature.xsd")
    
    #Cuerpo
    featureMember = ET.SubElement(root, "{http://www.opengis.net/ifoi/1.0}featureMember")


    SF_SpatialSamplingFeature = ET.SubElement(featureMember, 
                                              "{http://www.opengis.net/samplingSpatial/2.0}SF_SpatialSamplingFeature",
                                              {"{http://www.opengis.net/gml/3.2}id": ide})


    ET.SubElement(SF_SpatialSamplingFeature, "{http://www.opengis.net/gml/3.2}identifier",
                  {"codeSpace": " "}).text = identifier

    ET.SubElement(SF_SpatialSamplingFeature, "{http://www.opengis.net/gml/3.2}name").text = name

    ET.SubElement(SF_SpatialSamplingFeature, "{http://www.opengis.net/sampling/2.0}type",
                  {"{http://www.w3.org/1999/xlink}href": "http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingPoint"})

    ET.SubElement(SF_SpatialSamplingFeature, "{http://www.opengis.net/sampling/2.0}sampledFeature",
                  {"{http://www.w3.org/1999/xlink}href": "http://www.opengis.net/def/nil/OGC/0/unknown"})

    shape = ET.SubElement(SF_SpatialSamplingFeature, 
                          "{http://www.opengis.net/samplingSpatial/2.0}shape")

    point = ET.SubElement(shape, "{http://www.opengis.net/gml/3.2}Point", 
                          {"{http://www.opengis.net/gml/3.2}id": point_id})

    ET.SubElement(point, "{http://www.opengis.net/gml/3.2}pos", 
                  {"srsName": "http://www.opengis.net/def/crs/EPSG/0/4326"}).text = coor

    return root


# In[7]:


root = createXML_FOI(ide, identifier, name, point_id, coor)

dom = xml.dom.minidom.parseString(ET.tostring(root))
xml_string = dom.toprettyxml(encoding='UTF-8')


# In[9]:


#Guardado
f = open(output, "wb")
f.write(xml_string)
f.close()


# In[ ]:




