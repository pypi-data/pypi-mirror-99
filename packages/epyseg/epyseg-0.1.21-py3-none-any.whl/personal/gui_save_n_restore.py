# ok for now as long as all names are unique --> check

# now I can easily try to reload them

# need start to edit all buttons or edits with smart names

# https://docs.python.org/3/library/configparser.html
# TODO check object name is unique...
# maybe store by panel --> see how I can do that in a smart way --> maybe pass in the tab name and if so pass it
# maybe can also use it as a macro and tell which buttons need be pressed to move on to next step --> press go then continue setting the rest of the parameters except if fails... --> TODO try that

# TODO store init settings in the same way and store settings for predict, train or model, etc... maybe also store if model as used for retrain or for predict so that I can reload more smartly the thing...
# see how to do the reload as it's not so easy... because model need be loaded before I can move to other things --> maybe need some sort of lock --> think about it

# https://stackoverflow.com/questions/23279125/python-pyqt4-functions-to-save-and-restore-ui-widget-values

import configparser
import sys
from PyQt5.QtWidgets import QSpinBox, QComboBox, QApplication, QLineEdit, QRadioButton, QLabel, QCheckBox, \
    QGroupBox, QDoubleSpinBox, QTabWidget
from PyQt5 import QtCore, QtGui

from epyseg.epygui import EPySeg
from epyseg.gui.img import image_input_settings
from epyseg.postprocess.gui import PostProcessGUI
# logging
from epyseg.tools.logger import TA_logger

logger = TA_logger()


# this is how to assign a name:
# --> can greatly simplify my code I love it...

# button1.setObjectName('button1')
# or button1 = QPushButton('button caption', objectName='button1')
# or button1 = QPushButton('button caption', objectName='button1')
# button1 = QPushButton(text='button caption', objectName='button1', icon=icon1)
# same is True for connecting a method:
# button1 = QPushButton(text='button caption', objectName='button1', clicked=someMethod)
# button1.clicked.connect(someMethod)

# PROBABLY THIS CONFIGPARSER IS WHAT I WANT... TODO store a version in this so that I can handle big changes in a smooth way...
# maybe store properties as ways to set the tool --> indeed a good idea, then I need also save the files somewhere on the disk which is doable like for the images and other files such as md but then I need edit things

# example file
# [DEFAULT]
# ServerAliveInterval = 45
# Compression = yes
# CompressionLevel = 9
# ForwardX11 = yes
#
# [bitbucket.org]
# User = hg
#
# [topsecret.server.com]
# Port = 50022
# ForwardX11 = no
# https://docs.python.org/3/library/configparser.html --> how to read it and play with it...

# [Simple Values]
# key=value
# spaces in keys=allowed
# spaces in values=allowed as well
# spaces around the delimiter = obviously
# you can also use : to delimit keys from values
#
# [All Values Are Strings]
# values like this: 1000000
# or this: 3.14159265359
# are they treated as numbers? : no
# integers, floats and booleans are held as: strings
# can use the API to get converted values directly: true
#
# [Multiline Values]
# chorus: I'm a lumberjack, and I'm okay
#     I sleep all night and I work all day
#
# [No Values]
# key_without_value
# empty string value here =
#
# [You can use comments]
# # like this
# ; or this
#
# # By default only in an empty line.
# # Inline comments can be harmful because they prevent users
# # from using the delimiting characters as parts of values.
# # That being said, this can be customized.
#
#     [Sections Can Be Indented]
#         can_values_be_as_well = True
#         does_that_mean_anything_special = False
#         purpose = formatting for readability
#         multiline_values = are
#             handled just fine as
#             long as they are indented
#             deeper than the first line
#             of a value
#         # Did I mention we can indent comments, too?
# also would need to clean my code but in the end would be much simpler I think

# in fact that is really easy to do and also would need
def write_config_file():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'ServerAliveInterval': '45', 'Compression': 'yes', 'CompressionLevel': '9'}
    config['bitbucket.org'] = {}
    config['bitbucket.org']['User'] = 'hg'
    config['topsecret.server.com'] = {}
    topsecret = config['topsecret.server.com']
    topsecret['Port'] = '50022'  # mutates the parser
    topsecret['ForwardX11'] = 'no'  # same here
    config['DEFAULT']['ForwardX11'] = 'yes'
    with open('example.ini', 'w') as configfile:
        config.write(configfile)


