# -*- coding: utf-8 -*-

"""Provides a set of semi-automatically generated interfaces for all the QUIT fitting commands.
   These all have to go in one file so pickling works correctly
"""

import json
from copy import deepcopy
from os import path, getcwd
from nipype import logging
from nipype.utils.filemanip import fname_presuffix
from nipype.interfaces.base import traits, isdefined, CommandLine, CommandLineInputSpec, TraitedSpec, DynamicTraitedSpec, File, PackageInfo
from nipype.external.due import BibTeX

from qipype.base import InputSpec, BaseCommand

####################################################################################################
# The following commands define a set of "templates" to generate the Input/Output Specifications and
# commands for the QUIT Fitting and Simulation commands. All of these have very similar interfaces,
# so this saves a lot of tedious typing and ensures consistency. Sadly, because these objects have
# to be pickled in nipype pipelines, the outputs of these functions must be defined in the same file
# as the functions, otherwise pickle can't find the classes and throws an exception. This is not
# what was originally planned, and keeping all these in one file is a great big smelly hack.
####################################################################################################


def FitIS(name, fixed=None, in_files=None, extra=None):
    """
    Input Specification for tools in fitting mode
    """
    if fixed is None:
        fixed = []

    if in_files is None:
        in_files = ['in']

    attrs = {'covar': traits.Bool(decsc='Write out parameter covar images',
                                  argstr='--covar'),
             'residuals': traits.Bool(desc='Write out residuals for each data-point',
                                      argstr='--resids'),
             '__module__': __name__}

    for f in fixed:
        aname = '{}_map'.format(f)
        desc = 'Path to fixed {} map'.format(f)
        args = '--{}=%s'.format(f)
        attrs[aname] = File(argstr=args, exists=True, desc=desc)

    for idx, o in enumerate(in_files):
        aname = '{}_file'.format(o)
        desc = 'Output {} file'.format(o)
        attrs[aname] = File(argstr='%s', mandatory=True,
                            position=idx, desc=desc)
    if extra:
        for k, v in extra.items():
            attrs[k] = v
    T = type(name + 'FitIS', (InputSpec,), attrs)
    return T


def SimIS(name, varying, fixed=None, out_files=None, extra=None):
    """
    Input specification for tools in simulation mode
    """
    if fixed is None:
        fixed = []

    if out_files is None:
        out_files = ['out']

    attrs = {'noise': traits.Float(desc='Noise level to add to simulation',
                                   argstr='--simulate=%f', default_value=0.0, usedefault=True),
             '__module__': __name__}
    varying_names = []
    for v in varying:
        aname = '{}_map'.format(v)
        desc = 'Path to input {} map'.format(v)
        attrs[aname] = File(exists=True, desc='Path to {} map'.format(v))
        varying_names.append(aname)
    attrs['varying_names'] = varying_names

    for f in fixed:
        aname = '{}_map'.format(f)
        desc = 'Path to fixed {} map'.format(f)
        args = '--{}=%s'.format(f)
        attrs[aname] = File(argstr=args, exists=True, desc=desc)

    for idx, o in enumerate(out_files):
        aname = '{}_file'.format(o)
        desc = 'Output {} file'.format(o)
        attrs[aname] = File(argstr='%s', mandatory=True,
                            position=idx, desc=desc)
    if extra:
        for k, v in extra.items():
            attrs[k] = v
    T = type(name + 'SimIS', (InputSpec,), attrs)
    return T

################################# Output Specs #################################
#
# QUIT output specifications follow a consistent pattern, so these are defined
# as functions that return a type. Closest thing to C++ templates I could find


def FitOS(name, prefix, varying, derived=None):
    attrs = {'__module__': __name__}
    if derived is None:
        derived = []
    for p in varying + derived:
        pname = '{}_map'.format(p)
        fname = '{}_{}.nii.gz'.format(prefix, p)
        desc = 'Path to {}'.format(p)
        attrs[pname] = File(fname, desc=desc, usedefault=True)
    attrs['rmse_map'] = File('{}_rmse.nii.gz'.format(
        prefix), desc='Path to RMSE', usedefault=True)
    T = type(name + 'FitOS', (TraitedSpec,), attrs)
    return T


def SimOS(name, files=None):
    if files is None:
        files = ['out']
    attrs = {'__module__': __name__}
    for f in files:
        aname = '{}_file'.format(f)
        desc = 'Path to {} image file'.format(f)
        attrs[aname] = File(desc=desc)
    T = type(name + 'SimOS', (TraitedSpec,), attrs)
    return T


