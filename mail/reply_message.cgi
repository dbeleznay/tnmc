#!/usr/bin/perl

use lib '/tnmc';
use strict;

use tnmc::security::auth;
use tnmc::template;
use tnmc::cgi;

use tnmc::mail::data;
use tnmc::mail::parse;
use tnmc::mail::template;
use tnmc::mail::prefs::data;

#############
### Main logic

header();

if ($USERID) {
    show_heading('mail');

    my $Id = &tnmc::cgi::param('Id');

    my $orig_message = get_message($USERID,$Id);

    my %message;
    $message{AddrFrom} = mail_get_email_address($USERID);
    if ($$orig_message{ReplyTo}) {
        $message{AddrTo} = $$orig_message{ReplyTo};
    }
    else {
        $message{AddrTo} = $$orig_message{AddrFrom};
    }

    $message{Subject} = $$orig_message{Subject};
    if ($message{Subject} !~ /^re:/i) {
        $message{Subject} = "Re: " . $message{Subject};
    }

    my $Quote = mail_get_pref($USERID,'Quote');
    if ($Quote eq 'Yes') {
        $message{Body} = message_quote($orig_message);
    }

    message_print_compose(\%message);
}
    
footer();
