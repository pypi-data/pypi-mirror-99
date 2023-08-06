import pydicom as dcm
import numpy as np
from rw_cdb import read_cdbfile, write_cdb_mat
import time
from multiprocessing import Process, Manager, cpu_count
import os
from copy import deepcopy
from scipy.interpolate import NearestNDInterpolator
import quadpy as qp
import warnings
from ansys.mapdl.reader import Archive


class qctma(object):
    """
    Class used to load Dicom files and mesh file, and create a new mesh implementing materials based on gray level to
    density relationship and density to Young's modulus relationship.
    """

    def __init__(self, dcm_path="", mesh_path="", gl2density=lambda x: x, density2E=lambda x: x, deltaE=0, process=True, save_mesh_path=""):
        self.dcm_path = dcm_path  # Path to the directory containing the Dicom files
        self.mesh_path = mesh_path  # Path to the mesh file
        self.gl2density = gl2density  # Function transforming gray level 3D array to density 3D array
        self.density2E = density2E  # Function transforming density 3D array to Young's modulus 3D array
        self.deltaE = deltaE  # Step between each material. If 0 : each element will have a specific material.

        # MESH RELATED PARAMETERS
        self.elems = []  # 1D array of the elements ID
        self.connection_array = []  # 2D array of the connection table (i.e. for elems[i] -> connection_array[i] = [node1, ..., nodeN]
        self.matid = []  # 1D array of the materials id (materials[i] corresponds to elems_array[i])
        self.nodes = []  # 1D array of nodes id
        self.x = []  # 1D array of nodes x-coord (x[i] corresponds to nodes[i])
        self.y = []  # 1D array of nodes y-coord (y[i] corresponds to nodes[i])
        self.z = []  # 1D array of nodes z-coord (z[i] corresponds to nodes[i])
        self.e_pool = []  # 1D array of Young's modulus (e_pool[i] corresponds to materials[i])
        self.density_pool = []  # 1D array of density (density_pool[i] corresponds to materials[i])

        # DICOM RELATED PARAMETERS
        self.image_mat = []  # 3D array of voxel values in Dicoms
        self.position_x = []  # 3D array of x-coord of each voxel
        self.position_y = []  # 3D array of y-coord of each voxel
        self.position_z = []  # 3D array of z-coord of each voxel

        # MATERIAL RELATED
        self.e_mat = []  # 3D array of Young's modulus values corresponding to each voxel
        self.interpolator = None  # Interpolator Young's modulus = f(x, y, z)
        self.e_elems = []  # 1D array of Young's modulus of each element

        self.nb_process = cpu_count() - 1  # Number of core for the parallelized process

        # PROCESSING THE DATA
        if process:
            self.process(save_mesh_path=save_mesh_path)

    def process(self, save_mesh_path=""):
        """
        Process the data from the loading of the original mesh and Dicoms to the saving of the final mesh.
        :param save_mesh_path: Path to the final mesh.
        """
        self.load_mesh()
        self.load_dicom()
        self.convert2E()
        self.create_interpolator()
        self.create_materials()
        if self.deltaE:
            self.reduce_material_nb()
        else:
            self.e_pool = self.e_elems
            self.matid = range(1, len(self.e_elems) + 1)
        self.e_pool2density()
        self.save_mesh(save_mesh_path)


    def load_mesh(self):
        """
        Load the data in the mesh_path and extract the mesh related parameters.
        """
        if not self.mesh_path:
            warnings.warn("WARNING: Mesh path is empty!")
            return
        if self.mesh_path.lower().endswith(".cdb"):
            # Ansys mesh case
            archive = Archive(self.mesh_path)
            archive_elems = np.array(archive.elem)
            self.elems = archive_elems[:, 8]
            self.connection_array = archive_elems[:, 10:]
            self.materials = np.array(archive.material_type)
            self.nodes = np.array(range(1, len(archive.nodes)+1))
            self.x, self.y, self.z = np.array(archive.nodes).T

    def load_dicom(self):
        """
        Load the data in the Dicoms and extract the Dicom related parameters.
        """
        print("Reading dicom files...")
        ds = []  # List of dicoms
        for i, file in enumerate(os.listdir(self.dcm_path)):
            if i % 100 == 0:
                print(file)
            ds.append(dcm.dcmread(os.path.join(self.dcm_path, file)))
            if i % 100 == 0:
                print("...")

        print("Dicom reading done.\n")

        # MAKING 3D MATRIX OF DICOMS AND 3D MATRIX OF POSITION OF VOXEL
        print("Converting Dicoms into volume")
        self.image_mat = np.zeros((len(ds), len(ds[0].pixel_array), len(ds[0].pixel_array[0])))  # Pixel values

        # Extracting constant values along each slice of the dicom
        spacing_x, spacing_y = float(ds[0].PixelSpacing[0]), float(ds[0].PixelSpacing[1])
        orientation_x, orientation_y = float(ds[0].ImageOrientationPatient[0]), float(ds[0].ImageOrientationPatient[4])
        orig_x, orig_y, orig_z = float(ds[0].ImagePositionPatient[0]), float(ds[0].ImagePositionPatient[1]), float(
            ds[0].ImagePositionPatient[2])

        self.positions_x = orig_x + orientation_x * spacing_x * np.array(range(len(ds[0].pixel_array[0])))
        self.positions_y = orig_y + orientation_y * spacing_y * np.array(range(len(ds[0].pixel_array)))
        self.positions_z = np.zeros((len(ds)))

        # Extracting the image in each slice and the corresponding Z coordinate (which might not be linear).
        for i, d in enumerate(ds):
            if i % 100 == 0:
                print("...")
            self.image_mat[i] = d.pixel_array * d.RescaleSlope + d.RescaleIntercept
            self.positions_z[i] = float(ds[i].ImagePositionPatient[2])

        print("Volume created.\n")

    def convert2E(self):
        """
        Convert the gray level matrix to Young's modulus matrix.
        """
        print("E matrix creation...")
        density_mat = self.gl2density(self.image_mat)
        self.e_mat = self.density2E(density_mat)
        print("E matrix created.")

    def create_interpolator(self):
        """
        Create interpolator function Young's modulus = f(x, y, z)
        """
        # Truncation of the image matrix for interpolation
        coord_mesh_min = (np.min(self.x), np.min(self.y), np.min(self.z))
        coord_mesh_max = (np.max(self.x), np.max(self.y), np.max(self.z))
        idx_img_mat_min = self.pixel_location_from_coord(*coord_mesh_min,
                                                    self.positions_x, self.positions_y, self.positions_z)
        idx_img_mat_max = self.pixel_location_from_coord(*coord_mesh_max,
                                                    self.positions_x, self.positions_y, self.positions_z)
        idx_x = np.sort([idx_img_mat_min[0], idx_img_mat_max[0]])
        idx_y = np.sort([idx_img_mat_min[1], idx_img_mat_max[1]])
        idx_z = np.sort([idx_img_mat_min[2], idx_img_mat_max[2]])

        # Creating a list of coordinate [(x1, y1, z1), ..., (xi, yi, zi)]
        z_m, y_m, x_m = np.meshgrid(self.positions_z[idx_x[0]:idx_x[1]],
                                    self.positions_y[idx_y[0]:idx_y[1]],
                                    self.positions_x[idx_z[0]:idx_z[1]],
                                    indexing="ij")  # First creating a meshgrid.

        x_m = np.concatenate(np.concatenate(
            x_m))  # Concatenating each coordinate in order to have [slice1_coordinate then slice2_cordinate, etc.]
        y_m = np.concatenate(np.concatenate(y_m))
        z_m = np.concatenate(np.concatenate(z_m))
        coords = list(
            zip(x_m, y_m, z_m))  # Zipping th x, y ad z coordinates to get a list [(x1, y1, z1), ..., (xi, yi, zi)].

        # Getting the values corresponding to the created coordinates.
        val = np.concatenate(np.concatenate(self.e_mat[idx_x[0]:idx_x[1],
                                            idx_y[0]:idx_y[1],
                                            idx_z[0]:idx_z[1]]))

        # Creating the interpolation function based on the coordinates and the associated values.
        # Could be a custom function as long as it maps every points of the space to a Young's modulus value.
        self.interpolator = NearestNDInterpolator(coords, val)

    def pixel_location_from_coord(self, x, y, z, positions_x, positions_y, positions_z):
        """
        Returns the pixel location as (slice number, row number in slice, column number in slice).
        :param x: x-coord of the pixel
        :param y: y-coord of the pixel
        :param z: z-coord of the pixel
        :param positions_x: array that associates x coordinate to the position in the rows of a 3D matrix.
        :param positions_y: array that associates y coordinate to the position in the columns of a 3D matrix.
        :param positions_z: array that associates z coordinate to the position in the slices of a 3D matrix.
        :return: (slice_nb, row_nb, col_nb), equivalent position in the 3D matrix.
        """
        col_nb = np.abs(np.array(positions_x) - x).argmin()
        row_nb = np.abs(np.array(positions_y) - y).argmin()
        slice_nb = np.abs(np.array(positions_z) - z).argmin()

        return np.array((slice_nb, row_nb, col_nb))

    def create_materials(self):
        """
        Associate the Young's modulus to each element by integrating the E matrix over each element.
        Parallelized process! Needs to be launched within a __main__ process.
        """
        save_list = Manager().list([[]] * self.nb_process)
        p = [Process(target=self.material_integration, args=(self.connection_array, self.x, self.y, self.z, self.interpolator, save_list, self.nb_process, id)) for id in range(self.nb_process)]
        for i in range(self.nb_process):
            p[i].start()
        for i in range(self.nb_process):
            p[i].join()

        self.e_elems = np.concatenate(save_list)  # Integrals of interp over each elem (i.e. Young's modulus of each elem)

    def material_integration(self, connection_array, x, y, z, interp, save_list, nb_process, id):
        """
        Computes the integration of the Young's modulus over each element based on the mapping of the Young's
        modulus over each point (x, y, z) by the function interp.
        This function is made to be used in parallel processing.
        :param connection_array: Connection table [[node1, ..., nodeN], ...] for each elem. The assumption is made that
        the four first nodes are the vertices of the tetrahedron; or the first 8 nodes are the vertices of the cube.
        :param x: X coordinate of each node.
        :param y: Y coordinate of each node.
        :param z: Z coordinate of each node.
        :param interp: Function that maps the Young's modulus to every point of the 3D space.
        :param save_list: Persistent list where the integration of each element will be stored.
        :param id: ID of the process.
        """

        t0 = time.time()

        # Sharing equivalent part of the elems list between each process.
        start_elem_arg = len(connection_array) // nb_process * id
        finish_elem_arg = len(connection_array) // nb_process * (id + 1)
        if id == nb_process - 1:
            finish_elem_arg = len(connection_array)

        def f(args):
            # Returns the coordinates in the correct shape for 1: use it with the interp function and 2: use it with the
            # integrate function.
            # i.e. interp function uses the shape [tet1, ..., teti] with teti = [v1i, v2i, v3i, v4i]
            # integrate function uses the shape [integ_points1, ..., integ_pointsi] with integ_pointsi being the list of
            # integration points for tetrahedron i.
            x = np.transpose(args)
            return np.transpose(interp(x))

        is_cube = len(connection_array[0]) == 8 or len(connection_array[0]) == 20
        if is_cube:
            # WARNING: SOMETHING WRONG WITH CUBIC INTEGRATION (INTEGRAL VALUE IS DOUBLED...)
            def f(*args):
                # Returns the coordinates in the correct shape for 1: use it with the interp function and 2: use it with the
                # integrate function.
                # i.e. interp function uses the shape [tet1, ..., teti] with teti = [v1i, v2i, v3i, v4i]
                # integrate function uses the shape [integ_points1, ..., integ_pointsi] with integ_pointsi being the list of
                # integration points for tetrahedron i.
                return [interp(args[0][0][i], args[0][1][i], args[0][2][i]) for i in range(len(args[0][0]))]

            scheme = qp.c3._witherden_vincent.witherden_vincent_11()  # Integration scheme
        else:
            scheme = qp.t3._witherden_vincent.witherden_vincent_10()  # Integration scheme

        v1 = []  # List of the first vertex of each tetrahedron
        v2 = []  # List of the second vertex of each tetrahedron
        v3 = []  # List of the third vertex of each tetrahedron
        v4 = []  # List of the fourth vertex of each tetrahedron
        if is_cube:
            v_cube = []
        if is_cube:
            v5 = []  # List of the fifth vertex of each cuboid
            v6 = []  # List of the fifth vertex of each cuboid
            v7 = []  # List of the fifth vertex of each cuboid
            v8 = []  # List of the fifth vertex of each cuboid

        for elem_arg in range(start_elem_arg, finish_elem_arg):
            nodes_tetrahedron = connection_array[elem_arg]  # list of nodes of each tetrahedron
            nodes_tetrahedron -= 1  # Minus 1 to be able to use the number of the node as index.

            # Appending each vertex coordinate for each tetrahedron.
            v1.append(np.array((x[nodes_tetrahedron[0]], y[nodes_tetrahedron[0]], z[nodes_tetrahedron[0]])))
            v2.append(np.array((x[nodes_tetrahedron[1]], y[nodes_tetrahedron[1]], z[nodes_tetrahedron[1]])))
            v3.append(np.array((x[nodes_tetrahedron[2]], y[nodes_tetrahedron[2]], z[nodes_tetrahedron[2]])))
            v4.append(np.array((x[nodes_tetrahedron[3]], y[nodes_tetrahedron[3]], z[nodes_tetrahedron[3]])))
            if is_cube:
                v5.append(np.array((x[nodes_tetrahedron[4]], y[nodes_tetrahedron[4]], z[nodes_tetrahedron[4]])))
                v6.append(np.array((x[nodes_tetrahedron[5]], y[nodes_tetrahedron[5]], z[nodes_tetrahedron[5]])))
                v7.append(np.array((x[nodes_tetrahedron[6]], y[nodes_tetrahedron[6]], z[nodes_tetrahedron[6]])))
                v8.append(np.array((x[nodes_tetrahedron[7]], y[nodes_tetrahedron[7]], z[nodes_tetrahedron[7]])))
                cube_point = qp.c3.cube_points([np.min((v1[-1][0], v5[-1][0])), np.max((v1[-1][0], v5[-1][0]))],
                                               [np.min((v1[-1][1], v2[-1][1])), np.max((v1[-1][1], v2[-1][1]))],
                                               [np.min((v1[-1][2], v3[-1][2])), np.max((v1[-1][2], v3[-1][2]))])
                v_cube.append(deepcopy(cube_point))

            if not elem_arg % 100:
                print("id %i:" % id, elem_arg, time.time() - t0)
        # Integrating the Young's modulus over each element and dividing it by the volume of each element to get the mean.
        # Note: the function used to get the volume is x / x and not 1 in order to have the right shape in the end.
        if is_cube:
            elems_mat = scheme.integrate(f, np.stack(v_cube, axis=-2)) / scheme.integrate(lambda x: x[0] / x[0],
                                                                                          np.stack(v_cube, axis=-2))
        else:
            elems_mat = scheme.integrate(f, (v1, v2, v3, v4)) / scheme.integrate(lambda x: x[0] / x[0],
                                                                                 (v1, v2, v3, v4))

        save_list[id] = elems_mat  # Saving the results in the save_list param

    def reduce_material_nb(self):
        """
        Reduce the number of material by grouping material within a step defined by self.deltaE
        """
        mat_max = np.max(self.e_elems)
        self.e_pool = []
        self.matid = np.zeros(len(self.e_elems))
        while mat_max >= np.min(self.e_elems) and mat_max != -self.deltaE - 1:
            max_elem_group_mask = self.e_elems >= mat_max - self.deltaE  # Elements within mat_max and mat_max-deltaE
            self.e_pool.append(np.mean(self.e_elems[max_elem_group_mask]))  # np.mean() or mat_max ?
            self.matid[max_elem_group_mask] = len(self.e_pool)
            self.e_elems[max_elem_group_mask] = -self.deltaE - 1
            mat_max = np.max(self.e_elems)

    def inv_num(self, f, ys, init_guess=[0, 2], max_err=0.001):
        """
        Find the value corresponding to the inverse of the function f at y.
        :param f: Function to be inversed.
        :param ys: Values at which the inverse function will be computed.
        :param first_guess: First guess boundaries between which the inverse function will be investigated.
        :param max_err: Maximum desired error on the inverse function at y.
        :return inv_values: The result of the inverse function of f at y.
        """
        inv_values = []
        nb_sample = int((init_guess[1] - init_guess[0]) / (2 * max_err))
        if nb_sample > 1000:
            nb_sample = 1000
        for y in ys:
            step = 0
            first_guess = np.array(init_guess)
            while step < 100:
                step += 1
                delta = (first_guess[1] - first_guess[0]) / nb_sample
                x = np.linspace(*first_guess, nb_sample)
                f_x = f(x)
                diff = np.abs(f_x - y)
                argmin = np.argmin(diff)
                if delta <= max_err:
                    break
                if argmin == len(x) - 1:
                    first_guess[0] = 0
                    if first_guess[1] == 0:
                        first_guess[1] = 1
                    first_guess[1] *= 2
                elif argmin == 0:
                    first_guess[1] = 0
                    if first_guess[0] == 0:
                        first_guess[0] = -1
                    first_guess[0] *= 2
                else:
                    first_guess = [x[argmin] - delta, x[argmin] + delta]
            inv_values.append(x[argmin])

        return inv_values

    def e_pool2density(self):
        self.density_pool = self.inv_num(self.density2E, self.e_pool)

    def save_mesh(self, save_mesh_path):
        if save_mesh_path.lower().endswith(".cdb"):
            write_cdb_mat(self.mesh_path, save_mesh_path, self.matid, self.e_pool, self.density_pool)
        else:
            warnings.warn("WARNING: Extension of the desired save path of the mesh not recognized.")

