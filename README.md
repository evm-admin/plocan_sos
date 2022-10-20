# Repositorio SOS de 52ºNorth - PLOCAN 🌊

Repositorio que contiene los ficheros necesarios para la inserción de sensores y observaciones.

## Estructura del repositorio 📜

- **[/xml](https://github.com/evm-admin/plocan_sos/tree/main/xml)**:
  - **[/01_example_WG_SV2](https://github.com/evm-admin/plocan_sos/tree/main/xml/01_example_WG_SV2)**: Carpeta que contiene todos los ficheros XML necesarios para insertar en el servicio SOS el caso de estudio.

- **[/scripts](https://github.com/evm-admin/plocan_sos/tree/main/scripts)**:
  - **[/etl.py](https://github.com/evm-admin/plocan_sos/tree/main/scripts/etl.py)**: Limpieza de ficheros proporcionados por PLOCAN y guardado de ficheros CSV por cada proceso físico del caso de estudio.
  - **[/xml_creation_foi.py](https://github.com/evm-admin/plocan_sos/tree/main/scripts/xml_creation_foi.py)**: Creación del XML del FeatureOfInterest necesario para el caso de estudio.
  - **[/xml_creation_result.py](https://github.com/evm-admin/plocan_sos/tree/main/scripts/xml_creation_result.py)**: Creación del XML del InsertResult necesario para el caso de estudio.
