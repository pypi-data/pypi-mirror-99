import os
import numpy as np
import pickle
import astropy.units as u
import astropy.constants as const
import mathMB
from atomicdataMB import atomicmass


def sputdist(velocity, U, alpha, beta, species):
    mspecies = atomicmass(species)
    v_b = np.sqrt(2*U/mspecies)
    v_b = v_b.to(u.km/u.s)
    f_v = velocity**(2*beta+1) / (velocity**2 + v_b**2)**alpha
    f_v /= np.max(f_v)
    return f_v.value


def MaxwellianDist(velocity, temperature, species):
    vth2 = 2*temperature*const.k_B/atomicmass(species)
    vth2 = vth2.to(u.km**2/u.s**2)
    f_v = velocity**3 * np.exp(-velocity**2/vth2)
    f_v /= np.max(f_v)
    return f_v.value


def xyz_from_lonlat(lon, lat, isplan, exobase):
    if isplan:
        # Starting at a planet
        # 0 deg longitude = subsolar pt. = (0, -1, 0)
        # 90 deg longitude = dusk pt. = (1, 0, 0)
        # 270 deg longitude = dawn pt. = (-1, 0, 0)
        x0 = exobase * np.sin(lon) * np.cos(lat)
        y0 = -exobase * np.cos(lon) * np.cos(lat)
        z0 = exobase * np.sin(lat)
    else:
        # Starting at a satellite
        # 0 deg longitude = sub-planet pt. = (0, -1, 0)
        # 90 deg longitude = leading pt. = (-1, 0, 0)
        # 270 deg longitude = trailing pt. = (1, 0, 0)
        x0 = -exobase * np.sin(lon) * np.cos(lat)
        y0 = -exobase * np.cos(lon) * np.cos(lat)
        z0 = exobase * np.sin(lat)

    X0 = np.array([x0, y0, z0])

    # Error checking
    assert np.all(np.isfinite(X0)), 'Non-Finite values of X0'
    return X0


def surface_distribution(outputs):
    """ Distribute packets on a sphere with radius r = SpatialDist.exobase

    Returns (x0, y0, z0, lon0, lat0)
    for satellites, assumes satellite is at phi=0
    """

    spatialdist = outputs.inputs.spatialdist
    npack = outputs.npackets
    
    if spatialdist.type == 'uniform':
        # Choose the latitude: f(lat) = cos(lat)
        lat0 = spatialdist.latitude
        if lat0[0] == lat0[1]:
            lat = np.zeros(npack)+lat0[0]
        else:
            ll = (np.sin(lat0[0]), np.sin(lat0[1]))
            sinlat = ll[0] + (ll[1]-ll[0]) * outputs.randgen.random(npack)
            lat = np.arcsin(sinlat)
    
        # Choose the longitude: f(lon) = 1/(lonmax-lonmin)
        lon0 = spatialdist.longitude
        if lon0[0] > lon0[1]:
            lon0 = [lon0[0], lon0[1]+2*np.pi*u.rad]
        lon = ((lon0[0] + (lon0[1]-lon0[0]) * outputs.randgen.random(npack)) %
               (2*np.pi*u.rad))
    elif spatialdist.type == 'surface map':
        # Choose lon, lat based on predetermined map
        if spatialdist.mapfile == 'default':
            mapfile = os.path.join(os.path.dirname(__file__), 'data',
                f'{outputs.inputs.options.species}_surface_composition.pkl')
            with open(mapfile, 'rb') as mfile:
                sourcemap = pickle.load(mfile)
        elif spatialdist.mapfile.endswith('.pkl'):
            with open(spatialdist.mapfile, 'rb') as mfile:
                sourcemap = pickle.load(mfile)
        elif spatialdist.mapfile.endswith('.sav'):
            from scipy.io import readsav
            sourcemap_ = readsav(spatialdist.mapfile)['sourcemap']
            sourcemap = {'longitude':sourcemap_['longitude'][0]*u.rad,
                         'latitude':sourcemap_['latitude'][0]*u.rad,
                         'abundance':sourcemap_['map'][0].transpose(),
                         'coordinate_system':str(sourcemap_['coordinate_system'][0])}
        else:
            assert 0, 'Mapfile is the wrong format.'

        lon, lat = mathMB.random_deviates_2d(sourcemap['abundance'],
                                             sourcemap['longitude'],
                                             np.sin(sourcemap['latitude']),
                                             npack)
        lat = np.arcsin(lat)
        
        if (('planet' in sourcemap['coordinate_system']) and
            (outputs.inputs.spatialdist.subsolarlon is not None)):
            # Need to rotate to model coordinate system
            lon = ((outputs.inputs.spatialdist.subsolarlon.value - lon +
                    2*np.pi) % (2*np.pi))
        elif ('planet' in sourcemap['coordinate_system']):
            raise ValueError('inputs.spatialdist.subsolarlon is None')
        else:
            pass
    elif spatialdist.type == 'surface spot':
        lon0 = spatialdist.longitude
        lat0 = spatialdist.latitude
        sigma0 = spatialdist.sigma
    
        spot0 = ((np.sin(lon0)*np.cos(lat0)).value,
                 (-np.cos(lon0)*np.cos(lat0)).value,
                 (np.sin(lat0)).value)
        longitude = np.linspace(0, 2*np.pi, 361)*u.rad
        latitude = np.linspace(-np.pi/2, np.pi/2, 181)*u.rad
    
        ptsx = np.outer(np.sin(longitude.value), np.cos(latitude.value))
        ptsy = -np.outer(np.cos(longitude.value), np.cos(latitude.value))
        ptsz = -np.outer(np.ones_like(longitude.value), np.sin(latitude.value))
    
        cosphi = ptsx*spot0[0]+ptsy*spot0[1]+ptsz*spot0[2]
        cosphi[cosphi > 1] = 1
        cosphi[cosphi < -1] = -1
        phi = np.arccos(cosphi)
        sourcemap = np.exp(-phi/sigma0.value)
    
        lon, lat = mathMB.random_deviates_2d(sourcemap, longitude,
                                             np.sin(latitude), npack)
        lat = np.arcsin(lat)
    else:
        assert 0, "Can't get here"

    X_ = xyz_from_lonlat(lon, lat,
                         outputs.inputs.geometry.planet.type == 'Planet',
                         spatialdist.exobase)
    outputs.X0['x'] = X_[0,:]
    outputs.X0['y'] = X_[1,:]
    outputs.X0['z'] = X_[2,:]
    outputs.X0['longitude'] = lon
    outputs.X0['latitude'] = lat
    local_time = (lon.value * 12/np.pi + 12) % 24
    outputs.X0['local_time'] = local_time


