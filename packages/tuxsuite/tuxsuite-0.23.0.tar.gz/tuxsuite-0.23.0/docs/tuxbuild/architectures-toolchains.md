# Architecture and Toolchain Matrix

The following combinations of architecture and toolchain are supported.

|               | arc | arm | arm64 | i386 | mips | parisc | powerpc | riscv | s390 | sh  | sparc | x86_64 |
| ------------- | --- | --- | ----- | ---- | ---- | ------ | ------- | ----- | ---- | --- | ----- | ------ |
| clang-10      | no  | yes | yes   | yes  | yes  | no     | yes     | yes   | yes  | no  | yes   | yes    |
| clang-11      | no  | yes | yes   | yes  | yes  | no     | yes     | yes   | yes  | no  | yes   | yes    |
| clang-nightly | no  | yes | yes   | yes  | yes  | no     | yes     | yes   | yes  | no  | yes   | yes    |
| gcc-10        | no  | yes | yes   | yes  | yes  | yes    | yes     | yes   | yes  | yes | yes   | yes    |
| gcc-8         | yes | yes | yes   | yes  | yes  | yes    | yes     | yes   | yes  | yes | yes   | yes    |
| gcc-9         | yes | yes | yes   | yes  | yes  | yes    | yes     | yes   | yes  | yes | yes   | yes    |

This can be retrieved programatically with the following command:

```
curl -s "https://api.tuxbuild.com/v1/supportmatrix"
```
