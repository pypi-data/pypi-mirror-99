from .multiplicative import isotope_pattern_multiplicative
from .combinatoric import isotope_pattern_combinatoric, isotope_pattern_hybrid
from .simulated import gaussian_isotope_pattern
from .bar import bar_isotope_pattern, VALID_DROPMETHODS, VALID_GROUP_METHODS
try:
    from .isospec import isotope_pattern_isospec
except ImportError as e:
    import warnings
    warnings.warn(f'failed to import isospec: {e}')
    isotope_pattern_isospec = None

# valid isotope pattern generation methods
VALID_IPMETHODS = [
    'combinatorics',
    'multiplicative',
    'hybrid',
    # 'cuda',
]
if isotope_pattern_isospec is not None:
    VALID_IPMETHODS.append('isospec')

__all__ = [
    'VALID_IPMETHODS',
    'VALID_DROPMETHODS',
    'VALID_GROUP_METHODS',
    'isotope_pattern_multiplicative',
    'isotope_pattern_combinatoric',
    'isotope_pattern_hybrid',
    'gaussian_isotope_pattern',
    'isotope_pattern_isospec',
    'bar_isotope_pattern',
]
