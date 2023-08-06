===========================
Working with BASIC Programs
===========================

``cbm-shell`` can be used to quickly edit BASIC programs without
starting up an emulator:

.. code-block:: text

    (cbm) list 0:MYPROGRAM myprogram.txt
    (cbm) edit myprogram.txt
    [perform changes, save and exit editor]
    (cbm) unlist myprogram.txt 0:NEWPROGRAM
 
