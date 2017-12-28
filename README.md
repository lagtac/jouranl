# Jouranl

Jouranl is a personal note taking tool that works on the command line. https://github.com/lagtac/jouranl

    $ jour write: This is my first entry.
    $ jour write: 'This is my second entry'
    $ jour write: -h1 Topic of the day
    $ jour write: -p A paragraph. -p Another paragraph. -u --list item --another list item.
    $ jour write --interactive
    > I missed my appointment with the doctor.
    > New notification: 28 Oct 17:00, See doctor.
    >

    $ jour read
    $ jour read --last 
    $ jour read --first
    $ jour read --current
    $ jour read --ago [2d, 2m, 2h]
    $ jour read --when 2017-09-01 

    $ jour list --all
    $ jour list --first
    $ jour list --today
    $ jour list --when 2d
    $ jour list --since 12-10-2017 [--until yesterday]
    