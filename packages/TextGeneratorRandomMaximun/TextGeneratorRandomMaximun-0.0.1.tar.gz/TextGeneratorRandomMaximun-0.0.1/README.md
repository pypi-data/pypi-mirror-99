# Proyecto de ejemplo

### Prueba de como subir un paquete a PyPi desde la consola

---

Para instalarlo simplemente ejecuta `pip install mercadona-package`

Licencia MIT LICENSE es la comun para SW Libre

`setup.py` toda la configuración del paquete

1. `pip install wheel`
   1. Crear el paquete de producción. Fichero de distribución
2. `python setup.py sdist bdist_wheel`
   1. Esto genera:
        - build
          - bdist.Tu OS desde el que lo ejecutas
          - lib: lo que instalas en tu proyecto final. Con `pip` por ejemplo
        - dist
          - tar.gz
          - whl
        - nombreProyecto.egg-into
          - egg: Lista de dependencias --> dependency_links.txt
          - PKG_INFO: todo lo que biene del setup.py
          - Sources.txt: lista de SRC
          - top_level.txt: nombre del paquete python
3. `pip install twine`
   - Herramienta para subir a los repositorios **TestPiPy** y **PyPi**
4. `twine upload --repository testpypi dist/*`

Una vez subido estará disponible e instalable a través de `pip install nombre_proyecto==version`

   - `-i https://test.pypi.org/simple`
    - Si se quiere hacer uso de la versión del paquete del entorno de test. Así, se podrá probar nuevas versiones de tu paquete sin perjudicar la versión de PRO.

