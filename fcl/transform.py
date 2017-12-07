import numpy as np

def rotation_to_quaternion(rot):
    next_idx = (1, 2, 0)
    data = np.zeros(4)
    trace = np.trace(rot)
    if trace > 0.0:
        root = np.sqrt(trace + 1.0)
        data[0] = 0.5 * root
        root = 0.5 / root
        data[1] = (rot[2, 1] - rot[1, 2]) * root
        data[2] = (rot[0, 2] - rot[2, 0]) * root
        data[3] = (rot[1, 0] - rot[0, 1]) * root
    else:
        i = 0
        if rot[1, 1] > rot[0, 0]:
            i = 1
        if rot[2, 2] > rot[i, i]:
            i = 2
        j = next_idx[i]
        k = next_idx[j]

        root = np.sqrt(rot[i, i] - rot[j, j] - rot[k, k] + 1.0)
        data[i + 1] = 0.5 * root
        root = 0.5 / root
        data[0] = (rot[k, j] - rot[j, k]) * root
        data[j + 1] = (rot[j, i] + rot[i, j]) * root
        data[k + 1] = (rot[k, i] + rot[i, k]) * root
    return Quaternion(data)

def quaternion_to_rotation(quat):
    data = quat._data
    twoX  = 2.0 * data[1]
    twoY  = 2.0 * data[2]
    twoZ  = 2.0 * data[3]
    twoWX = twoX * data[0]
    twoWY = twoY * data[0]
    twoWZ = twoZ * data[0]
    twoXX = twoX * data[1]
    twoXY = twoY * data[1]
    twoXZ = twoZ * data[1]
    twoYY = twoY * data[2]
    twoYZ = twoZ * data[2]
    twoZZ = twoZ * data[3]

    return np.array([[1.0 - (twoYY + twoZZ), twoXY - twoWZ, twoXZ + twoWY],
                        [twoXY + twoWZ, 1.0 - (twoXX + twoZZ), twoYZ - twoWX],
                        [twoXZ - twoWY, twoYZ + twoWX, 1.0 - (twoXX + twoYY)]])

def axisangle_to_quaternion(axis, angle):
    half_angle = 0.5 * angle
    sn = np.sin(half_angle)
    data = np.zeros(4)
    data[0] = np.cos(half_angle)
    data[1:] = sn * axis
    return Quaternion(data)

def quaternion_to_axisangle(quat):
    data = quat._data
    sqr_length = sum(np.square(data[1:]))
    axis = np.zeros(3)
    if sqr_length > 0:
        angle = 2.0 * np.arccos(data[0])
        inv_length = 1.0 / np.sqrt(sqr_length)
        axis = inv_length * data[1:]
    else:
        angle = 0
        axis[0] = 1
        axis[1] = 0
        axis[2] = 0
    return axis, angle

class Quaternion(object):
    def __init__(self, *args):
        if len(args) == 0:
            self._data = np.zeros(4)
            self._data[0] = 1.0
        elif len(args) == 4:
            self._data = np.array(args)
        elif len(args) == 1 and len(args[0]) == 4:
            self._data = np.array(args[0])

    @property
    def w(self):
        return self._data[0]
    @w.setter
    def w(self, value):
        self._data[0] = value

    @property
    def x(self):
        return self._data[1]
    @x.setter
    def x(self, value):
        self._data[1] = value

    @property
    def y(self):
        return self._data[2]
    @y.setter
    def y(self, value):
        self._data[2] = value

    @property
    def z(self):
        return self._data[3]
    @z.setter
    def z(self, value):
        self._data[3] = value

    @property
    def v(self):
        return self._data[1:]
    @v.setter
    def v(self, value):
        self._data[1:] = value

    def __getitem__(self, idx):
        return self._data[idx]
    def __setitem__(self, idx, value):
        self._data[idx] = value

    def isIdentity(self):
        return self._data[0] == 1 and \
               all((d == 0 for d in self._data[1:]))
    def __add__(self, other):
        return Quaternion(self._data + other._data)
    def __sub__(self, other):
        return Quaternion(self._data - other._data)
    def __neg__(self):
        return Quaternion(-self._data)
    def __mul__(self, other):
        v = self.w * other.v + other.w * self.v + np.cross(self.v, other.v)
        return Quaternion(self.w * other.w - np.dot(self.v, other.v),
                          v[0], v[1], v[2])
    def dot(self, other):
        return Quaternion(np.dot(self._data, other._data))

    def conj(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def __str__(self):
        return str(self._data)

    def inverse(self):
        data = np.zeros(4)
        sqr_length = sum(np.square(data))
        if sqr_length > 0:
            inv_length = 1 / np.sqrt(sqr_length);
            data[0] *= inv_length
            data[1:] *= (-inv_length)
        else:
            data[1:] *= (-1)
        return Quaternion(data)

    def transform(self, vec):
        r = self * Quaternion(0.0, vec[0], vec[1], vec[2]) * self.conj()
        return r.v


class Transform(object):
    def __init__(self, rot=None, pos=None):
        if not pos is None:
            self.t = np.array(pos)
        else:
            self.t = np.zeros(3)

        if rot is None:
            self.q = Quaternion()
        elif isinstance(rot, Quaternion):
            self.q = rot
        else:
            self.q = rotation_to_quaternion(rot)
