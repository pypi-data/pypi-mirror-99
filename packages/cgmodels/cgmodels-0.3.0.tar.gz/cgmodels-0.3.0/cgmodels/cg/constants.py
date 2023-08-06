from enum import Enum


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class Pipeline(StrEnum):
    BALSAMIC: str = "balsamic"
    FASTQ: str = "fastq"
    FLUFFY: str = "fluffy"
    MICROSALT: str = "microsalt"
    MIP_DNA: str = "mip-dna"
    MIP_RNA: str = "mip-rna"
    SARS_COV_2: str = "sars-cov-2"