def acces_config_file():
    config = configparser.ConfigParser()
    config.sections()
    config.read('example.ini')
    # ['example.ini']
    config.sections()
    # ['bitbucket.org', 'topsecret.server.com']
    'bitbucket.org' in config
    # True
    'bytebong.com' in config
    # False
    config['bitbucket.org']['User']
    # 'hg'
    config['DEFAULT']['Compression']
    # 'yes'
    topsecret = config['topsecret.server.com']
    topsecret['ForwardX11']
    # 'no'
    topsecret['Port']
    # '50022'
    for key in config['bitbucket.org']:
        # ...
        print(key)
    # user
    # compressionlevel
    # serveraliveinterval
    # compression
    # forwardx11
    config['bitbucket.org']['ForwardX11']
    # 'yes'
    topsecret.getboolean('ForwardX11')
    # False
    config['bitbucket.org'].getboolean('ForwardX11')
    # True
    config.getboolean('bitbucket.org', 'Compression')
    # True
    int(topsecret['Port'])
    # 50022
    float(topsecret['CompressionLevel'])
    # 9.0
    topsecret.get('Port')
    # '50022'
    topsecret.get('CompressionLevel')
    # '9'
    topsecret.get('Cipher')
    topsecret.get('Cipher', '3des-cbc')
    # '3des-cbc'
    config.get('bitbucket.org', 'monster', fallback='No such things as monsters')
    # 'No such things as monsters'


# pas mal en fait... --> je dois pouvoir faire ce que je veux avec ça...
'''
[Simple Values]
key=value
spaces in keys=allowed
spaces in values=allowed as well
spaces around the delimiter = obviously
you can also use : to delimit keys from values

[All Values Are Strings]
values like this: 1000000
or this: 3.14159265359
are they treated as numbers? : no
integers, floats and booleans are held as: strings
can use the API to get converted values directly: true

[Multiline Values]
chorus: I'm a lumberjack, and I'm okay
    I sleep all night and I work all day

[No Values]
key_without_value
empty string value here =

[You can use comments]
# like this
; or this

# By default only in an empty line.
# Inline comments can be harmful because they prevent users
# from using the delimiting characters as parts of values.
# That being said, this can be customized.

    [Sections Can Be Indented]
        can_values_be_as_well = True
        does_that_mean_anything_special = False
        purpose = formatting for readability
        multiline_values = are
            handled just fine as
            long as they are indented
            deeper than the first line
            of a value
        # Did I mention we can indent comments, too?
'''


# TODO try store ROIs too inside the file if possible... --> TODO...


# everything seems ol and in the proper order --> check how I can use that ??? for storing settings inside a category... --> TODO
# not bad I think though --> can I get parent
# TODO try fill in the settings somewhere

