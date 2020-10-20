# musicly

A Cli tool to play and download music

Disclamer:  Mac OS Only

# Usage

```
./musicly play "<Song Name>"
./musicly download "<Song Name>"
```
  
Playlists:

You can create playlists using specfiles, just create a file ending with .spec and put song titles in the file
Then use:
```
./musicly playlist gen <Path to your spec file>
```
To download the songs and generate a playlist.info file, then to play your playlist use:
```
./musicly playlist play <Path to the playlist folder> [options]
 ```
 
 options:
 --shuffle: shuffles the playlist
 
 --volume=x: sets volume to whatever x is (between 0 to 1)
