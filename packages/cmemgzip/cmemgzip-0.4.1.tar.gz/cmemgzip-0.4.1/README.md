# cmemgzip

cmemgzip v.0.4.1 

A Python 3 Open Source utility created by Carles Mateo.

http://blog.carlesmateo.com/cmemgzip

cmemgzip is created for those ocasions when we are in a Server, and has the drive/s full, there is no disk space, and we don't want to delete the core files/dumps or logs.
What cmemgzip does is to read the file in binary mode, to keep completely in memory, to compress it from memory, then ensure it has write permissions on the folder (by creating and empty file), and delete the original file, and write from memory the compressed file.
It can also load the file per blocks, and compress those blocks, at the cost of a bit of loss of compression efficiency. For that parameters -m=XXM or -m=YYG is used.
Refer to the PDF manual for more details.

This file can be later decompressed by **gzip/gunzip** or reviewed with **zcat**.

# The default mode: Allocate all the file in memory

In order to be able to do its job, your server or instance, must have enough free memory to allocate all the file in memory, and its version compressed.

For example, in order to **cmemgzip** a 2.7GB core dump file, you will need:

2.7GB from the original file + 270MB from the compressed file, aprox 3.1GB of RAM Memory free.

# The Block mode: Use a chunk size

In the compression by blocks you specify how many Megabytes or Gigabytes will be used to read the Block from the file.
Then that block will be compressed in memory and a new block will be loaded.

For example, in order to compress a log file of 2 GB in size, by using an small amount of memory you can run:

`cmemgzip -m=100M myfile.log`

This will load the file in blocks of 100MB and compress them into memory.
For a 2GB log file that result in 200 MB once compressed, using blocks of 100MB, the memory requirements for cmemgzip would be around 300 MB.
However, you can specify to use a block size of 10 MB, and then memory required will be only around 220 MB.
It depends on how much it is compressed.
By general rule for logs, the biggest the block size is, the better savings in disk space you'll get. 

# Risks

This tool must be used very carefully. If you have many processes competing to write to the drive, they may fill the space recovered when deleting the original file fast, and make impossible to write its compressed version.
On this version 0.2, in that (extreme) situation, it asks for another destination to store the compressed file.
This should not happen unless that server was under extreme load. If you compress logs or core dumps, the compression ratio is so high, that is really difficult that this mnay happen. As the space gain is massive. (From 2.7GB uncompressed core dump file, to 268MB when compressed). Use it wisely at your own risk.

cmemgzip will check that files compressed are at least 100 bytes in size, and will cancel the process if the compressed version is bigger than the original file (typically if you attempt to compress an already compressed file).


Release notes:
==============

This version v. 0.4.1 has been tested with Ubuntu and Windows 10 64 bit.
Previous version v. 0.4 has been tested with Ubuntu, Windows 10 Professional, Mac Os X and Ubuntu 20.04 LTS in Raspberry Pi 4.

Version 0.4.1 autodetects Windows and disables colors.

Be careful not to use on programs that keep a fd (File Descriptor) open to the log file, as deleting the original log file will not return the space to the Filesystem. That was tipically the case of some webservers. You should stop the webserver first, or deal with the fds.
