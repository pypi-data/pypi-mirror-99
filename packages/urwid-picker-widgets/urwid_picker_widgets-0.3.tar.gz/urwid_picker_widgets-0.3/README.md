# Urwid Picker Widgets

Specialized picker widgets for urwid that extend its features.

The [additional_urwid_widgets](https://github.com/AFoeee/additional_urwid_widgets) library by [AFoeee](https://github.com/AFoeee) adds some good specialized picker widgets, e.g. date picker, integer picker, etc.

However, due to a lack of activity/sync from that project, I decided to extend and update the features by adding a `time picker widget` to the list.

This library mainly focuses on `*Picker` widgets for urwid.
(Also checkout [**MessageDialog**](https://github.com/AFoeee/additional_urwid_widgets/wiki/MessageDialog) widget from `additional_urwid_widgets`!)

***


## Installation

The project can be installed via [pip](https://pypi.org/project/urwid-picker-widgets/).


### Options

There are several approaches to install a package via the terminal (as described [here](https://github.com/googlesamples/assistant-sdk-python/issues/236#issuecomment-383039470)):
*  Setup a virtual env to install the package (**recommended**):

        python3 venv env
        source ./env/bin/activate
        python3 -m pip install urwid-picker-widgets
    
* Install the package to the user folder:

        python3 -m pip install --user urwid-picker-widgets
    
* Install to the system folder (**not recommended**):

        python3 -m pip install urwid-picker-widgets

***


## Widgets

See the corresponding wiki entries of the widgets for more information.

* [**DatePicker**](https://github.com/Ezio-Sarthak/urwid_picker_widgets/wiki/DatePicker)
A (rudimentary) date picker.

![date_picker](https://user-images.githubusercontent.com/55916430/111909895-19056700-8a85-11eb-9fff-1cfd7e924548.png)


* [**TimePicker**](https://github.com/Ezio-Sarthak/urwid_picker_widgets/wiki/TimePicker)
A (rudimentary) time picker.

![time_picker](https://user-images.githubusercontent.com/55916430/111909982-700b3c00-8a85-11eb-974f-46e62fa34f64.png)

* [**IndicativeListBox**](https://github.com/Ezio-Sarthak/urwid_picker_widgets/wiki/IndicativeListBox)
A [`urwid.ListBox`](http://urwid.org/reference/widget.html#listbox) with additional bars to indicate hidden list items.

![indicative_list_box](https://user-images.githubusercontent.com/55916430/111909930-389c8f80-8a85-11eb-8c01-64dbb07dbc56.png)

* [**IntegerPicker**](https://github.com/Ezio-Sarthak/urwid_picker_widgets/wiki/IntegerPicker)
A selector for integer numbers.

![integer_picker](https://user-images.githubusercontent.com/55916430/111909955-4a7e3280-8a85-11eb-97fd-740d550f478e.png)

* [**SelectableRow**](https://github.com/Ezio-Sarthak/urwid_picker_widgets/wiki/SelectableRow)
Wraps [`urwid.Columns`](http://urwid.org/reference/widget.html#columns) to make it selectable and adds behavior.

![selectable_row](https://user-images.githubusercontent.com/55916430/111909964-579b2180-8a85-11eb-93f1-1ed6f52ce052.png)


## FAQ

**Symbols are not encoded properly (Instead question mark symbol '?' is visible')**

Type following command in terminal for the fix.

```
export LANG="en_IN.UTF-8"
```

(Here `IN` refers to the `India`, the native country of the user)