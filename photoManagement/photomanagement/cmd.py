import argparse

parser = argparse.ArgumentParser(
                    prog='PhotoManagement',
                    description=
                        '''
                        This program allows the user to store and manage photos in a library.
                        The program generates a description of each image and allows the user to listen to the description.
                        The program notifies the user of duplicate images and allows filters to be applied to the image.
                        '''
                    )
parser.add_argument("-d", action="store", nargs=1)