# Docker Container for poremaps 

## Build and run
Check permissions and if make executable if necessary.

```bash
chmod +x docker_krach2025-poremaps.sh
chmod +x install_Krach2025-poremaps.py
chmod +x set_poremaps_shared_folder_permissions.sh
```

Build Docker image:
```bash 
docker build -f Dockerfile -t krach2025-poremaps --no-cache .
```

Open image and run:
```bash
./docker_krach2025-poremaps.sh open
```


## License

The solver is licensed under the terms and conditions of the MIT License version 3 or - at your option - any later
version. The License can be [found online](https://opensource.org/license/mit/) or in the LICENSE.md file
provided in the topmost directory of source code tree.

## How to cite

The solver is research software and developed at a research institute. Please cite **specific releases** according to [**DaRUS**](https://doi.org/10.18419/darus-3676) version.

If you are using poremaps in scientific publications and in the academic context, please cite our publications:

```bib
@article{Krach2025a,
    author={Krach, David and Ruf, Matthias and Steeb, Holger}, 
    title={{POREMAPS}: A finite difference based Porous Media Anisotropic Permeability Solver for   Stokes flow}, 
    DOI={10.69631/ipj.v2i1nr39}, 
    journal={InterPore Journal}, 
    pages={IPJ260225–7}, 
    volume={2}, 
    number={1}, 
    month={Feb.}, 
    year={2025}, 
    place={De Bilt, The Netherlands}
}
```

```bib
@data{Krach2024a,
    author = {Krach, David and Ruf, Matthias and Steeb, Holger},
    publisher = {DaRUS},
    title = {{POREMAPS 1.0.0: Code, Benchmarks, Applications}},
    year = {2024},
    version = {V1},
    doi = {10.18419/darus-3676},
    url = {https://doi.org/10.18419/darus-3676}
}
```

## Solver is used in following publications

[![Identifier](https://img.shields.io/badge/Publication_ADWR_Krach_et.al._(2025)-blue)](https://doi.org/10.1016/j.advwatres.2024.104860)

```bib
@article{Krach2025b,
    title = {A novel geometry-informed drag term formulation for pseudo-3D Stokes simulations with varying apertures},
    journal = {Advances in Water Resources},
    volume = {195},
    year = {2025},
    doi = {https://doi.org/10.1016/j.advwatres.2024.104860},
    author = {David Krach and Felix Weinhardt and Mingfeng Wang and Martin Schneider and Holger Class and Holger Steeb},
    keywords = {Porous media, Stokes flow, Biomineralization, Microfluidics, Image-based simulations, Computational efficiency versus accuracy}
}

```

## Developer

- [David Krach](https://www.mib.uni-stuttgart.de/institute/team/Krach/) E-mail: [david.krach@mib.uni-stuttgart.de](mailto:david.krach@mib.uni-stuttgart.de)

