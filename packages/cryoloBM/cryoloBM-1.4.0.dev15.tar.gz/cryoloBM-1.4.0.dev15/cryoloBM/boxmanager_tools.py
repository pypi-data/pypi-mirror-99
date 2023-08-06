#
# This fiel contains command line cryoloBM_tools for box management
#
import sys
import argparse

PARSER=None

def create_coords2warp_parser(parser):
    scale_required_group = parser.add_argument_group(
            "Required arguments",
            "Converts .coords to a WARP compatible .star file.",
        )

    scale_required_group.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input folder or file. Files should be coords format. If the .coords provides a filament id, prior information are automatically added.",
    )

    scale_required_group.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output folder where to write the WARP compatible star file.",
    )

    scale_required_group.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="Coordinates get scaled by this factor. This is useful incase you have .coords files from binned reconstructions.",
    )

    scale_required_group.add_argument(
        "--apix",
        required=True,
        type=float,
        help="Pixel size in Angstrom.",
    )

    scale_required_group.add_argument(
        "--mag",
        type=float,
        default=10000,
        help="Magnification",
    )


def create_scale_parser(parser):
    scale_required_group = parser.add_argument_group(
        "Required arguments",
        "Scales coordinate files.",
    )

    scale_required_group.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input folder or file.",
    )

    scale_required_group.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output folder where to write the scaled coordinates.",
    )

    scale_required_group.add_argument(
        "-s",
        "--scale",
        type=float,
        required=True,
        help="Scale factor",
    )

def create_priors2star_parser(parser):
    priors2star_required_group = parser.add_argument_group(
        "Required arguments",
        "Add filament prior information to star",
    )

    priors2star_required_group.add_argument(
        "-i",
        "--input",
        required=True,
        help="Path to particles.star file.",
    )
    priors2star_required_group.add_argument(
        "-fi",
        "--fidinput",
        required=True,
        help="Input folder or file with *_fid.coords files from crYOLO .",
    )

    priors2star_required_group.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output folder where to write the augmented star files..",
    )

TYPE_CBOX=0
TYPE_COORDS=1
TYPE_EMAN_BOX=2
TYPE_EMAN_BOX_3D=3
TYPE_EMAN_HELICON=4
TYPE_EMAN_START_END=5
TYPE_RELION_STAR=6

def get_file_type(path):
    from cryolo import CoordsIO
    if CoordsIO.is_eman1_filament_start_end(path):
        return TYPE_EMAN_START_END
    if CoordsIO.is_eman1_helicon(path):
        return TYPE_EMAN_HELICON
    if CoordsIO.is_star_filament_file(path):
        return TYPE_RELION_STAR
    if path.endswith(".coords"):
        return TYPE_COORDS
    if path.endswith(".cbox"):
        return TYPE_CBOX
    return -1


def create_parser():
    parent_parser = argparse.ArgumentParser(
        description="Boxmanager Tools",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parent_parser.add_subparsers(help="sub-command help")

    # Config generator
    parser_scale = subparsers.add_parser(
        "scale",
        help="Scales all sort of coordinate files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    create_scale_parser(parser_scale)

    # Config generator
    parser_coords2warp = subparsers.add_parser(
        "coords2warp",
        help="Converts coords file to Warp compatible star file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    create_coords2warp_parser(parser_coords2warp)

    parser_priors2star = subparsers.add_parser(
        "priors2star",
        help="Add filament prior information to star file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    create_priors2star_parser(parser_priors2star)

    return parent_parser


def _main_():
    global PARSER

    PARSER = create_parser()

    args = PARSER.parse_args()

    if "scale" in sys.argv[1]:
        from cryoloBM_tools import scale
        scale.scale(
            input_path=args.input,
            output_path=args.output,
            scale_factor=args.scale
                    )
    if "coords2warp" in sys.argv[1]:
        from cryoloBM_tools import coords2warp
        coords2warp.convert(
            input_path=args.input,
            output_path=args.output,
            scale=args.scale,
            pixelsize=args.apix,
            magnification=args.mag
        )

    if "priors2star" in sys.argv[1]:
        from cryoloBM_tools import priors2star
        import os
        import glob

        if os.path.isfile(args.input):
            star_file = args.input
        else:
            raise ValueError("Can't find input star file.")

        if os.path.isfile(args.fidinput):
            fid_files = [args.fidinput]
        else:
            path = os.path.join(os.path.abspath(args.fidinput), "*_fid.coords")
            fid_files = glob.glob(path)

        # Find star fid paris
        outname = os.path.splitext(os.path.basename(star_file))[0] + "_with_prior.star"
        priors2star.add_prior_to_star(
            in_star=star_file,
            coords_fid_paths=fid_files,
            output_star=os.path.join(args.output, outname),
        )


if __name__ == "__main__":
    _main_()