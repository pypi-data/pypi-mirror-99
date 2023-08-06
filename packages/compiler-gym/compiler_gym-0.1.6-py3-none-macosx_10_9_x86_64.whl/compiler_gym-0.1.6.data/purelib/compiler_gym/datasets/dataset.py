# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import io
import json
import os
import shutil
import tarfile
import warnings
from pathlib import Path
from typing import List, NamedTuple, Optional, Union

import fasteners
from deprecated.sphinx import deprecated

from compiler_gym.util.download import download


class LegacyDataset(NamedTuple):
    """A collection of benchmarks for use by an environment.

    .. deprecated:: 0.1.4
       The next release of CompilerGym will introduce a new API for describing
       datasets with extended functionality. See
       `here <https://github.com/facebookresearch/CompilerGym/issues/45>`_ for
       more information.
    """

    name: str
    """The name of the dataset."""

    license: str
    """The license of the dataset."""

    file_count: int
    """The number of files in the unpacked dataset."""

    size_bytes: int
    """The size of the unpacked dataset in bytes."""

    url: str = ""
    """A URL where the dataset can be downloaded from. May be an empty string."""

    sha256: str = ""
    """The sha256 checksum of the dataset archive. If provided, this is used to
    verify the contents of the dataset upon download.
    """

    compiler: str = ""
    """The name of the compiler that this dataset supports."""

    description: str = ""
    """An optional human-readable description of the dataset."""

    platforms: List[str] = ["macos", "linux"]
    """A list of platforms supported by this dataset. Allowed platforms 'macos' and 'linux'."""

    deprecated_since: str = ""
    """The CompilerGym release in which this dataset was deprecated."""

    @property
    def deprecated(self) -> bool:
        """Whether the dataset is deprecated."""
        return bool(self.deprecated_since)

    @classmethod
    def from_json_file(cls, path: Path) -> "LegacyDataset":
        """Construct a dataset form a JSON metadata file.

        :param path: Path of the JSON metadata.
        :return: A LegacyDataset instance.
        """
        try:
            with open(str(path), "rb") as f:
                data = json.load(f)
        except json.decoder.JSONDecodeError as e:
            raise OSError(
                f"Failed to read dataset metadata file:\n"
                f"Path: {path}\n"
                f"Error: {e}"
            )
        return cls(**data)

    def to_json_file(self, path: Path) -> Path:
        """Write the dataset metadata to a JSON file.

        :param path: Path of the file to write.
        :return: The path of the written file.
        """
        with open(str(path), "wb") as f:
            json.dump(self._asdict(), f)
        return path


@deprecated(
    version="0.1.4",
    reason=(
        "Activating datasets will be removed in v0.1.5. "
        "`More information <https://github.com/facebookresearch/CompilerGym/issues/45>`_."
    ),
)
def activate(env, name: str) -> bool:
    """Move a directory from the inactive to active benchmark directory.

    :param: The name of a dataset.
    :return: :code:`True` if the dataset was activated, else :code:`False` if
        already active.
    :raises ValueError: If there is no dataset with that name.
    """
    with fasteners.InterProcessLock(env.datasets_site_path / "LOCK"):
        if (env.datasets_site_path / name).exists():
            # There is already an active benchmark set with this name.
            return False
        if not (env.inactive_datasets_site_path / name).exists():
            raise ValueError(f"Inactive dataset not found: {name}")
        os.rename(env.inactive_datasets_site_path / name, env.datasets_site_path / name)
        os.rename(
            env.inactive_datasets_site_path / f"{name}.json",
            env.datasets_site_path / f"{name}.json",
        )
        return True


@deprecated(
    version="0.1.4",
    reason=(
        "Deleting datasets will be removed in v0.1.5. "
        "`More information <https://github.com/facebookresearch/CompilerGym/issues/45>`_."
    ),
)
def delete(env, name: str) -> bool:
    """Delete a directory in the inactive benchmark directory.

    :param: The name of a dataset.
    :return: :code:`True` if the dataset was deleted, else :code:`False` if
        already deleted.
    """
    with fasteners.InterProcessLock(env.datasets_site_path / "LOCK"):
        deleted = False
        if (env.datasets_site_path / name).exists():
            shutil.rmtree(str(env.datasets_site_path / name))
            os.unlink(str(env.datasets_site_path / f"{name}.json"))
            deleted = True
        if (env.inactive_datasets_site_path / name).exists():
            shutil.rmtree(str(env.inactive_datasets_site_path / name))
            os.unlink(str(env.inactive_datasets_site_path / f"{name}.json"))
            deleted = True
        return deleted


