package tnmc::templates::user;

use strict;

use tnmc::cookie;

#
# module configuration
#

use Exporter;
use vars qw(@ISA @EXPORT @EXPORT_OK);

@ISA = qw(Exporter);

@EXPORT = qw(show_user_homepage);

@EXPORT_OK = qw();

#
# module vars
#

#
# module routines
#

sub show_user_homepage {
    my $today;

    ############################
    ### Do the date stuff.
    open (DATE, "/bin/date |");
    while (<DATE>) {
        chop;
        $today = $_;
    }
    close (DATE);
    
    if ($USERID != 1){
        open (LOG, '>>user/log/splash.log');
        print LOG "$today\t$ENV{REMOTE_ADDR}";
        print LOG "\t$USERID";
        print LOG "\t$USERID{username}";
        
        print LOG "\n";
        close (LOG);
    }
}

1;