from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import logging
logger = logging.getLogger(__name__)

from dune.common.checkconfiguration import assertHave, ConfigurationError

try:
    assertHave("HAVE_DUNE_ALUGRID")

    def _module(includes, typeName, defaultGrid, *args, **kwargs):

        module = None
        if defaultGrid is not None:
            # try to load default module
            try:
                import importlib
                module = importlib.import_module( "dune.alugrid."+defaultGrid )
            except ImportError:
                module = None

        if module is None:
            # generate module code, compile and load
            try:
                generator = kwargs.pop("generator")
            except KeyError:
                from dune.generator.generator import SimpleGenerator
                generator = SimpleGenerator("HierarchicalGrid", "Dune::Python")

            from dune.common.hashit import hashIt
            includes = includes + ["dune/python/grid/hierarchical.hh"]
            typeHash = "hierarchicalgrid_" + hashIt(typeName)
            module = generator.load(includes, typeName, typeHash, *args, **kwargs)

        from dune.grid.grid_generator import addAttr, levelView, persistentContainer
        addAttr(module, module.LeafGrid)

        # register reference element for this grid
        import dune.geometry
        for d in range(module.LeafGrid.dimension+1):
            dune.geometry.module(d)
        setattr(module.HierarchicalGrid,"levelView",levelView)
        setattr(module.HierarchicalGrid,"persistentContainer",persistentContainer)
        return module


    def aluGrid(constructor, dimgrid=None, dimworld=None, elementType=None, comm=None, serial=False, **parameters):
        from dune.grid.grid_generator import module, getDimgrid

        if not dimgrid:
            dimgrid = getDimgrid(constructor)

        if dimworld is None:
            dimworld = dimgrid
        if elementType is None:
            elementType = parameters.pop("type")
        refinement = parameters["refinement"]

        if refinement == "conforming":
            refinement="Dune::conforming"
        elif refinement == "nonconforming":
            refinement="Dune::nonconforming"

        if not (2 <= dimgrid and dimgrid <= dimworld):
            raise KeyError("Parameter error in ALUGrid with dimgrid=" + str(dimgrid) + ": dimgrid has to be either 2 or 3")
        if not (2 <= dimworld and dimworld <= 3):
            raise KeyError("Parameter error in ALUGrid with dimworld=" + str(dimworld) + ": dimworld has to be either 2 or 3")
        if refinement=="Dune::conforming" and elementType=="Dune::cube":
            raise KeyError("Parameter error in ALUGrid with refinement=" + refinement + " and type=" + elementType + ": conforming refinement is only available with simplex element type")

        typeName = "Dune::ALUGrid< " + str(dimgrid) + ", " + str(dimworld) + ", " + elementType + ", " + refinement
        # if serial flag is true serial version is forced.
        if serial:
            typeName += ", Dune::ALUGridNoComm"

        typeName += " >"
        includes = ["dune/alugrid/grid.hh", "dune/alugrid/dgf.hh"]

        if dimgrid == dimworld and serial == False:
            _, _, shortElType  = elementType.partition('::')
            _, _, shortRefType = refinement.partition('::')
            defaultGrid = '_defaultalu' + shortElType + shortRefType + str(dimgrid) + str(dimworld)
        else:
            defaultGrid = None
        gridModule = _module(includes, typeName, defaultGrid)

        if comm is not None:
            raise Exception("Passing communicator to grid construction is not yet implemented in Python bindings of dune-grid")
            return gridModule.LeafGrid(gridModule.reader(constructor, comm))
        else:
            return gridModule.LeafGrid(gridModule.reader(constructor))


    def aluConformGrid(constructor, dimgrid=None, dimworld=None, comm=None, serial=False, **parameters):
        return aluGrid(constructor, dimgrid, dimworld, elementType="Dune::simplex", refinement="Dune::conforming", comm=comm, serial=serial)


    def aluCubeGrid(constructor, dimgrid=None, dimworld=None, comm=None, serial=False, **parameters):
        return aluGrid(constructor, dimgrid, dimworld, elementType="Dune::cube", refinement="Dune::nonconforming", comm=comm, serial=serial)


    def aluSimplexGrid(constructor, dimgrid=None, dimworld=None, comm=None, serial=False, **parameters):
        return aluGrid(constructor, dimgrid, dimworld, elementType="Dune::simplex", refinement="Dune::nonconforming", comm=comm, serial=serial)

    grid_registry = {
            "ALU"        : aluGrid,
            "ALUConform" : aluConformGrid,
            "ALUCube" :    aluCubeGrid,
            "ALUSimplex" : aluSimplexGrid,
        }
except ConfigurationError:
    grid_registry = {}
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
