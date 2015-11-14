# Introduction #

## Source distribution ##

For windows users it's better to get a zip file.

```
python setup.py sdist --formats=zip 
```

## Debian packaging ##

It's something :). Here are the package that you'll have to install:

> - dpkg-

&lt;something&gt;

 ...
> - fakeroot
> - dh\_make
> - setuputils

I think I'm close, but I still have tons of errors ...

I have to say that Adept package manager is a good tool, but urpmf command is missing. (I know there is an equivalent with apt-cache thought)...