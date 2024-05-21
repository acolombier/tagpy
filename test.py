import tagpy
import tagpy.id3v2

def get_cover(f):
    tag = None
    if isinstance(f, tagpy.FileRef):
        tag = f.tag()
        f = f.file()
    covers = []
    if hasattr(tag, "covers"):
        covers = tag.covers
    elif hasattr(f, "ID3v2Tag"):
        covers = [a for a in f.ID3v2Tag().frameList() if isinstance(a, tagpy.id3v2.AttachedPictureFrame)]

    if covers:
        cover = covers[0]
        fmt = tagpy.mp4.CoverArtFormats.Unknown
        if isinstance(cover, tagpy.mp4.CoverArt):
            return cover
        else:
            mime = cover.mimeType().lower().strip()
            if "image/jpeg":
                fmt = tagpy.mp4.CoverArtFormats.JPEG
            elif "image/png":
                fmt = tagpy.mp4.CoverArtFormats.PNG
            elif "image/bmp":
                fmt = tagpy.mp4.CoverArtFormats.BMP
            elif "image/gif":
                fmt = tagpy.mp4.CoverArtFormats.GIF
            return tagpy.mp4.CoverArt(fmt, cover.picture())
        return covers[0]

f1 = tagpy.FileRef('/tmp/calypso.mp3')
f2 = tagpy.FileRef('/tmp/EV_ThinkComplex.stem.mp4')
t1 = f1.tag()
t2 = f2.tag()
t2.title = t1.title
t2.artist = t1.artist
t2.album = t1.album
t2.comment = t1.comment
t2.genre = t1.genre
t2.year = t1.year
t2.track = t1.track
c = tagpy.mp4.CoverArtList()
c.append(get_cover(f1))
t2.covers = c

f2.save()