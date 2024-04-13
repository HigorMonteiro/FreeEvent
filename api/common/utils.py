from enum import Enum


class EventStatus(Enum):
    DRAFT = 'rascunho'
    PUBLISHED = 'publicado'
    CANCELED = 'cancelado'