class FitCommand(BaseCommand):
    """
    Support for standard fitting tools.
    """

    def _list_outputs(self):
        outputs = self.output_spec().get()
        prefixed = {}
        for key, trait in outputs.items():
            prefixed[key] = self._gen_fname(trait, prefix=self.inputs.prefix)
        return prefixed

    def __init__(self, sequence={}, **kwargs):
        self._json = deepcopy(sequence)
        BaseCommand.__init__(self, **kwargs)


class SimCommand(BaseCommand):
    """
    Base support for QUIT simulator commands.
    """

    def __init__(self, sequence={}, **kwargs):
        self._json = deepcopy(sequence)
        BaseCommand.__init__(self, **kwargs)

    def _parse_inputs(self, skip=None):
        if skip is None:
            skip = []
        for v in self.input_spec.varying_names:
            if isdefined(getattr(self.inputs, v)):
                self._json[v] = getattr(self.inputs, v)
                skip.append(v)
        parsed = super()._parse_inputs(skip)
        return parsed

    def _list_outputs(self):
        inputs = self.inputs.get()
        outputs = self.output_spec().get()
        for k, v in outputs.items():
            outputs[k] = path.abspath(inputs[k])
        return outputs


def Command(toolname, cmd, file_prefix, varying,
            derived=None, fixed=None, files=None, extra=None,
            init=None):
    fit_ispec = FitIS(toolname,
                      fixed=fixed,
                      in_files=files,
                      extra=extra)
    sim_ispec = SimIS(toolname,
                      varying=varying,
                      fixed=fixed,
                      out_files=files,
                      extra=extra)

    fit_ospec = FitOS(toolname, file_prefix,
                      varying=varying, derived=derived)
    sim_ospec = SimOS(toolname, files=files)

    fit_attrs = {'_cmd': cmd, 'input_spec': fit_ispec,
                 'output_spec': fit_ospec}
    sim_attrs = {'_cmd': cmd, 'input_spec': sim_ispec,
                 'output_spec': sim_ospec}
    if init:
        fit_attrs['__init__'] = init
        sim_attrs['__init__'] = init

    fit_cmd = type(toolname, (FitCommand,), fit_attrs)
    sim_cmd = type(toolname + 'Sim', (SimCommand,), sim_attrs)

    return (fit_cmd, sim_cmd, fit_ispec, fit_ospec, sim_ispec, sim_ospec)


# Relaxometry Commands

DESPOT1, DESPOT1Sim, DESPOT1FitIS, DESPOT1FitOS, DESPOT1SimIS, DESPOT1SimOS = Command(
    'DESPOT1', 'qi despot1', 'D1',
    varying=['PD', 'T1'],
    fixed=['B1'],
    extra={'algo': traits.String(desc="Choose algorithm (l/w/n)", argstr="--algo=%s"),
           'iterations': traits.Int(desc='Max iterations for WLLS/NLLS (default 15)', argstr='--its=%d')})

HIFI, HIFISim, HIFIFitIS, HIFIFitOS, HIFISimIS, HIFISimOS = Command(
    'HIFI', 'qi despot1hifi', 'HIFI',
    varying=['PD', 'T1', 'B1'],
    files=['spgr', 'mprage'],
    extra={'clamp_T1': traits.Float(desc='Clamp T1 between 0 and value', argstr='--clamp=%f')})

DESPOT2, DESPOT2Sim, DESPOT2FitIS, DESPOT2FitOS, DESPOT2SimIS, DESPOT2SimOS = Command(
    'DESPOT2', 'qi despot2', 'D2',
    varying=['PD', 'T2'],
    fixed=['T1', 'B1'],
    extra={'algo': traits.Enum("LLS", "WLS", "NLS", desc="Choose algorithm", argstr="--algo=%d"),
           'ellipse': traits.Bool(desc="Data is ellipse geometric solution", argstr='--gs'),
           'iterations': traits.Int(desc='Max iterations for WLLS/NLLS (default 15)', argstr='--its=%d'),
           'clamp_PD': traits.Float(desc='Clamp PD between 0 and value', argstr='-f %f'),
           'clamp_T2': traits.Float(desc='Clamp T2 between 0 and value', argstr='--clampT1=%f')})

FM, FMSim, FMFitIS, FMFitOS, FMSimIS, FMSimOS = Command(
    'FM', 'qi despot2fm', 'FM',
    varying=['PD', 'T2', 'f0'],
    fixed=['B1', 'T1'],
    extra={'asym': traits.Bool(desc="Fit asymmetric (+/-) off-resonance frequency", argstr='--asym'),
           'algo': traits.Enum("LLS", "WLS", "NLS", desc="Choose algorithm", argstr="--algo=%d")})

