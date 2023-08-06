"""
import functions so they can be run as the module
"""

#from .prefetch_from_dictionary import prefetch_from_dictionary
#from .prefetch_from_file import file_to_prefetch as prefetch_from_file
#from .prefetch_from_url import url_to_prefetch as prefetch_from_url
#from .prefetch_parse import parse_prefetch as prefetch_parse
#from .prefetch_validate import validate_prefetch as prefetch_validate
#from .prefetch import prefetch
#from .prefetches_have_matching_hashes import prefetches_have_matching_hashes

from . import prefetch_validate
from . import prefetches_have_matching_hashes
from . import prefetch_from_dictionary
from . import prefetch_from_file
from . import prefetch_from_url
from . import prefetch_parse
from . import prefetch
