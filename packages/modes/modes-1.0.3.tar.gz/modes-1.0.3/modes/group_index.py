from typing import List

import numpy as np
import pytest
from numpy import float64

from modes.mode_solver_full import mode_solver_full


def group_index(
    wavelength: float = 1.55,
    wavelength_step: float = 0.01,
    overwrite: bool = False,
    n_modes: int = 1,
    **wg_kwargs,
) -> List[float64]:
    r"""
    Solve for the group index, :math:`n_g`, of a structure at a particular
    wavelength.

    Args:
        structure (Structure): The target structure to solve
            for modes.
        wavelength_step (float): The step to take below and
            above the nominal wavelength.  This is used for
            approximating the gradient of :math:`n_\mathrm{eff}`
            at the nominal wavelength.  Default is 0.01.
        n_modes: number of modes
        x_step: 0.02
        y_step: 0.02
        thickness: 0.22
        width: 0.5
        slab_thickness: 0
        sub_thickness: 0.5
        sub_width: 2.0
        clad_thickness: [0.5]
        n_sub: sio2
        n_wg: si
        n_clads: [sio2]
        wavelength: 1.55
        angle: 90.0

    Returns:
        List of the group indices found for each mode.
    """
    n_gs = []

    msc = mode_solver_full(
        wavelength=wavelength, overwrite=overwrite, n_modes=n_modes, **wg_kwargs
    )
    msf = mode_solver_full(
        wavelength=wavelength + wavelength_step,
        overwrite=overwrite,
        n_modes=n_modes,
        **wg_kwargs,
    )
    msb = mode_solver_full(
        wavelength=wavelength - wavelength_step,
        overwrite=overwrite,
        n_modes=n_modes,
        **wg_kwargs,
    )

    n_ctrs = np.real(msc.n_effs)
    n_bcks = np.real(msb.n_effs)
    n_frws = np.real(msf.n_effs)

    filename = (
        msc._modes_directory / f"_ng_{msc.name}_{wavelength}_{wavelength_step}.dat"
    )

    n_gs = []
    for n_ctr, n_bck, n_frw in zip(n_ctrs, n_bcks, n_frws):
        n_gs.append(n_ctr - wavelength * (n_frw - n_bck) / (2 * wavelength_step))

    with open(filename, "w") as fs:
        fs.write("# Mode idx, Group index\n")
        for idx, n_g in enumerate(n_gs):
            fs.write("%i,%.3f\n" % (idx, np.round(n_g.real, 3)))

    return n_gs


@pytest.mark.parametrize("overwrite", [True, False])
def test_sweep(overwrite: bool) -> None:
    ng = group_index(n_modes=2)
    print(ng)
    assert np.isclose(
        ng, np.array([4.123932892727449, 3.9318152179618666]), atol=0.1
    ).all()


if __name__ == "__main__":
    # import matplotlib.pylab as plt
    print(group_index(g=2))
    # test_sweep(overwrite=False)
    # plt.show()
