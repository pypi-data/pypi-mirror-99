import os
import shutil
import logging
import pathlib
import argparse
import numpy as np

# Set tensorflow log level to error only
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from rich.table import Table
from rich.style import Style
from rich.console import Console

import tensorflow as tf
import tensorflow.python.util.deprecation as deprecation

from ganpdfs.hyperscan import hyper_train
from ganpdfs.pdformat import XNodes
from ganpdfs.pdformat import InputPDFs
from ganpdfs.hyperscan import load_yaml
from ganpdfs.hyperscan import run_hyperparameter_scan

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

deprecation._PRINT_DEPRECATION_WARNINGS = False

console = Console()
logging.basicConfig(
        level=logging.WARNING,
        format="\033[0;32m[%(levelname)s]\033[97m %(message)s",
    )
logger = logging.getLogger(__name__)

# Random Seeds
tf.random.set_seed(0)


NF = 6      # Number of flavours
Q0 = 1.65   # Initial energy scale


def splash():
    """Splash information."""

    style = Style(color="blue")
    logo = Table(show_header=True, header_style="bold blue", style=style)
    logo.add_column("𝖌𝖆𝖓𝖕𝖉𝖋𝖘", justify="center", width=80)
    logo.add_row("[bold blue]Generative Adversarial Neural Networks (GANs) for PDF replicas.")
    logo.add_row("[bold blue]https://n3pdf.github.io/ganpdfs/")
    logo.add_row("[bold blue]© N3PDF 2021")
    logo.add_row("[bold blue]Authors: Stefano Carrazza, Juan M. Cruz-Martinez, Tanjona R. Rabemananjara")
    console.print(logo)


def normalize_inpdf(input_pdf):
    pdfabsolute = np.absolute(input_pdf)
    normalization = np.max(pdfabsolute) + 1e-8
    normalized_pdf = (input_pdf - normalization) / normalization
    return normalization, normalized_pdf


def posint(value):
    """Checks that a given number is positive."""

    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"Negative values are not allowed: {value}")
    return ivalue


def argument_parser():
    """Parse the input arguments for wganpdfs.
    """
    # read command line arguments
    parser = argparse.ArgumentParser(description="Generate synthetic replicas with GANs.")
    parser.add_argument("-f", "--force", action="store_true")
    parser.add_argument("runcard", help="A json file with the setup.")
    parser.add_argument("-c", "--cluster", help="Enable cluster scan.")
    parser.add_argument("-s", "--hyperopt", type=int, help="Enable hyperopt scan.")
    parser.add_argument("-t", "--totrep", type=posint, help="Number of output replicas.")
    args = parser.parse_args()

    # check the runcard
    if not os.path.isfile(args.runcard):
        raise ValueError("Invalid runcard: not a file.")
    if args.force:
        logger.warning("Running with --force will overwrite existing results.")

    return args


def main():
    """Main controller from which the main parameters are set and defined.
    """
    splash()
    args = argument_parser()

    hps = load_yaml(args.runcard)
    hps["tot_replicas"] = args.totrep
    nf = hps.get("nf", NF)
    qvalue = hps.get("q", Q0)
    hps["save_output"] = str(hps["pdf"]) + "_enhanced"
    out_folder = pathlib.Path(hps["save_output"]).absolute()
    out_folder.mkdir(exist_ok=True)
    shutil.copyfile(args.runcard, f"{out_folder}/input-runcard.json")

    console.print(
            "\n• Computing PDF grids with the following parameters:",
            style="bold blue"
    )
    init_pdf = InputPDFs(hps["pdf"], qvalue, nf)

    # Choose the LHAPDF x-grid by default
    hps["pdfgrid"] = init_pdf.extract_xgrid()
    if hps["x_grid"] == "lhapdf":
        xgrid = hps["pdfgrid"]
    elif hps["x_grid"] == "custom":
        xgrid = XNodes().build_xgrid()
    elif hps["x_grid"] == "standard":
        xgrid = init_pdf.custom_xgrid(nbpoints=hps.get("nb_xpoints", 200))
    else:
        raise ValueError("{hps['x_grid']} is not a valid grid.")

    # Print summary table of PDF grids
    summary = Table(show_header=True, header_style="bold blue")
    summary.add_column("Parameters", justify="left", width=30)
    summary.add_column("Description", justify="center", width=40)
    summary.add_row("Prior PDF set", f"{hps['pdf']}")
    summary.add_row("Input energy Q0", f"{Q0} GeV")
    summary.add_row(
        "x-grid size",
        f"{xgrid.shape[0]} points, x=({xgrid[0]:.4e}, {xgrid[-1]:.4e})"
    )
    console.print(summary)

    pdf = init_pdf.build_pdf(xgrid)
    pdf_lhapdf = init_pdf.lhaPDF_grids()
    norm, npdf = normalize_inpdf(pdf)
    pdfs = (norm, npdf, pdf_lhapdf)

    # Number of Output replicas (Prior+Synthetics)
    hps["input_replicas"] = pdf.shape[0]
    hps["out_replicas"] = hps["input_replicas"] if args.totrep is None else \
            args.totrep - hps["input_replicas"]

    console.print("\n• Training:", style="bold blue")
    # If hyperscan is True
    if args.hyperopt:
        hps["scan"] = True  # Enable hyperscan

        def fn_hyper_train(params):
            return hyper_train(params, xgrid, pdfs)

        # Run hyper scan
        hps = run_hyperparameter_scan(
            fn_hyper_train, hps, args.hyperopt, args.cluster, out_folder
        )

    # Run the best Model and output logs
    hps["scan"] = False
    hps["verbose"] = True
    loss = hyper_train(hps, xgrid, pdfs)
