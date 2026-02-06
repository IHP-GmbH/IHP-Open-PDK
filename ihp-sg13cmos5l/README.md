# IHP SG13CMOS5L PDK (M1-M4-TM1 stack)
> [!WARNING]
> This repo is meant to be used **only** as a temporary storage during the development of the `build/compile` migration script for the sg13 cmos5l PDK.

## How to use it during development stage
```bash
git clone --branch dev --recurse-submodules https://github.com/IHP-GmbH/IHP-Open-PDK.git
cd IHP-Open-PDK
git clone https://github.com/IHP-GmbH/ihp-sg13cmos5l.git
```
You're done! Now return to your working directory and switch between PDKs changing the `$PDK` env variable.
Note: for general configuration settings go to the IHP-Open-PDK [documentation](https://ihp-open-pdk-docs.readthedocs.io/en/latest).
