#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom


# In[21]:


ctd = pd.read_csv('./csv_cleaned/wg_cleaned.csv')


# ### Definición de constantes

# In[23]:


nMeasure = 200
columnMeasure = [1]
columnLoc = [2, 3]
columnTime = 'TimeStamp'
template_name = 'WG_SV2_Result_Template'
xml_string_output = './XML_generados/InsertResultWG.xml'


# ### Modificaciones que realizar al df antes de empezar a convertirlo

# In[24]:


def create_values_result(df, columnMeasure, columnLoc, nMeasure, columnTime):
    '''
    inputs:
        nMeasure: número de medidas a introducir en el XML
        colunmMeasure: columnas que poseen las medidas
        columnLoc: columnas asociadas a la localización
        template_name: nombre de la plantilla
        xml_string_output: path de salida del XML generado
    output:
        array_list: valores en formato insertValues del XML
    '''
    
    UTC = '+00:00'
    tokenSeparator = '#'
    blockSeparator = '@'
    array_list = []
    array = ''
    
    #Conversión de formatos
    df[columnTime] = pd.to_datetime(df[columnTime], infer_datetime_format=True)

    #Creación formato de fecha
    df[columnTime] = df[columnTime].apply(lambda x: x.strftime('%Y-%m-%d') + 'T' + x.strftime('%H:%M:%S') + UTC)
    
    #Creación de los valores de la etiqueta result
    for i in np.arange(nMeasure):
        #Valores relacionados con Medidas
        measures = ctd.iloc[i][columnMeasure].values.tolist()
        measuresString = tokenSeparator.join(str(x) for x in measures)

        #Valores relacionados con Localización
        loc = ctd.iloc[i][columnLoc].values.tolist()
        locString = tokenSeparator.join(str(x) for x in loc)

        array = array + ctd.loc[i, columnTime] + tokenSeparator + measuresString + tokenSeparator + locString + blockSeparator

    array = array[:-1]
    array_list.append(array)
    
    return array_list


# In[25]:


values = create_values_result(ctd, columnMeasure, columnLoc, nMeasure, columnTime)


# ### Creación del XML insertResult

# In[26]:


#Namespaces
ET.register_namespace('sos',"http://www.opengis.net/sos/2.0") 
ET.register_namespace('xsi',"http://www.w3.org/2001/XMLSchema-instance")

#Primera etiqueta
root = ET.Element("{http://www.opengis.net/sos/2.0}InsertResult")
root.set('service', "SOS")
root.set('version', "2.0.0")
root.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation', "http://www.opengis.net/sos/2.0 http://schemas.opengis.net/sos/2.0/sos.xsd")

#Offering
ET.SubElement(root, "{http://www.opengis.net/sos/2.0}template").text = template_name
ET.SubElement(root, '{http://www.opengis.net/sos/2.0}resultValues').text = values[0]


# In[27]:


dom = xml.dom.minidom.parseString(ET.tostring(root))
xml_string = dom.toprettyxml(encoding='UTF-8')


# In[28]:


#Guardado
f = open(xml_string_output, "wb")
f.write(xml_string)
f.close()