def guisave(ui, config):  # , name='DEFAULT'

    # for child in ui.children():  # works like getmembers, but because it traverses the hierarachy, you would have to call guisave recursively to traverse down the tree

    # ça ne marche pas, ça récupère que les fonctions de mon dialog
    # much better this is what I want in fact and need do this recursively whenever I enter a new container...

    # first need check if end object and if so return otherwhise keep on browsing...
    # check if stuff is enabled otherwise skip

    # TODO also get my own objects and put them on top then go for simpler objects --> very good idea

    # would be an easy way to load different model with preconfigured things --> a good idea can maybe also ask for folders or things alike or even functions so that I can ask for folders or parameters ofr training different models such as seg model and denoise model --> TODO...
    # try:
    #     if not ui.isEnabled(): # or do things with that too... --> think about it...
    #         return
    # except:
    #     pass

    # if layout need browse children ...

    # it is duplicated because the object is two time in the stuff --> make each instance unique... --> add a master identifier to avoid issues

    # this is for debug but is really important to avoid issues

    # so now I could save predict and or train databases and reload them
    # see if list can be reloaded
    if ui.objectName() in config['DEFAULT']:
        logger.error('duplicate entry ' + str(ui.objectName()))

        # several are duplicated --> need remove those

    if isinstance(ui, QLabel):
        # nothing to do --> just return
        return

    # otherwise store all in default but just make sure names are unique --> easy to check with an entry

    # there is a bug cause scanned twice
    if isinstance(ui, QTabWidget):
        print('QTabWidget', ui.currentIndex(), ui.tabText(ui.currentIndex()))
        # config['DEFAULT'].update({ui.tabText(ui.currentIndex()):str(ui.currentIndex())})
        # config['DEFAULT'].update({ui.objectName(): str(ui.tabText(ui.currentIndex()))})

        # bug here this thing is undefined and is not the right config --> should pass the parent only not something lower level... --> bug
        # try:
        #     config[ui.objectName()]= str(ui.tabText(ui.currentIndex()))# vraiment pas mal --> maintenant ça va aller très vite...
        # except:
        #     config['DEFAULT'].update({ui.objectName(): str(ui.tabText(ui.currentIndex()))})

        # orig config
        # loop over all tabs of a tab widget
        for iii in range(ui.count()):
            wg = ui.widget(iii)
            print('further ', ui.tabText(iii))

            # how can I change config here config[ui.tabText(iii)]

            # init a new section

            # browse_further(wg, config, name=str(ui.tabText(iii))) # change the config file
            strg = str(ui.tabText(iii))
            # print('strg', strg)
            # print(config)
            # print(config.sections())

            # is it an original config ????

            # config[strg] = {}
            # config[strg]=strg
            # out = config[strg]
            # out = config
            browse_further(wg, config)  # change the config file

        # maybe should browse all of its progeny too otherwise will stall...

        return

    if isinstance(ui, QLineEdit):
        if not ui.objectName():
            print("error", ui)
            return
        print('lineedit', ui.text(), ui.objectName())
        # try:
        #     config.update({ui.objectName(): str(ui.text())})
        # except:
        config['DEFAULT'].update({ui.objectName(): str(ui.text())})
        return

    if isinstance(ui, QDoubleSpinBox):
        if not ui.objectName():
            print("error", ui)
            return
            # config['DEFAULT'].update({'double spin': str(ui.value())})
        print('double spin', ui.value(), ui.objectName())
        # try:
        #     config.update({ui.objectName(): str(ui.text())})
        # except:

        config['DEFAULT'].update({ui.objectName(): str(ui.value())})
        return

    if isinstance(ui, QSpinBox):
        if not ui.objectName():
            print("error", ui)
            return
        print('spin', ui.value(), ui.objectName())
        # try:
        #     # config[ui.objectName()] = str(ui.value())# ça marche au top --> fix all
        #     config.update({ui.objectName(): str(ui.text())})
        # except:
        config['DEFAULT'].update({ui.objectName(): str(ui.value())})  # ça marche au top --> fix all
        return

    if isinstance(ui, QGroupBox):
        if not ui.objectName():
            print("error", ui)
            return
        print('groupbox', ui.title(), ui.isChecked(), ui.objectName())
        # try:
        #     config.update({ui.objectName(): str(ui.text())})
        # except:
        config['DEFAULT'].update({ui.objectName(): str(ui.isChecked())})
        # need browse further
        browse_further(ui, config)
        return

    if isinstance(ui, QLineEdit):
        if not ui.objectName():
            print("error", ui)
            return
        print('lineedit', ui.text(), ui.objectName())
        # try:
        #     config.update({ui.objectName(): str(ui.text())})
        # except:
        config['DEFAULT'].update({ui.objectName(): str(ui.text())})
        # print(ui.title())
        return

    if isinstance(ui, QComboBox):
        if not ui.objectName():
            print("error", ui)
            return
        print('QComboBox', ui.currentText(), ui.isEnabled(), ui.objectName())

        # try:
        #     config.update({ui.objectName(): str(ui.text())})
        # except:
        config['DEFAULT'].update({ui.objectName(): str(ui.currentText())})

        # also store if enabled or not maybe and if visible ...
        # or best is to ignore the value if disabled --> we don't set it ??? think about it cause not sure...
        return

    if isinstance(ui, QCheckBox):
        if not ui.objectName():
            print("error", ui)
            return
        print('QCheckBox', ui.text(), ui.isChecked(), ui.objectName())
        # try:
        #     config.update({ui.objectName(): str(ui.text())})
        # except:
        config['DEFAULT'].update({ui.objectName(): str(ui.isChecked())})
        # print(ui.title())
        return

    if isinstance(ui, QRadioButton):
        if not ui.objectName():
            print("error", ui)
            return
        print('QRadioButton', ui.text(), ui.isChecked(), ui.objectName())
        # try:
        #     config.update({ui.objectName(): str(ui.text())})
        # except:
        config['DEFAULT'].update({ui.objectName(): str(ui.isChecked())})
        # TODO see how to get the checked one --> should work
        return

    # if isinstance(ui, QWidget):
    #     # guisave(ui, settings)
    #     return

    # what else do I need ???

    # only save things that can be saved...

    for child in ui.children():
        # print(child)
        # print(child.objectName()) # --> object has no name maybe I should give a name to all objects that need be saved so that I prevent false assignment and restore only what need be restored
        # ça ça marche mais pb si je change le texte # could also do it like that

        guisave(child, config)  # , name=name # add parent to settings
    # if has child go recursively in it

    # browse childs recursively

    # maybe not always browse inside depending on type --> see how I can do that maybe return whether useful to browse in it or not

    # for name, obj in inspect.getmembers(ui):
    #     # print(name)
    #     if isinstance(obj, QComboBox):
    #         name   = obj.objectName()      # get combobox name
    #         index  = obj.currentIndex()    # get current index from combobox
    #         text   = obj.itemText(index)   # get the text for current index
    #         settings.setValue(name, text)   # save combobox selection to registry
    #
    #     if isinstance(obj, QLineEdit):
    #         name = obj.objectName()
    #         value = obj.text()
    #         settings.setValue(name, value)    # save ui values, so they can be restored next time
    #
    #     if isinstance(obj, QCheckBox):
    #         name = obj.objectName()
    #         state = obj.checkState()
    #         settings.setValue(name, state)


