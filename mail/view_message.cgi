#!/usr/bin/perl

use lib '/tnmc';
use strict;

use tnmc::security::auth;
use tnmc::template;
use tnmc::cgi;

use tnmc::mail::data;
use tnmc::mail::template;

#############
### Main logic

header();

if ($USERID) {
    show_heading('mail');

    my $Id = &tnmc::cgi::param('Id');
    my $message_ref = get_message($USERID,$Id);
    message_print($message_ref);
}
    
footer();
