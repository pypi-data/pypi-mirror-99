import numpy as np
import json
import csv
import os
from typing import NamedTuple
from pathlib import Path

TrajectoryPoint = NamedTuple('TrajectoryPoint', x=float, y=float, z=float,
                             t=float, theta=float)


class Trajectory():
    """
    Represents a trajectory.

    Parameters
    ----------
    x : np.ndarray
        Array containing position data of X axis.
    y : np.ndarray
        Array containing position data of Y axis. (Default is None).
    z : np.ndarray
        Array containing position data of X axis. (Default is None).
    t : np.ndarray
        Array containing time data. (Default is None).
    theta : np.ndarray
        Array containing angle data. (Default is None).
    dt : float
        If no time data (``t``) is given this represents the time
        between each position data value.
    id : str
        Id of the trajectory.

    Attributes
    ----------
    dt : float
        If no time data (``t``) is given this represents the time
        between each position data value.
    id : str
        Id of the trajectory.

    Raises
    ------
    ValueError
        If ``x`` is not given.
    ValueError
        If all the given position data (``x``, ``y`` and/or ``z``)
        does not have the same shape.
    """

    def __init__(self, x: np.ndarray, y: np.ndarray = None,
                 z: np.ndarray = None, t: np.ndarray = None,
                 theta: np.ndarray = None, dt: float = 1.0, 
                 id: str = None):

        self.data = [x, y, z, t, theta]        


        for i, item in enumerate(self.data):
            if item is not None:
                self.data[i] = np.array(item)

        lengths = [len(item) for item in self.data if item is not None]
        
        if x is None:
            raise ValueError('Trajectory requires at least one dimension')
        elif lengths.count(lengths[0]) != len(lengths):
            raise ValueError('All input arrays must have the same shape')

        self.dt = dt
        self.id = id
    
    @property
    def x(self) -> np.ndarray:
        """np.ndarray : Array containing position data of X axis."""
        return self.data[0]

    @property
    def y(self) -> np.ndarray:
        """np.ndarray : Array containing position data of Y axis."""
        return self.data[1]

    @property
    def z(self) -> np.ndarray:
        """np.ndarray : Array containing position data of Z axis."""
        return self.data[2]

    @property
    def t(self) -> np.ndarray:
        """np.ndarray : Array containing time data."""
        return self.data[3]

    @property
    def theta(self) -> np.ndarray:
        """np.ndarray : Array containing angle data."""
        return self.data[4]
    
    @property
    def dim(self) -> int:
        """int : Trajectory dimension."""
        for i, d in enumerate(self.data[:3]):
            if d is None:
                return i
        return 3
        
    def __len__(self):
        return len(self.x)

    def __iter__(self):
        current_time = 0
        for i in range(len(self)):
            # x, y, z, t, theta
            sp = [None]*5

            for j, d in enumerate(self.data):
                sp[j] = d[i] if d is not None else None

            if sp[3] is None and self.dt is not None: 
                sp[3] = current_time
                current_time += self.dt

            x, y, z, t, theta = sp
            yield TrajectoryPoint(x, y, z, t, theta)

    @staticmethod
    def save_trajectories(trajectories: list, folder_path: str = '.',
                          file_type: str = 'json', overwrite: bool = True):
        """
        Save a list of trajectories.

        Parameters
        ----------
        trajectories : list[Trajectory]
            List of trajectories that will be saved.
        folder_path : str
            Path where to save the trajectory. (Default is ``'.'``).
        file_type : str
            Type of the file. (Default is ``json``).

            The only types avaliable are: ``json`` and ``csv``.
        overwrite : bool
            Wheter or not to overwrite the file if it already exists. (Default
            is True).
        """

        for i, traj in enumerate(trajectories):
            path = str(Path(folder_path))
            name = str(Path(f'trajectory_{i}'))
            traj.save(name, path, file_type, overwrite)

    def save(self, file_name: str, path: str = '.', file_type: str = 'json',
               overwrite: bool = True):
        """
        Saves a trajectory

        Parameters
        ----------
        file_name : str
            Name of the file.
        path : str
            Path where to save the trajectory. (Default is ``'.'``).
        file_time : str
            Type of the file. (Default is ``json``).

            The only types avaliable are: ``json`` and ``csv``.
        overwrite : bool
            Wheter or not to overwrite the file if it already exists. (Default
            is True).

        Raises
        ------        
        ValueError
            If ``override`` parameter is ``False`` and the file already exists.
        ValueError
            If ``file_type`` is not ``json`` or ``csv``.
        """

        # Contruct full path
        full_path = Path(path) / Path(f'{file_name}.{file_type}')

        # Check file existance
        if not overwrite and full_path.exists():
            raise ValueError(f"File '{str(full_path)}' already exist")

        def convert_to_list(array_data):
            if array_data is None:
                return array_data
            if array_data is not list:
                array_data = list(array_data)
            return array_data

        if file_type == 'json':
            json_dict = {
                'dt' : self.dt,
                'id' : self.id,
                'x' : convert_to_list(self.x),
                'y' : convert_to_list(self.y),
                'z' : convert_to_list(self.z),
                't' : convert_to_list(self.t),
                'theta' : convert_to_list(self.theta)
            }
            with open(str(full_path), 'w') as f:
                json.dump(json_dict, f)

        elif file_type == 'csv':
            with open(str(full_path), 'w', newline='') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow([self.id, self.dt])
                for tp in self:
                    writer.writerow([tp.x, tp.y, tp.z, tp.t, tp.theta])
        else:
            raise ValueError(f"Invalid export file type '{file_type}'")

    @staticmethod
    def load_folder(folder_path='.'):
        """
        Loads all the trajectories from a folder.

        Parameters
        ----------
        folder_path : str
            Path of the trajectories folder.

        Returns
        -------
        List[Trajectory]
            List of the loaded trajectories.
        """
        
        trajectories = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                path = str(Path(root) / Path(file))
                try:
                    trajectories.append(Trajectory.load(path))
                except:  # TODO: add errors
                    pass
        return trajectories
    
    @staticmethod
    def load(file_path: str):
        """
        Loads a trajectory

        Parameters
        ----------
        file_path : str
            Path of the trajectory file
        
        Returns
        -------
        Trajecotry
            Trajectory loaded.

        Raises
        ------
        ValueError
            If ``file_path`` is a non existing path.
        ValueError
            If ``file_path`` is a not a file.
        ValueError
            If ``file_path`` extension is not ``json`` or ```csv``.        
        """

        path = Path(file_path)

        # Check valid path
        if not path.exists():
            raise ValueError('Path does not exist.')
        if not path.is_file():
            raise ValueError("Path must be a file.")
    
        # Check valid file type
        file_type = path.suffix
        if not path.suffix in ['.json', '.csv']:
            raise ValueError("Invalid file type.")

        with open(file_path, 'r') as f:
            if file_type == '.json':

                data = json.load(f)
                dt = data['dt']
                traj_id = data['id']
                x = data['x']
                y = data['y']
                z = data['z']
                t = data['t']
                theta = data['theta']
                return Trajectory(x=x, y=y, z=z,
                                  t=t, theta=theta, dt=dt,
                                  id=traj_id)

            elif file_type == '.csv':

                def check_empty_val(val):
                    return None if val == '' else val               

                x, y, z = [], [], []
                t, theta = [], []
                traj_id, dt = None, None

                def add_val(arr, val):
                    if arr is not None:
                        arr.append(val)
                    
                for i, row in enumerate(csv.reader(f)):
                    if i == 0:
                        traj_id = check_empty_val(row[0])
                        dt = check_empty_val(row[1])
                        if dt is not None:
                            dt = float(dt)
                        continue

                    add_val(x, check_empty_val(row[0]))
                    add_val(y, check_empty_val(row[1]))
                    add_val(z, check_empty_val(row[2]))
                    add_val(t, check_empty_val(row[3]))
                    add_val(theta, check_empty_val(row[4]))
                
                x = None if not x else x
                y = None if not y else y
                z = None if not z else z
                t = None if not t else t
                theta = None if not theta else theta

                return Trajectory(x=x, y=y, z=z,
                                  t=t, theta=theta, dt=dt,
                                  id=traj_id)
                                  
    def t_diff(self):
        if self.t is not None:
            return np.ediff1d(self.t)

    def x_diff(self):
        return np.ediff1d(self.x)

    def y_diff(self):
        if self.y is not None:
            return np.ediff1d(self.y)

    def z_diff(self):
        if self.z is not None:
            return np.ediff1d(self.z)

    def theta_diff(self):
        if self.theta is not None:
            return np.ediff1d(self.theta)

    def diff(self):
        dx = self.x_diff()
        dy = self.y_diff()
        if dy is not None:
            dz = self.y_diff()
            if dz is not None:
                return np.sqrt(dx**2 + dy**2 + dz**2)
            else:
                return np.sqrt(dx**2 + dy**2)
        else:
            return dx

    def x_velocity(self):
        return self.x_diff() / self.dt

    def y_velocity(self):
        if self.y is not None:
            return self.y_diff() / self.dt

    def z_velocity(self):
        if self.z is not None:
            return self.z_diff() / self.dt

    def theta_velocity(self):
        if self.theta is not None:
            return self.theta_diff() / self.dt

    def velocity(self):
        return self.diff() / self.dt

if __name__ == '__main__':

    traj_1 = Trajectory(
        x=[1.0, 2.0],
        y=[2.0, 3.0]
    )

    traj_2 = Trajectory(
        x=[10.0, 20.0],
        y=[20.0, 30.0]
    )

    tps = [(tp.x, tp.y) for tp in traj_1]
    assert tps == [(1,2),(2,3)]

    Trajectory.save_trajectories([traj_1, traj_2])

    trajs = Trajectory.load_folder('.')
    
    t1 = trajs[0]

    assert t1.x[0] == 1.0
    assert t1.x[1] == 2.0

    