@deprecated(
    version="0.1.4",
    reason=(
        "Deactivating datasets will be removed in v0.1.5. "
        "`More information <https://github.com/facebookresearch/CompilerGym/issues/45>`_."
    ),
)
def deactivate(env, name: str) -> bool:
    """Move a directory from active to the inactive benchmark directory.

    :param: The name of a dataset.
    :return: :code:`True` if the dataset was deactivated, else :code:`False` if
        already inactive.
    """
    with fasteners.InterProcessLock(env.datasets_site_path / "LOCK"):
        if not (env.datasets_site_path / name).exists():
            return False
        os.rename(env.datasets_site_path / name, env.inactive_datasets_site_path / name)
        os.rename(
            env.datasets_site_path / f"{name}.json",
            env.inactive_datasets_site_path / f"{name}.json",
        )
        return True


def require(env, dataset: Union[str, LegacyDataset]) -> bool:
    """Require that the given dataset is available to the environment.

    This will download and activate the dataset if it is not already installed.
    After calling this function, benchmarks from the dataset will be available
    to use.

    Example usage:

        >>> env = gym.make("llvm-v0")
        >>> require(env, "blas-v0")
        >>> env.reset(benchmark="blas-v0/1")

    :param env: The environment that this dataset is required for.
    :param dataset: The name of the dataset to download, the URL of the dataset,
        or a :class:`LegacyDataset` instance.
    :return: :code:`True` if the dataset was downloaded, or :code:`False` if the
        dataset was already available.
    """

    def download_and_unpack_archive(
        url: str, sha256: Optional[str] = None
    ) -> LegacyDataset:
        json_files_before = {
            f
            for f in env.inactive_datasets_site_path.iterdir()
            if f.is_file() and f.name.endswith(".json")
        }
        tar_data = io.BytesIO(download(url, sha256))
        with tarfile.open(fileobj=tar_data, mode="r:bz2") as arc:
            arc.extractall(str(env.inactive_datasets_site_path))
        json_files_after = {
            f
            for f in env.inactive_datasets_site_path.iterdir()
            if f.is_file() and f.name.endswith(".json")
        }
        new_json = json_files_after - json_files_before
        if not len(new_json):
            raise OSError(f"Downloaded dataset {url} contains no metadata JSON file")
        return LegacyDataset.from_json_file(list(new_json)[0])

    def unpack_local_archive(path: Path) -> LegacyDataset:
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")
        json_files_before = {
            f
            for f in env.inactive_datasets_site_path.iterdir()
            if f.is_file() and f.name.endswith(".json")
        }
        with tarfile.open(str(path), "r:bz2") as arc:
            arc.extractall(str(env.inactive_datasets_site_path))
        json_files_after = {
            f
            for f in env.inactive_datasets_site_path.iterdir()
            if f.is_file() and f.name.endswith(".json")
        }
        new_json = json_files_after - json_files_before
        if not len(new_json):
            raise OSError(f"Downloaded dataset {url} contains no metadata JSON file")
        return LegacyDataset.from_json_file(list(new_json)[0])

    with fasteners.InterProcessLock(env.datasets_site_path / "LOCK"):
        # Resolve the name and URL of the dataset.
        sha256 = None
        if isinstance(dataset, LegacyDataset):
            name, url = dataset.name, dataset.url
        elif isinstance(dataset, str):
            # Check if we have already downloaded the dataset.
            if "://" in dataset:
                name, url = None, dataset
                dataset: Optional[LegacyDataset] = None
            else:
                try:
                    dataset: Optional[LegacyDataset] = env.available_datasets[dataset]
                except KeyError:
                    raise ValueError(f"Dataset not found: {dataset}")
                name, url, sha256 = dataset.name, dataset.url, dataset.sha256
        else:
            raise TypeError(
                f"require() called with unsupported type: {type(dataset).__name__}"
            )

        if dataset and dataset.deprecated:
            warnings.warn(
                f"Dataset '{dataset.name}' is deprecated as of CompilerGym "
                f"release {dataset.deprecated_since}, please update to the "
                "latest available version",
                DeprecationWarning,
            )

        # Check if we have already downloaded the dataset.
        if name:
            if (env.datasets_site_path / name).is_dir():
                # Dataset is already downloaded and active.
                return False
            elif not (env.inactive_datasets_site_path / name).is_dir():
                # Dataset is downloaded but inactive.
                name = download_and_unpack_archive(url, sha256=sha256).name
        elif url.startswith("file:///"):
            name = unpack_local_archive(Path(url[len("file:///") :])).name
        else:
            name = download_and_unpack_archive(url, sha256=sha256).name

        activate(env, name)
        return True
