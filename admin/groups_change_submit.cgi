#!/usr/bin/perl

##################################################################
#    Scott Thompson - scottt@interchange.ubc.ca
##################################################################
### Opening Stuff. Modules and all that. nothin' much interesting.

use lib '/tnmc';
use tnmc::db;
use tnmc::security::auth;
use tnmc::user;
use tnmc::cgi;



    #############
    ### Main logic
    
    &db_connect();
    # &header();

    my $group = &tnmc::cgi::param('group');

    #
    # fore every user that's been submited,
    # see if the rank for this group has changed,
    # if so, then save the new rank in the db.
    #
    foreach $key (&tnmc::cgi::param()){
        
        next if ($key !~ s/^USER//);
        $newRank = &tnmc::cgi::param("USER$key");

        &get_user($key, \%user);
        if ($newRank ne $user{"group$group"}){
            $user{"group$group"} = $newRank;
            &set_user(%user);
            ## debugging
            # print "$key : " . &tnmc::cgi::param("USER$key") ." $user{username} <br>";
        }
    }

    # &footer();
    &db_disconnect();

    print "Location: groups.cgi?groupID=$group\n\n";

