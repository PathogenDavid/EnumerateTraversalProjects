# Enumerate `Microsoft.Build.Traversal` Projects

[![MIT Licensed](https://img.shields.io/github/license/infectedlibraries/clangsharp.pathogen?style=flat-square)](LICENSE.txt)
[![Sponsor](https://img.shields.io/badge/sponsor-%E2%9D%A4-lightgrey?logo=github&style=flat-square)](https://github.com/sponsors/PathogenDavid)

This project represents an experiment to enumerate all of the projects directly or indirectly referenced by a [Traversal](https://github.com/microsoft/MSBuildSdks/tree/master/src/Traversal) project. The idea is eventually to use this technique to generate solution files from a Traversal project purely from MSBuild properties and items.

## License

This project is licensed under the MIT License. [See the license file for details](LICENSE.txt).

Additionally, this project has some third-party dependencies. [See the third-party notice listing for details](THIRD-PARTY-NOTICES.md).

## How to run

You can build on test project or all of them. The `dirs.proj` in the root is simply a Traversal project that builds all of the test projects. If you don't build all of them, you'll get verifications failures.

To build, simply build the `Rebuild` target with with `dotnet` or `msbuild` as you normally would:

```shell
# With .NET CLI
dotnet build dirs.proj /Restore /Target:Rebuild

# With msbuild
msbuild dirs.proj /Restore /Target:Rebuild /Verbosity:Minimal
```

(Note: If you don't rebuild, you'll get an error about the traversal project listing file already existing. This is to protect against it unexpectedly being rewritten.)

After building, a `*.proj.Traversed.txt` file will be generated next to each traversal project with a list of projects it references (including ones it references transitively.) You can verify that all the projects were enumerated correctly by running `python Verify.py`

## Adding a test

A test must be contained within a folder at the root of the repository, and the traversal project must be named `dirs.proj`.

Additionally, for each traversal project (including the main test one and any others it might reference) you must create a file named `dirs.proj.Expected.txt` that lists the projects that should be enumerated, one on each line using `/` as a directory separator. It's recommended that this file be written by hand.

If your test doesn't support the .NET CLI (for example, your test involves `vcxproj` projects), you should add `<Import Project="$(DisableOnDotNetCli)" />` to the end of the file. (See [SingleCppProj](SingleCppProj/dirs.proj) for an example.)

## How it works

More details soon, but the heart of the experiment is the `EnumerateTraversedProjects` target in [`Directory.Build.targets`](Directory.Build.targets). It uses [MSBuild's ProjectReference guts](https://github.com/dotnet/msbuild/blob/aed5e7ed0b7e031d3e486c63b206902bf825b128/documentation/ProjectReference-Protocol.md) to determine what projects need to be built to build each project in the traversal project. One downside to this approach is it causes the transitive dependencies of the projects to be built whether you wanted them to or not.
