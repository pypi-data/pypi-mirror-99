# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020-2021, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
"""
"""
from . import utils
from .exceptions import UndefinedChemical
from ._chemical import Chemical
from .indexer import ChemicalIndexer
import thermosteam as tmo
import numpy as np

__all__ = ('Chemicals', 'CompiledChemicals')
setattr = object.__setattr__

# %% Functions

def must_compile(*args, **kwargs): # pragma: no cover
    raise TypeError("method valid only for compiled chemicals; "
                    "run <Chemicals>.compile() to compile")

def chemical_data_array(chemicals, attr, dtype=float):
    getfield = getattr
    data = np.asarray([getfield(i, attr) for i in chemicals], dtype)
    data.setflags(0)
    return data
    

# %% Chemicals

class Chemicals:
    """
    Create a Chemicals object that contains Chemical objects as attributes.

    Parameters
    ----------
    chemicals : Iterable[str or :class:`~thermosteam.Chemical`]
        Strings should be one of the following [-]:
           * Name, in IUPAC form or common form or a synonym registered in PubChem
           * InChI name, prefixed by 'InChI=1S/' or 'InChI=1/'
           * InChI key, prefixed by 'InChIKey='
           * PubChem CID, prefixed by 'PubChem='
           * SMILES (prefix with 'SMILES=' to ensure smiles parsing)
           * CAS number
    cache : bool, optional
        Wheather or not to use cached chemicals.
    
    Examples
    --------
    Create a Chemicals object from chemical identifiers:
    
    >>> from thermosteam import Chemicals
    >>> chemicals = Chemicals(['Water', 'Ethanol'], cache=True)
    >>> chemicals
    Chemicals([Water, Ethanol])
    
    All chemicals are stored as attributes:
        
    >>> chemicals.Water, chemicals.Ethanol
    (Chemical('Water'), Chemical('Ethanol'))
    
    Chemicals can also be accessed as items:
    
    >>> chemicals = Chemicals(['Water', 'Ethanol', 'Propane'], cache=True)
    >>> chemicals['Ethanol']
    Chemical('Ethanol')
    >>> chemicals['Propane', 'Water']
    [Chemical('Propane'), Chemical('Water')]
    
    A Chemicals object can be extended with more chemicals:
        
    >>> from thermosteam import Chemical
    >>> Methanol = Chemical('Methanol')
    >>> chemicals.append(Methanol)
    >>> chemicals
    Chemicals([Water, Ethanol, Propane, Methanol])
    >>> new_chemicals = Chemicals(['Hexane', 'Octanol'], cache=True)
    >>> chemicals.extend(new_chemicals)
    >>> chemicals
    Chemicals([Water, Ethanol, Propane, Methanol, Hexane, Octanol])
    
    Chemical objects cannot be repeated:
    
    >>> chemicals.append(chemicals.Water)
    Traceback (most recent call last):
    ValueError: Water already defined in chemicals
    >>> chemicals.extend(chemicals['Ethanol', 'Octanol'])
    Traceback (most recent call last):
    ValueError: Ethanol already defined in chemicals
    
    A Chemicals object can only contain Chemical objects:
        
    >>> chemicals.append(10)
    Traceback (most recent call last):
    TypeError: only 'Chemical' objects can be appended, not 'int'
    
    You can check whether a Chemicals object contains a given chemical:
        
    >>> 'Water' in chemicals
    True
    >>> chemicals.Water in chemicals
    True
    >>> 'Butane' in chemicals
    False
    
    An attempt to access a non-existent chemical raises an UndefinedChemical error:
    
    >>> chemicals['Butane']
    Traceback (most recent call last):
    UndefinedChemical: 'Butane'
    
    """
    def __new__(cls, chemicals, cache=False):
        self = super().__new__(cls)
        isa = isinstance
        setfield = setattr
        CASs = set()
        chemicals = [i if isa(i, Chemical) else Chemical(i, cache=cache) for i in chemicals]
        for i in chemicals:
            CAS = i.CAS
            if CAS in CASs: continue
            CASs.add(CAS)
            setfield(self, i.ID, i)
        return self
    
    def __getnewargs__(self):
        return (tuple(self),)
    
    def __setattr__(self, ID, chemical):
        raise TypeError("can't set attribute; use <Chemicals>.append instead")
    
    def __setitem__(self, ID, chemical):
        raise TypeError("can't set item; use <Chemicals>.append instead")
    
    def __getitem__(self, key):
        """
        Return a chemical or a list of chemicals.
        
        Parameters
        ----------
        key : Iterable[str] or str
              Chemical identifiers.
        
        """
        dct = self.__dict__
        try:
            if isinstance(key, str):
                return dct[key]
            else:
                return [dct[i] for i in key]
        except KeyError as key_error:
            raise UndefinedChemical(key_error.args[0])
    
    def copy(self):
        """Return a copy."""
        copy = object.__new__(Chemicals)
        for chem in self: setattr(copy, chem.ID, chem)
        return copy
    
    def append(self, chemical):
        """Append a Chemical."""
        if not isinstance(chemical, Chemical):
            raise TypeError("only 'Chemical' objects can be appended, "
                           f"not '{type(chemical).__name__}'")
        ID = chemical.ID
        if ID in self.__dict__:
            raise ValueError(f"{ID} already defined in chemicals")
        setattr(self, ID, chemical)
    
    def extend(self, chemicals):
        """Extend with more Chemical objects."""
        if isinstance(chemicals, Chemicals):
            self.__dict__.update(chemicals.__dict__)
        else:
            for chemical in chemicals: self.append(chemical)
    
    def subgroup(self, IDs):
        """
        Create a new subgroup of chemicals.
        
        Parameters
        ----------
        IDs : Iterable[str]
              Chemical identifiers.
              
        Examples
        --------
        
        >>> chemicals = Chemicals(['Water', 'Ethanol', 'Propane'])
        >>> chemicals.subgroup(['Propane', 'Water'])
        Chemicals([Propane, Water])
        
        """
        return type(self)([getattr(self, i) for i in IDs])
    
    def compile(self, skip_checks=False):
        """
        Cast as a CompiledChemicals object.
        
        Parameters
        ----------
        skip_checks : bool, optional
            Whether to skip checks for missing or invalid properties.
            
        Warning
        -------
        If checks are skipped, certain features in thermosteam (e.g. phase equilibrium)
        cannot be guaranteed to function properly. 
        
        Examples
        --------
        Compile ethanol and water chemicals:
        
        >>> import thermosteam as tmo
        >>> chemicals = tmo.Chemicals(['Water', 'Ethanol'])
        >>> chemicals.compile()
        >>> chemicals
        CompiledChemicals([Water, Ethanol])
        
        Attempt to compile chemicals with missing properties:
            
        >>> Substance = tmo.Chemical('Substance', search_db=False)
        >>> chemicals = tmo.Chemicals([Substance])
        >>> chemicals.compile()
        Traceback (most recent call last):
        RuntimeError: Substance is missing key thermodynamic properties 
        (V, S, H, Cn, Psat, Tb and Hvap); use the `<Chemical>.get_missing_properties()` 
        to check all missing properties
        
        Compile chemicals with missing properties (skipping checks) and note 
        how certain features do not work:
        
        >>> chemicals.compile(skip_checks=True)
        >>> tmo.settings.set_thermo(chemicals)
        >>> s = tmo.Stream('s', Substance=10)
        >>> s.rho
        Traceback (most recent call last):
        DomainError: Substance (CAS: Substance) has no valid liquid molar 
        volume model at T=298.15 K and P=101325 Pa
        
        """
        chemicals = tuple(self)
        setattr(self, '__class__', CompiledChemicals)
        try: self._compile(chemicals, skip_checks)
        except Exception as error:
            setattr(self, '__class__', Chemicals)
            setattr(self, '__dict__', {i.ID: i for i in chemicals})
            raise error
    
    kwarray = array = index = indices = must_compile
        
    def show(self):
        print(self)
    _ipython_display_ = show
    
    def __len__(self):
        return len(self.__dict__)
    
    def __contains__(self, chemical):
        if isinstance(chemical, str):
            return chemical in self.__dict__
        elif isinstance(chemical, Chemical):
            return chemical in self.__dict__.values()
        else: # pragma: no cover
            return False
    
    def __iter__(self):
        yield from self.__dict__.values()
    
    def __repr__(self):
        return f"{type(self).__name__}([{', '.join(self.__dict__)}])"


