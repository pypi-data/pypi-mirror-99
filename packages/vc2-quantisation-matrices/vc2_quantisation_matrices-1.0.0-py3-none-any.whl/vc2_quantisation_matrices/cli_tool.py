"""
Quantisation Matrix Calculation Tool
====================================

This module implements a command-line tool which calculates and prints out
quantisation matrices for arbitrary filter combinations.
"""

from argparse import ArgumentParser, ArgumentTypeError

from collections import OrderedDict

from vc2_data_tables import WaveletFilters

from vc2_quantisation_matrices import derive_quantisation_matrix


# A lookup from identifier strings to VC-2 wavelet indices.
WAVELET_IDENTIFIERS = OrderedDict()
# Allow specification of wavelet by index
for index in WaveletFilters:
    WAVELET_IDENTIFIERS[str(int(index))] = index
# Allow specication of wavelet by name
for index in WaveletFilters:
    WAVELET_IDENTIFIERS[index.name] = index

def parse_wavelet_identifier(identifier):
    if identifier in WAVELET_IDENTIFIERS:
        return WAVELET_IDENTIFIERS[identifier]
    else:
        raise ArgumentTypeError("{!r} is not a valid wavelet identifier (see --help).".format(
            identifier
        ))

def format_quantisation_matrix(matrix):
    return "\n".join(
        "Level {}: {}".format(
            level,
            ", ".join(
                "{}: {:2d}".format(orientation, orientations[orientation])
                for orientation in sorted(
                    orientations,
                    key={  # Ensure order as shown in spec
                        "L": 0,
                        "H": 1,
                        "LL": 2,
                        "HL": 3,
                        "LH": 4,
                        "HH": 5,
                    }.get,
                )
            ),
        )
        for level, orientations in sorted(matrix.items())
    )


def main(argv=None):
    parser = ArgumentParser(description="""
        Calculates a VC-2 quantisation matrix which normalises noise power over
        all transform bands.
    """)
    
    parser.add_argument(
        "--wavelet-index", "-w",
        required=True, type=parse_wavelet_identifier,
        help="""
            The wavelet type used for vertical filtering (use
            --wavelet-index-ho to set the horizontal filter type). The index or
            name of one of the VC-2 filters: {}.
        """.format(
            ", ".join(
                "{} or {}".format(int(index), index.name)
                for index in WaveletFilters
            ),
        ),
    )
    
    parser.add_argument(
        "--wavelet-index-ho", "-W",
        type=parse_wavelet_identifier,
        help="""
            The wavelet type used for horizontal filtering. (If
            is not given, the same value as --wavelet-index will be assumed).
        """,
    )
    
    parser.add_argument(
        "--dwt-depth", "-d",
        required=True, type=int,
        help="""
            The 2D wavelet transform depth.
        """,
    )
    
    parser.add_argument(
        "--dwt-depth-ho", "-D",
        type=int, default=0,
        help="""
            The number of horizontal only wavelet transform levels. (Default:
            0).
        """,
    )
    
    args = parser.parse_args(argv)
    
    if args.dwt_depth < 0:
        raise parser.error("--dwt-depth/-d must be non-negative.")
    if args.dwt_depth_ho < 0:
        raise parser.error("--dwt-depth-ho/-D must be non-negative.")
    
    matrix = derive_quantisation_matrix(
        wavelet_index=args.wavelet_index,
        wavelet_index_ho=(
            args.wavelet_index_ho
            if args.wavelet_index_ho is not None else
            args.wavelet_index
        ),
        dwt_depth=args.dwt_depth,
        dwt_depth_ho=args.dwt_depth_ho,
    )
    
    print(format_quantisation_matrix(matrix))
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
