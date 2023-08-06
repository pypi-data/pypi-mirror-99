from pathlib import Path

from openpecha.catalog.utils import create_pecha_id
from openpecha.core.layer import InitialCreationEnum, Layer, LayersEnum, MetaData
from openpecha.core.pecha import OpenPechaFS

from .. import config


class EmptyEbook:
    def __init__(self, output_path=config.PECHAS_PATH, metadata={}, assets={}) -> None:
        self.output_path = Path(output_path if output_path else config.PECHAS_PATH)
        self.metadata = metadata
        self.meta_fn = None
        self.pecha_path = None
        self.assets = assets
        self.layers = [
            LayersEnum.book_title,
            LayersEnum.author,
            LayersEnum.chapter,
            LayersEnum.citation,
            LayersEnum.tsawa,
            LayersEnum.sabche,
            LayersEnum.yigchung,
        ]

    def get_dummy_layers(self):
        layers = {}
        for layer in self.layers:
            layers[layer] = Layer(
                annotation_type=layer, revision="00001", annotations={}
            )
        return layers

    def create_opf(self, text, id_):
        pecha_id = create_pecha_id(id_)
        openpecha = OpenPechaFS(
            base={"v001": text},
            layers={"v001": self.get_dummy_layers()},
            meta=MetaData(
                id=pecha_id,
                initial_creation_type=InitialCreationEnum.ebook,
                source_metadata=self.metadata,
            ),
            assets=self.assets,
        )

        openpecha.save(output_path=self.output_path)
        self.meta_fn = openpecha.meta_fn
        self.pecha_path = openpecha.opf_path.parent
