"""
import functions so they can be run as the module
"""

from bigfix_prefetch.prefetch_from_dictionary import prefetch_from_dictionary
from bigfix_prefetch.prefetch_from_file import file_to_prefetch as prefetch_from_file
from bigfix_prefetch.prefetch_from_url import url_to_prefetch as prefetch_from_url
from bigfix_prefetch.prefetch_parse import parse_prefetch as prefetch_parse
from bigfix_prefetch.prefetch_validate import validate_prefetch as prefetch_validate
from bigfix_prefetch.prefetch import prefetch
from bigfix_prefetch.prefetches_have_matching_hashes import prefetches_have_matching_hashes