def speed_distribution(outputs):
    speeddist = outputs.inputs.speeddist
    npackets = outputs.npackets

    if speeddist.type.lower() == 'gaussian':
        if speeddist.sigma == 0.:
            v0 = np.zeros(npackets)*u.km/u.s + speeddist.vprob
        else:
            v0 = (outputs.randgen.standard_normal(npackets) *
                  speeddist.sigma.value + speeddist.vprob.value)
            v0 *= speeddist.vprob.unit
    elif speeddist.type == 'sputtering':
        velocity = np.linspace(.1, 50, 5000)*u.km/u.s
        f_v = sputdist(velocity, speeddist.U, speeddist.alpha,
                       speeddist.beta, outputs.inputs.options.species)

        v0 = (mathMB.random_deviates_1d(velocity.value, f_v, npackets) *
              velocity.unit)
    elif speeddist.type == 'maxwellian':
        if speeddist.temperature != 0*u.K:
            # Use a constant temperature
            amass = atomicmass(outputs.inputs.options.species)
            v_th = np.sqrt(2*speeddist.temperature*const.k_B/amass)
            v_th = v_th.to(u.km/u.s)
            velocity = np.linspace(0.1*u.km/u.s, v_th*5, 5000)
            f_v = MaxwellianDist(velocity, speeddist.temperature,
                                 outputs.inputs.options.species)
            v0 = (mathMB.random_deviates_1d(velocity.value, f_v, npackets) *
                  velocity.unit)
        else:
            # Use a surface temperature map
            # Need to write this
            assert 0, 'Not implemented yet'
    elif speeddist.type == 'flat':
        v0 = (outputs.randgen.random(npackets)*2*speeddist.delv +
              speeddist.vprob - speeddist.delv)
    elif speeddist.type == 'user defined':
        source = pickle.load(open(speeddist.vdistfile, 'rb'))
        v0 = mathMB.random_deviates_1d(source['velocity'].value, source['vdist'],
                                       npackets) * source['velocity'].unit
    else:
        # Need to add more distributions
        assert 0, 'Distribtuion does not exist'
        
    v0 = v0.to(outputs.unit/u.s)
    outputs.X0['v'] = v0.value

    assert np.all(np.isfinite(v0)), 'Infinite values for v0'

    return v0


def angular_distribution(outputs):
    npackets = outputs.npackets

    angulardist = outputs.inputs.angulardist

    if angulardist.type == 'none':
        return
    elif angulardist.type == 'radial':
        # All packets going radially outward
        alt = (np.zeros(npackets) + np.pi/2.) * u.rad
        az = np.zeros(npackets) * u.rad
    elif angulardist.type == 'isotropic':
        # Choose the altitude -- f(alt) = cos(alt)
        alt0 = angulardist.altitude
        aa = (np.sin(alt0[0]), np.sin(alt0[1]))
        sinalt = outputs.randgen.random(npackets) * (aa[1] - aa[0]) + aa[0]
        alt = np.arcsin(sinalt)

        # Choose the azimuth -- f(az) = 1/(azmax-azmin)
        az0, az1 = angulardist.azimuth
        m = (az0, az1) if az0 < az1 else (az1, az0+2*np.pi)
        az = m[0] + (m[1]-m[0])*outputs.randgen.random(npackets)
    else:
        assert 0, 'Angular Distribution not defined.'

    # Find the velocity components in coordinate system centered on packet
    v_rad = np.sin(alt.value)                 # Radial component of velocity
    v_tan0 = np.cos(alt.value) * np.cos(az.value)   # Component along latitude (points E)
    v_tan1 = np.cos(alt.value) * np.sin(az.value)   # Component along longitude (points N)

    # Now rotate to proper surface point
    # v_ren = M # v_xyz => v_xyz = invert(M) # v_ren
    X0 = outputs.X0.values
    x0, y0, z0 = X0[:,2], X0[:,3], X0[:,4]

    rad = np.array([x0, y0, z0]).transpose()
    east = np.array([y0, -x0, np.zeros_like(z0)]).transpose()
    north = np.array([-z0*x0, -z0*y0, x0**2+y0**2]).transpose()

    rad_ = np.linalg.norm(rad, axis=1)
    rad = rad/rad_[:,np.newaxis]
    east_ = np.linalg.norm(east, axis=1)
    east = east/east_[:,np.newaxis]
    north_ = np.linalg.norm(north, axis=1)
    north = north/north_[:,np.newaxis]

    v0 = (v_tan0[:,np.newaxis]*north + v_tan1[:,np.newaxis]*east +
          v_rad[:,np.newaxis]*rad)
    
    outputs.X0['vx'] = v0[:,0] * outputs.X0.v.values
    outputs.X0['vy'] = v0[:,1] * outputs.X0.v.values
    outputs.X0['vz'] = v0[:,2] * outputs.X0.v.values
