import numpy as np


def group_array(array, threshold):
    """Provided a given array and threshold, this will return a list of groups within the array."""
    groups = []

    # for simplicity and speed, a boolean reference array is created which will keep track of which positions have
    # already been checked for group membership.
    reference_array = np.zeros(array.shape, dtype=bool)

    # search an array for values above a certain limit
    for row in range(array.shape[0]):
        for column in range(array.shape[1]):
            if array[row, column] >= threshold and not reference_array[row, column]:
                # when one is encountered, and is not apart of a group, create a new group
                new_group = Group(row, column, threshold, array, reference_array)
                new_group.search_and_add()  # build the group from its initial point
                groups.append(new_group)
    return groups


class Group:
    def __init__(self, row, column, threshold, array, reference_array):
        """Builds a group object that searches out and keeps track of its members.

        Parameters
        ------------
        row: (int) row of the initial point of the group, from which the group will begin its search for additional members.
        column: (int) column of the initial point of the group, from which the group will begin its search for additional members.
        threshold: (float) minimum value of a point needed to be included in the group. This is to prevent accidentaly
            including noise as a group member.
        array: (ndarray) The array from which to search for new group members.
        reference_array: (ndarray) A boolean array of the same size as array, which is updated when positions have been
            checked for group membership. This is to make the search faster and easier.
        """

        self._group_members = [(row, column)]
        self._threshold = threshold
        self._array = array
        self._reference_array = reference_array
        self._positions_to_add = []

    def _search(self, starting_position):
        """Searches the surrounding points of a given row/column pair to check whether they are part of the group using
        breadth first search.

        Parameters
        -------------
        row: (int) row position of point in 2D array
        column: (int) column position of point in 2D array
        """

        positions = valid_neighbor_positions(starting_position, self._reference_array)
        positions_to_add = []
        while positions:
            pos = positions.pop()
            if not self._reference_array[pos[0], pos[1]] and self._array[pos[0], pos[1]] >= self._threshold:
                positions_to_add.append(pos)
                self._reference_array[pos[0], pos[1]] = True
                positions.extend(valid_neighbor_positions(pos, self._reference_array))
            else:
                self._reference_array[pos[0], pos[1]] = True
        self._add_positions_to_group(positions_to_add)


    def _add_positions_to_group(self, positions):
        """Appends points identified in the search algorithm to the group members"""
        for pos in positions:
            if pos not in self._group_members:
                self._group_members.append(pos)
        self._positions_to_add = []

    def search_and_add(self):
        """API for building the group from initial point"""
        self._search(self._group_members[0])
        self._add_positions_to_group(self._positions_to_add)

    def group_members(self):
        """Returns list of group member tuples (x, y)"""
        return self._group_members

    def walking_median(self):
        """Returns a list of the median for each unique y value."""
        group_members = np.array(self._group_members)
        indicies = np.argsort(group_members[:, 0])
        group_members = group_members[indicies]
        walking_median = []
        for t in np.unique(group_members[:, 1]):
            med = np.median(group_members[group_members[:, 1] == t, 0])
            walking_median.append((t, med))
        return walking_median


def valid_neighbor_positions(pos, reference_array):
    search_rows = [0]
    search_columns = [0]
    if 0 < pos[0] < reference_array.shape[0] - 1:
        search_rows.extend([-1, 1])
    else:
        placement = True if pos[0] > 0 else False
        search_rows.append(1 - 2 * placement)
    if 0 < pos[1] < reference_array.shape[1] - 1:
        search_columns.extend([-1, 1])
    else:
        placement = True if pos[1] > 0 else False
        search_columns.append(1 - 2 * placement)
    return [comb for comb in combinations(pos[0], pos[1], search_rows, search_columns)
            if not reference_array[comb[0], comb[1]]]


def combinations(x, y, list1, list2):
    """Given an x and y central coordinate, returns all adjoining positions that are possible, given by list1 and list2.
    List1 is associated with the x position and list2 is associated with the y position. If the central coordinate is
    not at the edge, the return will be a the positions around the central coordinate that form a cross pattern."""
    combinations = []
    for row in list1:
        combinations.append((x + row, y))
    for col in list2:
        combinations.append((x , y + col))
    return combinations


def moving_average(x, n):
    """Returns the moving average of an array, x, with the frame dictated by n. In context, this is used to smooth the
    walking median of a group."""
    try:
        t = np.zeros((x.shape[0] - (n - 1), x.shape[1]))
        cumsum = np.cumsum(np.insert(x[:, 1], 0, 0))
        t[:, 0] = x[n - 1:, 0]
        t[:, 1] = (cumsum[n:] - cumsum[:-n]) / float(n)
        return t
    except ValueError:
        return x


def group_statistics(x):
    """Returns a dictionary of basic statistics of an array x. In context, this is used with the moving average of a
    group."""
    stat_dict = {}
    stat_dict['time min'] = np.min(x[:, 0])
    stat_dict['time max'] = np.max(x[:, 0])
    stat_dict['time mid'] = np.median(x[:, 0])
    stat_dict['time diff'] = stat_dict['time max'] - stat_dict['time min']
    stat_dict['frequency min'] = np.min(x[:, 1])
    stat_dict['frequency max'] = np.max(x[:, 1])
    stat_dict['frequency mid'] = np.median(x[:, 1])
    stat_dict['frequency diff'] = np.median(x[:int(x.shape[0] / 2), 1]) - np.median(x[int(x.shape[0] / 2):, 1])
    return stat_dict


if __name__ == '__main__':
    # a simple test
    test_array = np.array([[1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                           [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                           [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                           [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                           [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                           [1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                           [1, 1, 1, 0, 0, 0, 1, 0, 0, 1]])

    print(test_array, '\n')
    groups = group_array(test_array, threshold=1, max_count=1000)
    x = np.arange(len(groups))
    group_dict = {group: num + 1 for group, num in zip(groups, x)}

    y = np.zeros(test_array.shape)
    for key, value in group_dict.items():
        group_pos = key.group_members()
        for pos in group_pos:
            y[pos[0], pos[1]] = value

    print(y)