"""Flywheel meta extraction helpers."""
import typing as t

import orjson
from fw_utils import AttrDict, attrify, inflate_dotdict
from memoization import cached

from .config import tz
from .fields import FIELD_LIST, FIELDS, validate_field_value
from .pattern import MetaPattern, Tokenizer

__all__ = ["MetaData", "MetaExtractor", "extract_meta"]

Patterns = t.Union[t.List[t.Tuple[str, str]], t.Dict[str, str]]


class MetaData(dict):
    """Flywheel metadata dictionary."""

    def __getattr__(self, name: str):
        """Return dictionary keys as attributes."""
        return getattr(self.dict, name)

    def __iter__(self):
        """Return dict key iterator respecting the hierarchy/field order."""
        return iter(sorted(super().keys(), key=self.sort_key))

    @staticmethod
    def sort_key(key: str) -> t.Tuple[int, str]:
        """Return sorting key to order meta fields by hierarchy/importance."""
        num = FIELD_LIST.index(key) if key in FIELDS else len(FIELDS)
        return num, key

    def keys(self):
        """Return dict keys, sorted."""
        return list(self)

    def values(self):
        """Return dict values, sorted."""
        return [self[k] for k in self]

    def items(self):
        """Return key, value pairs, sorted."""
        return iter((k, self[k]) for k in self)

    @property
    def dict(self) -> AttrDict:
        """Return inflated metadata dict ready for Flywheel uploads."""
        return attrify(inflate_dotdict(self))

    @property
    def json(self) -> bytes:
        """Return JSON dump of the inflated meta."""
        return orjson.dumps(self.dict)


@cached
class MetaExtractor:  # pylint: disable=too-few-public-methods
    """Meta Extractor."""

    def __init__(
        self,
        *,
        patterns: t.Optional[Patterns] = None,
        defaults: t.Optional[t.Dict[str, str]] = None,
        overrides: t.Optional[t.Dict[str, str]] = None,
        customize: t.Optional[t.Callable[[dict, dict], None]] = None,
    ) -> None:
        """Validate, compile and (functools)cache metadata extraction patterns."""
        # pre-compile/validate extract patterns
        patterns_ = patterns.items() if isinstance(patterns, dict) else patterns
        self.patterns = [
            (MetaPattern(pattern), field) for pattern, field in patterns_ or []
        ]
        # validate default fields and values
        self.defaults = dict(
            validate_field_value(field, default)
            for field, default in (defaults or {}).items()
        )
        # validate override fields and values
        self.overrides = dict(
            validate_field_value(field, override)
            for field, override in (overrides or {}).items()
        )
        self.customize = customize

    def extract(self, file: dict) -> MetaData:
        """Extract metadata from given dict like object."""
        meta: t.Dict[str, t.Any] = dict()
        temp: t.Dict[str, t.Any] = dict()
        for pattern, src in self.patterns:
            try:
                src_value = format_source_string(src, temp, file)
            except (KeyError, ValueError):
                # skip if key not found or value is empty
                continue
            for fw_field, value in pattern.extract(src_value, temp).items():
                # setdefault allows using multiple patterns as fallback
                meta.setdefault(*validate_field_value(fw_field, value))
        # apply user-defaults (eg. {'project.label': 'Default Project'})
        for field, user_default in self.defaults.items():
            meta.setdefault(field, user_default)
        # apply file-defaults (eg. {'session.label': 'StudyDescription'})
        for field, file_default in getattr(file, "default_meta", {}).items():
            meta.setdefault(*validate_field_value(field, file_default))
        # apply user-overrides (eg. {'project.label': 'Override Project'})
        for field, override in self.overrides.items():
            meta[field] = override
        # set timezone if timestamp present
        for prefix in ("session", "acquisition"):
            if meta.get(f"{prefix}.timestamp"):
                meta[f"{prefix}.timezone"] = str(tz())
        # trigger user-callback if given for further meta customization
        if self.customize is not None:
            self.customize(file, meta)
        return MetaData(meta)


def extract_meta(
    file: dict,
    *,
    patterns: t.Optional[Patterns] = None,
    defaults: t.Optional[t.Dict[str, str]] = None,
    overrides: t.Optional[t.Dict[str, str]] = None,
    customize: t.Optional[t.Callable[[dict, dict], None]] = None,
) -> MetaData:
    """Extract Flywheel metadata from a dict like object."""
    # NOTE using the class enables validation and caching
    meta_extractor = MetaExtractor(
        patterns=patterns,
        defaults=defaults,
        overrides=overrides,
        customize=customize,
    )
    return meta_extractor.extract(file)


def format_source_string(src_str: str, *mappings: dict) -> str:
    """Format source string using the given mappings."""
    source = Tokenizer(src_str)

    def get_val(key: str) -> str:
        for mapping in mappings:
            val = getattr(mapping, key, None) or mapping.get(key)
            if val is None or val == "":
                continue
            return str(val)
        raise KeyError(f"invalid key {key}")

    result = ""
    is_template = False
    while char := source.next:
        source.set_next()

        if char in ("\\{", "\\}"):
            result += char[1]
        elif char == "{":
            key = source.get_until("}")
            if not key:
                raise ValueError("missing key name")
            if not source.match("}"):
                raise ValueError("missing }, unterminated pattern")
            result += get_val(key)
            is_template = True
        else:
            # keep everything else as is
            result += char
    if not is_template:
        # shorthand notation like 'PatientID'
        return get_val(result)
    return result
