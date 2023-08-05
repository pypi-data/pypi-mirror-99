# Make Targets

Make targets are optional positional arguments that can be provided to modify
what parts of the source tree are built.

These targets are not the same as targets in tree. Rather, they are TuxMake
pseudo targets.

By default, the `default` target is built, but one or more targets may be
specified to modify the default behavior.

Refer to [TuxMake documentation](https://docs.tuxmake.org/targets/) for the
full description of each target.

The following targets are supported:

- config
- debugkernel
- dtbs
- kernel
- modules
- xipkernel
- kselftest
- kselftest-merge
- cpupower
- perf

Additional targets will be enabled as needed.

## Examples

### `tuxsuite build`

Build config and modules (but not a kernel).

```
tuxsuite build \
--git-repo https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git \
--git-ref master \
--target-arch arm \
--toolchain clang-10 \
--kconfig tinyconfig \
config modules
```

## `tuxsuite build-set`

In order to pass make targets in build-set use the following syntax in
the build-set file (`./example.yaml`):

```
sets:
  - name: example
    builds:
      - target_arch: arm64
        toolchain: gcc-8
        kconfig: allnoconfig
        targets:
          - config
          - dtbs
```

Perform the build-set:

```sh
tuxsuite build-set \
--git-repo 'https://github.com/torvalds/linux.git' \
--git-ref master \
--tux-config example.yaml \
--set-name example
```