# see how to store data --> best is tpo store type in name --> auto_mode_bool auto_threshold_int or just get it by value --> if value is True then has to be a checkable stuff --> think about that and do try and log stuff


# , name='DEFAULT'
def browse_further(child, config):
    inner_childs = child.children()
    if inner_childs:
        for grandson in inner_childs:
            # maybe ignore some of the childs
            guisave(grandson, config)


def guirestore(ui, config):
    # TODO just duplicate and edit the other file, the one with the other guisave to allow it to restore instead of save
    # hack first the IMG GUI to see if I can recover everything
    # can I implement a parser of text to automatically edit

    # look for object with a name in the settings and try to load it... --> TODO very good idea

    # best is to loop over childs again and see if a parameter for it is present in the

    # for name, obj in inspect.getmembers(ui):
    #     if isinstance(obj, QComboBox):
    #         index  = obj.currentIndex()    # get current region from combobox
    #         #text   = obj.itemText(index)   # get the text for new selected index
    #         name   = obj.objectName()
    #
    #
    #         # value = unicode(settings.value(name))
    #         value = (config.value(name))
    #
    #         if value == "":
    #             continue
    #
    #         index = obj.findText(value)   # get the corresponding index for specified string in combobox
    #
    #         if index == -1:  # add to list if not found
    #             obj.insertItems(0,[value])
    #             index = obj.findText(value)
    #             obj.setCurrentIndex(index)
    #         else:
    #             obj.setCurrentIndex(index)   # preselect a combobox value by index
    #
    #     if isinstance(obj, QLineEdit):
    #         name = obj.objectName()
    #         # value = unicode(settings.value(name))  # get stored value from registry
    #         value = (config.value(name))  # get stored value from registry
    #         obj.setText(value)  # restore lineEditFile
    #
    #     if isinstance(obj, QCheckBox):
    #         name = obj.objectName()
    #         value = config.value(name)   # get stored value from registry
    #         if value != None:
    #             obj.setCheckState(value)   # restore checkbox

    # if isinstance(obj, QRadioButton):
    pass


if __name__ == "__main__":
    # write_config_file()

    app = QApplication(sys.argv)
    # dialog = PostProcessGUI(parent_window=None)

    # dialog = image_input_settings(parent_window=None,
    #                                                         show_normalization=True,
    #                                                         show_preview=True,
    #                                                         show_predict_output=True,
    #                                                         show_overlap=True, show_input=True,
    #                                                         show_output=True,
    #                                                         show_preprocessing=True,
    #                                                         show_tiling=True,
    #                                                         show_channel_nb_change_rules=True,
    #                                                         show_HQ_settings=True,
    #                                                         show_run_post_process=True,
    #                                                         allow_bg_subtraction=True)
    #
    # result = dialog.exec_()

    if True:
        dialog = EPySeg()
        dialog.show()

        config = configparser.ConfigParser()
        # config =config['DEFAULT']
        config['DEFAULT'] = {'EPySeg': 'v0.1'}
        guisave(dialog, config)
        with open('example.ini', 'w') as configfile:
            config.write(configfile)
        sys.exit(app.exec_())

    # settings = QtCore.QSettings('IBDM', 'EPySeg')

    config = configparser.ConfigParser()
    guisave(dialog, config)

    print(config)
    print(config.sections())
    with open('example.ini', 'w') as configfile:
        config.write(configfile)

    # print(settings.allKeys())

    # parameters, ok = PostProcessGUI.getDataAndParameters(parent_window=None)
    # print(parameters, ok)

    sys.exit(0)
