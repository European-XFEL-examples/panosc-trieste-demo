#!/usr/bin/env python3

import argparse
import os
import sys

from jupyter_client import kernelspec


def install_kernel(*, template_path, overlay_path, kernel_name):
    kernel_instrument = os.path.basename(os.path.dirname(os.environ['SINGULARITY_CONTAINER']))
    kerenl_image = os.environ['SINGULARITY_NAME'].replace('.sif', '')

    if kernel_name is None:
        kernel_name = f"{kernel_instrument}-{kerenl_image}"

    ksm = kernelspec.KernelSpecManager()

    if kernel_name in ksm.get_all_specs().keys():
        print(f"Removing existing kernelspec in {ksm.get_kernel_spec(kernel_name).resource_dir}")

    ksm.install_kernel_spec(
        template_path,
        kernel_name=kernel_name,
        user=True
    )

    kernel = ksm.get_kernel_spec(kernel_name)

    print(f"Installed kernelspec {kernel_name} in {kernel.resource_dir}")

    #  Overlay command templating
    if overlay_path is not None:
        if not os.path.isabs(overlay_path):
            overlay_path = os.path.abspath(overlay_path)

        overlay_cmd = f"--overlay\", \"{overlay_path}"
    else:
        overlay_cmd = ""

    #  Crappily hard-coded list of binds, TODO: IMBROVE BIND PATH TEMPLATING
    target_bind = ["/gpfs", "/data", "/afs", "/cvmfs", "/pnfs", "/nfs", "/asap3", "/run"]
    bind_cmd = ["-B\", \"{0}:{0}".format(b) for b in target_bind]

    #  Fill in kernel.json variables
    spec_path = os.path.join(kernel.resource_dir, 'kernel.json')
    with open(spec_path, 'r+') as spec_file:
        spec = spec_file.read()

        spec = spec.replace('{{OVERLAY_CMD}}', overlay_cmd)

        spec = spec.replace('{{BIND_CMD}}', "\",\n    \"".join(bind_cmd))

        spec = spec.replace('{{IMAGE_PATH}}', os.environ['SINGULARITY_CONTAINER'])

        spec = spec.replace('{{KERNEL_ROOT}}', kernel.resource_dir)
        spec = spec.replace('{{KERNEL_NAME}}', kernel_name)

        #  TODO: Better way of doing this empty quote stripping thing
        spec_no_empty_quotes = []
        for l in spec.split("\n"):
            if '""' in l:
                pass
            else:
                spec_no_empty_quotes.append(l)

        spec_file.seek(0)
        spec_file.write("\n".join(spec_no_empty_quotes))


def main():
    parser = argparse.ArgumentParser(
        description="Use this command to install the kernel into your user directory"
    )

    parser.add_argument(
        '-n', '--name',
        help='Name the installed kernel should have, defaults to image name',
        default=None,
        required=False
    )

    parser.add_argument(
        '-o', '--overlay',
        help='Path to an overlay the kernel will load',
        default=None,
        required=False
    )

    parser.add_argument(
        '-t', '--template',
        help='Path to the template file used to create the kerenel',
        default="/repo/.singularity/kernel-template",
        required=False
    )

    res = parser.parse_args(sys.argv[1:])

    install_kernel(
        template_path=res.template,
        overlay_path=res.overlay,
        kernel_name=res.name
    )


if __name__ == "__main__":
    main()
