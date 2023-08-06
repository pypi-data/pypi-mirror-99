import pandas as pd
import numpy as np
import warnings as w

from VESIcal import core

from copy import deepcopy


class Sample(object):
    """ WORK IN PROGRESS.
    The sample class stores compositional information for samples, and contains methods
    for normalization and other compositional calculations.
    """

    def __init__(self, composition, units='wtpt_oxides', default_normalization='none', default_units='wtpt_oxides'):
        """ Initialises the sample class.

        The composition is stored as wtpt. If the composition
        is provided as wtpt, no normalization will be applied. If the composition is supplied as
        mols, the composition will be normalized to 100 wt%.

        Parameters
        ----------
        composition     dict or pandas.Series
            The composition of the sample in the format specified by the composition_type
            parameter. Default is oxides in wtpt.

        units     str
            Specifies the units and type of compositional information passed in the
            composition parameter. Choose from 'wtpt_oxides', 'mol_oxides', 'mol_cations'.

        default_normalization:     None or str
            The type of normalization to apply to the data by default. One of:
                - None (no normalization)
                - 'standard' (default): Normalizes an input composition to 100%.
                - 'fixedvolatiles': Normalizes major element oxides to 100 wt%, including volatiles.
                The volatile wt% will remain fixed, whilst the other major element oxides are reduced
                proportionally so that the total is 100 wt%.
                - 'additionalvolatiles': Normalises major element oxide wt% to 100%, assuming it is
                volatile-free. If H2O or CO2 are passed to the function, their un-normalized values will
                be retained in addition to the normalized non-volatile oxides, summing to >100%.

        default_units     str
            The type of composition to return by default, one of:
            - wtpt_oxides (default)
            - mol_oxides
            - mol_cations
            - mol_singleO
        """

        composition = deepcopy(composition)

        if isinstance(composition, dict):
            composition = pd.Series(composition, dtype='float64')
        elif isinstance(composition, pd.Series) == False:
            raise core.InputError("The composition must be given as either a dictionary or a pandas Series.")

        if units == 'wtpt_oxides':
            self._composition = composition
        elif units == 'mol_oxides':
            self._composition = self._molOxides_to_wtpercentOxides(composition)
        elif units == 'mol_cations':
            self._composition = self._molCations_to_wtpercentOxides(composition)
        else:
            raise core.InputError("Units must be one of 'wtpt_oxides', 'mol_oxides', or 'mol_cations'.")

        self.set_default_normalization(default_normalization)
        self.set_default_units(default_units)


    def set_default_normalization(self, default_normalization):
        """ Set the default type of normalization to use with the get_composition() method.

        Parameters
        ----------
        default_normalization:    str
            The type of normalization to apply to the data. One of:
            - 'none' (no normalization)
            - 'standard' (default): Normalizes an input composition to 100%.
            - 'fixedvolatiles': Normalizes major element oxides to 100 wt%, including volatiles.
            The volatile wt% will remain fixed, whilst the other major element oxides are reduced
            proportionally so that the total is 100 wt%.
            - 'additionalvolatiles': Normalises major element oxide wt% to 100%, assuming it is
            volatile-free. If H2O or CO2 are passed to the function, their un-normalized values will
            be retained in addition to the normalized non-volatile oxides, summing to >100%.
                
        """
        if default_normalization in ['none','standard','fixedvolatiles','additionalvolatiles']:
            self.default_normalization = default_normalization
        else:
            raise core.InputError("The normalization method must be one of 'none', 'standard', 'fixedvolatiles',\
             or 'additionalvolatiles'.")

    def set_default_units(self, default_units):
        """ Set the default units of composition to return when using the get_composition() method.

        Parameters
        ----------
        default_units     str
            The type of composition to return, one of:
            - wtpt_oxides (default)
            - mol_oxides
            - mol_cations
            - mol_singleO
        """
        if default_units in ['wtpt_oxides','mol_oxides','mol_cations','mol_singleO']:
            self.default_units = default_units
        else:
            raise core.InputError("The units must be one of 'wtpt_oxides','mol_oxides','mol_cations','mol_singleO'.")


    def get_composition(self, species=None, normalization=None, units=None, exclude_volatiles=False):
        """ Returns the composition in the format requested, normalized as requested.

        Parameters
        ----------
        species:    NoneType or str
            The name of the oxide or cation to return the concentration of. If NoneType (default) the
            whole composition will be returned as a pandas.Series. If an oxide is passed, the value in
            wtpt will be returned unless units is set to 'mol_oxides', even if the default units for the
            sample object are mol_oxides. If an element is passed, the concentration will be returned as
            mol_cations, unless 'mol_singleO' is specified as units, even if the default units for the
            sample object are mol_singleO. Unless normalization is specified in the method call, none
            will be applied.
        normalization:     NoneType or str
            The type of normalization to apply to the data. One of:
            - 'none' (no normalization)
            - 'standard' (default): Normalizes an input composition to 100%.
            - 'fixedvolatiles': Normalizes major element oxides to 100 wt%, including volatiles.
            The volatile wt% will remain fixed, whilst the other major element oxides are reduced
            proportionally so that the total is 100 wt%.
            - 'additionalvolatiles': Normalises major element oxide wt% to 100%, assuming it is
            volatile-free. If H2O or CO2 are passed to the function, their un-normalized values will
            be retained in addition to the normalized non-volatile oxides, summing to >100%.

            If NoneType is passed the default normalization option will be used (self.default_normalization).

        units:     NoneType or str
            The units of composition to return, one of:
            - wtpt_oxides (default)
            - mol_oxides
            - mol_cations
            - mol_singleO

            If NoneType is passed the default units option will be used (self.default_type).

        exclude_volatiles   bool
            If True, volatiles will be excluded from the returned composition, prior to normalization and
            conversion.

        Returns
        -------
        pandas.Series or float
            The sample composition, as specified.
        """

        # Fetch the default return types if not specified in function call
        if normalization == None and species == None:
            normalization = self.default_normalization
        if units == None and species == None:
            units = self.default_units

        # Check for a species being provided, if so, work out which units to return.
        if isinstance(species,str):
            if species in core.oxides:
                if units in ['mol_cations, mol_singleO'] or units == None:
                    units = 'wtpt_oxides'
            elif species in core.cations_to_oxides:
                if units in ['wtpt_oxides','mol_oxides'] or units == None:
                    units = 'mol_cations'
            else:
                raise core.InputError(species + " was not recognised, check spelling, capitalization and stoichiometry.")
            if normalization == None:
                normalization = 'none'
        elif species != None:
            raise core.InputError("Species must be either a string or a NoneType.")

        if exclude_volatiles == True:
            composition = self._composition.copy()
            if 'H2O' in composition.index:
                composition = composition.drop(index='H2O')
            if 'CO2' in composition.index:
                composition = composition.drop(index='CO2')
        else:
            composition = self._composition.copy()

        # Do requested normalization
        if normalization == 'none':
            normed = composition
        elif normalization == 'standard':
            normed = self._normalize_Standard(composition)
        elif normalization == 'fixedvolatiles':
            normed = self._normalize_FixedVolatiles(composition)
        elif normalization == 'additionalvolatiles':
            normed = self._normalize_AdditionalVolatiles(composition)
        else:
            raise core.InputError("The normalization method must be one of 'none', 'standard', 'fixedvolatiles',\
             or 'additionalvolatiles'.")

        # Get the requested type of composition
        if units == 'wtpt_oxides':
            final = normed
        elif units == 'mol_oxides':
            final = self._wtpercentOxides_to_molOxides(normed)
        elif units == 'mol_cations':
            final = self._wtpercentOxides_to_molCations(normed)
        elif units == 'mol_singleO':
            final = self._wtpercentOxides_to_molSingleO(normed)
        else:
            raise core.InputError("The units must be one of 'wtpt_oxides', 'mol_oxides', 'mol_cations', \
            or 'mol_singleO'.")

        if species == None:
            return final
        elif isinstance(species,str):
            return final[species]

    def change_composition(self, new_composition, units='wtpt_oxides', inplace=True):
        """
        Change the concentration of some component of the composition.

        If the units are moles, they are read as moles relative to the present composition,
        i.e. if you wish to double the moles of MgO, if the present content is 0.1 moles,
        you should provide {'MgO':0.2}. The composition will then be re-normalized. If the
        original composition was provided in un-normalized wt%, the unnormalized total will
        be lost.

        Parameters
        ----------
        new_composition:    dict or pandas.Series
            The components to be updated.
        units:      str
            The units of new_composition. Should be one of:
            - wtpt_oxides (default)
            - mol_oxides
            - mol_cations
        inplace:    bool
            If True the object will be modified in place. If False, a copy of the Sample
            object will be created, modified, and then returned.

        Returns
        -------
        Sample class
            Modified Sample class.
        """

        # if new_composition is pandas.Series, convert to dict
        if isinstance(new_composition, pd.Series):
            new_composition = dict(new_composition)

        if inplace == False:
            newsample = deepcopy(self)
            return newsample.change_composition(new_composition, units=units)

        if units == 'wtpt_oxides':
            for ox in new_composition:
                self._composition[ox] = new_composition[ox]

        elif units == 'mol_oxides':
            _comp = self.get_composition(units='mol_oxides')
            for ox in new_composition:
                _comp[ox] = new_composition[ox]
            self._composition = self._molOxides_to_wtpercentOxides(_comp)

        elif units == 'mol_cations':
            _comp = self.get_composition(units='mol_cations')
            for el in new_composition:
                _comp[el] = new_composition[el]
            self._composition = self._molCations_to_wtpercentOxides(_comp)

        else:
            raise core.InputError("Units must be one of 'wtpt_oxides', 'mol_oxides', or 'mol_cations'.")

        return self


    def get_formulaweight(self,exclude_volatiles=False):
        """ Converts major element oxides in wt% to the formula weight (on a 1 oxygen basis).

        Parameters
        ----------
        exclude_volatiles   bool
            If True the formula weight will be calculated without volatiles

        Returns
        -------
        float
            The formula weight of the composition, on a one oxygen basis.
        """

        cations = self.get_composition(units='mol_singleO',exclude_volatiles=exclude_volatiles)

        # if type(cations) != dict:
        #     cations = dict(cations)

        FW = 15.999
        for cation in cations.index:
            FW += cations[cation]*core.CationMass[core.cations_to_oxides[cation]]

        return FW

    def check_oxide(self, oxide):
        """
        Check whether the sample composition contains the given oxide.

        Parameters
        ----------
        oxide:  str
            Oxide name to check composition for.

        Returns
        -------
        bool
            Whether the composition contains the given oxide, or not.
        """

        if oxide not in core.oxides:
            w.warn("Oxide name not recognised. If it is in your sample, unexpected behaviour might occur!",
                    RuntimeWarning,stacklevel=2)
        return oxide in self._composition

    def check_cation(self, cation):
        """
        Check whether the sample composition contains the given cation.

        Parameters
        ----------
        cation:    str
            The element name to check the composition for.

        Returns
        -------
        bool
            Whether the composition contains the given element, or not.
        """

        if cation not in core.cations_to_oxides:
            w.warn("Cation name not recognised. If it is in your sample, unexpected behaviour might occur!",
                    RuntimeWarning,stacklevel=2)
        return cation in self.get_composition(units='mol_cations')


    def _normalize_Standard(self, composition):
        """
        Normalizes the given composition to 100 wt%, including volatiles. This method
        is intended only to be called by the get_composition() method.

        Parameters
        ----------
        composition:     pandas.Series
            A rock composition with oxide names as keys and wt% concentrations as values.

        Returns
        -------
        pandas.Series
            Normalized oxides in wt%.
        """
        comp = composition.copy()
        comp = dict(comp)
        return pd.Series({k: 100.0 * v / sum(comp.values()) for k, v in comp.items()})

    def _normalize_FixedVolatiles(self, composition):
        """
        Normalizes major element oxides to 100 wt%, including volatiles. The volatile
        wt% will remain fixed, whilst the other major element oxides are reduced proportionally
        so that the total is 100 wt%.

        Intended to be called only by the get_composition() method.

        Parameters
        ----------
        composition:     pandas Series
            Major element oxides in wt%

        Returns
        -------
        pandas Series
            Normalized major element oxides.
        """
        comp = composition.copy()
        normalized = pd.Series({},dtype=float)
        volatiles = 0
        if 'CO2' in list(comp.index):
            volatiles += comp['CO2']
        if 'H2O' in list(comp.index):
            volatiles += comp['H2O']

        for ox in list(comp.index):
            if ox != 'H2O' and ox != 'CO2':
                normalized[ox] = comp[ox]

        normalized = normalized/np.sum(normalized)*(100-volatiles)

        if 'CO2' in list(comp.index):
            normalized['CO2'] = comp['CO2']
        if 'H2O' in list(comp.index):
            normalized['H2O'] = comp['H2O']

        return normalized

    def _normalize_AdditionalVolatiles(self, composition):
        """
        Normalises major element oxide wt% to 100%, assuming it is volatile-free. If
        H2O or CO2 are passed to the function, their un-normalized values will be retained
        in addition to the normalized non-volatile oxides, summing to >100%.

        Intended to be called only by the get_composition() method.

        Parameters
        ----------
        sample:     pandas.Series
            Major element oxides in wt%

        Returns
        -------
        pandas.Series
            Normalized major element oxides.
        """
        comp = composition.copy()
        normalized = pd.Series({}, dtype=float)
        for ox in list(comp.index):
            if ox != 'H2O' and ox != 'CO2':
                normalized[ox] = comp[ox]

        normalized = normalized/np.sum(normalized)*100
        if 'H2O' in comp.index:
            normalized['H2O'] = comp['H2O']
        if 'CO2' in comp.index:
            normalized['CO2'] = comp['CO2']

        return normalized

    def _wtpercentOxides_to_molOxides(self, composition):
        """
        Converts a wt% oxide composition to mol oxides, normalised to 1 mol.

        Intended to be called only by the get_composition() method.

        Parameters
        ----------
        composition:    pandas.Series
            Major element oxides in wt%

        Returns
        -------
        pandas.Series
            Molar proportions of major element oxides, normalised to 1.
        """
        molOxides = {}
        comp = composition.copy()
        oxideslist = list(comp.index)

        for ox in oxideslist:
            molOxides[ox] = comp[ox]/core.oxideMass[ox]

        molOxides = pd.Series(molOxides)
        molOxides = molOxides/molOxides.sum()

        return molOxides

    def _wtpercentOxides_to_molCations(self, composition):
        """
        Converts a wt% oxide composition to molar proportions of cations (normalised to 1).

        Intended to be called only by the get_composition() method.

        Parameters
        ----------
        composition        pandas.Series
            Major element oxides in wt%.

        Returns
        -------
        pandas.Series
            Molar proportions of cations, normalised to 1.
        """
        molCations = {}
        comp = composition.copy()
        oxideslist = list(comp.index)

        for ox in oxideslist:
            cation = core.oxides_to_cations[ox]
            molCations[cation] = core.CationNum[ox]*comp[ox]/core.oxideMass[ox]

        molCations = pd.Series(molCations)
        molCations = molCations/molCations.sum()

        return molCations

    def _wtpercentOxides_to_molSingleO(self, composition):
        """
        Constructs the chemical formula, on a single oxygen basis, from wt% oxides.

        Intended to be called only by the get_composition() method.

        Parameters
        ----------
        composition        pandas.Series
            Major element oxides in wt%

        Returns
        -------
        pandas.Series
            The chemical formula of the composition, on a single oxygen basis. Each element is
            a separate entry in the Series.
        """
        molCations = {}
        comp = composition.copy()

        oxideslist = list(comp.index)

        total_O = 0.0
        for ox in oxideslist:
            cation = core.oxides_to_cations[ox]
            molCations[cation] = core.CationNum[ox]*comp[ox]/core.oxideMass[ox]
            total_O += core.OxygenNum[ox]*comp[ox]/core.oxideMass[ox]

        molCations = pd.Series(molCations)
        molCations = molCations/total_O

        return molCations

    def _molOxides_to_wtpercentOxides(self, composition):
        """
        Converts mol oxides to wt% oxides. Returned composition is normalized to 100 wt%.

        Parameters
        ----------
        composition:     pandas.Series
            mol fraction oxides

        Returns
        -------
        pandas.Series
            wt% oxides normalized to 100 wt%.
        """

        comp = composition.copy()
        wtpt = {}

        for ox in composition.index:
            wtpt[ox] = comp[ox]*core.oxideMass[ox]

        wtpt = pd.Series(wtpt)
        wtpt = wtpt/wtpt.sum()*100

        return wtpt

    def _molOxides_to_molCations(self, composition):
        """
        Converts mol oxides to mol cations. Returned composition is normalized to 1 mol
        cations.

        Parameters
        ----------
        composition:     pandas.Series
            mole fraction oxides

        Returns
        -------
        pandas.Series
            mole fraction cations
        """

        comp = composition.copy()
        molcations = {}

        for ox in comp.index:
            molcations[core.oxides_to_cations[ox]] = comp[ox]*core.CationNum[ox]

        molcations = pd.Series(molcations)
        molcations = molcations/molcations.sum()

        return molcations

    def _molCations_to_wtpercentOxides(self, composition):
        """
        Converts mole fraction cations to wt% oxides, normalized to 100 wt%.

        Parameters
        ----------
        composition:     pandas.Series
            Mole fraction cations

        Returns
        -------
        pandas.Series
            Wt% oxides, normalized to 100 wt%.
        """

        comp = composition.copy()
        wtpt = {}

        for el in comp.index:
            wtpt[core.cations_to_oxides[el]] = comp[el]/core.CationNum[core.cations_to_oxides[el]]*\
            core.oxideMass[core.cations_to_oxides[el]]

        wtpt = pd.Series(wtpt)
        wtpt = wtpt/wtpt.sum()*100

        return wtpt

    def _molCations_to_molOxides(self, composition):
        """
        Converts mole fraction cations to mole fraction oxides, normalized to 1 mole.

        Parameters
        ----------
        composition:     pandas.Series
            Mole fraction cations

        Returns
        -------
        pandas.Series
            Mole fraction oxides, normalized to one.
        """
        comp = composition.copy()
        moloxides = {}

        for el in comp.index:
            moloxides[core.cations_to_oxides[el]] = comp[el]/core.CationNum[core.cations_to_oxides[el]]

        moloxides = pd.Series(moloxides)
        moloxides = moloxides/moloxides.sum()

        return moloxides