JSR, JSRSim, JSRFitIS, JSRFitOS, JSRSimIS, JSRSimOS = Command(
    'JSR', 'qi jsr', 'JSR',
    varying=['PD', 'T1', 'T2', 'df0'],
    fixed=['B1'], files=['spgr', 'ssfp'],
    extra={'npsi': traits.Int(desc='Number of psi/off-resonance starts', argstr='--npsi=%d')})

Multiecho, MultiechoSim, MultiechoFitIS, MultiechoFitOS, MultiechoSimIS, MultiechoSimOS = Command(
    'Multiecho', 'qi multiecho', 'ME', varying=['PD', 'T2'], extra={'algo': traits.String(desc="Choose algorithm (l/a/n)", argstr="--algo=%s"), 'iterations': traits.Int(desc='Max iterations for WLLS/NLLS (default 15)', argstr='--its=%d'), 'thresh_PD': traits.Float(desc='Only output maps when PD exceeds threshold value', argstr='-t=%f'), 'clamp_T2': traits.Float(desc='Clamp T2 between 0 and value', argstr='-p=%f')})

MPMR2s, MPMR2sSim, MPMR2sFitIS, MPMR2sFitOS, MPMR2sSimIS, MPMR2sSimOS = Command(
    'MPMR2s', 'qi mpm_r2s', 'MPM', varying=['R2s', 'S0_PDw', 'S0_T1w', 'S0_MTw'], files=['PDw', 'T1w', 'MTw'])

Ellipse, EllipseSim, EllipseFitIS, EllipseFitOS, EllipseSimIS, EllipseSimOS = Command(
    'Ellipse', 'qi ssfp_ellipse', 'ES', varying=['G', 'a', 'b', 'theta_0', 'phi_rf'], extra={'algo': traits.String(desc='Choose algorithm (h/d)', argstr='--algo=%s')})

PLANET, PLANETSim, PLANETFitIS, PLANETFitOS, PLANETSimIS, PLANETSimOS = Command(
    'PLANET', 'qi planet', 'PLANET', varying=['PD', 'T1', 'T2'], fixed=['B1'], files=['G', 'a', 'b'])


MPMR2s, MPMR2sSim, MPMR2sFitIS, MPMR2sFitOS, MPMR2sSimIS, MPMR2sSimOS = Command(
    'MPMR2s', 'qi mpm_r2s', 'MPM',
    varying=['R2s', 'S0_PDw', 'S0_T1w', 'S0_MTw'],
    files=['PDw', 'T1w', 'MTw'],
    extra={'rician': traits.Float(argstr='--rician=%f', desc='Rician noise level correction')})

###
# MT Commands
###

MTSat, MTSatSim, MTSatFitIS, MTSatFitOS, MTSatSimIS, MTSatSimOS = Command(
    'MTSat', 'qi mtsat', 'MTSat',
    varying=['PD', 'R1', 'delta'],
    fixed=['B1'],
    files=['PDw', 'T1w', 'MTw'])

qMT, qMTSim, qMTFitIS, qMTFitOS, qMTSimIS, qMTSimOS = Command(
    'qMT', 'qi qmt', 'QMT',
    varying=['M0_f', 'F_over_R1_f', 'T2_b', 'T1_f_over_T2_f', 'k'],
    derived=['PD', 'T1_f', 'T2_f', 'T2_b', 'k_bf', 'f_b'],
    fixed=['f0', 'B1', 'T1'],
    extra={'lineshape': traits.String(argstr='--lineshape=%s', mandatory=True,
                                      desc='Gauss/Lorentzian/SuperLorentzian/path to JSON file')})

eMT, eMTSim, eMTFitIS, eMTFitOS, eMTSimIS, eMTSimOS = Command(
    'eMT', 'qi ssfp_emt', 'EMT',
    varying=['PD', 'f_b', 'k_bf', 'T1_f', 'T2_f'],
    fixed=['f0', 'B1'],
    files=['G', 'a', 'b'],
    extra={'T2b': traits.Float(desc='T2 of bound pool', argstr='--T2b=%f')})


