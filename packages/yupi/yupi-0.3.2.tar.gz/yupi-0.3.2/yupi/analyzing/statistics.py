import numpy as np
import scipy.stats
from yupi.analyzing import turning_angles, subsample_trajectory

# relative and cumulative turning angles
def estimate_turning_angles(trajs, accumulate=False, 
                    degrees=False, centered=False):    
    """[summary]

    Parameters
    ----------
    trajs : [type]
        [description]
    accumulate : bool, optional
        [description], by default False
    degrees : bool, optional
        [description], by default False
    centered : bool, optional
        [description], by default False

    Returns
    -------
    [type]
        [description]
    """

    theta = [turning_angles(traj) for traj in trajs]
    return np.concatenate(theta)


# Returns measured velocity samples on all the trajectories
# subsampling them at a given stem
def estimate_velocity_samples(trajs, step):
    """[summary]

    Parameters
    ----------
    trajs : [type]
        [description]
    step : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """

    step = 1
    trajs_ = [subsample_trajectory(traj, step) for traj in trajs]
    return np.concatenate([traj.velocity() for traj in trajs_])

# mean square displacement (ensemble average)
def estimate_msd_ensemble(trajs):
    """[summary]

    Parameters
    ----------
    trajs : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """

    msd = []
    for traj in trajs:
        # position vectors
        r = traj.position_vectors()

        # square displacements
        r_2 = (r - r[0])**2            # square coordinates
        r2 = np.sum(r_2, axis=1)       # square distances
        msd.append(r2)                 # append square distances
    
    # transpose to have time/trials as first/second axis
    msd = np.transpose(msd)
    return msd


# mean square displacement (time average)
def estimate_msd_time(trajs, lag):
    """[summary]

    Parameters
    ----------
    trajs : [type]
        [description]
    lag : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """

    msd = []
    for traj in trajs:
        # position vectors
        r = traj.position_vectors()

        # compute msd for a single trajectory
        msd_ = np.empty(lag)
        for lag_ in range(1, lag + 1):
            dr = r[lag_:] - r[:-lag_]      # lag displacement vectors
            dr2 = np.sum(dr**2, axis=1)    # lag displacement
            msd_[lag_ - 1] = np.mean(dr2)  # averaging over a single realization
        
        # append all square displacements
        msd.append(msd_)
    
    # transpose to have time/trials as first/second axis
    msd = np.transpose(msd)
    return msd


# mean square displacement
def estimate_msd(trajs, time_avg=True, lag=None):
    """[summary]

    Parameters
    ----------
    trajs : [type]
        [description]
    time_avg : bool, optional
        [description], by default True
    lag : [type], optional
        [description], by default None

    Returns
    -------
    [type]
        [description]
    """

    if not time_avg:
        msd = estimate_msd_ensemble(trajs)   # ensemble average
    else:
        msd = estimate_msd_time(trajs, lag)  # time average

    msd_mean = np.mean(msd, axis=1)  # mean
    msd_std = np.std(msd, axis=1)    # standard deviation
    return msd_mean, msd_std


# velocity autocorrelation function (ensemble average)
def estimate_vacf_ensemble(trajs):
    """[summary]

    Parameters
    ----------
    trajs : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """

    vacf = []
    for traj in trajs:
        # cartesian velocity components
        v = traj.velocity_vectors()

        # pair-wise dot product between velocities at t0 and t
        v0_dot_v = np.sum(v[0] * v, axis=1)
        
        # append all veloctiy dot products
        vacf.append(v0_dot_v)

    # transpose to have time/trials as first/second axis
    vacf = np.transpose(vacf)
    return vacf


# velocity autocorrelation function (time average)
def estimate_vacf_time(trajs, lag):
    """[summary]

    Parameters
    ----------
    trajs : [type]
        [description]
    lag : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """

    vacf = []
    for traj in trajs:
        # cartesian velocity components
        v = traj.velocity_vectors()

        # compute vacf for a single trajectory
        vacf_ = np.empty(lag)
        for lag_ in range(1, lag + 1):
            v1v2 = v[:-lag_] * v[lag_:]           # multiply components given lag
            v1_dot_v2 = np.sum(v1v2, axis=1)      # dot product for a given lag time
            vacf_[lag_ - 1] = np.mean(v1_dot_v2)  # averaging over a single realization

        # append the vacf for a every single realization
        vacf.append(vacf_)

    # transpose to have time/trials as first/second axis
    vacf = np.transpose(vacf)
    return vacf


# velocity autocorrelation function
def estimate_vacf(trajs, time_avg=True, lag=None):
    """[summary]

    Parameters
    ----------
    trajs : [type]
        [description]
    time_avg : bool, optional
        [description], by default True
    lag : [type], optional
        [description], by default None

    Returns
    -------
    [type]
        [description]
    """

    if not time_avg:
        vacf = estimate_vacf_ensemble(trajs)   # ensemble average
    else:
        vacf = estimate_vacf_time(trajs, lag)  # time average

    vacf_mean = np.mean(vacf, axis=1)  # mean
    vacf_std = np.std(vacf, axis=1)    # standard deviation
    return vacf_mean, vacf_std


# kurtosis (ensemble average)
# TODO: Fix this implementation for dim != 2 Traj
def estimate_kurtosis_ensemble(trajs):
    """[summary]

    Parameters
    ----------
    trajs : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """

    kurtosis = []
    for traj in trajs:
        dx = traj.x - traj.x[0]
        dy = traj.y - traj.y[0]
        kurt = np.sqrt(dx**2 + dy**2)
        kurtosis.append(kurt)
    return scipy.stats.kurtosis(kurtosis, axis=0, fisher=False)


# kurtosis (time average)
# TODO: Fix this implementation for dim != 2 Traj
def estimate_kurtosis_time(trajs, lag):
    """[summary]

    Parameters
    ----------
    trajs : [type]
        [description]
    lag : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """

    kurtosis = []
    for traj in trajs:
        kurt = np.empty(lag)
        for lag_ in range(1, lag + 1):
            dx = traj.x[lag_:] - traj.x[:-lag_]
            dy = traj.y[lag_:] - traj.y[:-lag_]
            dr = np.sqrt(dx**2 + dy**2)
            kurt[lag_ - 1] = scipy.stats.kurtosis(dr, fisher=False)
        kurtosis.append(kurt)
    return np.mean(kurtosis, axis=0)


# get displacements for ensemble average and
# kurtosis for time average
def estimate_kurtosis(trajs, time_avg=True, lag=None):
    """[summary]

    Parameters
    ----------
    trajs : [type]
        [description]
    time_avg : bool, optional
        [description], by default True
    lag : [type], optional
        [description], by default None

    Returns
    -------
    [type]
        [description]
    """

    if not time_avg:
        return estimate_kurtosis_ensemble(trajs)
    else:
        return estimate_kurtosis_time(trajs, lag)
