import os
import sys

EXCLUDE_FOLDERS = ['VIDEO_TS', 'AUDIO_TS', 'BDMV', 'CERTIFICATE', 'SUBS']
EXCLUDE_FILE_EXT = ['.MKV', '.ISO', '.MP4', '.MPG', '.MPEG', '.MOV', '.H264', '.H265', '.TS',
                    '.PDF', '.FLAC', '.WAV', '.OGG', '.MP3']
MIN_FILESIZE = 100 * 1024 * 1024  # 100 MB
DONOTDELETE = '.donotdelete'

if __name__ == '__main__':
    params = dict()

    try:
        for args in sys.argv[1:]:
            key, value = args.split('=')
            params.update({key: value})
    except (IndexError, ValueError), e:
        print e.message
        exit(1)

    if not 'media' or not 'action' in params:
        print 'Run with options media=<media-start-folder> action=dry-run|execute exclude=".nfo .idx"'
        exit(1)
    if params['media'] == '' or not os.path.exists(params['media']):
        print 'Root folder couldn\'t execute, folder \'%s\' doesn\'t exists' % params['media']
        exit(1)
    if params['action'] == '' or params['action'] not in ('dry-run', 'execute'):
        print 'Unkown parameter for action'
        exit(1)
    if 'exclude' in params:
        for param in params['exclude'].split(): EXCLUDE_FILE_EXT.append(param.upper())
        print "excluding files with extension:"
        print EXCLUDE_FILE_EXT

    _dcount = 0
    _fcount = 0
    _dskipped = 0
    _fskipped = 0
    _dwiped = 0
    _fwiped = 0

    for root, dirs, files in os.walk(params['media']):
        dirs[:] = [d for d in dirs if d.upper() not in EXCLUDE_FOLDERS]
        bSkip = False
        if DONOTDELETE in files:
            print '[donotdelete] skip folder %s' % root
            _dskipped += 1
            bSkip = True
        if bSkip: continue
        _dcount += 1
        for filenames in files:
            _fcount +=1
            filepath = os.path.join(root, filenames)
            _f, _e = os.path.splitext(filepath)
            if _e.upper() not in EXCLUDE_FILE_EXT:
                if os.path.getsize(filepath) < MIN_FILESIZE:
                    if params['action'] == 'execute':
                        try:
                            os.remove(filepath)
                            print 'removed: %s' % filepath
                            _fwiped += 1
                        except OSError, e:
                            print 'ERROR: couldn\'t remove %s' % filepath
                            print str(e)

                    elif params['action'] == 'dry-run':
                        print '[dry run]: would removed: %s' % filepath
                        _fwiped += 1
                    else:
                        pass
                else:
                    print '[file size]: wouldn\'t remove because of filesize: %s' % filepath
                    _fskipped += 1
            else:
                _fskipped += 1

    if params['action'] == 'dry-run':
        print '%s files in %s directories proceed' % (_fcount, _dcount)
        print '%s directories and %s files will be skipped' % (_dskipped, _fskipped)
        print '%s empty directories (on first run) and %s files will be deleted' % (_dwiped, _fwiped)
    else:
        print '%s files in %s directories proceed' % (_fcount, _dcount)
        print '%s directories and %s files skipped' % (_dskipped, _fskipped)
        print '%s directories and %s files wiped out' % (_dwiped, _fwiped)

    _dwiped = 0

    if params['action'] == 'execute':
        print 'second run, remove empty folders resulted from first run...'
        for root, dirs, files in os.walk(params['media']):
            dirs[:] = [d for d in dirs if d.upper() not in EXCLUDE_FOLDERS]
            if len(dirs) is 0 and len(files) is 0:
                if os.path.normpath(root).split(os.path.sep)[-1] not in EXCLUDE_FOLDERS:
                    print 'delete empty directory: %s' % root
                    try:
                        os.rmdir(root)
                        _dwiped += 1
                    except OSError, e:
                        print 'ERROR: couldn\'t remove %s' % root
                        print str(e)
        print '%s empty folders removed' % _dwiped