from enum import Enum
from pydantic import BaseModel, Field
from typing import Any, List, Optional

from pyrasgo.schemas.attributes import Attribute
from pyrasgo.schemas.data_source import DataSource
from pyrasgo.schemas.granularity import Granularity

class DataType(Enum):
    INT = 'int'
    INTEGER = 'integer'
    FLOAT = 'float'
    FLOAT64 = 'float64'
    DECIMAL = 'decimal'
    NUMERIC = 'numeric'
    NUMBER = 'number'
    REAL = 'real'
    DOUBLE = 'double'
    STRING = 'string'
    TEXT = 'text'
    VARCHAR = 'varchar'
    CHAR = 'char'
    DATE = 'date'
    DATETIME = 'datetime'
    TIMESTAMP = 'timestamp'
    BINARY = 'binary'
    BOOLEAN = 'boolean'
    BOOL = 'bool'

    @classmethod
    def __missing__(cls, key):
        formatted = key.replace(" ", "").lower()
        try:
            return cls._value2member_map_[formatted]
        except KeyError:
            raise ValueError("%r is not a valid %s" % (key, cls.__name__))

# Schemas to be used for general pyrasgo
class Dimension(BaseModel):
    columnName: str
    dataType: DataType
    granularity: Optional[str]

class Feature(BaseModel):
    columnName: str
    dataType: DataType
    description: Optional[str]
    displayName: Optional[str]
    status: Optional[str]
    tags: Optional[List[str]]
    attributes: Optional[List[Attribute]]
    class Config:
        allow_population_by_field_name = True

class FeatureSet(BaseModel):
    id: Optional[int]
    name: Optional[str]
    sourceTable: str
    dimensions: Optional[List[Dimension]]
    features: Optional[List[Feature]]
    dataSource: Optional[DataSource]
    granularities: Optional[List[Granularity]]


# Schema to be used for YML files
# TODO: sync with new schema when customers' legacy files are converted
class DimensionYML(BaseModel):
    columnName: str
    dataType: str
    granularity: str
    class Config:
        allow_population_by_field_name = True

class FeatureYML(BaseModel):
    columnName: str
    dataType: str
    description: Optional[str]
    displayName: Optional[str]
    tags: Optional[List[str]]
    class Config:
        allow_population_by_field_name = True

class DataSourceYML(BaseModel):
    name: Optional[str]

class FeatureSetYML(BaseModel):
    name: Optional[str] = ''
    sourceTable: str
    dimensions: Optional[List[DimensionYML]]
    features: Optional[List[FeatureYML]]
    dataSource: Optional[DataSourceYML]
    script: Optional[str] = ''
    class Config:
        allow_population_by_field_name = True