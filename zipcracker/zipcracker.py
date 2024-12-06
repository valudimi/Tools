"""
Crack a passworded .zip using a provided wordlist.
"""

import os
import sys
import zipfile

def zip_open(target: str, attributes: str='r'):
    """
    Create ZipFile object.
    """

    try:
        archive = zipfile.ZipFile(target, attributes)

    except FileNotFoundError as e:
        print(e)
        sys.exit()

    else:
        return archive

def crack(archive: zipfile, dictionary: str):
    """
    Run the wordlist attack on an available zipfile.
    """

    try:
        with open(dictionary, 'rb') as f:
            # If file exists, make 'extracted/' directory
            try:
                os.mkdir('extracted/')

            except FileExistsError:
                print('Directory already exists, extracting to it...')

            except PermissionError:
                print('Cannot create directory: lacking permissions. Exiting.')
                return None

            for line in f.readlines():
                try:
                    archive.extractall(pwd=line[:-1], path='extracted/')

                except RuntimeError:
                    continue

                except zipfile.BadZipFile:
                    continue

                else:
                    password = line[:-1]
                    print('Password extraction successful!\n\n' +
                        f'Password: {password.decode()}\n' +
                        f'Bytes: {password}')
                    return password

            print('Password not found in the wordlist.')
            return None

    except FileNotFoundError as e:
        print(e)
        sys.exit()

if __name__ == '__main__':
    print('Usage: "python3 zipcracker.py <zip file> <dictionary file>')

    try:
        zf = sys.argv[1]
    except IndexError:
        print('You need to provide a zip file as an argument!\n')
        sys.exit()
    else:
        zf = zip_open(zf)

    try:
        wordlist = sys.argv[2]
    except IndexError:
        print('You need to provide a dictionary file as an argument!\n')
        sys.exit()
    else:
        crack(zf, wordlist)
