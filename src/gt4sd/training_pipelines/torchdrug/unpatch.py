import typing
from typing import List

import torch
import torch.utils.data.dataset as dataset
from torch.utils.data.dataset import (
    ChainDataset,
    ConcatDataset,
    Dataset,
    DFIterDataPipe,
    IterableDataset,
    IterDataPipe,
    MapDataPipe,
    Subset,
    TensorDataset,
)

sane_datasets = [
    Dataset,
    ChainDataset,
    ConcatDataset,
    DFIterDataPipe,
    IterableDataset,
    IterDataPipe,
    MapDataPipe,
    Subset,
    TensorDataset,
]


@typing.no_type_check
def fix_datasets(sane_datasets: List[dataset.Dataset]) -> None:
    """
    Helper function to revert TorchDrug dataset handling (which breaks core
    pytorch functionalities). For details see:
    https://github.com/DeepGraphLearning/torchdrug/issues/96

    Args:
        sane_datasets: A list of pytorch datasets.

    Raises:
        AttributeError: If a passed dataset was not sane.
    """
    dataset = sane_datasets[0]
    torch.utils.data.dataset.Dataset = dataset  # type: ignore
    torch.utils.data.dataset.ChainDataset = sane_datasets[1]  # type: ignore
    torch.utils.data.dataset.ConcatDataset = sane_datasets[2]  # type: ignore
    torch.utils.data.dataset.DFIterDataPipe = sane_datasets[3]  # type: ignore
    torch.utils.data.dataset.IterableDataset = sane_datasets[4]  # type: ignore
    torch.utils.data.dataset.IterDataPipe = sane_datasets[5]  # type: ignore
    torch.utils.data.dataset.MapDataPipe = sane_datasets[6]  # type: ignore
    torch.utils.data.dataset.Subset = sane_datasets[7]  # type: ignore
    torch.utils.data.dataset.TensorDataset = sane_datasets[8]  # type: ignore

    for ds in sane_datasets[1:]:
        if not issubclass(ds, dataset):
            raise AttributeError(
                f"Reverting silent TorchDrug overwriting failed, {ds} is not a subclass"
                f" of {dataset}."
            )