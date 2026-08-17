{
  description = "Flake using pyproject.toml metadata";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
  inputs.pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";

  outputs =
    { self, nixpkgs, pyproject-nix, ... }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;

      project = pyproject-nix.lib.project.loadPyproject {
        projectRoot = self;
      };

    in
    {
      devShells = forAllSystems (system: let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3;
        arg = project.renderers.withPackages { inherit python; };
        pythonEnv = python.withPackages arg;
      in {
        default =
          pkgs.mkShell {
            packages = [ pythonEnv ];
          };
        });

      packages = forAllSystems (system: let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python3;
          attrs = project.renderers.buildPythonPackage { inherit python; };
        in {
          default = python.pkgs.buildPythonPackage attrs;
        }
      );
    };
}