@utils.read_only(methods=('append', 'extend', '__setitem__'))
class CompiledChemicals(Chemicals):
    """
    Create a CompiledChemicals object that contains Chemical objects as attributes.

    Parameters
    ----------
    chemicals : Iterable[str or Chemical]
           Strings should be one of the following [-]:
              * Name, in IUPAC form or common form or a synonym registered in PubChem
              * InChI name, prefixed by 'InChI=1S/' or 'InChI=1/'
              * InChI key, prefixed by 'InChIKey='
              * PubChem CID, prefixed by 'PubChem='
              * SMILES (prefix with 'SMILES=' to ensure smiles parsing)
              * CAS number
    cache : optional
        Whether or not to use cached chemicals.
        
    Attributes
    ----------
    tuple : tuple[Chemical]
            All compiled chemicals.
    size : int
           Number of chemicals.
    IDs : tuple[str]
          IDs of all chemicals.
    CASs : tuple[str]
           CASs of all chemicals
    MW : 1d ndarray
         MWs of all chemicals.
    Hf : 1d ndarray
         Heats of formation of all chemicals.
    Hc : 1d ndarray
         Heats of combustion of all chemicals.
    vle_chemicals : tuple[Chemical]
        Chemicals that may have vapor and liquid phases.
    lle_chemicals : tuple[Chemical]
        Chemicals that may have two liquid phases.
    heavy_chemicals : tuple[Chemical]
        Chemicals that are only present in liquid or solid phases.
    light_chemicals : tuple[Chemical]
        IDs of chemicals that are only present in gas phases.
        
    Examples
    --------
    Create a CompiledChemicals object from chemical identifiers
    
    >>> from thermosteam import CompiledChemicals, Chemical
    >>> chemicals = CompiledChemicals(['Water', 'Ethanol'], cache=True)
    >>> chemicals
    CompiledChemicals([Water, Ethanol])
    
    All chemicals are stored as attributes:
        
    >>> chemicals.Water, chemicals.Ethanol
    (Chemical('Water'), Chemical('Ethanol'))
    
    Note that because they are compiled, the append and extend methods do not work:
        
    >>> Propane = Chemical('Propane', cache=True)
    >>> chemicals.append(Propane)
    Traceback (most recent call last):
    TypeError: 'CompiledChemicals' object is read-only
    
    You can check whether a Chemicals object contains a given chemical:
        
    >>> 'Water' in chemicals
    True
    >>> chemicals.Water in chemicals
    True
    >>> 'Butane' in chemicals
    False
    
    """  
    _cache = {}
    
    def __new__(cls, chemicals, cache=None):
        chemicals = tmo.Chemicals(chemicals)
        chemicals_tuple = tuple(chemicals) 
        cache = cls._cache
        if chemicals in cache:
            self = cache[chemicals]
        else:
            chemicals.compile(cache)
            self = cache[chemicals_tuple] = chemicals
        return self
    
    def __dir__(self):
        return ('append', 'array', 'compile', 'extend', 
                'get_combustion_reactions', 'get_index',
                'get_lle_indices', 'get_synonyms',
                'get_vle_indices', 'iarray', 'ikwarray',
                'index', 'indices', 'kwarray', 'refresh_constants', 
                'set_synonym', 'subgroup') + self.IDs
    
    def __reduce__(self):
        return CompiledChemicals, (self.tuple,)
    
    def compile(self, skip_checks=False):
        """Do nothing, CompiledChemicals objects are already compiled.""" 
    
    def refresh_constants(self):
        """
        Refresh constant arrays according to their chemical values,
        including the molecular weight, heats of formation,
        and heats of combustion.
        
        """
        dct = self.__dict__
        chemicals = self.tuple
        dct['MW'] = chemical_data_array([i.MW for i in chemicals])
        dct['Hf'] = chemical_data_array([i.Hf for i in chemicals])
        dct['LHV'] = chemical_data_array([i.LHV for i in chemicals])
        dct['HHV'] = chemical_data_array([i.HHV for i in chemicals])

    def get_combustion_reactions(self):
        """
        Return a ParallelReactions object with all defined combustion reactions.
        
        Examples
        --------
        >>> chemicals = CompiledChemicals(['H2O', 'Methanol', 'Ethanol', 'CO2', 'O2'], cache=True)
        >>> rxns = chemicals.get_combustion_reactions()
        >>> rxns.show()
        ParallelReaction (by mol):
        index  stoichiometry                     reactant    X[%]
        [0]    Methanol + 1.5 O2 -> 2 H2O + CO2  Methanol  100.00
        [1]    Ethanol + 3 O2 -> 3 H2O + 2 CO2   Ethanol   100.00
        
        """
        reactions = [i.get_combustion_reaction(self) for i in self]
        return tmo.reaction.ParallelReaction([i for i in reactions if i is not None])

    def _compile(self, chemicals, skip_checks=False):
        dct = self.__dict__
        tuple_ = tuple
        free_energies = ('H', 'S', 'H_excess', 'S_excess')
        for chemical in chemicals:
            if chemical.get_missing_properties(free_energies):
                chemical.reset_free_energies()
            if skip_checks: continue
            key_properties = chemical.get_key_property_names()
            missing_properties = chemical.get_missing_properties(key_properties)
            if not missing_properties: continue
            missing = utils.repr_listed_values(missing_properties)
            raise RuntimeError(
                f"{chemical} is missing key thermodynamic properties ({missing}); "
                "use the `<Chemical>.get_missing_properties()` to check "
                "all missing properties")
        IDs = tuple_([i.ID for i in chemicals])
        CAS = tuple_([i.CAS for i in chemicals])
        size = len(IDs)
        index = tuple_(range(size))
        for i in chemicals: dct[i.CAS] = i
        dct['tuple'] = chemicals
        dct['size'] = size
        dct['IDs'] = IDs
        dct['CASs'] = tuple_([i.CAS for i in chemicals])
        dct['MW'] = chemical_data_array(chemicals, 'MW')
        dct['Hf'] = chemical_data_array(chemicals, 'Hf')
        dct['LHV'] = chemical_data_array(chemicals, 'LHV')
        dct['HHV'] = chemical_data_array(chemicals, 'HHV')
        dct['_index'] = index = dict((*zip(CAS, index),
                                      *zip(IDs, index)))
        dct['_index_cache'] = {}
        repeated_names = set()
        names = set()
        all_names_list = []
        for i in chemicals:
            if not i.iupac_name: i.iupac_name = ()
            all_names = set([*i.iupac_name, *i.synonyms, i.common_name, i.formula])
            all_names_list.append(all_names)
            for name in all_names:
                if not name: continue
                if name in names:
                    repeated_names.add(name)
                else:
                    names.add(name)
        for all_names, i in zip(all_names_list, chemicals):
            ID = i.ID
            for name in all_names:
                if name and name not in repeated_names:
                    self.set_synonym(ID, name)
        vle_chemicals = []
        lle_chemicals = []
        heavy_chemicals = []
        light_chemicals = []
        for i in chemicals:
            locked_phase = i.locked_state
            if locked_phase:
                if locked_phase in ('s', 'l'):
                    heavy_chemicals.append(i)
                    if i.Dortmund or i.UNIFAC or i.NIST or i.PSRK:
                        lle_chemicals.append(i)
                    if i.N_solutes is None: i._N_solutes = 0
                elif locked_phase == 'g':
                    light_chemicals.append(i)
                else:
                    raise Exception('chemical locked state has an invalid phase')
            else:
                vle_chemicals.append(i)
                lle_chemicals.append(i)
        dct['vle_chemicals'] = tuple_(vle_chemicals)
        dct['lle_chemicals'] = tuple_(lle_chemicals)
        dct['heavy_chemicals'] = tuple_(heavy_chemicals)
        dct['light_chemicals'] = tuple_(light_chemicals)
        dct['_has_vle'] = has_vle = np.zeros(size, dtype=bool)
        dct['_has_lle'] = has_lle = np.zeros(size, dtype=bool)
        dct['_heavy_solutes'] = chemical_data_array(heavy_chemicals, 'N_solutes')
        dct['_heavy_indices'] = [index[i.ID] for i in heavy_chemicals]
        dct['_light_indices'] = [index[i.ID] for i in light_chemicals]
        vle_index = [index[i.ID] for i in vle_chemicals]
        lle_index = [index[i.ID] for i in lle_chemicals]
        has_vle[vle_index] = True
        has_lle[lle_index] = True
        
    @property
    def formula_array(self):
        """
        An array describing the formulas of all chemicals.
        Each column is a chemical and each row an element.
        Rows are ordered by atomic number.
        
        Examples
        --------
        >>> chemicals = CompiledChemicals(['Water', 'Ethanol', 'Propane'], cache=True)
        >>> chemicals.formula_array
        array([[2., 6., 8.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 2., 3.],
               [0., 0., 0.],
               [1., 1., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.]])
        """
        try: return self._formula_array
        except: pass
        self.__dict__['_formula_array'] = formula_array = np.zeros((118, self.size))
        atoms_to_array = tmo.chemicals.elements.atoms_to_array
        for i, chemical in enumerate(self):
            formula_array[:, i] = atoms_to_array(chemical.atoms)
        formula_array.setflags(0)
        return formula_array
    
    def subgroup(self, IDs):
        """
        Create a new subgroup of chemicals.
        
        Parameters
        ----------
        IDs : Iterable[str]
              Chemical identifiers.
              
        Examples
        --------
        >>> chemicals = CompiledChemicals(['Water', 'Ethanol', 'Propane'], cache=True)
        >>> chemicals.subgroup(['Propane', 'Water'])
        CompiledChemicals([Propane, Water])
        
        """
        chemicals = self[IDs]
        new = Chemicals(chemicals)
        new.compile()
        for i in new.IDs:
            for j in self.get_synonyms(i):
                try: new.set_synonym(i, j)
                except: pass
        return new
    
    def get_parsable_synonym(self, ID):
        """
        Return a synonym of the given chemical identifier that can be 
        parsed by Python as a variable name
        
        Parameters
        ----------
        ID : str
            Chemical identifier.
            
        Examples
        --------
        Get parsable synonym of 2,3-Butanediol:
        
        >>> from thermosteam import CompiledChemicals
        >>> chemicals = CompiledChemicals(['2,3-Butanediol'], cache=True)
        >>> chemicals.get_parsable_synonym('2,3-Butanediol')
        'C4H10O2'
        
        """
        isvalid = utils.is_valid_ID      
        for i in self.get_synonyms(ID):
            if isvalid(i): return i        
    
    def get_synonyms(self, ID):
        """
        Return all synonyms of a chemical.
        
        Parameters
        ----------
        ID : str
            Chemical identifier.
            
        Examples
        --------
        Get all synonyms of water:
        
        >>> from thermosteam import CompiledChemicals
        >>> chemicals = CompiledChemicals(['Water'], cache=True)
        >>> synonyms = chemicals.get_synonyms('Water')
        >>> synonyms.sort()
        >>> synonyms
        ['7732-18-5', 'H2O', 'Water', 'oxidane', 'water']
        
        """
        k = self._index[ID]
        return [i for i, j in self._index.items() if j==k] 

    def set_synonym(self, ID, synonym):
        """
        Set a new synonym for a chemical.
        
        Parameters
        ----------
        ID : str
            Chemical identifier.
        synonym : str
            New identifier for chemical.
            
        Examples
        --------
        Set new synonym for water:
        
        >>> from thermosteam import CompiledChemicals
        >>> chemicals = CompiledChemicals(['Water', 'Ethanol'], cache=True)
        >>> chemicals.set_synonym('Water', 'H2O')
        >>> chemicals.H2O is chemicals.Water
        True
        
        Note that you cannot use one synonym for two chemicals:
        
        >>> chemicals.set_synonym('Ethanol', 'H2O')
        Traceback (most recent call last):
        ValueError: synonym 'H2O' already in use by Chemical('Water')
        
        """
        chemical = getattr(self, ID)
        dct = self.__dict__
        if synonym in dct and dct[synonym] is not chemical:
            raise ValueError(f"synonym '{synonym}' already in use by {repr(dct[synonym])}")
        else:
            self._index[synonym] = self._index[ID]
            dct[synonym] = chemical
        chemical.synonyms.add(synonym)
    
    def zeros(self):
        """
        Return an array of zeros with entries that correspond to the orded chemical IDs.
        
        Examples
        --------
        >>> from thermosteam import CompiledChemicals
        >>> chemicals = CompiledChemicals(['Water', 'Ethanol'], cache=True)
        >>> chemicals.zeros()
        array([0., 0.])
        
        """
        return np.zeros(self.size) 
    
    def ones(self):
        """
        Return an array of ones with entries that correspond to the orded chemical IDs.
        
        Examples
        --------
        >>> from thermosteam import CompiledChemicals
        >>> chemicals = CompiledChemicals(['Water', 'Ethanol'], cache=True)
        >>> chemicals.ones()
        array([1., 1.])
        
        """
        return np.ones(self.size) 
    
    def kwarray(self, ID_data):
        """
        Return an array with entries that correspond to the orded chemical IDs.
        
        Parameters
        ----------
        ID_data : dict
                 ID-data pairs.
            
        Examples
        --------
        >>> from thermosteam import CompiledChemicals
        >>> chemicals = CompiledChemicals(['Water', 'Ethanol'], cache=True)
        >>> chemicals.kwarray(dict(Water=2))
        array([2., 0.])
        
        """
        return self.array(*zip(*ID_data.items()))
    
    def array(self, IDs, data):
        """
        Return an array with entries that correspond to the ordered chemical IDs.
        
        Parameters
        ----------
        IDs : iterable
              Compound IDs.
        data : array_like
               Data corresponding to IDs.
            
        Examples
        --------
        >>> from thermosteam import CompiledChemicals
        >>> chemicals = CompiledChemicals(['Water', 'Ethanol'], cache=True)
        >>> chemicals.array(['Water'], [2])
        array([2., 0.])
        
        """
        array = self.zeros()
        array[self.get_index(tuple(IDs))] = data
        return array

    def iarray(self, IDs, data):
        """
        Return a chemical indexer.
        
        Parameters
        ----------
        IDs : iterable
              Chemical IDs.
        data : array_like
               Data corresponding to IDs.
            
        Examples
        --------
        Create a chemical indexer from chemical IDs and data:
        
        >>> from thermosteam import CompiledChemicals
        >>> chemicals = CompiledChemicals(['Water', 'Methanol', 'Ethanol'], cache=True)
        >>> chemical_indexer = chemicals.iarray(['Water', 'Ethanol'], [2., 1.])
        >>> chemical_indexer.show()
        ChemicalIndexer:
         Water    2
         Ethanol  1
        
        Note that indexers allow for computationally efficient indexing using identifiers:
            
        >>> chemical_indexer['Ethanol', 'Water']
        array([1., 2.])
        >>> chemical_indexer['Ethanol']
        1.0
        
        """
        array = self.array(IDs, data)
        return ChemicalIndexer.from_data(array, chemicals=self)

    def ikwarray(self, ID_data):
        """
        Return a chemical indexer.
        
        Parameters
        ----------
        ID_data : Dict[str: float]
              Chemical ID-value pairs.
            
        Examples
        --------
        Create a chemical indexer from chemical IDs and data:
        
        >>> from thermosteam import CompiledChemicals
        >>> chemicals = CompiledChemicals(['Water', 'Methanol', 'Ethanol'], cache=True)
        >>> chemical_indexer = chemicals.ikwarray(dict(Water=2., Ethanol=1.))
        >>> chemical_indexer.show()
        ChemicalIndexer:
         Water    2
         Ethanol  1
        
        Note that indexers allow for computationally efficient indexing using identifiers:
            
        >>> chemical_indexer['Ethanol', 'Water']
        array([1., 2.])
        >>> chemical_indexer['Ethanol']
        1.0
        
        """
        array = self.kwarray(ID_data)
        return ChemicalIndexer.from_data(array, chemicals=self)

    def isplit(self, split, order=None):
        """
        Create a chemical indexer that represents chemical splits.
    
        Parameters
        ----------   
        split : Should be one of the following
                * [float] Split fraction
                * [array_like] Componentwise split 
                * [dict] ID-split pairs
        order=None : Iterable[str], options
            Chemical order of split. Defaults to biosteam.settings.chemicals.IDs
           
        Examples
        --------
        From a dictionary:
        
        >>> from thermosteam import CompiledChemicals
        >>> chemicals = CompiledChemicals(['Water', 'Methanol', 'Ethanol'], cache=True)
        >>> chemical_indexer = chemicals.isplit(dict(Water=0.5, Ethanol=1.))
        >>> chemical_indexer.show()
        ChemicalIndexer:
         Water    0.5
         Ethanol  1
        
        From iterable given the order:
        
        >>> chemical_indexer = chemicals.isplit([0.5, 1], ['Water', 'Ethanol'])
        >>> chemical_indexer.show()
        ChemicalIndexer:
         Water    0.5
         Ethanol  1
           
        From a fraction:
        
        >>> chemical_indexer = chemicals.isplit(0.75)
        >>> chemical_indexer.show()
        ChemicalIndexer:
         Water     0.75
         Methanol  0.75
         Ethanol   0.75
            
        From an iterable (assuming same order as the Chemicals object):
        
        >>> chemical_indexer = chemicals.isplit([0.5, 0, 1])
        >>> chemical_indexer.show()
        ChemicalIndexer:
         Water    0.5
         Ethanol  1
            
        """
        if isinstance(split, dict):
            assert not order, "cannot pass 'order' key word argument when split is a dictionary"
            order, split = zip(*split.items())
        
        if order:
            isplit = self.iarray(order, split)
        elif hasattr(split, '__len__'):
            isplit = ChemicalIndexer.from_data(np.asarray(split),
                                               phase=None,
                                               chemicals=self)
        else:
            split = split * np.ones(self.size)
            isplit = ChemicalIndexer.from_data(split,
                                               phase=None,
                                               chemicals=self)
        return isplit

    def index(self, ID):
        """
        Return index of specified chemical.

        Parameters
        ----------
        ID: str
            Chemical identifier.

        Examples
        --------
        Index by ID:
        
        >>> from thermosteam import CompiledChemicals
        >>> chemicals = CompiledChemicals(['Water', 'Ethanol'])
        >>> chemicals.index('Water')
        0

        Indices by CAS number:
        
        >>> chemicals.index('7732-18-5')
        0

        """
        try: return self._index[ID]
        except KeyError:
            raise UndefinedChemical(ID)

    def indices(self, IDs):
        """
        Return indices of specified chemicals.

        Parameters
        ----------
        IDs : iterable
              Chemical indentifiers.

        Examples
        --------
        Indices by ID:
        
        >>> from thermosteam import CompiledChemicals
        >>> chemicals = CompiledChemicals(['Water', 'Ethanol'])
        >>> chemicals.indices(['Water', 'Ethanol'])
        [0, 1]

        Indices by CAS number:
        
        >>> chemicals.indices(['7732-18-5', '64-17-5'])
        [0, 1]

        """
        try:
            dct = self._index
            return [dct[i] for i in IDs]
        except KeyError as key_error:
            raise UndefinedChemical(key_error.args[0])
    
    def get_index(self, IDs):
        """
        Return index/indices of specified chemicals.

        Parameters
        ----------
        IDs : iterable[str] or str
              Chemical identifiers.

        Notes
        -----
        CAS numbers are also supported.

        Examples
        --------
        Get multiple indices with a tuple of IDs:
        
        >>> from thermosteam import CompiledChemicals
        >>> chemicals = CompiledChemicals(['Water', 'Ethanol'], cache=True)
        >>> IDs = ('Water', 'Ethanol')
        >>> chemicals.get_index(IDs)
        [0, 1]
        
        Get a single index with a string:
        
        >>> chemicals.get_index('Ethanol')
        1
        
        An Ellipsis returns a slice:
        
        >>> chemicals.get_index(...)
        slice(None, None, None)

        Anything else returns an error:
        
        >>> chemicals.get_index(['Water', 'Ethanol'])
        Traceback (most recent call last):
        TypeError: only strings, tuples, and ellipsis are valid index keys

        """
        cache = self._index_cache
        try: 
            index = cache[IDs]
        except KeyError: 
            cache[IDs] = index = self._get_index(IDs)
            utils.trim_cache(cache)
        except TypeError:
            raise TypeError("only strings, tuples, and ellipsis are valid index keys")
        return index
    
    def _get_index(self, IDs):
        if isinstance(IDs, str):
            return self.index(IDs)
        elif isinstance(IDs, tuple):
            return self.indices(IDs)
        elif IDs is ...:
            return slice(None)
        else: # pragma: no cover
            raise TypeError("only strings, tuples, and ellipsis are valid index keys")    
    
    def __len__(self):
        return self.size
    
    def __contains__(self, chemical):
        if isinstance(chemical, str):
            return chemical in self.__dict__
        elif isinstance(chemical, Chemical):
            return chemical in self.tuple
        else: # pragma: no cover
            return False
    
    def __iter__(self):
        return iter(self.tuple)
    
    def get_vle_indices(self, nonzeros):
        """
        Return indices of species in vapor-liquid equilibrium given an array
        dictating whether or not the chemicals are present.
        
        Examples
        --------
        >>> from thermosteam import CompiledChemicals
        >>> chemicals = CompiledChemicals(['Water', 'Methanol', 'Ethanol'])
        >>> data = chemicals.kwarray(dict(Water=2., Ethanol=1.))
        >>> chemicals.get_vle_indices(data!=0)
        [0, 2]
        
        """
        return [i for i, j in enumerate(self._has_vle & nonzeros) if j]
    
    def get_lle_indices(self, nonzeros):
        """
        Return indices of species in liquid-liquid equilibrium given an array
        dictating whether or not the chemicals are present.
        
        Examples
        --------
        >>> from thermosteam import CompiledChemicals
        >>> chemicals = CompiledChemicals(['Water', 'Methanol', 'Ethanol'])
        >>> data = chemicals.kwarray(dict(Water=2., Ethanol=1.))
        >>> chemicals.get_lle_indices(data!=0)
        [0, 2]
        
        """
        return [i for i, j in enumerate(self._has_lle & nonzeros) if j]
    
    def __repr__(self):
        return f"{type(self).__name__}([{', '.join(self.IDs)}])"