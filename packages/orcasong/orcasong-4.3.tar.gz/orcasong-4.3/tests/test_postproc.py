from unittest import TestCase
import os
import h5py
import numpy as np
import orcasong.tools.postproc as postproc
import orcasong.tools.shuffle2 as shuffle2

__author__ = 'Stefan Reck'

test_dir = os.path.dirname(os.path.realpath(__file__))
MUPAGE_FILE = os.path.join(test_dir, "data", "mupage.root.h5")


class TestPostproc(TestCase):
    def setUp(self):
        self.output_file = "temp_output.h5"

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_shuffle(self):
        postproc.postproc_file(
            input_file=MUPAGE_FILE,
            output_file=self.output_file,
            shuffle=True,
            event_skipper=None,
            delete=False,
            seed=13,
        )

        with h5py.File(self.output_file, "r") as f:
            np.testing.assert_equal(f["event_info"]["event_id"], np.array([1, 0, 2]))
            self.assertTrue("origin" in f.attrs.keys())


class TestShuffleV2(TestCase):
    def setUp(self):
        self.temp_input = "temp_input.h5"
        self.temp_output = "temp_output.h5"

        self.x, self.y = _make_shuffle_dummy_file(self.temp_input)
        np.random.seed(42)
        shuffle2.h5shuffle2(
            input_file=self.temp_input,
            output_file=self.temp_output,
            datasets=("x", "y"),
            max_ram=400,  # -> 2 batches
        )

    def tearDown(self):
        for f in (self.temp_input, self.temp_output):
            if os.path.exists(f):
                os.remove(f)

    def test_shuffled_has_same_entries_as_input(self):
        with h5py.File(self.temp_output, "r") as f:
            x_s = f["x"][()]
            np.testing.assert_array_equal(
                self.x[:, 1:], x_s[:, 1:][np.argsort(x_s[:, 0])]
            )

    def test_all_shuffled_datasets_have_same_order(self):
        with h5py.File(self.temp_output, "r") as f:
            np.testing.assert_array_equal(
                f["x"][:, 0], f["y"][:, 0]
            )

    def test_seed_produces_this_shuffled_order(self):
        target_order = np.array(
            [12.,  5.,  0., 20.,  6.,  2., 19., 13.,  1.,  9.,  8.,  4.,  3.,
             11., 16., 15.,  7., 10., 17., 14., 21., 18.])
        with h5py.File(self.temp_output, "r") as f:
            np.testing.assert_array_equal(
                f["x"][:, 0], target_order
            )

    def test_run_3_iterations(self):
        # just check if it goes through without errors
        fname = "temp_output_triple.h5"
        try:
            shuffle2.h5shuffle2(
                input_file=self.temp_input,
                output_file=fname,
                datasets=("x", "y"),
                iterations=3,
            )
        finally:
            if os.path.exists(fname):
                os.remove(fname)


def _make_shuffle_dummy_file(filepath):
    x = np.random.rand(22, 2)
    x[:, 0] = np.arange(22)
    y = np.random.rand(22, 3)
    y[:, 0] = np.arange(22)
    with h5py.File(filepath, "w") as f:
        f.create_dataset("x", data=x, chunks=(5, 2))
        f.create_dataset("y", data=y, chunks=(5, 3))
    return x, y
