
What is this?
=============
push_public is a little tool for pushing content to a webserver. It is suitable for usage with Rapsberry Pi but works with other Linux based servers as well.
When combined with the awesome h5ai project, you can even get a gallery display similar to what services like Dropbox offer. As a bonus you can even download all the pictures at once.


Download
=============
You can get the code at https://github.com/jazzer/push_public/zipball/master. The setup instructions include the download :).


Setup
=============
This is to be executed on your *desktop computer*:

    # get the source
    wget https://github.com/jazzer/push_public/zipball/master
    # unpack
    unzip master
    # rename the folder
    mv jazzer-push_public* push_public
    # remove zip file
    rm master

This is to executed on your *Raspberry Pi*:

    # install Apache webserver
    sudo groupadd www-data
    sudo usermod -a -G www-data www-data
    sudo apt-get update
    sudo apt-get install apache2
    # get rsync
    sudo apt-get install rsync
    # make folder for synchronization
    mkdir -p /home/pi/public/p
    cd /home/pi/public/p
    nano .htaccess
    # write in the open editor:
    Options -Indexes
    # save by hitting F2 and Y for yes
    # enable reading file for everyone (including the webserver)
    sudo chmod -R 755 p
    chmod +x $HOME
    # make a link
    sudo ln -s /home/pi/public/p/ /var/www/p
    # install h5ai (somewhat optional, but it looks soooo damn good, don't miss it!)
    wget http://larsjung.de/release/h5ai/h5ai-0.20.zip
    unzip h5ai-0.20.zip
    rm h5ai-0.20.zip
    sudo mv _h5ai /var/www/
    sudo chown www-data:www-data /var/www/_h5ai

Installation instructions for Apache taken from [here](http://fusionstrike.com/2012/installing-apache2-raspberry-pi-debian)


Usage
=============
Make a profile for your Raspberry Pi in the profiles directory. You can start from the profile named ```example-pi``` in there. For the next steps we assume you called your profile ```pi```.

From your desktop computer, you then can push content, i.e. a file or a folder with one of these commands:

    ./push_public.py pi testfile.txt
    ./push_public.py pi testfolder

If you want to generate links that are not protected by a random string in the url, you can add ```pub``` in the end, i.e.:

    ./push_public.py pi testfile.txt pub
    ./push_public.py pi testfolder pub


What else?
=============
It might be useful to enable automatic login to your Raspberry Pi [using key files](http://www.thegeekstuff.com/2008/11/3-steps-to-perform-ssh-login-without-password-using-ssh-keygen-ssh-copy-id/). That way you can have things fully automated.

If you are deploying this apart from Raspberry Pi, you might have to take a look to open_basedir (set to /var/www/vhosts/slzm.de/httpdocs:/home/johannes/p/ or similar) and disable safe_mode. http://domain.tld/_h5ai/ gives information about the status.

