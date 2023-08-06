import re
from typing import List

import numpy as np
import torch
from deepchainapps import log
from esm import pretrained

PATTERN = r"esm.+_t(\d{1,2}).+"

BACKEND = [
    "esm1_t12_85M_UR50S",
    "esm1_t34_670M_UR100",
    "esm1_t34_670M_UR50D",
    "esm1_t34_670M_UR50S",
    "esm1_t6_43M_UR50S",
    "esm1b_t33_650M_UR50S",
    "esm_msa1_t12_100M_UR50S",
]


class TransformersApp:
    def __init__(
        self, device: str,
        model_uri: str = None,
        model_type: str = "esm1_t6_43M_UR50S"
    ):
        """
        Use ESM embedding : possibility to have 6 models of different size in backend
        """
        self.model_type = model_type
        self.device = torch.device(device)
        self.model_uri = model_uri

        if device == "cpu" and model_type != "esm1_t6_43M_UR50S":
            log.warning(
                "You should choose esm1_t6_43M_UR50S based on your cpu configuration."
            )
        try:
            fn = getattr(pretrained, model_type)
        except:
            msg = (
                f"Couldn't find model type {model_type} in backend "
                f"Choose model inside list {' / '.join(BACKEND)}"
            )
            raise ImportError(msg)

        self.model, self.token = fn()
        self.model = self.model.to(self.device)
        self.emb_version = int(re.findall(PATTERN, model_type)[0])

    @classmethod
    def list_esm_backend(cls) -> None:
        log.info(f"Use ESM backend in this list {' / '.join(BACKEND)}")

    def predict_embedding(self, sequences: List[str]):
        """Return the embedding of a sequence of Am.Ac."""
        batch_converter = self.token.get_batch_converter()
        sequences = self.convert_batch_format(sequences)
        batch_labels, batch_strs, batch_tokens = batch_converter(sequences)

        with torch.no_grad():
            output = self.model(batch_tokens, repr_layers=[self.emb_version])

        output = output["representations"][self.emb_version].mean(1)

        return output

    def convert_batch_format(self, sequences: str):
        """Convert to the correct format exptected by the model"""
        return [(f"protein_{i}", seq) for i, seq in enumerate(sequences)]