def Lorentzian(name, pools):
    ###
    #  Lorentzian fitting is a bit special as it can have a variable number of pools, and the
    #  varying parameters will change name depending on the pools. Hence provide a function
    #  to create the correct Fit/Sim types for the specified pools
    #  The specified name must match the name that is used for the class in the module you call this
    #  function from if you ever intend to pickle it (which nipype does)
    ###
    """
    Returns a type for fitting a Lorentzian function to a Z-spectrum with the specified pools
    """
    pars = []
    for pool in pools:
        poolname = pool['name']
        for par in ['f0', 'fwhm', 'A']:
            pname = '{}_{}'.format(poolname, par)
            pars.append(pname)

    def lorentz_init(self, **kwargs):
        FitCommand.__init__(self, **kwargs)
        self._json['pools'] = pools

    interfaces = Command(name, 'qi lorentzian --pools={}'.format(len(pools)), 'LTZ',
                         varying=pars,
                         extra={'additive': traits.Bool(argstr='--add', desc='Use an additive instead of subtractive model'),
                                'Zref': traits.Float(argstr='--zref=%f', desc='Set reference Z-spectrum value (usually 1 or 0)')},
                         init=lorentz_init)
    return interfaces


ds_mt = [{'name': 'DS',
          'df0': [0, -2.5, 2.5],
          'fwhm': [1.0, 1.e-6, 3.0],
          'A': [0.2, 1.e-3, 1.0],
          'use_bandwidth': True},
         {'name': 'MT',
          'df0': [-2.5, -5.0, -0.5],
          'fwhm': [50.0, 35.0, 200.0],
          'A': [0.3, 1.e-3, 1.0]}]
LtzWaterMT, LtzWaterMTSim, LtzWaterMTFitIS, LtzWaterMTFitOS, LtzWaterMTSimIS, LtzWaterMTSimOS = Lorentzian(
    'LtzWaterMT', ds_mt)
an_pools = [{'name': 'Amide',
             'df0': [3.5, 2.0, 6.0],
             'fwhm': [2.0, 0.4, 4.0],
             'A': [0.2, 1.e-3, 0.2],
             'use_bandwidth': True},
            {'name': 'NOE',
             'df0': [-4.0, -6.0, -2.0],
             'fwhm': [2.0, 0.4, 4.0],
             'A': [0.2, 1.e-3, 0.2],
             'use_bandwidth': True}]
LtzAmNOE, LtzAmNOESim, LtzAmNOEFitIS, LtzAmNOEFitOS, LtzAmNOESimIS, LtzAmNOESimOS = Lorentzian(
    'LtzAmNOE', an_pools)

###
# Perfusion Commands
###
ASE, ASESim, ASEFitIS, ASEFitOS, ASESimIS, ASESimOS = Command(
    'ASE', 'qi ase_oef', 'ASE',
    varying=['S0', 'dT', 'R2p'],
    derived=['Tc', 'OEF', 'dHb'],
    extra={'B0': traits.Float(desc='Field-strength (Tesla), default 3', argstr='--B0=%f'),
           'fix_DBV': traits.Float(desc='Fix Deoxygenated Blood Volume to value (fraction)', argstr='--DBV=%f', mandatory=True)}
)

ASEDBV, ASEDBVSim, ASEDBVFitIS, ASEDBVFitOS, ASEDBVSimIS, ASEDBVSimOS = Command(
    'ASEDBV', 'qi ase_oef', 'ASE',
    varying=['S0', 'dT', 'R2p', 'DBV'],
    derived=['Tc', 'OEF', 'dHb'],
    extra={'B0': traits.Float(
        desc='Field-strength (Tesla), default 3', argstr='--B0=%f')}
)


class ASL(FitCommand):
    """
    Calculate CBF from CASL data

    """

    _cmd = 'qi asl'
    input_spec = FitIS('CASL',
                       extra={'average': traits.Bool(desc='Average across time-series', argstr='--average'),
                              'dummies': traits.Int(desc='Remove dummies from timeseries', argstr='--dummies=%d'),
                              'T1_blood': traits.Float(desc='Value of blood T1 (default 1.65)', argstr='--blood=%f'),
                              'T1_tissue': traits.String(desc='Path to tissue T1 map (units are seconds)', argstr='--tissue=%s'),
                              'PD_map': traits.String(desc='Path to PD weighted image', argstr='--pd=%s'),
                              'label_efficiency': traits.Float(desc='Labelling efficiency, default 0.9', argstr='--alpha=%f'),
                              'blood_brain_partition': traits.Float(desc='Blood-Brain Partition Co-efficient, default 0.9 mL/g', argstr='--lambda=%f'),
                              'slicetime': traits.Bool(desc='Apply slice-timing correction (number of PLDs and slices must match)', argstr='--slicetime')
                              })
    output_spec = FitOS('ASL', 'CASL', varying=['CBF'])
