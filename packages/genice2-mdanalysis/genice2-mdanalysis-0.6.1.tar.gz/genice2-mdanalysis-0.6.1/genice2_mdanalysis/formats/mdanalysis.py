# coding: utf-8
"""
Write the ice structure in various file formats with the help of MDAnalysis.

Usage:
    % genice 1c -f mdanalysis > 1c.pickle
    % genice 1c -f mdanalysis[1c.gro]
    % genice 1c -f mdanalysis[1c.xtc]

Options:
    filename  The file name to be written. The file type is specified by the
              suffix. All the [file types supported by MDAnalysis](https://docs.mdanalysis.org/stable/documentation_pages/coordinates/init.html) 
              are available. 
              If the file name is not specified, the Universe instance of
              MDAnalysis is written to the stdout in the python pickle
              format.

"""
desc={"ref": {"MDanalysis": "https://github.com/MDAnalysis/mdanalysis"},
      "brief": "MDAnalysis integration.",
      "usage": __doc__}


# from collections import defaultdict
from logging import getLogger
import numpy as np
from genice2.decorators import timeit, banner
import genice2.formats
import MDAnalysis as mda
from genice2.cell import cellshape
from genice2.molecules  import serialize

class Format(genice2.formats.Format):
    """
Make a Universe for MDAnalysis. 

Options:
    filename   The file name to be written. If not specified, the universe will
               be written to the stdout in the python pickle format.
    """


    def __init__(self, **kwargs):
        unknown = dict()
        self.filename = None
        jupyter = False
        for k, v in kwargs.items():
            assert self.filename is None
            assert v
            self.filename = k
        super().__init__(**unknown)


    def hooks(self):
        return {7:self.Hook7}

    @timeit
    @banner
    def Hook7(self, ice):
        "Process all molecules."

        logger = getLogger()
        
        atoms = []
        for mols in ice.universe:
            atoms += serialize(mols)
        
        n_atoms  = len(atoms)
        atomnames = [row[2] for row in atoms]
        atom_resindex = []
        resnames      = []
        n_residues = 0
        last=-1
        for atom in atoms:
            if last != atom[4]:
                n_residues += 1
                last       =  atom[4]
                resnames.append(atom[1])
            atom_resindex.append(n_residues-1)
        universe = mda.Universe.empty(n_atoms=n_atoms,
                                      n_residues=n_residues,
                                      atom_resindex=atom_resindex,
                                      trajectory=True,)
        universe.add_TopologyAttr('name',    atomnames)
        universe.add_TopologyAttr('type',    atomnames)
        universe.add_TopologyAttr('resids',  [x+1 for x in range(n_residues)])
        universe.add_TopologyAttr('resname', resnames)
        universe.atoms.positions = np.array([row[3] for row in atoms])*10 # AA
        # cellは?
        universe.dimensions = cellshape(ice.repcell.mat*10)
        
        if self.filename is None:
            self.output = universe
        else:
            allatoms = universe.select_atoms("all")
            allatoms.write(self.filename)
            self.output = ""
