# VersionArchive
A repository containing data for VALORANT versions.
You might also want to check out [VersionUtils](https://github.com/NotToDisturb/VersionUtils).

## Regarding the data
The version data has the following structure:

|**Attribute**      |Type |**Description**|
|-------------------|-----|---------------|
|`manifest`         |`str`|A hexadecimal string that identifies a patch|
|`branch`           |`str`|Either `release` or `pbe`|
|`version`          |`str`|The client version visible in-game|
|`date`             |`int`|The date of the build|
|`upload_timestamp` |`int`|UNIX timestamp representing when Riot uploaded the version to their CDN|
|`release_timestamp`|`int`|UNIX timestamp representing when the version became available to players (`0` if data unavailable)|

The full list can be found in the [`manifests.json`](/out/manifests.json) file.

## Credits
floxay [Go](https://github.com/floxay) <br>
Shiick [Go](https://github.com/Shiick) <br>
PixelButts [Go](https://twitter.com/PixelButts)