## Scripts directory

This contains useful scripts for the website.
All scripts should be run from the root directory, e.g. :

```
$ python3 -m scripts.johniangetter
```

* `johniangetter`
  * This retrieves the CRSids of all known Johnians and stores them in a pickled list for authentication.
  On the server this is run on a cronjob so once a week the list is updated and the website is restarted for changes to take effect.
* `htmleditor`
  * Used to edit html files en masse. It can strip out the main and header of pages using the John's template. See file for more info.
* `purge_pycache`
  * Can be used to delete all pycache files, useful if they are causing a problem. If your changes don't seem to be taking effect
  clearing your pycache and your browser cookies/ cache can help.
