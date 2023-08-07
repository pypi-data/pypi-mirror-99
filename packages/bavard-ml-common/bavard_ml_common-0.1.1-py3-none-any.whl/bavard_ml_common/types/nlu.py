import typing as t

from pydantic import BaseModel

from bavard_ml_common.ml.dataset import LabeledDataset


class TrainingTag(BaseModel):
    """A tag as it appears in NLU training data.
    """
    tagType: str
    start: int
    end: int


class NLUExample(BaseModel):
    intent: t.Optional[str]
    text: str
    tags: t.List[TrainingTag]


class NLUExampleDataset(LabeledDataset[NLUExample]):
    def get_label(self, item: NLUExample) -> str:
        return item.intent

    def unique_tag_types(self) -> t.Set[str]:
        return set(tag.tagType for ex in self for tag in ex.tags)
