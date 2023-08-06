from datetime import datetime, timedelta
import math
from os import PathLike
import pathlib

import numpy as np

from adcircpy.mesh.mesh import AdcircMesh


class Fort15:
    def __init__(self, mesh: AdcircMesh = None):
        self._mesh = mesh
        self._runtype = None

    @property
    def mesh(self):
        return self._mesh

    def fort15(self, runtype: str):
        self._runtype = runtype
        # ----------------
        # model options
        # ----------------
        f = []
        f.extend([
            f'{self.RUNDES:<63} ! RUNDES',
            f'{self.RUNID:<63} ! RUNID',
            f'{self.NFOVER:<63d} ! NFOVER',
            f'{self.NABOUT:<63d} ! NABOUT',
            f'{self.NSCREEN:<63d} ! NSCREEN',
            f'{self.IHOT:<63d} ! IHOT',
            f'{self.ICS:<63d} ! ICS',
            f'{self.IM:<63d} ! IM',
        ])
        if self.IM in [21, 611113]:
            f.append(f'{self.IDEN:<63d} ! IDEN')
        f.extend([
            f'{self.NOLIBF:<63G} ! NOLIBF',
            f'{self.NOLIFA:<63d} ! NOLIFA',
            f'{self.NOLICA:<63d} ! NOLICA',
            f'{self.NOLICAT:<63d} ! NOLICAT',
            f'{self.NWP:<63d} ! NWP',
        ])
        if self._runtype == 'coldstart':
            attributes = self.mesh.get_coldstart_attributes()
        elif self._runtype == 'hotstart':
            attributes = self.mesh.get_hotstart_attributes()
        f.extend(f'{attribute:<63}' for attribute in attributes)
        f.extend([
            f'{self.NCOR:<63d} ! NCOR',
            f'{self.NTIP:<63d} ! NTIP',
            f'{int((self.NRS * 100) + self.NWS):<63d} ! NWS',
            f'{self.NRAMP:<63d} ! NRAMP',
            f'{self.G:<63G} ! gravitational acceleration',
            f'{self.TAU0:<63G} ! TAU0',
        ])
        if self.TAU0 == -5:
            f.append(
                f'{self.Tau0FullDomainMin:G} '
                f'{self.Tau0FullDomainMax:G}'.ljust(63)
                + ' ! Tau0FullDomainMin Tau0FullDomainMax'
            )
        f.extend([
            f'{self.DTDP:<63.6f} ! DTDP',
            f'{self.STATIM:<63G} ! STATIM',
            f'{self.REFTIM:<63G} ! REFTIM',
        ])
        if self.NWS not in [0, 1, 9, 11]:
            interval = f'{self.WTIMINC}'
            description = 'WTIMINC - meteorological data time increment'
            if self.NRS in [1, 3, 4, 5]:
                interval += f' {self.RSTIMINC}'
                description += ', RSTIMINC wave forcing increment'
            f.append(f'{interval:<63} ! {description}')
        f.extend([
            f'{self.RNDAY:<63G} ! RNDAY',
            f'{self.DRAMP:<63} ! DRAMP',
            f'{self.A00:G} {self.B00:G} {self.C00:G}'.ljust(63)
            + ' ! A00 B00 C00',
            f'{self.H0:G} 0 0 {self.VELMIN:G}'.ljust(63) + ' ! H0 ? ? VELMIN',
            f'{self.SLAM0:G} {self.SFEA0:G}'.ljust(63) + ' ! SLAM0 SFEA0',
            f'{self.FFACTOR:<63} ! {"CF HBREAK FTHETA FGAMMA" if self.NOLIBF == 2 else "FFACTOR"}',
            f'{self.ESLM:<63G} ! {"ESL - LATERAL EDDY VISCOSITY COEFFICIENT" if not self.smagorinsky else "smagorinsky coefficient"}',
            f'{self.CORI:<63G} ! CORI',
        ])
        # ----------------
        # tidal forcings
        # ----------------
        f.append(self.get_tidal_forcing())
        f.append(f'{self.ANGINN:<63G} ! ANGINN')
        # ----------------
        # other boundary forcings go here.
        # (e.g. river boundary forcing)
        # ----------------
        for id, bnd in self.mesh.open_boundaries.items():
            # f.append(f'{bnd["neta"]}')
            # velocity
            if bnd['ifltype'] in [0, 1, 4]:
                pass
            else:
                raise NotImplementedError(f'bctides generation not implemented'
                                          f' for "ifltype={bnd["ifltype"]}"')
            # temperature
            if bnd['itetype'] == 0:
                pass
            else:
                raise NotImplementedError(f'bctides generation not implemented'
                                          f' for "itetype={bnd["itetype"]}"')
            # salinity
            if bnd['isatype'] == 0:
                pass
            else:
                raise NotImplementedError(f'bctides generation not implemented'
                                          f' for "isatype={bnd["isatype"]}"')
            # tracers
            if bnd['itrtype'] == 0:
                pass
            else:
                raise NotImplementedError(f'bctides generation not implemented'
                                          f' for "itrtype={bnd["itrtype"]}"')
        # ----------------
        # output requests
        # ----------------
        # elevation out stations
        f.extend([
            f'{self.NOUTE:G} {self.TOUTSE:G} '
            f'{self.TOUTFE:G} {self.NSPOOLE:G}'.ljust(63)
            + f' ! NOUTE TOUTSE TOUTFE NSPOOLE',
            f'{self.NSTAE:<63d} ! NSTAE',
        ])
        stations = self.elevation_stations_output
        if stations['sampling_rate'] is not None:
            if self._runtype == 'coldstart':
                if stations['spinup']:
                    f.extend(
                        f'{x:G} {y:G}'.ljust(63) + f' ! {station_id}'
                        for station_id, (x, y) in
                        stations['collection'].items()
                    )
            else:
                f.extend(
                    f'{x:G} {y:G}'.ljust(63) + f' ! {station_id}'
                    for station_id, (x, y) in stations['collection'].items()
                )
        # velocity out stations
        f.extend([
            (f'{self.NOUTV:G} {self.TOUTSV:G} '
             + f'{self.TOUTFV:G} {self.NSPOOLV:G}').ljust(63)
            + ' ! NOUTV TOUTSV TOUTFV NSPOOLV',
              f'{self.NSTAV:<63G} ! NSTAV'
        ])
        stations = self.velocity_stations_output
        if stations['sampling_rate'] is not None:
            if self._runtype == 'coldstart':
                if stations['spinup']:
                    f.extend(
                        f'{x:G} {y:G}'.ljust(63) + f' ! {station_id}'
                        for station_id, (x, y) in
                        stations['collection'].items()
                    )
            else:
                f.extend(
                    f'{x:G} {y:G}'.ljust(63) + f' ! {station_id}'
                    for station_id, (x, y) in stations['collection'].items()
                )
        if self.IM == 10:
            # concentration out stations
            f.extend([
                (f'{self.NOUTC:G} {self.TOUTSC:G} '
                 + f'{self.TOUTFC:G} {self.NSPOOLC:G}').ljust(63)
                + ' ! NOUTC TOUTSC TOUTFC NSPOOLC\n',
                f'{self.NSTAC:<63d} ! NSTAC\n',
            ])
            stations = self.concentration_stations_output
            if stations['sampling_rate'] is not None:
                if self._runtype == 'coldstart':
                    if stations['spinup']:
                        f.extend(
                            f'{x:G} {y:G}'.ljust(63) + f' ! {station_id}\n'
                            for station_id, (x, y) in
                            stations['collection'].items()
                        )
                else:
                    f.extend(
                        f'{x:G} {y:G}'.ljust(63) + f' ! {station_id}'
                        for station_id, (x, y) in
                        stations['collection'].items()
                    )
        if self.NWS > 0:
            # meteorological out stations
            f.extend([
                (f'{self.NOUTM:G} {self.TOUTSM:G} '
                 + f'{self.TOUTFM:G} {self.NSPOOLM:G}').ljust(63)
                + ' ! NOUTM TOUTSM TOUTFM NSPOOLM',
                f'{self.NSTAM:<63d} ! NSTAM',
            ])
            stations = self.meteorological_stations_output
            if stations['sampling_rate'] is not None:
                if stations['sampling_rate'] is not None:
                    if self._runtype == 'coldstart':
                        if stations['spinup']:
                            f.extend(
                                f'{x:G} {y:G}'.ljust(63) + f' ! {station_id}'
                                for station_id, (x, y) in
                                stations['collection'].items()
                            )
                    else:
                        f.extend(
                            f'{x:G} {y:G}'.ljust(63) + f' ! {station_id}'
                            for station_id, (x, y) in
                            stations['collection'].items()
                        )
        # elevation global outputs
        f.append(
            (f'{self.NOUTGE:d} {self.TOUTSGE:f} '
             + f'{self.TOUTFGE:f} {self.NSPOOLGE:d}').ljust(63)
            + ' ! NOUTGE TOUTSGE TOUTFGE NSPOOLGE'
        )
        # velocity global otuputs
        f.append(
            (f'{self.NOUTGV:d} {self.TOUTSGV:f} '
             + f'{self.TOUTFGV:f} {self.NSPOOLGV:d}').ljust(63)
            + ' ! NOUTGV TOUTSGV TOUTFGV NSPOOLGV'
        )
        if self.IM == 10:
            f.append(
                (f'{self.NOUTGC:d} {self.TOUTSGC:f} '
                 + f'{self.TOUTFGC:f} {self.NSPOOLGC:d}').ljust(63)
                + ' ! NOUTSGC TOUTGC TOUTFGC NSPOOLGC'
            )
        if self.NWS != 0:
            f.append(
                (f'{self.NOUTGM:d} {self.TOUTSGM:f} '
                 + f'{self.TOUTFGM:f} {self.NSPOOLGM:d}').ljust(63)
                + ' ! NOUTGM TOUTSGM TOUTFGM NSPOOLGM'
            )
        # harmonic analysis requests
        harmonic_analysis = False
        self._outputs = [
            self.elevation_surface_output,
            self.velocity_surface_output,
            self.elevation_stations_output,
            self.velocity_stations_output,
        ]
        for _output in self._outputs:
            if _output['harmonic_analysis']:
                if self._runtype == 'coldstart':
                    if _output['spinup']:
                        harmonic_analysis = True
                        break
                else:
                    harmonic_analysis = True
                    break
        f.append(f'{self.NFREQ:<63d} ! NFREQ')
        if harmonic_analysis:
            for constituent, forcing in self.tidal_forcing:
                f.extend([
                    f'{constituent:<63} ',
                    (f'{forcing[1]:<.16G} {forcing[3]:<.16G}'
                     + f'{forcing[4]:<.16G}').ljust(63),
                ])
        f.extend([
            (f'{self.THAS:G} {self.THAF:G} '
             + f'{self.NHAINC} {self.FMV}').ljust(63)
            + ' ! THAS THAF NHAINC FMV',
            (f'{self.NHASE:G} {self.NHASV:G} '
             + f'{self.NHAGE:G} {self.NHAGV:G}').ljust(63)
            + ' ! NHASE NHASV NHAGE NHAGV',
        ])
        # ----------------
        # hostart file generation
        # ----------------
        f.extend([
            f'{self.NHSTAR:d} {self.NHSINC:d}'.ljust(63) + ' ! NHSTAR NHSINC',
            (f'{self.ITITER:<1d} {self.ISLDIA:<1d} '
             + f'{self.CONVCR:<.15G} {self.ITMAX:<4d}').ljust(63)
            + ' ! ITITER ISLDIA CONVCR ITMAX',
        ])
        if self.vertical_mode == '3D':
            raise NotImplementedError('3D runs not yet implemented')
        f.extend([
            f'{self.NCPROJ:<63} ! NCPROJ',
            f'{self.NCINST:<63} ! NCINST',
            f'{self.NCSOUR:<63} ! NCSOUR',
            f'{self.NCHIST:<63} ! NCHIST',
            f'{self.NCREF:<63} ! NCREF',
            f'{self.NCCOM:<63} ! NCCOM',
            f'{self.NCHOST:<63} ! NCHOST',
            f'{self.NCCONV:<63} ! NCONV',
            f'{self.NCCONT:<63} ! NCCONT',
            f'{self.NCDATE:<63} ! Forcing start date / NCDATE',
        ])
        del self._outputs

        for name, namelist in self.namelists.items():
            f.append(f'&{name} ' +
                     ', '.join([f'{key}={value}'
                                for key, value in namelist.items()]) +
                     ' \\')

        return '\n'.join(f)

    def write(self, runtype: str, path: PathLike, overwrite: bool = False):
        assert runtype in ['coldstart', 'hotstart']
        fort15 = pathlib.Path(path)
        if fort15.exists() and not overwrite:
            raise Exception(f'{fort15} exists. '
                            f'Pass `overwrite=True` to overwrite.')
        with open(fort15, 'w', newline='\n') as f:
            f.write(self.fort15(runtype))

    def get_tidal_forcing(self):
        f = []
        f.append(f'{self.NTIF:<63d} ! NTIF')
        active = self._get_active_tidal_potential_constituents()
        for constituent in active:
            forcing = self.tidal_forcing(constituent)
            f.extend([
                f'{constituent}',
                f'{forcing[0]:G} {forcing[1]:G} {forcing[2]:G} {forcing[3]:G} {forcing[4]:G}',
            ])
        f.append(f'{self.NBFR:d}')
        active = self._get_active_tidal_forcing_constituents()
        for constituent in active:
            forcing = self.tidal_forcing(constituent)
            f.extend(
                [
                    f'{constituent}',
                    f'{forcing[1]:G} ' f'{forcing[3]:G} ' f'{forcing[4]:G}',
                    # f'{len(self.mesh.open_boundaries)}',
                ]
            )
        for id, bnd in self.mesh.open_boundaries.items():
            # f.append(f'{bnd["neta"]}')
            # elevation
            if bnd['iettype'] in [0, 1, 4]:
                pass
            elif bnd['iettype'] in [3, 5]:
                for constituent in self.tidal_forcing.get_active_constituents():
                    f.append(f'{constituent}')
                    vertices = self.mesh.get_xy(crs='EPSG:4326')[
                               bnd['indexes'], :]
                    amp, phase = self.tidal_forcing.tidal_dataset(
                            constituent, vertices)
                    f.extend(f'{amp[i]:.8e} {phase[i]:.8e}' for i in
                             range(len(vertices)))
            elif bnd['iettype'] in 2:
                bnd['iettype']['obj'].ethconst
        return '\n'.join(f)

    @property
    def namelists(self) -> {str: {str: str}}:
        namelists = {}
        if self.NRS in [1, 3, 4, 5]:
            namelists['SWANOutputControl'] = {
                'SWAN_OutputHS': 'False',
                'SWAN_OutputDIR': 'False',
                'SWAN_OutputTM01': 'False',
                'SWAN_OutputTPS': 'False',
                'SWAN_OutputWIND': 'False',
                'SWAN_OutputTM02': 'False',
                'SWAN_OutputTMM10': 'False'
            }
        return namelists

    def set_time_weighting_factors_in_gcwe(self, A00, B00, C00):
        A00 = float(A00)
        B00 = float(B00)
        C00 = float(C00)
        assert A00 + B00 + C00 == 1.0, '"A00 + B00 + C00" must equal 1'
        self.__A00 = A00
        self.__B00 = B00
        self.__C00 = C00

    @staticmethod
    def parse_stations(path, station_type):
        stations = dict()
        with open(path, 'r') as f:
            for line in f:
                if station_type in line:
                    line = f.readline().split('!')[0]
                    num = int(line)
                    for i in range(num):
                        line = f.readline().split('!')
                        if len(line) > 0:
                            station_name = line[1].strip(' \n')
                        else:
                            station_name = str(i)
                        vertices = line[0].split(' ')
                        vertices = [float(x) for x in vertices if x != '']
                        x = float(vertices[0])
                        y = float(vertices[1])
                        try:
                            z = float(vertices[2])
                            stations[station_name] = (x, y, z)
                        except IndexError:
                            stations[station_name] = (x, y)
        return stations

    @property
    def vertical_mode(self):
        """
        '2D' (default) | '3D'
        """
        try:
            return self.__vertical_mode
        except AttributeError:
            return '2D'

    @property
    def lateral_stress_in_gwce(self):
        """
        'kolar_grey' (default) | 'velocity_based' | 'flux_based'
        """
        try:
            return self.__lateral_stress_in_gwce
        except AttributeError:
            if self.smagorinsky:
                return 'velocity_based'
            else:
                return 'kolar_grey'

    @property
    def lateral_stress_in_gwce_is_symmetrical(self):
        """
        True | False (default)
        """
        try:
            return self.__lateral_stress_in_gwce_is_symmetrical
        except AttributeError:
            if self.smagorinsky:
                return True
            else:
                return False

    @property
    def advection_in_gwce(self):
        """
        'non_conservative' (default) | 'form_1' | 'form_2'
        """
        try:
            return self.__advection_in_gwce
        except AttributeError:
            return 'non_conservative'

    @property
    def lateral_stress_in_momentum(self):
        """
        'velocity_based' (default) | 'flux_based'
        """
        try:
            return self.__lateral_stress_in_momentum
        except AttributeError:
            return 'velocity_based'

    @property
    def lateral_stress_in_momentum_is_symmetrical(self):
        """
        True | False (default)
        """
        try:
            return self.__lateral_stress_in_momentum_is_symmetrical
        except AttributeError:
            return False

    @property
    def lateral_stress_in_momentum_method(self):
        """
        True | False (default)
        """
        try:
            return self.__lateral_stress_in_momentum_method
        except AttributeError:
            return 'integration_by_parts'

    @property
    def advection_in_momentum(self):
        """
        'non_conservative' (default) | 'form_1' | 'form_2'
        """
        try:
            return self.__advection_in_momentum
        except AttributeError:
            return 'non_conservative'

    @property
    def area_integration_in_momentum(self):
        """
        'corrected' (default) | 'original'
        """
        try:
            return self.__area_integration_in_momentum
        except AttributeError:
            return 'corrected'

    @property
    def baroclinicity(self):
        """
        True | False (default)
        """
        try:
            return self.__baroclinicity
        except AttributeError:
            return False

    @property
    def smagorinsky(self):
        """
        True (default) | False
        """
        try:
            return self.__smagorinsky
        except AttributeError:
            return True

    @property
    def smagorinsky_coefficient(self):
        try:
            return self.__smagorinsky_coefficient
        except AttributeError:
            return 0.2

    @property
    def gwce_solution_scheme(self):
        """
        'semi-implicit' (default) | 'explicit | 'semi-implicit-legacy'
        """
        try:
            return self.__gwce_solution_scheme
        except AttributeError:
            return 'semi-implicit'

    @property
    def horizontal_mixing_coefficient(self):
        try:
            return self.__horizontal_mixing_coefficient
        except AttributeError:
            return 10.0

    @property
    def passive_scalar_transport(self):
        """
        True | False (default)
        """
        try:
            return self.__passive_scalar_transport
        except AttributeError:
            return False

    @property
    def stress_based_3D(self):
        try:
            return self.__stress_based_3D
        except AttributeError:
            return False

    @property
    def predictor_corrector(self):
        try:
            return self.__predictor_corrector
        except AttributeError:
            return True

    @property
    def timestep(self):
        return np.abs(self.DTDP)

    @property
    def RUNDES(self):
        try:
            self.__RUNDES
        except AttributeError:
            return datetime.now().strftime('created on %Y-%m-%d %H:%M')

    @property
    def RUNID(self):
        try:
            self.__RUNID
        except AttributeError:
            return self.mesh.description

    @property
    def IHOT(self):
        return self._IHOT

    @property
    def _IHOT(self):
        try:
            return self.__IHOT
        except AttributeError:
            if self._runtype == 'coldstart':
                return 0
            elif self._runtype == 'hotstart':
                return 567

    @property
    def NFOVER(self):
        try:
            self.__NFOVER
        except AttributeError:
            return 1

    @property
    def WarnElev(self):
        try:
            return self.__WarnElev
        except AttributeError:
            raise NotImplementedError

    @property
    def iWarnElevDump(self):
        try:
            return self.__iWarnElevDump
        except AttributeError:
            raise NotImplementedError

    @property
    def WarnElevDumpLimit(self):
        try:
            return self.__WarnElevDumpLimit
        except AttributeError:
            raise NotImplementedError

    @property
    def ErrorElev(self):
        try:
            return self.__ErrorElev
        except AttributeError:
            raise NotImplementedError

    @property
    def NABOUT(self):
        try:
            self.__NABOUT
        except AttributeError:
            return 1

    @property
    def NSCREEN(self):
        try:
            return self.__NSCREEN
        except AttributeError:
            return 100

    @property
    def NWS(self) -> int:
        """
        wind stress number
        http://adcirc.org/home/documentation/users-manual-v50/input-file-descriptions/nws-values-table/
        """

        if self._runtype == 'coldstart':
            nws = 0
        elif self.mesh is not None:
            wind_forcing = self.mesh._surface_forcing['imetype']
            if wind_forcing is not None:
                # check for wave forcing here as well.
                nws = int(wind_forcing.NWS % 100)
            else:
                nws = 0
        else:
            nws = 0

        return nws

    @property
    def NRS(self) -> int:
        """
        radiative (wave) stress number

        100 - fort.23
        300 - SWAN
        400 - STWAVE
        500 - WW3
        """

        if self._runtype == 'coldstart':
            nrs = 0
        elif self.mesh is not None:
            wind_forcing = self.mesh._surface_forcing['imetype']
            wave_forcing = self.mesh._surface_forcing['iwrtype']
            if wave_forcing is not None:
                nrs = wave_forcing.NRS
            elif wind_forcing is not None:
                nrs = int(math.floor(wind_forcing.NWS / 100))
            else:
                nrs = 0
        else:
            nrs = 0

        return nrs

    @property
    def ICS(self):
        if self.mesh.crs.is_geographic:
            return 2
        else:
            return 1

    @property
    def IM(self):
        if self.stress_based_3D:
            return 2

        elif self.passive_scalar_transport:
            if self.vertical_mode == '2D':
                if not self.baroclinicity:
                    return 10
                else:
                    return 30
            else:
                if not self.baroclinicity:
                    return 11
                else:
                    return 31
        else:

            def get_digit_1():
                if self.vertical_mode == '2D':
                    if self.lateral_stress_in_gwce == 'kolar_grey':
                        return 1
                    elif self.lateral_stress_in_gwce == 'flux_based':
                        if self.lateral_stress_in_gwce_is_symmetrical:
                            return 4
                        else:
                            return 2
                    elif self.lateral_stress_in_gwce == 'velocity_based':
                        if self.lateral_stress_in_gwce_is_symmetrical:
                            return 5
                        else:
                            return 3
                else:
                    return 6

            def get_digit_2():
                if self.advection_in_gwce == 'non_conservative':
                    return 1
                elif self.advection_in_gwce == 'form_1':
                    return 2
                elif self.advection_in_gwce == 'form_2':
                    return 3

            def get_digit_3():
                if self.lateral_stress_in_momentum == 'velocity_based':
                    if self.lateral_stress_in_momentum_method == 'integration_by_parts':
                        if self.lateral_stress_in_momentum_is_symmetrical:
                            return 3
                        else:
                            return 1
                    else:
                        raise NotImplementedError('not implemented in adcirc')
                        return 5
                elif self.lateral_stress_in_momentum == 'flux_based':
                    if self.lateral_stress_in_momentum_method == 'integration_by_parts':
                        if self.lateral_stress_in_momentum_is_symmetrical:
                            return 4
                        else:
                            return 2
                    else:
                        raise NotImplementedError('not implemented in adcirc')
                        return 6

            def get_digit_4():
                if self.advection_in_momentum == 'non_conservative':
                    return 1
                elif self.advection_in_momentum == 'form_1':
                    return 2
                elif self.advection_in_momentum == 'form_2':
                    return 3

            def get_digit_5():
                if self.area_integration_in_momentum == 'corrected':
                    return 1
                elif self.area_integration_in_momentum == 'original':
                    return 2

            def get_digit_6():
                if (not self.baroclinicity and
                    self.gwce_solution_scheme == 'semi-implicit-legacy'):
                    return 1

                elif (not self.baroclinicity and
                      self.gwce_solution_scheme == 'explicit'):
                    return 2

                elif (not self.baroclinicity and
                      self.gwce_solution_scheme == 'semi-implicit'):
                    return 3

                else:
                    raise Exception(
                        f'No IM digit 6 for {self.baroclinicity}, '
                        f'{self.gwce_solution_scheme}')

                # elif (self.baroclinicity and
                #       self.gwce_solution_scheme == 'semi-implicit'):
                #     return 3
                # elif (self.baroclinicity and
                #       self.gwce_solution_scheme == 'explicit'):
                #     return 4

            IM = '{:d}'.format(get_digit_1())
            IM += '{:d}'.format(get_digit_2())
            IM += '{:d}'.format(get_digit_3())
            IM += '{:d}'.format(get_digit_4())
            IM += '{:d}'.format(get_digit_5())
            IM += '{:d}'.format(get_digit_6())
            return int(IM)

    @property
    def IDEN(self):
        raise NotImplementedError
        return self.__IDEN

    @property
    def NOLIBF(self):
        try:
            return self.__NOLIBF
        except AttributeError:
            NOLIBF = 2
            mesh_attributes = self.mesh.get_nodal_attribute_names()
            for attribute in [
                'quadratic_friction_coefficient_at_sea_floor',
                'mannings_n_at_sea_floor',
                'chezy_friction_coefficient_at_sea_floor',
            ]:
                if attribute in mesh_attributes:
                    attr = self.mesh.get_nodal_attribute(attribute)
                    if self._runtype == 'coldstart':
                        if attr['coldstart'] is True:
                            NOLIBF = 1
                    else:
                        if attr['hotstart'] is True:
                            NOLIBF = 1
            return NOLIBF

    @property
    def NOLIFA(self):
        try:
            return self.__NOLIFA
        except AttributeError:
            return 2

    @property
    def NOLICA(self):
        try:
            return self.__NOLICA
        except AttributeError:
            return 1

    @property
    def NOLICAT(self):
        try:
            return self.__NOLICAT
        except AttributeError:
            return 1

    @property
    def NWP(self):
        if self._runtype == 'coldstart':
            return len(self.mesh.get_coldstart_attributes())
        else:
            return len(self.mesh.get_hotstart_attributes())

    @property
    def NRAMP(self):
        if self.spinup_time.total_seconds() == 0:
            return 1
        if self._runtype == 'coldstart':
            return 1
        else:
            return 8

    @property
    def NCOR(self):
        try:
            return self.__NCOR
        except AttributeError:
            return 1

    @property
    def NTIP(self):
        try:
            NTIP = self.__NTIP
            if NTIP == 2:
                try:
                    self.fort24
                except AttributeError:
                    raise Exception('Must generate fort.24 file.')
            return NTIP
        except AttributeError:
            return 1

    @property
    def CFL(self):
        try:
            return self.__CFL
        except AttributeError:
            return 0.7

    @property
    def G(self):
        try:
            return self.__G
        except AttributeError:
            return 9.81

    @property
    def DTDP(self):
        try:
            return self.__DTDP
        except AttributeError:
            DTDP = self.mesh.critical_timestep(self.CFL)
            if not self.predictor_corrector:
                DTDP = -DTDP
            self.__DTDP = DTDP
            return self.__DTDP

    @property
    def TAU0(self):
        try:
            return self.__TAU0
        except AttributeError:
            if self.mesh.has_nodal_attribute(
                'primitive_weighting_in_continuity_equation', self._runtype
            ):
                return -3
            if self.NOLIBF != 2:
                return self.CF
            else:
                return 0.005

    @property
    def FFACTOR(self):
        try:
            return self.__FFACTOR
        except AttributeError:
            FFACTOR = f'{self.CF:G} '
            if self.NOLIBF == 2:
                FFACTOR += f'{self.HBREAK:G} '
                FFACTOR += f'{self.FTHETA:G} '
                FFACTOR += f'{self.FGAMMA:G}'
                return FFACTOR
            else:
                return FFACTOR

    @property
    def CF(self):
        try:
            return self.__CF
        except AttributeError:
            return 0.0025

    @property
    def ESLM(self):
        try:
            return self.__ESLM
        except AttributeError:
            if self.smagorinsky:
                return -self.smagorinsky_coefficient
            else:
                return self.horizontal_mixing_coefficient

    @property
    def STATIM(self):
        try:
            return self.__STATIM
        except AttributeError:
            if self._runtype == 'coldstart':
                return 0
            else:
                # Looks like this has always to be zero!
                # the following makes adcirc crash with not enough time
                # in meteorological inputs.
                # return (
                #     (self.start_date - self.forcing_start_date).total_seconds()
                #     / (60.*60.*24))
                return 0

    @property
    def REFTIM(self):
        try:
            return self.__REFTIM
        except AttributeError:
            return 0.0

    @property
    def WTIMINC(self):
        if self.NWS not in [0, 1, 9, 11]:
            return int(self.wind_forcing.interval / timedelta(seconds=1))
        else:
            return 0

    @property
    def RSTIMINC(self):
        if self.NRS in [1, 3, 4, 5]:
            if self.wave_forcing is not None:
                return int(self.wave_forcing.interval / timedelta(seconds=1))
            else:
                return self.WTIMINC
        else:
            return 0

    @property
    def RNDAY(self):
        if self._runtype == 'coldstart':
            if self.spinup_time.total_seconds() > 0.0:
                RNDAY = self.start_date - self.forcing_start_date
            else:
                RNDAY = self.end_date - self.start_date
            return RNDAY.total_seconds() / (60.0 * 60.0 * 24.0)
        else:
            RNDAY = self.end_date - self.forcing_start_date
            return RNDAY.total_seconds() / (60.0 * 60.0 * 24.0)

    @property
    def DRAMP(self):
        try:
            DRAMP = '{:<.16G}'.format(self.__DRAMP)
            DRAMP += 10 * ' '
            return DRAMP
        except AttributeError:
            DRAMP = self.spinup_factor * (
                (self.start_date - self.forcing_start_date).total_seconds()
                / (60.0 * 60.0 * 24.0)
            )
            if self.NRAMP in [0, 1]:
                DRAMP = '{:<.16G}'.format(DRAMP)
                DRAMP += 10 * ' '
                return DRAMP
            else:
                DRAMP = '{:<.3f} '.format(DRAMP)
                DRAMP += '{:<.3f} '.format(self.DRAMPExtFlux)
                DRAMP += '{:<.3f} '.format(self.FluxSettlingTime)
                DRAMP += '{:<.3f} '.format(self.DRAMPIntFlux)
                DRAMP += '{:<.3f} '.format(self.DRAMPElev)
                DRAMP += '{:<.3f} '.format(self.DRAMPTip)
                DRAMP += '{:<.3f} '.format(self.DRAMPMete)
                DRAMP += '{:<.3f} '.format(self.DRAMPWRad)
                DRAMP += '{:<.3f} '.format(self.DUnRampMete)
                return DRAMP

    @property
    def DRAMPExtFlux(self):
        try:
            return self.__DRAMPExtFlux
        except AttributeError:
            return 0.0

    @property
    def FluxSettlingTime(self):
        try:
            return self.__FluxSettlingTime
        except AttributeError:
            return 0.0

    @property
    def DRAMPIntFlux(self):
        try:
            return self.__DRAMPIntFlux
        except AttributeError:
            return 0.0

    @property
    def DRAMPElev(self):
        try:
            return self.__DRAMPElev
        except AttributeError:
            return self.spinup_factor * (
                (self.start_date - self.forcing_start_date).total_seconds()
                / (60.0 * 60.0 * 24.0)
            )

    @property
    def DRAMPTip(self):
        try:
            return self.__DRAMPTip
        except AttributeError:
            return self.spinup_factor * (
                (self.start_date - self.forcing_start_date).total_seconds()
                / (60.0 * 60.0 * 24.0)
            )

    @property
    def DRAMPMete(self):
        try:
            return self.__DRAMPMete
        except AttributeError:
            return 1.0

    @property
    def DRAMPWRad(self):
        try:
            return self.__DRAMPWRad
        except AttributeError:
            return 0.0

    @property
    def DUnRampMete(self):
        try:
            return self.__DUnRampMete
        except AttributeError:
            dt = self.start_date - self.forcing_start_date
            return (self.STATIM + dt.total_seconds()) / (24.0 * 60.0 * 60.0)

    @property
    def A00(self):
        try:
            return self.__A00
        except AttributeError:
            if self.gwce_solution_scheme == 'explicit':
                return 0
            if self.gwce_solution_scheme == 'semi-implicit-legacy':
                return 0.35
            if self.gwce_solution_scheme == 'semi-implicit':
                return 0.5

    @property
    def B00(self):
        try:
            return self.__B00
        except AttributeError:
            if self.gwce_solution_scheme == 'explicit':
                return 1
            if self.gwce_solution_scheme == 'semi-implicit-legacy':
                return 0.30
            if self.gwce_solution_scheme == 'semi-implicit':
                return 0.5

    @property
    def C00(self):
        try:
            return self.__C00
        except AttributeError:
            if self.gwce_solution_scheme == 'explicit':
                return 0
            if self.gwce_solution_scheme == 'semi-implicit-legacy':
                return 0.35
            if self.gwce_solution_scheme == 'semi-implicit':
                return 0

    @property
    def H0(self):
        try:
            return self.__H0
        except AttributeError:
            return 0.01

    @property
    def NODEDRYMIN(self):
        try:
            return self.__NODEDRYMIN
        except AttributeError:
            return 0

    @property
    def NODEWETRMP(self):
        try:
            return self.__NODEWETRMP
        except AttributeError:
            return 0

    @property
    def VELMIN(self):
        try:
            return self.__VELMIN
        except AttributeError:
            return 0.01

    @property
    def SLAM0(self):
        try:
            return self.__SLAM0
        except AttributeError:
            return np.median(self.mesh.x)

    @property
    def SFEA0(self):
        try:
            return self.__SFEA0
        except AttributeError:
            return np.median(self.mesh.y)

    @property
    def HBREAK(self):
        try:
            return self.__HBREAK
        except AttributeError:
            return 1.0

    @property
    def FTHETA(self):
        try:
            return self.__FTHETA
        except AttributeError:
            return 10.0

    @property
    def FGAMMA(self):
        try:
            return self.__FGAMMA
        except AttributeError:
            return 1.0 / 3.0

    @property
    def CORI(self):
        try:
            return self.__CORI
        except AttributeError:
            if self.NCOR == 0:
                raise NotImplementedError
            else:
                return 0.0

    @property
    def tidal_forcing(self):
        if not hasattr(self, '_tidal_forcing'):
            self._tidal_forcing = self.mesh._boundary_forcing['iettype'].get(
                'obj')
        return self._tidal_forcing

    @property
    def NTIF(self):
        NTIF = 0
        if self.tidal_forcing is not None:
            for constituent in self.tidal_forcing.get_active_constituents():
                if constituent in self.tidal_forcing.major_constituents:
                    NTIF += 1
        return NTIF

    @property
    def NBFR(self):
        if self.iettype in [3, 5]:
            return self.tidal_forcing.nbfr
        return 0

    @property
    def ANGINN(self):
        try:
            return self.__ANGINN
        except AttributeError:
            return 110.0

    @property
    def NOUTE(self):
        try:
            self.__NOUTE
        except AttributeError:
            return self._get_NOUT__('stations', 'elevation')

    @property
    def TOUTSE(self):
        try:
            return self.__TOUTSE
        except AttributeError:
            return self._get_TOUTS__('stations', 'elevation')

    @property
    def TOUTFE(self):
        try:
            return self.__TOUTFE
        except AttributeError:
            return self._get_TOUTF__('stations', 'elevation')

    @property
    def NSPOOLE(self):
        try:
            return self.__NSPOOLE
        except AttributeError:
            return self._get_NSPOOL__('stations', 'elevation')

    @property
    def NSTAE(self):
        try:
            return self.__NSTAE
        except AttributeError:
            return self._get_NSTA_('elevation')

    @property
    def NOUTV(self):
        try:
            self.__NOUTV
        except AttributeError:
            return self._get_NOUT__('stations', 'velocity')

    @property
    def TOUTSV(self):
        try:
            return self.__TOUTSV
        except AttributeError:
            return self._get_TOUTS__('stations', 'velocity')

    @property
    def TOUTFV(self):
        try:
            return self.__TOUTFV
        except AttributeError:
            return self._get_TOUTF__('stations', 'velocity')

    @property
    def NSPOOLV(self):
        try:
            return self.__NSPOOLV
        except AttributeError:
            return self._get_NSPOOL__('stations', 'velocity')

    @property
    def NSTAV(self):
        try:
            return self.__NSTAV
        except AttributeError:
            return self._get_NSTA_('velocity')

    @property
    def NOUTM(self):
        try:
            self.__NOUTM
        except AttributeError:
            return self._get_NOUT__('stations', 'meteorological')

    @property
    def TOUTSM(self):
        try:
            return self.__TOUTSM
        except AttributeError:
            return self._get_TOUTS__('stations', 'meteorological')

    @property
    def TOUTFM(self):
        try:
            return self.__TOUTFM
        except AttributeError:
            return self._get_TOUTF__('stations', 'meteorological')

    @property
    def NSPOOLM(self):
        try:
            return self.__NSPOOLM
        except AttributeError:
            return self._get_NSPOOL__('stations', 'meteorological')

    @property
    def NSTAM(self):
        try:
            return self.__NSTAM
        except AttributeError:
            return self._get_NSTA_('meteorological')

    @property
    def NOUTC(self):
        try:
            self.__NOUTC
        except AttributeError:
            return self._get_NOUT__('stations', 'concentration')

    @property
    def TOUTSC(self):
        try:
            return self.__TOUTSC
        except AttributeError:
            return self._get_TOUTS__('stations', 'concentration')

    @property
    def TOUTFC(self):
        try:
            return self.__TOUTFC
        except AttributeError:
            return self._get_TOUTF__('stations', 'concentration')

    @property
    def NSPOOLC(self):
        try:
            return self.__NSPOOLC
        except AttributeError:
            return self._get_NSPOOL__('stations', 'concentration')

    @property
    def NSTAC(self):
        try:
            return self.__NSTAC
        except AttributeError:
            return self._get_NSTA_('concentration')

    @property
    def NOUTGE(self):
        try:
            return self.__NOUTGE
        except AttributeError:
            return self._get_NOUT__('surface', 'elevation')

    @property
    def TOUTSGE(self):
        try:
            return self.__TOUTSGE
        except AttributeError:
            return self._get_TOUTS__('surface', 'elevation')

    @property
    def TOUTFGE(self):
        try:
            return self.__TOUTFGE
        except AttributeError:
            return self._get_TOUTF__('surface', 'elevation')

    @property
    def NSPOOLGE(self):
        try:
            return self.__NSPOOLGE
        except AttributeError:
            return self._get_NSPOOL__('surface', 'elevation')

    @property
    def NOUTGV(self):
        try:
            return self.__NOUTGV
        except AttributeError:
            return self._get_NOUT__('surface', 'velocity')

    @property
    def TOUTSGV(self):
        try:
            return self.__TOUTSGV
        except AttributeError:
            return self._get_TOUTS__('surface', 'velocity')

    @property
    def TOUTFGV(self):
        try:
            return self.__TOUTFGV
        except AttributeError:
            return self._get_TOUTF__('surface', 'velocity')

    @property
    def NSPOOLGV(self):
        try:
            return self.__NSPOOLGV
        except AttributeError:
            return self._get_NSPOOL__('surface', 'velocity')

    @property
    def NOUTGM(self):
        try:
            return self.__NOUTGM
        except AttributeError:
            return self._get_NOUT__('surface', 'meteorological')

    @property
    def TOUTSGM(self):
        try:
            return self.__TOUTSGM
        except AttributeError:
            return self._get_TOUTS__('surface', 'meteorological')

    @property
    def TOUTFGM(self):
        try:
            return self.__TOUTFGM
        except AttributeError:
            return self._get_TOUTF__('surface', 'meteorological')

    @property
    def NSPOOLGM(self):
        try:
            return self.__NSPOOLGM
        except AttributeError:
            return self._get_NSPOOL__('surface', 'meteorological')

    @property
    def NOUTGC(self):
        try:
            return self.__NOUTGC
        except AttributeError:
            return self._get_NOUT__('surface', 'concentration')

    @property
    def TOUTSGC(self):
        try:
            return self.__TOUTSGC
        except AttributeError:
            return self._get_TOUTS__('surface', 'concentration')

    @property
    def TOUTFGC(self):
        try:
            return self.__TOUTFGC
        except AttributeError:
            return self._get_TOUTF__('surface', 'concentration')

    @property
    def NSPOOLGC(self):
        try:
            return self.__NSPOOLGC
        except AttributeError:
            return self._get_NSPOOL__('surface', 'concentration')

    @property
    def NFREQ(self):
        if self._runtype == 'coldstart':
            if np.any([_['spinup'] for _ in self._outputs]):
                if np.any([_['sampling_rate'] for _ in self._outputs]):
                    if np.any([_['harmonic_analysis'] for _ in self._outputs]):
                        return len(
                            self.tidal_forcing.get_active_constituents())
        else:
            if np.any([_['sampling_rate'] for _ in self._outputs]):
                if np.any([_['harmonic_analysis'] for _ in self._outputs]):
                    return len(self.tidal_forcing.get_active_constituents())
        return 0

    @property
    def THAS(self):
        try:
            return self.__THAS
        except AttributeError:
            if self.NFREQ > 0:
                try:
                    if self._runtype == 'coldstart':
                        return self.STATIM + float(self.DRAMP)
                    else:
                        dt = self.start_date - self.forcing_start_date
                        return (self.STATIM + dt.total_seconds()) / (
                            24.0 * 60.0 * 60.0)
                except TypeError:
                    #  if self.DRAMP is not castable to float()
                    raise
            else:
                return 0

    @property
    def THAF(self):
        try:
            return self.__THAF
        except AttributeError:
            if self.NFREQ == 0:
                return 0
            dt = self.start_date - self.forcing_start_date
            if self._runtype == 'coldstart':
                if dt.total_seconds() == 0:
                    dt = self.end_date - self.start_date
                    return dt.total_seconds() / (24.0 * 60.0 * 60.0)
                else:
                    return dt.days
            else:
                dt = self.start_date - self.forcing_start_date
                return (self.STATIM + dt.total_seconds()) / (
                    24.0 * 60.0 * 60.0)

    @property
    def NHAINC(self):
        try:
            return self.__NHAINC
        except AttributeError:
            NHAINC = float('inf')
            for _output in self._outputs:
                if _output['harmonic_analysis']:
                    if self._runtype == 'coldstart':
                        if _output['spinup']:
                            fs = _output['sampling_rate']
                            NHAINC = np.min([NHAINC, fs.total_seconds()])
                    else:  # consider a "metonly" run?
                        fs = _output['sampling_rate']
                        NHAINC = np.min([NHAINC, fs.total_seconds()])
            if NHAINC == float('inf'):
                NHAINC = 0
            return int(NHAINC / self.DTDP)

    @property
    def FMV(self):
        try:
            return self.__FMV
        except AttributeError:
            return 0

    @property
    def NHASE(self):
        try:
            return self.__NHASE
        except AttributeError:
            return self._get_harmonic_analysis_state(
                self.elevation_stations_output)

    @property
    def NHASV(self):
        try:
            return self.__NHASV
        except AttributeError:
            return self._get_harmonic_analysis_state(
                self.velocity_stations_output)

    @property
    def NHAGE(self):
        try:
            return self.__NHAGE
        except AttributeError:
            return self._get_harmonic_analysis_state(
                self.elevation_surface_output)

    @property
    def NHAGV(self):
        try:
            return self.__NHAGV
        except AttributeError:
            return self._get_harmonic_analysis_state(
                self.velocity_surface_output)

    @property
    def NHSTAR(self):
        try:
            return self.__NHSTAR
        except AttributeError:
            if self.forcing_start_date == self.start_date:
                return 0
            if self._runtype == 'coldstart':
                if self.netcdf is True:
                    return 5
                else:
                    return 3
            else:
                return 0

    @property
    def NHSINC(self):
        try:
            return self.__NHSINC
        except AttributeError:
            if self.NHSTAR == 0:
                return 0
            else:
                dt = self.start_date - self.forcing_start_date
                if dt.total_seconds() == 0:
                    dt = self.end_date - self.forcing_start_date
                    return int(dt.total_seconds() / np.around(self.DTDP, 6))
                else:
                    return int(dt.total_seconds() / np.around(self.DTDP, 6))

    @property
    def ITITER(self):
        try:
            return self.__ITITER
        except AttributeError:
            return 1

    @property
    def ISLDIA(self):
        try:
            return self.__ISLDIA
        except AttributeError:
            return 0

    @property
    def CONVCR(self):
        try:
            return self.__CONVCR
        except AttributeError:
            # https://stackoverflow.com/questions/19141432/python-numpy-machine-epsilon
            # return 500*(7./3 - 4./3 - 1)
            return 1.0e-8

    @property
    def ITMAX(self):
        try:
            return self.__ITMAX
        except AttributeError:
            return 25

    @property
    def NCPROJ(self):
        try:
            return self.__NCPROJ
        except AttributeError:
            return ""

    @property
    def NCINST(self):
        try:
            return self.__NCINST
        except AttributeError:
            return ""

    @property
    def NCSOUR(self):
        try:
            return self.__NCSOUR
        except AttributeError:
            return ""

    @property
    def NCHIST(self):
        try:
            return self.__NCHIST
        except AttributeError:
            return ""

    @property
    def NCREF(self):
        try:
            return self.__NCREF
        except AttributeError:
            return ""

    @property
    def NCCOM(self):
        try:
            return self.__NCCOM
        except AttributeError:
            return ""

    @property
    def NCHOST(self):
        try:
            return self.__NCHOST
        except AttributeError:
            return ""

    @property
    def NCCONV(self):
        try:
            return self.__NCCONV
        except AttributeError:
            return ""

    @property
    def NCCONT(self):
        try:
            return self.__NCCONT
        except AttributeError:
            return ""

    @property
    def NCDATE(self):
        return self.forcing_start_date.strftime('%Y-%m-%d %H:%M')

    @property
    def FortranNamelists(self):
        return self.__FortranNamelists

    @predictor_corrector.setter
    def predictor_corrector(self, predictor_corrector):
        assert isinstance(predictor_corrector, bool)
        self.__predictor_corrector = predictor_corrector

    @RUNDES.setter
    def RUNDES(self, RUNDES):
        self.__RUNDES = str(RUNDES)

    @_IHOT.setter
    def _IHOT(self, IHOT):
        assert IHOT in [0, 567, 568]
        self.__IHOT = IHOT

    @RUNID.setter
    def RUNID(self, RUNID):
        self.__RUNID = str(RUNID)

    @NFOVER.setter
    def NFOVER(self, NFOVER):
        assert NFOVER in [0, 1]
        self.__NFOVER = NFOVER

    @WarnElev.setter
    def WarnElev(self, WarnElev):
        if WarnElev is not None:
            self.__WarnElev = float(WarnElev)
        else:
            self.__WarnElev = None

    @iWarnElevDump.setter
    def iWarnElevDump(self, iWarnElevDump):
        if iWarnElevDump is not None:
            iWarnElevDump = int(iWarnElevDump)
            if iWarnElevDump not in [0, 1]:
                raise TypeError('iWarnElevDump must be 0 or 1')
            self.__iWarnElevDump = int(iWarnElevDump)
        else:
            if self.WarnElev is not None:
                raise RuntimeError(
                    'Must set iWarnElevDump if WarnElev is not ' + 'None')

    @WarnElevDumpLimit.setter
    def WarnElevDumpLimit(self, WarnElevDumpLimit):
        if WarnElevDumpLimit is not None:
            assert isinstance(WarnElevDumpLimit, int)
            assert WarnElevDumpLimit > 0
            self.__WarnElevDumpLimit = WarnElevDumpLimit
        else:
            if self.WarnElev is not None:
                raise RuntimeError(
                    'Must set WarnElevDumpLimit if WarnElev is ' + 'not None')

    @ErrorElev.setter
    def ErrorElev(self, ErrorElev):
        if ErrorElev is not None:
            self.__ErrorElev = float(ErrorElev)
        else:
            if self.WarnElev is not None:
                raise RuntimeError(
                    'Must set iWarnElevDump if WarnElev is not ' + 'None')

    @NABOUT.setter
    def NABOUT(self, NABOUT):
        assert isinstance(NABOUT, int)
        assert NABOUT in [-1, 0, 1, 2, 3]
        self.__NABOUT = NABOUT

    @NSCREEN.setter
    def NSCREEN(self, NSCREEN):
        assert isinstance(NSCREEN, int)
        self.__NSCREEN = NSCREEN

    @IDEN.setter
    def IDEN(self, IDEN):
        if IDEN is not None:
            raise NotImplementedError('3D runs not yet supported.')

    @NOLIBF.setter
    def NOLIBF(self, NOLIBF):
        assert NOLIBF in [0, 1, 2]
        self.__NOLIBF = NOLIBF

    @NOLIFA.setter
    def NOLIFA(self, NOLIFA):
        NOLIFA = int(NOLIFA)
        assert NOLIFA in [0, 1, 2]
        self.__NOLIFA = NOLIFA

    @NOLICA.setter
    def NOLICA(self, NOLICA):
        NOLICA = int(NOLICA)
        assert NOLICA in [0, 1]
        self.__NOLICA = NOLICA

    @NOLICAT.setter
    def NOLICAT(self, NOLICAT):
        NOLICAT = int(NOLICAT)
        assert NOLICAT in [0, 1]
        self.__NOLICAT = NOLICAT

    @NCOR.setter
    def NCOR(self, NCOR):
        assert NCOR in [0, 1]
        self.__NCOR = NCOR

    @NTIP.setter
    def NTIP(self, NTIP):
        NTIP = int(NTIP)
        assert NTIP in [0, 1, 2]
        self.__NTIP = NTIP

    @G.setter
    def G(self, G):
        self.__G = float(G)

    @TAU0.setter
    def TAU0(self, TAU0):
        self.__TAU0 = float(TAU0)

    @DTDP.setter
    def DTDP(self, DTDP):
        DTDP = np.abs(float(DTDP))
        assert DTDP != 0.0
        self.__DTDP = DTDP

    @STATIM.setter
    def STATIM(self, STATIM):
        self.__STATIM = float(STATIM)

    @REFTIM.setter
    def REFTIM(self, REFTIM):
        self.__REFTIM = float(REFTIM)

    @DRAMP.setter
    def DRAMP(self, DRAMP):
        self.__DRAMP = float(DRAMP)

    @DRAMPExtFlux.setter
    def DRAMPExtFlux(self, DRAMPExtFlux):
        self.__DRAMPExtFlux = float(DRAMPExtFlux)

    @FluxSettlingTime.setter
    def FluxSettlingTime(self, FluxSettlingTime):
        self.__FluxSettlingTime = float(FluxSettlingTime)

    @DRAMPIntFlux.setter
    def DRAMPIntFlux(self, DRAMPIntFlux):
        self.__DRAMPIntFlux = float(DRAMPIntFlux)

    @DRAMPElev.setter
    def DRAMPElev(self, DRAMPElev):
        self.__DRAMPElev = float(DRAMPElev)

    @DRAMPTip.setter
    def DRAMPTip(self, DRAMPTip):
        self.__DRAMPTip = float(DRAMPTip)

    @DRAMPMete.setter
    def DRAMPMete(self, DRAMPMete):
        self.__DRAMPMete = float(DRAMPMete)

    @DRAMPWRad.setter
    def DRAMPWRad(self, DRAMPWRad):
        self.__DRAMPWRad = float(DRAMPWRad)

    @DUnRampMete.setter
    def DUnRampMete(self, DUnRampMete):
        if DUnRampMete is None:
            DUnRampMete = self.DRAMP
        self.__DUnRampMete = float(DUnRampMete)

    @H0.setter
    def H0(self, H0):
        self.__H0 = float(H0)

    @NODEDRYMIN.setter
    def NODEDRYMIN(self, NODEDRYMIN):
        self.__NODEDRYMIN = int(NODEDRYMIN)

    @NODEWETRMP.setter
    def NODEWETRMP(self, NODEWETRMP):
        self.__NODEWETRMP = int(NODEWETRMP)

    @VELMIN.setter
    def VELMIN(self, VELMIN):
        self.__VELMIN = float(VELMIN)

    @SLAM0.setter
    def SLAM0(self, SLAM0):
        self.__SLAM0 = float(SLAM0)

    @SFEA0.setter
    def SFEA0(self, SFEA0):
        self.__SFEA0 = float(SFEA0)

    @FFACTOR.setter
    def FFACTOR(self, FFACTOR):
        self.__FFACTOR = float(FFACTOR)

    @CF.setter
    def CF(self, CF):
        # CF is an alias for FFACTOR
        self.__FFACTOR = float(CF)

    @ESLM.setter
    def ESLM(self, ESLM):
        self.__ESLM = float(ESLM)

    @HBREAK.setter
    def HBREAK(self, HBREAK):
        self.__HBREAK = float(HBREAK)

    @FTHETA.setter
    def FTHETA(self, FTHETA):
        self.__FTHETA = float(FTHETA)

    @FGAMMA.setter
    def FGAMMA(self, FGAMMA):
        self.__FGAMMA = float(FGAMMA)

    @ESLM.setter
    def ESLM(self, ESLM):
        self.__ESLM = float(np.abs(ESLM))

    @NOUTGE.setter
    def NOUTGE(self, NOUTGE):
        self.__NOUTGE = NOUTGE

    @TOUTSGE.setter
    def TOUTSGE(self, TOUTSGE):
        self.__TOUTSGE = float(np.abs(TOUTSGE))

    @TOUTFGE.setter
    def TOUTFGE(self, TOUTFGE):
        self.__TOUTFGE = float(np.abs(TOUTFGE))

    @NSPOOLGE.setter
    def NSPOOLGE(self, NSPOOLGE):
        self.__NSPOOLGE = int(np.abs(NSPOOLGE))

    @NOUTGV.setter
    def NOUTGV(self, NOUTGV):
        self.__NOUTGV = NOUTGV

    @TOUTSGV.setter
    def TOUTSGV(self, TOUTSGV):
        self.__TOUTSGV = float(np.abs(TOUTSGV))

    @TOUTFGV.setter
    def TOUTFGV(self, TOUTFGV):
        self.__TOUTFGV = float(np.abs(TOUTFGV))

    @NSPOOLGV.setter
    def NSPOOLGV(self, NSPOOLGV):
        self.__NSPOOLGV = int(np.abs(NSPOOLGV))

    @NOUTGM.setter
    def NOUTGM(self, NOUTGM):
        self.__NOUTGM = NOUTGM

    @TOUTSGM.setter
    def TOUTSGM(self, TOUTSGM):
        self.__TOUTSGM = float(np.abs(TOUTSGM))

    @TOUTFGM.setter
    def TOUTFGM(self, TOUTFGM):
        self.__TOUTFGM = float(np.abs(TOUTFGM))

    @NSPOOLGM.setter
    def NSPOOLGM(self, NSPOOLGM):
        self.__NSPOOLGM = int(np.abs(NSPOOLGM))

    @NOUTGC.setter
    def NOUTGC(self, NOUTGC):
        self.__NOUTGC = NOUTGC

    @TOUTSGC.setter
    def TOUTSGC(self, TOUTSGC):
        self.__TOUTSGC = float(np.abs(TOUTSGC))

    @TOUTFGC.setter
    def TOUTFGC(self, TOUTFGC):
        self.__TOUTFGC = float(np.abs(TOUTFGC))

    @NSPOOLGC.setter
    def NSPOOLGC(self, NSPOOLGC):
        self.__NSPOOLGC = int(np.abs(NSPOOLGC))

    @CORI.setter
    def CORI(self, CORI):
        if CORI is None:
            if self.NCOR == 0:
                raise Exception('Must pass CORI when NCOR=0')
            else:
                CORI = 0.0
        else:
            CORI = float(CORI)
        self.__CORI = CORI

    @ANGINN.setter
    def ANGINN(self, ANGINN):
        self.__ANGINN = float(ANGINN)

    @THAS.setter
    def THAS(self, THAS):
        THAS = float(THAS)
        assert THAS >= 0.0
        self.__THAS = THAS

    @THAF.setter
    def THAF(self, THAF):
        THAF = float(THAF)
        assert THAF >= 0.0
        self.__THAF = THAF

    @NHAINC.setter
    def NHAINC(self, NHAINC):
        NHAINC = int(NHAINC)
        assert NHAINC >= 0
        self.__NHAINC = NHAINC

    @FMV.setter
    def FMV(self, FMV):
        FMV = float(FMV)
        assert FMV >= 0.0 and FMV <= 1.0
        self.__FMV = FMV

    @NHSTAR.setter
    def NHSTAR(self, NHSTAR):
        assert NHSTAR in [0, 1, 2, 3, 5]
        self.__NHSTAR = NHSTAR

    @NHSINC.setter
    def NHSINC(self, NHSINC):
        self.__NHSINC = int(NHSINC)

    @ITITER.setter
    def ITITER(self, ITITER):
        ITITER = int(ITITER)
        assert ITITER in [1, -1]
        self.__ITITER = ITITER

    @ISLDIA.setter
    def ISLDIA(self, ISLDIA):
        ISLDIA = int(ISLDIA)
        assert ISLDIA in [0, 1, 2, 3, 4, 5]
        self.__ISLDIA = ISLDIA

    @CONVCR.setter
    def CONVCR(self, CONVCR):
        self.__CONVCR = float(CONVCR)

    @ITMAX.setter
    def ITMAX(self, ITMAX):
        self.__ITMAX = int(ITMAX)

    @NCPROJ.setter
    def NCPROJ(self, NCPROJ):
        self.__NCPROJ = str(NCPROJ)

    @NCINST.setter
    def NCINST(self, NCINST):
        self.__NCINST = str(NCINST)

    @NCSOUR.setter
    def NCSOUR(self, NCSOUR):
        self.__NCSOUR = str(NCSOUR)

    @NCHIST.setter
    def NCHIST(self, NCHIST):
        self.__NCHIST = str(NCHIST)

    @NCREF.setter
    def NCREF(self, NCREF):
        self.__NCREF = str(NCREF)

    @NCCOM.setter
    def NCCOM(self, NCCOM):
        self.__NCCOM = str(NCCOM)

    @NCHOST.setter
    def NCHOST(self, NCHOST):
        self.__NCHOST = str(NCHOST)

    @NCCONV.setter
    def NCCONV(self, NCCONV):
        self.__NCCONV = str(NCCONV)

    @NCCONT.setter
    def NCCONT(self, NCCONT):
        self.__NCCONT = str(NCCONT)

    @vertical_mode.setter
    def vertical_mode(self, vertical_mode):
        assert vertical_mode in ['2D', '3D']
        self.__vertical_mode = vertical_mode

    @timestep.setter
    def timestep(self, timestep):
        self.DTDP = timestep

    @lateral_stress_in_gwce.setter
    def lateral_stress_in_gwce(self, lateral_stress_in_gwce):
        assert lateral_stress_in_gwce in ['kolar-grey', 'velocity_based',
                                          'flux_based']
        self.__lateral_stress_in_gwce = lateral_stress_in_gwce

    @lateral_stress_in_gwce_is_symmetrical.setter
    def lateral_stress_in_gwce_is_symmetrical(self,
                                              lateral_stress_in_gwce_is_symmetrical):
        self.__lateral_stress_in_gwce_is_symmetrical = bool(
            lateral_stress_in_gwce_is_symmetrical
        )

    @advection_in_gwce.setter
    def advection_in_gwce(self, advection_in_gwce):
        assert advection_in_gwce in ['non_conservative', 'form_1', 'form_2']
        self.__advection_in_gwce = advection_in_gwce

    @lateral_stress_in_momentum.setter
    def lateral_stress_in_momentum(self, lateral_stress_in_momentum):
        assert lateral_stress_in_momentum in ['velocity_based', 'flux_based']
        self.__lateral_stress_in_momentum = lateral_stress_in_momentum

    @lateral_stress_in_momentum_is_symmetrical.setter
    def lateral_stress_in_momentum_is_symmetrical(
        self, lateral_stress_in_momentum_is_symmetrical
    ):
        self.__lateral_stress_in_momentum_is_symmetrical = bool(
            lateral_stress_in_momentum_is_symmetrical
        )

    @lateral_stress_in_momentum_method.setter
    def lateral_stress_in_momentum_method(self,
                                          lateral_stress_in_momentum_method):
        assert lateral_stress_in_momentum_method in ['2_part',
                                                     'integration_by_parts']
        self.__lateral_stress_in_momentum_method = lateral_stress_in_momentum_method

    @advection_in_momentum.setter
    def advection_in_momentum(self, advection_in_momentum):
        assert advection_in_momentum in ['non_conservative', 'form_1',
                                         'form_2']
        self.__advection_in_momentum = advection_in_momentum

    @area_integration_in_momentum.setter
    def area_integration_in_momentum(self, area_integration_in_momentum):
        assert area_integration_in_momentum in ['corrected', 'original']
        self.__area_integration_in_momentum = area_integration_in_momentum

    @baroclinicity.setter
    def baroclinicity(self, baroclinicity):
        self.__baroclinicity = bool(baroclinicity)

    @gwce_solution_scheme.setter
    def gwce_solution_scheme(self, gwce_solution_scheme):
        assert gwce_solution_scheme in ['semi-implicit', 'explicit',
                                        'semi-implicit-legacy']
        self.__gwce_solution_scheme = gwce_solution_scheme

    @passive_scalar_transport.setter
    def passive_scalar_transport(self, passive_scalar_transport):
        self.__passive_scalar_transport = bool(passive_scalar_transport)

    @stress_based_3D.setter
    def stress_based_3D(self, stress_based_3D):
        self.__stress_based_3D = bool(stress_based_3D)

    @smagorinsky.setter
    def smagorinsky(self, smagorinsky):
        self.__smagorinsky = bool(smagorinsky)

    @smagorinsky_coefficient.setter
    def smagorinsky_coefficient(self, smagorinsky_coefficient):
        self.__smagorinsky_coefficient = np.abs(float(smagorinsky_coefficient))

    @horizontal_mixing_coefficient.setter
    def horizontal_mixing_coefficient(self, horizontal_mixing_coefficient):
        self.__horizontal_mixing_coefficient = np.abs(
            float(horizontal_mixing_coefficient))

    @CFL.setter
    def CFL(self, CFL):
        self.__CFL = float(CFL)

    def _get_active_tidal_potential_constituents(self):
        if self.iettype in [3, 5]:
            return self.tidal_forcing.get_active_potential_constituents()
        else:
            return []

    def _get_active_tidal_forcing_constituents(self):
        if self.iettype in [3, 5]:
            return self.tidal_forcing.get_active_forcing_constituents()
        else:
            return []

    @property
    def elevbc(self):
        return self.mesh._boundary_forcing['iettype']['obj']

    @property
    def iettype(self):
        if self.elevbc is not None:
            return self.elevbc.iettype
        else:
            return 0

    def _get_NSTA_(self, physical_var):
        stations = self._container['stations'][physical_var]
        if self._runtype == 'coldstart':
            if stations['spinup'] is not None:
                return len(stations['collection'].keys())
            else:
                return 0
        else:
            if np.abs(self._get_NOUT__('stations', physical_var)) > 0:
                return len(stations['collection'].keys())
            else:
                return 0

    def _get_NOUT__(self, output_type, physical_var):
        output = self._container[output_type][physical_var]
        if self._runtype == 'coldstart':
            if output['spinup'] is not None:
                if output['netcdf'] is True:
                    return -5
                else:
                    return -1
            else:
                return 0

        elif self._runtype == 'hotstart':
            if output['sampling_rate'] is not None:
                if output['netcdf'] is True:
                    return -5
                else:
                    return -1
            else:
                return 0

    def _get_TOUTS__(self, output_type, physical_var):
        output = self._container[output_type][physical_var]
        # coldstart
        if self._runtype == 'coldstart':
            if output['spinup'] is not None:
                start = output['spinup_start']
            else:
                return 0

        # hotstart
        else:
            if output['sampling_rate'] is not None:
                start = output['start']
            else:
                return 0

        # typecast
        if isinstance(start, int):  # int interpreted as literal timestep
            start = timedelta(seconds=(start * self.timestep))
            if self._runtype == 'coldstart':
                start = start - self.forcing_start_date
            else:
                start = start - self.start_date

        elif isinstance(start, type(None)):
            if self._runtype == 'hotstart':
                dt = self.start_date - self.forcing_start_date
                return dt.total_seconds() / (60 * 60 * 24)
            else:
                return 0

        return start.total_seconds() / (60.0 * 60.0 * 24.0)

    def _get_TOUTF__(self, output_type, physical_var):
        output = self._container[output_type][physical_var]
        # coldstart
        if self._runtype == 'coldstart':
            if output['spinup'] is not None:
                if output['spinup_end'] is None:
                    if self.NOUTGE != 0:
                        time = self.spinup_time.total_seconds() / (
                            60.0 * 60.0 * 24.0)
                        if time > 0:
                            return time
                        else:
                            dt = self.end_date - self.start_date
                            return dt.total_seconds() / (60.0 * 60.0 * 24.0)
                    else:
                        return 0
                else:
                    raise NotImplementedError
            else:
                return 0

        # hotstart
        elif self._runtype == 'hotstart':
            if output['sampling_rate'] is not None:
                if output['end'] is None:
                    if self._runtype == 'hotstart':
                        dt = self.end_date - self.forcing_start_date
                        return dt.total_seconds() / (60 * 60 * 24)
                    # if self.NOUTGE != 0:
                    #     time = self.spinup_time.total_seconds()/(60.*60.*24.)
                    #     if time > 0:
                    #         return time
                    #     else:
                    #         dt = self.end_date - self.forcing_start_date
                    #         return dt.total_seconds()/(60.*60.*24.)
                    else:
                        dt = self.start_date - self.forcing_start_date
                        return dt.total_seconds() / (60 * 60 * 24)
                else:
                    raise NotImplementedError
            else:
                return 0

    def _get_NSPOOL__(self, output_type, physical_var):
        output = self._container[output_type][physical_var]
        if self._runtype == 'coldstart':
            if output['spinup']:
                return int(round(output['spinup'].total_seconds() / self.DTDP))
            else:
                return 0
        else:
            if output['sampling_rate'] is not None:
                if output_type == 'surface' and output[
                    'sampling_rate'].total_seconds() == 0:
                    return int((
                                   self.end_date - self.start_date).total_seconds() / self.DTDP)
                return int(round(
                    (output['sampling_rate'].total_seconds() / self.DTDP)))
            else:
                return 0

    def _get_harmonic_analysis_state(self, output):
        state = 0
        if self._runtype == 'coldstart':
            if output['spinup'] and output['harmonic_analysis']:
                if self.netcdf:
                    return 5
                else:
                    return 1
        else:
            if output['harmonic_analysis']:
                if self.netcdf:
                    return 5
                else:
                    return 1
        return state
