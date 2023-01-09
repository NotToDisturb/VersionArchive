# VersionArchive
A repository containing data for VALORANT versions.
You might also want to check out [VersionUtils](https://github.com/NotToDisturb/VersionUtils)

## Regarding the data
The version data has the following structure:

|**Attribute**      |Type |**Description**|
|-------------------|-----|---------------|
|`manifest`         |`str`|A hexadecimal string that identifies a patch|
|`branch`           |`str`|Either `release` or `pbe`|
|`version`          |`str`|The client version visible in-game|
|`release_timestamp`|`int`|An integer that represent the release time of the patch in milliseconds|

The full list can be found in the [`manifests.json`](/out/manifests.json) file.

## Credits
floxay [Go](https://github.com/floxay) <br>
PixelButts [Go](https://twitter.com/PixelButts)