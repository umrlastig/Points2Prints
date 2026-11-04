---
icon: lucide/download
---

# Installation

1. Install [pixi](https://pixi.prefix.dev/latest/) and add it to the path.
    For example on Linux:
    ```bash
    curl -fsSL https://pixi.sh/install.sh | sh
    echo 'export PATH="$HOME/.pixi/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
    ```
2. Install most of the dependencies of the project:
    ```bash
    pixi install
    ```
3. Clone and compile [LiDARHD_Traj_Estimation](https://github.com/whuwuteng/LiDARHD_Traj_Estimation) at the root of the project (not public yet):
    ```bash
    cd Points2Prints
    git clone <git_path>
    cd LiDARHD_Traj_Estimation/
    pixi run build
    ```
4. Optionally, you may need to install [`roofer`](https://github.com/3DBAG/roofer) (documentation [there](https://innovation.3dbag.nl/roofer/getting_started.html)) and the [binary of `cjseq`](https://github.com/cityjson/cjseq).
