{
  description = "IHP SG13CMOS5L - 5-metal CMOS PDK with LibreLane RTL-to-GDS flow";

  nixConfig = {
    extra-substituters = [
      "https://openlane.cachix.org"
      "https://nix-cache.fossi-foundation.org"
    ];
    extra-trusted-public-keys = [
      "openlane.cachix.org-1:qqdwh+QMNGmZAuyeQJTH9ErW57OWSvdtuwfBKdS254E="
      "nix-cache.fossi-foundation.org:3+K59iFwXqKsL7BNu6Guy0v+uTlwsxYQxjspXzqLYQs="
    ];
  };

  inputs = {
    # LibreLane with IHP support
    librelane.url = "github:librelane/librelane/3.0.0.dev43";
    nixpkgs.follows = "librelane/nix-eda/nixpkgs";
  };

  outputs = { self, nixpkgs, librelane }:
    let
      nix-eda = librelane.inputs.nix-eda;
      devshell = librelane.inputs.devshell;
      lib = nixpkgs.lib;
    in {
      legacyPackages = nix-eda.forAllSystems (system:
        import nixpkgs {
          inherit system;
          overlays = [
            nix-eda.overlays.default
            devshell.overlays.default
            librelane.overlays.default
          ];
        }
      );

      packages = nix-eda.forAllSystems (system: let
        pkgs = self.legacyPackages.${system};
        basePackages = librelane.packages.${system};
      in basePackages // {
        default = basePackages.default;
      });

      devShells = nix-eda.forAllSystems (system: let
        pkgs = self.legacyPackages.${system};
      in {
        default = lib.callPackageWith pkgs (librelane.createOpenLaneShell {
          extra-packages = with pkgs; [
            gnumake
            gnugrep
            git
          ];
          extra-python-packages = with pkgs.python3.pkgs; [
            docopt
          ];
        }) {};
      });
    };
}
