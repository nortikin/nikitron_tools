#!/usr/bin/python3
# -*- coding: utf-8 -*-
# AUTHOR:	   (c) Nikitron
# NAME:		   get_subfolders_files
# DESCRIPTION:     GUI скрипт для Caja, достать файлы из под-папок
# REQUIRES:	   python3, python-gtk3
# LICENSE:	   GNU GPL v3 (http://www.gnu.org/licenses/gpl.html)
# WEBSITE:	   https://nikitron.cc.ua
# ICON_USED:       /usr/share/icons/gnome-colors-common/16x16/actions/media-eject.png


import os
import os.path as path
import shutil

#import pygtk
#pygtk.require('2.0')
#import gtk


class USBsGUI:


        def delete_event(self, widget, event, data=None):
                return False


        def destroy(self, widget, data=None):
                gtk.main_quit()
       
        def get_active_text(self, combobox):
                model = combobox.get_model()
                active = combobox.get_active()
                if active < 0:
                        return None
                return model[active][0]
       
        def get_devices_list(self):
                model=self.seats_treeview.get_model()
                seats_usbs_list=[]
                n=0
                for seat_iter in self.iter_seats_list:
                        if model.iter_has_child(seat_iter):
                                usb_iter=model.iter_children(seat_iter)
                        else:
                                usb_iter=None
                        seats_usbs_list.append([])
                        x=0
                        while usb_iter!=None:
                                seats_usbs_list[n].append(str(model[usb_iter][0]))
                                x+=1
                                usb_iter=model.iter_next(usb_iter)
                        n+=1
                return seats_usbs_list


        def umount_callback(self, widget, data=None):
                (model_usb, iter_usb) = self.ubs_treeview.get_selection().get_selected()
                usb=model_usb.get_value(iter_usb,0)
                #print usb
                try:
                        unmount_and_detach(usb)
                except:
                        md = gtk.MessageDialog(self.window, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,  gtk.BUTTONS_CLOSE, "Сбой: Невозможно извлечь устройство")
                        md.run()
                        md.destroy()
                self.reload_callback(widget)
       
        def reload_callback(self, widget, data=None):
                model=self.ubs_treeview.get_model()
                iters=[]
                itera=model.get_iter_first()
                while itera!=None:
                        iters.append(itera)
                        itera=model.iter_next(itera)
                for itera in iters:
                        path = model.get_path(itera)
                        model.remove(itera)
                        model.row_deleted(path)
                for usb in usb_list():
                        model.append(None, usb)
       
        def init_treeview(self, labels):
                treestore = gtk.TreeStore(str, str)
                # create the TreeView using treestore
                treeview = gtk.TreeView(treestore)
                n=0
                for label in labels:
                        if label!=None:
                                # create the TreeViewColumn to display the data
                                tvcolumn = gtk.TreeViewColumn(label)
                                # add tvcolumn to treeview
                                treeview.append_column(tvcolumn)
                                # create a CellRendererText to render the data
                                cell = gtk.CellRendererText()
                                # add the cell to the tvcolumn and allow it to expand
                                tvcolumn.pack_start(cell, True)
                                # set the cell "text" attribute to column n - retrieve text
                                # from that column in treestore
                                tvcolumn.add_attribute(cell, 'text', n)
                        n+=1
                # make it searchable
                treeview.set_search_column(0)
                # Allow sorting on the column
                tvcolumn.set_sort_column_id(0)
                treeview.get_selection().set_mode(gtk.SELECTION_SINGLE)
                return treeview
       
        def init_gui_area(self):
                # create the TreeView using treestore
                self.ubs_treeview = self.init_treeview([None, 'Mount point'])
               
                #self.scrolled_window=self.init_usb_list_gui()
                vbox=gtk.VBox()
                hbox=gtk.HBox()
                vbox.pack_start(hbox, True, True)
                vbox1=gtk.VBox()
               
                hbox.pack_start(vbox1, True, True)
               
                scrolled_window = gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
                scrolled_window.add_with_viewport(self.ubs_treeview)
                scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
                scrolled_window.show()
                vbox1.pack_start(scrolled_window, True, True)
               
                remove_button=gtk.Button(stock=gtk.STOCK_REMOVE)
                remove_button.connect("clicked", self.umount_callback, None)
                vbox1.pack_start(remove_button, False, False)
                remove_button.show()
               
                refresh_button=gtk.Button(stock=gtk.STOCK_REFRESH)
                refresh_button.connect("clicked", self.reload_callback, None)
                vbox1.pack_start(refresh_button, False, False)
                refresh_button.show()
                refresh_button.connect("clicked", self.reload_callback, None)
               
                hbox.show_all()
                vbox1.show_all()
                vbox.show_all()
               
                return vbox


        def __init__(self):
                pass
       
        def init_window(self):
                # create a new window
                self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
                self.window.connect("delete_event", self.delete_event)
                self.window.connect("destroy", self.destroy)
                self.window.set_border_width(10)
                self.window.add(self.init_gui_area())
                # and the window
                self.window.resize(300,300)
                self.window.show()
                self.reload_callback(None)


        def main(self):
                gtk.main()

'''
Destination:
get files from subfolders to curent folder
Author:
Nikitron
Usage:
#python3 get_subfolders_files.py
'''

cd = path.abspath('.')
rmrf = os.removedirs
rem = []

for i in os.walk(cd):
    for f in i[2]:
        if f in os.listdir('.'):
           f2 = 'повтор_'+f
        else:
           f2 = f
        shutil.move(path.join(path.abspath(i[0]),f),path.join(cd,f2))
    if not i[1]:
        # remove folders, but need check for existing files inside
        rem = i[0]
#for i in rem:
#    rmrf(i)
print('done \n')

#if __name__ == "__main__":
#        gui = FilesGUI()
#        gui.init_window()
#        gui.main()
