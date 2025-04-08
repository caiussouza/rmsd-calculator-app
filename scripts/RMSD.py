import math


class RMSD():
    """
    Class for calculating the Root Mean Square Deviation (RMSD) between
    two molecular structures.

    Methods:
        calculate(target, model):
            Compute RMSD between target and model DataFrames.
            Raises ValueError if molecules differ in atom count or order.
    """

    @staticmethod
    def calculate(target, model):
        """
        Calculate the RMSD (Root Mean Square Deviation) between
        two molecular structures.
        Args:
            target (DataFrame): Target molecule dataframe.
            model (DataFrame): Model molecule dataframe.
        Returns:
            float: RMSD value.
        Raises:
            ValueError: If molecules differ in atom count or order.
        """

        same_len = len(target) == len(model)
        same_order = target["atom_name"].str[0].equals(
            model["atom_name"].str[0])
        if not same_len:
            raise ValueError("The molecules have different number of atoms")
        if not same_order:
            raise ValueError("The molecules have different order of atoms")

        target_coords = target[["x", "y", "z"]].values
        model_coords = model[["x", "y", "z"]].values

        N = len(target_coords)
        dist_sum = sum(
            (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
            for (x1, y1, z1), (x2, y2, z2) in zip(target_coords, model_coords)
        )
        return math.sqrt(dist_sum / N)
