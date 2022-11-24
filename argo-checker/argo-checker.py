
import requests
from bs4 import BeautifulSoup
import sys
import argparse
import tempfile
import urllib.request
import shutil
import os
import re
import tarfile
import subprocess
import fileinput

messages_quiet = False

def inform_status(msg):
    if not messages_quiet:
        print(msg, file=sys.stderr)

def find_latest_tool_url():
    doi_link = 'https://doi.org/10.17882/45538'
    inform_status(f'Checking for latest tool at <{doi_link}>...')
    page = requests.get(doi_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    links = soup.find_all('a')
    link_vals = [l.attrs['href'] for l in links if 'href' in l.attrs]

    # these files are named sequentially, so newer version should
    # in theory have a filename with a bigger number in front
    file_re = re.compile(r'([0-9]+)\.tar\.gz$')
    tar_gz_vals = [l for l in link_vals if file_re.search(l)]
    which_max, val_max = None, float('-inf')
    for i, url in enumerate(tar_gz_vals):
        val = int(file_re.search(url).group(1))
        if val > val_max:
            which_max = i
            val_max = val

    if which_max is None:
        raise ValueError(f'Failed to find latest tool source.')
    
    inform_status(f'Latest tool source is located at <{tar_gz_vals[which_max]}>.')
    return tar_gz_vals[which_max]

def install_tool_from_url(url, dest):
    inform_status(f"Downloading tool from <{url}>")
    fd, tmp = tempfile.mkstemp()
    install_root = os.path.dirname(dest)

    try:
        with open(tmp, 'wb') as f:
            shutil.copyfileobj(urllib.request.urlopen(url), f)

        inform_status('Extracting...')
        with tarfile.open(tmp) as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, install_root)
    finally:
        os.close(fd)
        os.unlink(tmp)

    inform_status(f"Installing tool to '{dest}'")
    current_root = [d for d in os.listdir(install_root) if d.startswith('format_control')]
    if not current_root:
        raise ValueError(f"Can't find extracted files in '{install_root}'")
    elif len(current_root) > 1:
        raise ValueError(f"More than one possible value for extracted files in '{install_root}'")

    if os.path.exists(dest):
        inform_status('Removing previous installation')
        shutil.rmtree(dest)
    
    current_root = os.path.join(install_root, current_root[0])
    os.rename(current_root, dest)
    return dest

def argo_checker_find(update=False, force=False):
    dir_re = re.compile(r'tool_([0-9]+)')
    file_re = re.compile(r'([0-9]+)\.tar\.gz$')

    which_max, val_max = None, float('-inf')
    this_dir = os.path.abspath(os.path.dirname(__file__))
    inform_status(f"Searching for installed tool in '{this_dir}'")

    dirs = [d for d in os.listdir(this_dir) if dir_re.match(d)]
    for i, dirname in enumerate(dirs):
        val = int(dir_re.match(dirname).group(1))
        if val > val_max:
            which_max = i
            val_max = int(dir_re.match(dirname).group(1))
    
    if which_max is None:
        inform_status('Installed tool was not found.')
        tool_dir = None
    else:
        tool_dir = os.path.join(this_dir, dirs[which_max])
        inform_status(f"Installed tool found at '{tool_dir}'.")
    
    if update:
        inform_status('Checking for newer version, as requested...')
    
    if update or tool_dir is None:
        latest_url = find_latest_tool_url()
        latest_val = int(file_re.search(latest_url).group(1))
        latest_dest = os.path.join(this_dir, f'tool_{latest_val}')
        if tool_dir is None:
            inform_status('Installing latest version because no tool is installed')
            return install_tool_from_url(latest_url, latest_dest)
        elif latest_val > val_max:
            inform_status('Latest version is newer: upgrading...')
            return install_tool_from_url(latest_url, latest_dest)
        elif force:
            inform_status('Latest version is not newer but installing anyway (--force)')
            return install_tool_from_url(latest_url, latest_dest)
        else:
            inform_status('Version is latest version.')

    return tool_dir

def run_tool(tool_dir, files):
    if os.name == 'nt':
        classpath_sep = ';'
    else:
        classpath_sep = ':'
    
    class_paths_rel = ('./resources', './jar/formatcheckerClassic-1.17-jar-with-dependencies.jar')
    class_paths = classpath_sep.join(class_paths_rel)
    more_args = ['-Dapplication.properties=application.properties', '-Dfile.encoding=UTF8', 'oco.FormatControl']

    for file in files:
        tmp_fd, tmp = None, None
        try:
            if file.startswith('http://') or file.startswith('https://') or file.startswith('ftp://'):
                inform_status(f'Downloading <{file}>')
                tmp_fd, tmp = tempfile.mkstemp(suffix=os.path.basename(file))
                with open(tmp, 'wb') as f:
                    shutil.copyfileobj(urllib.request.urlopen(file), f)
                file = tmp
            
            file = os.path.abspath(file)
            all_args = ['java', '-cp', class_paths] + more_args + [file, ]
            command = ' '.join(all_args)
            inform_status(f"Running '{command}'")
            if subprocess.call(all_args, cwd=tool_dir) != 0:
                raise ValueError(f"Command '{command}' had a non-zero exit code.")
        finally:
            if tmp is not None:
                os.close(tmp_fd)
                os.unlink(tmp)

if __name__ == '__main__':
    description = """
    Run, serve, or upgrade the Ifremer
    NetCDF file format checker for Argo floats
    <https://doi.org/10.17882/45538>.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('action', type=str, nargs=1, choices=('check', 'serve'),
                        help="Use 'check' to export XML to stdout based on 'files' and 'serve' to serve a minimal web-based interface.")
    parser.add_argument('files_or_urls', type=str, nargs='*',
                        help="Zero or more files or URLs if 'action' is 'check'")
    parser.add_argument('--update', action='store_true',
                        help="Update to the latest distributed version of the tool before running 'action'")
    parser.add_argument('--force', action='store_true',
                        help="Reinstall even if tool is at latest version.")
    parser.add_argument('--quiet', action='store_true',
                        help="Suppress status messages.")

    args = parser.parse_args()

    if args.quiet:
        messages_quiet = True

    tool_dir = argo_checker_find(update=args.update, force=args.force)
    
    if args.action[0] == 'check':
        if args.files_or_urls:
            run_tool(tool_dir, args.files_or_urls)
        else:
            # read from stdin
            tmp_fd, tmp = None, None
            try:
                tmp_fd, tmp = tempfile.mkstemp(suffix='.nc')
                with open(tmp, 'wb') as f:
                    shutil.copyfileobj(sys.stdin.buffer, f)
                run_tool(tool_dir, [tmp])
            finally:
                if tmp is not None:
                    os.close(tmp_fd)
                    os.unlink(tmp)
    else:
        raise NotImplementedError(f"action '{args.action}' is not implemented")

    sys.exit(0)
