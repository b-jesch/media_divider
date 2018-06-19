<h1>Media Divider</h1>

This Python script frees Kodi media folders from unnecessary waste. This means:

- all empty folders are deleted
- all folders without media files are deleted
- all non-media files within the media folders and subfolders are deleted

<b>Media files are:</b>

- Files with extension Files ending in .MKV, .ISO, .MP4, .MPG, .MPEG, .MOV, .H264, .H265, .TS, .PDF, .FLAC, .WAV, .OGG, .MP3
- Files with filesize larger then 100MB

I would like to point out that if you use this script incorrectly, most of the movies, audio files and pictures can be deleted and are gone forever.

<b>Usage (e.g. LibreElec):</b>

    python default.py media=/storage/videos action=dry-run

<b>Params:</b>

    media:      <root folder> from where starts cleaning recursively
    action:     dry-run | execute

This is a 'dry run', i.e. only files that will be deleted are listed, or exceptions are displayed. Before you trigger the executive run, you absolutely have a look at the generated output on dry-run.<br>
If there are files/folders that you don't want to delete, there are several options:

- Complete folders including subfolders can be excluded by creating a (hidden) file named .donotdelete in the folder. The dot (.) in front of the .donotdelete is important!
- excluded file formats or directories can be permanently inserted in the script itself (line 4/5)
- additional excluded file types/formats can be added optionally to the call by parameter 'exclude'

Example (excluding files with extension NFO, IDX, PNG; naming is case-insensitive):

    python default.py media=/storage/videos action=dry-run exclude=".nfo .idx .png"
    
If the dry run was successful and there are no files that shouldn't be deleted in the generated list, you can do a 'hot' run. 
ATTENTION: Files will be deleted without asking you, in a following 2nd run also all empty directories!

    python default.py media=/storage/videos action=execute exclude=".nfo .idx .png"
    
After this run, there are only files in the media folders with the file extensions listed above (including the exclude files) or larger than 100 MB. This also applies to files in folders + subfolders that have a .donotdelete in the directory. Empty folders are disappeared.

It is completely useless to apply the script to the pictures folder, all jpg, jpeg, tif, png etc. are deleted then! Likewise, it makes also no sense to think 'bulk cleaning' is media =/storage. After that you are allowed to reinstall your system!

<b>I assume no liability, everyone must know what he does! Making a backup before is always useful!</b>
