"""
indi game engine \n
apprication utilities
"""
import igeCore as core
import igeVmath as vmath
import os.path


def makeDirectories(dir):
    """
    Make local directory recursive
    :param dir: file path to make directory
    :return: None
    """
    path = os.path.normpath(dir)

    list = []
    while os.path.exists(path)==False:
        if path == '':
            break
        path,tail = os.path.split(path)
        if tail =='' and tail.find('.') != -1:
            list.append(path)
            break
        else:
            list.append(tail)

    i =len(list)-1
    while i >= 0:
        name, ext = os.path.splitext(list[i])
        if ext != '':
            path = os.path.join(path, list[i])
            path = os.path.normpath(path)
            break
        else:
            path = os.path.join(path, list[i])
            path = os.path.normpath(path)
            os.mkdir(path)
        i-=1


def platformName(platform):
    """
    Return the name corresponding to the platform type

    :param platform: core.TARGET_PLATFORM_XX
    :return: string
    """
    if platform == core.TARGET_PLATFORM_PC:
        return 'pc'
    if platform == core.TARGET_PLATFORM_IOS:
        return 'ios'
    if platform == core.TARGET_PLATFORM_ANDROID:
        return 'android'
    return 'unknown'

def targetFolderName(platform):
    if platform == core.TARGET_PLATFORM_PC:
        return 'pc'
    return 'mobile'
