{
  description = "Flake using pyproject.toml metadata";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
  { self, nixpkgs, pyproject-nix, uv2nix, pyproject-build-systems, ... }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;

      workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };

      overlay = workspace.mkPyprojectOverlay {
        sourcePreference = "wheel";
      };

      editableOverlay = workspace.mkEditablePyprojectOverlay {
        root = "$REPO_ROOT";
      };

      pythonSets = forAllSystems (system: let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3;
      in 
        (pkgs.callPackage pyproject-nix.build.packages {
          inherit python;
        }).overrideScope
        (
          lib.composeManyExtensions [
            pyproject-build-systems.overlays.wheel
            overlay
          ]
        )
      );

    in
    {
      devShells = forAllSystems (system: let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonSet = pythonSets.${system}.overrideScope editableOverlay;
        virtualenv = pythonSet.mkVirtualEnv "horizont-dev-env" workspace.deps.all;
      in {
        default =
          pkgs.mkShell {
            packages = [ 
              virtualenv
              pkgs.uv
              pkgs.librewolf
            ];
            env = {
              UV_PYTHON = pkgs.python3.interpreter;
            };
            shellHook = ''
              unset PYTHONPATH
              export REPO_ROOT=$(readlink -f .)
              . ${virtualenv}/bin/activate
            '';
          };
        });

      packages = forAllSystems (system: {
        default = pythonSets.mkVirtualEnv "horizont-env" workspace.deps.default; 
      });
    };
}
