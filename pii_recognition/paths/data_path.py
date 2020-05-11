from pii_recognition.data_readers import reader_registry

from .path import Path


class DataPath(Path):
    pattern_str: str = r".*datasets/(?P<data_name>[a-zA-Z]+)(?P<version>\d+)/"

    @property
    def reader_name(self):
        mapping = {"conll": "ConllReader", "wnut": "WnutReader"}

        reader_presented = set(mapping.values())
        readers_available = set(reader_registry.keys())
        assert reader_presented == readers_available, (
            f"Missing data path mapping for readers: "
            f"{readers_available - reader_presented}"
        )

        if self.data_name not in mapping:
            raise NameError(f"No reader found to process {self.data_name} dataset")
        return mapping[self.data_name]
