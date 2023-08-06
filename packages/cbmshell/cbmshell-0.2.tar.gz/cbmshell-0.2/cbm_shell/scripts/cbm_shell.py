import argparse
import glob
import os.path
import shutil
import string
import sys

from pathlib import Path

import cbmcodecs  # noqa: F401
import cmd2
from cmd2.utils import basic_complete

from cbm_files import BASICFile, ProgramFile
from cbm_files.tokensets import token_set_names
from d64 import DiskImage

from cbm_shell.image_path import Drive, ImagePath
from cbm_shell.images import Images


def is_path(p):
    if isinstance(p, Path):
        return not p.is_dir()
    return not isinstance(p, Drive)


class CBMShell(cmd2.Cmd):
    def __init__(self):
        shortcuts = dict(cmd2.DEFAULT_SHORTCUTS)
        shortcuts.update({'$': 'directory'})
        super().__init__(shortcuts=shortcuts)
        self.prompt = '(cbm) '

        self.encoding = 'petscii-c64en-uc'
        self.add_settable(cmd2.Settable('encoding', str, 'Text encoding'))
        self.token_set = 'basic-v2'
        self.add_settable(cmd2.Settable('token_set', str, 'BASIC tokens'))

        self.images = Images()

    def expand_paths(self, files_in):
        ret = []
        for f in files_in:
            if ImagePath.is_image_path(f):
                # drive or path in an image
                drive, path_name = ImagePath.split(f, self.encoding)
                if path_name:
                    image = self.images[drive]
                    expanded = ImagePath.glob(drive, path_name, image)
                    if expanded:
                        ret += expanded
                    else:
                        ret.append(ImagePath(drive, image.path(path_name)))
                else:
                    # just a drive
                    ret.append(Drive(drive))
            else:
                # local filesystem path
                expanded = os.path.expanduser(f)
                globbed = glob.glob(expanded)
                if globbed:
                    ret += [Path(p) for p in globbed]
                else:
                    ret.append(Path(expanded))
        return ret

    def src_dest_pairs(self, paths_in, expand_drive=True):
        dest = paths_in[-1]

        if is_path(dest):
            if len(paths_in) != 2:
                # multiple sources
                self.perror("Destination '{!s}' is not a drive or directory".format(dest))
                return None

            src = paths_in[0]
            if not is_path(src):
                # source is a directory or drive
                self.perror("Source '{!s}' is not a path".format(src))
                return None
            return [(src, dest)]

        val = []
        if isinstance(dest, Path):
            # destination is a directory
            for src in paths_in[:-1]:
                if isinstance(src, Path):
                    if src.is_dir():
                        val += self.src_dest_pairs([p for p in src.iterdir() if p.is_file()]+[dest])
                    else:
                        val.append((src, dest / src.name))
                elif isinstance(src, Drive):
                    if expand_drive:
                        src_image = self.images[src]
                        val += self.src_dest_pairs(ImagePath.expand(src, b'', src_image)+[dest])
                    else:
                        val.append((src, dest))
                else:
                    # source is an image path
                    val.append((src, dest / Path(src.name(self.encoding))))
        else:
            # destination is a drive
            image = self.images[dest]
            for src in paths_in[:-1]:
                if isinstance(src, Path):
                    if src.is_dir():
                        val += self.src_dest_pairs([p for p in src.iterdir() if p.is_file()]+[dest])
                    else:
                        val.append((src, ImagePath(dest, image.path(src.name.encode(self.encoding)))))
                elif isinstance(src, Drive):
                    if expand_drive:
                        src_image = self.images[src]
                        val += self.src_dest_pairs(ImagePath.expand(src, b'', src_image)+[dest])
                    else:
                        val.append((src, dest))
                else:
                    # source is an image path
                    val.append((src, ImagePath(dest, image.path(src._path.name))))

        return val

    attach_parser = argparse.ArgumentParser()
    attach_parser.add_argument('--read-only', action='store_true', help="prevent modifications to image")
    attach_parser.add_argument('image', nargs='+', help="image file name")

    @cmd2.with_argparser(attach_parser)
    def do_attach(self, args):
        """Attach an image to a drive number"""
        mode = 'r' if args.read_only else 'w'
        for path in self.expand_paths(args.image):
            next_drive = self.images.get_free_drive()
            if next_drive is None:
                self.perror("All drives in use")
                return None

            self.images[next_drive] = DiskImage(path).open(mode)
            self.poutput("Attached {!s} to {}".format(path, next_drive))

    detach_parser = argparse.ArgumentParser()
    detach_parser.add_argument('drive', type=int, nargs='+', help="drive to detach")

    @cmd2.with_argparser(detach_parser)
    def do_detach(self, args):
        """Detach an image from a drive letter"""
        for drive in args.drive:
            if drive in self.images:
                image = self.images.pop(drive)
                image.close()
                self.poutput("Detached {!s}".format(image))
            else:
                self.perror("Invalid drive: {}". format(drive))

    def do_images(self, args):
        """Display the attached images"""
        if self.images:
            for d in self.images.all_drives():
                ro = 'RW' if self.images[d].writeable else 'RO'
                self.poutput("    {}  {}  {!s}".format(d, ro, self.images[d]))
        else:
            self.poutput("No attached images")

    dir_parser = argparse.ArgumentParser()
    dir_parser.add_argument('drive', nargs='*', help="drive or pattern to list")

    @cmd2.with_argparser(dir_parser)
    def do_directory(self, args):
        """Display directory of a drive"""
        if not args.drive:
            args.drive = [str(d) for d in self.images.all_drives()]

        first = True
        for d in args.drive:
            kwargs = {'encoding': self.encoding}
            if not d[0] in string.digits:
                self.perror("Invalid argument: "+d)
                continue

            kwargs['drive'] = int(d[0])
            if len(d) > 1:
                if d[1] != ':':
                    self.perror("Invalid argument: "+d)
                    continue
                pattern = d[2:].encode(self.encoding)
                if pattern:
                    kwargs['pattern'] = pattern

            if kwargs['drive'] in self.images:
                if first:
                    first = False
                else:
                    self.poutput('')
                for l in self.images[kwargs['drive']].directory(**kwargs):
                    self.poutput(l)
            else:
                self.perror("Invalid drive: {}".format(d))

    file_parser = argparse.ArgumentParser()
    file_parser.add_argument('file', nargs='+', help="file")

    @cmd2.with_argparser(file_parser)
    def do_file(self, args):
        """Display information about a file"""
        files = self.expand_paths(args.file)

        for f in files:
            if isinstance(f, ImagePath):
                extra = ""
                if f.file_type == 'PRG':
                    with f.open('rb') as fileh:
                        prg = ProgramFile(fileh, self.token_set, self.encoding)
                    if prg:
                        extra = ", start=${:04x}".format(prg.start_addr)
                elif f.file_type == 'REL':
                    extra += ", record={} bytes".format(f.record_len)
                self.poutput("{}: {}, size={} bytes{}".format(f.name(self.encoding), f.file_type, f.size_bytes, extra))
            elif isinstance(f, Drive):
                self.poutput("Skipping drive {:d}".format(f))
            else:
                if f.is_file():
                    with f.open('rb') as fileh:
                        prg = ProgramFile(fileh, self.token_set, self.encoding)
                    self.poutput("{!s}: start=${:04x}".format(f, prg.start_addr))
                else:
                    self.poutput("Skipping non-file path {!s}".format(f))

    list_parser = argparse.ArgumentParser()
    list_parser.add_argument('file', nargs='+', help="BASIC program file")

    @cmd2.with_argparser(list_parser)
    def do_list(self, args):
        """List contents of a BASIC file"""
        files = self.expand_paths(args.file)

        if len(files) > 1:
            # output to file
            if not isinstance(files[-1], Path):
                self.perror("Cannot write listing to image path {!s}".format(files[-1]))
                return None

            path_pairs = self.src_dest_pairs(files, expand_drive=False)

            for src, dest in path_pairs:
                if src.exists():
                    with src.open('rb') as fileh:
                        prg = ProgramFile(fileh, self.token_set, self.encoding)
                    with dest.open('w') as fileh:
                        for line in prg.to_text():
                            print(line, file=fileh)
                else:
                    self.perror("File not found, {!s}".format(src))
        else:
            # output to stdout
            for f in files:
                if is_path(f):
                    if f.exists():
                        with f.open('rb') as fileh:
                            prg = ProgramFile(fileh, self.token_set, self.encoding)
                        for line in prg.to_text():
                            self.poutput(line)
                    else:
                        self.perror("File not found, {!s}".format(f))
                else:
                    self.poutput("Skipping non-file path {!s}".format(f))

    def hex_int(v):
        return int(v, 0)

    unlist_parser = argparse.ArgumentParser()
    unlist_parser.add_argument('--start', dest='start_addr', type=hex_int, default=0x1201, help="Program start address")
    unlist_parser.add_argument('file', nargs=(2,), help="file source or destination")

    @cmd2.with_argparser(unlist_parser)
    def do_unlist(self, args):
        """Convert text file to BASIC"""
        files = self.expand_paths(args.file)
        path_pairs = self.src_dest_pairs(files)

        for src, dest in path_pairs:
            self.poutput("Writing {!s} to {!s}".format(src, dest))
            prog = BASICFile(None, start_addr=args.start_addr)
            with src.open('r') as in_file:
                prog.from_text(in_file)
            kwargs = {}
            if isinstance(dest, ImagePath):
                kwargs['ftype'] = 'PRG'
            with dest.open('wb', **kwargs) as out_file:
                for line in prog.to_binary():
                    out_file.write(line)

    copy_parser = argparse.ArgumentParser()
    copy_parser.add_argument('--type', dest='file_type', help="DOS file type")
    copy_parser.add_argument('file', nargs=(2,), help="file source or destination")

    @cmd2.with_argparser(copy_parser)
    def do_copy(self, args):
        """Copy files between images"""
        files = self.expand_paths(args.file)
        path_pairs = self.src_dest_pairs(files)

        for src, dest in path_pairs:
            kwargs = {}
            ftype = args.file_type
            if isinstance(dest, ImagePath):
                if isinstance(src, ImagePath) and ftype is None:
                    ftype = src.file_type
                kwargs['ftype'] = ftype
                if ftype == 'REL':
                    kwargs['record_len'] = src.record_len
            self.poutput("Copying {!s} to {!s}".format(src, dest))
            with src.open('rb') as in_file:
                with dest.open('wb', **kwargs) as out_file:
                    shutil.copyfileobj(in_file, out_file)

    delete_parser = argparse.ArgumentParser()
    delete_parser.add_argument('file', nargs='+', help="file to delete")

    @cmd2.with_argparser(delete_parser)
    def do_delete(self, args):
        """Delete files"""
        files = self.expand_paths(args.file)

        for path in files:
            if is_path(path):
                self.poutput("Deleting {!s}".format(path))
                path.unlink()
            else:
                self.poutput("Skipping {!s}".format(path))

    def do_token_set(self, args):
        """List supported BASIC token sets"""
        for name in token_set_names():
            if not name.startswith('escape-'):
                self.poutput(name)

    complete_attach = cmd2.Cmd.path_complete

    def image_path_complete(self, text, line, begidx, endidx):
        if ImagePath.is_image_path(text):
            try:
                drive, name = ImagePath.split(text, self.encoding)
                all_paths = ImagePath.expand(drive, name, self.images[drive])
                choices = ["{}:{!s}".format(drive, p.name(self.encoding)) for p in all_paths]
                return basic_complete(text, line, begidx, endidx, choices)
            except (KeyError, UnicodeEncodeError):
                pass
        return self.path_complete(text, line, begidx, endidx)
    complete_file = image_path_complete
    complete_list = image_path_complete
    complete_unlist = image_path_complete
    complete_copy = image_path_complete
    complete_delete = image_path_complete


def main():
    c = CBMShell()
    ret = c.cmdloop()

    # close any attached images
    c.images.cleanup()

    sys.exit(ret)
