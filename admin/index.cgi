#!/usr/bin/perl

##################################################################
#    Scott Thompson - scottt@css.sfu.ca 
#    Jeff Steinbok  - steinbok@interchange.ubc.ca
##################################################################
### Opening Stuff. Modules and all that. nothin' much interesting.

use strict;
use lib '/tnmc';

use tnmc::db;
use tnmc::template;
use tnmc::user;
use tnmc::cgi;

#############
### Main logic

&header();
&db_connect();

&show_heading('<a id="personal">Personal</a>');
&show_basic_users_list();


&footer();
&db_disconnect();

##########################################################
#### sub procedures.
##########################################################

#########################################
sub show_basic_users_list{
    my (@users, %user, $userID, $key);

    my $cgih = &tnmc::cgi::get_cgih();
    my $order = $cgih->param('order') || 'username';

    &list_users(\@users, '', "ORDER BY $order");

    print qq{
        <table cellspacing="0" cellpadding="0" border="0">
        <tr>
            <th><a href="index.cgi?order=userID">userID</a></td>
            <th>&nbsp;&nbsp;</td>
            <th><a href="index.cgi?order=username">username</a></td>
            <th>&nbsp;&nbsp;</td>
            <th><a href="index.cgi?order=fullname">fullname</a></td>
            <th>&nbsp;&nbsp;</td>
            <th>&nbsp;&nbsp;</td>
        </tr>
    };

    foreach $userID (@users){
        get_user($userID, \%user);
        print qq{
            <tr>
                <td nowrap>$user{userID}</td>
                <td></td>
                <td nowrap>$user{username}</td>
                <td></td>
                <td nowrap>$user{fullname}</td>
                <td></td>
                <td nowrap>
                <a href="user_edit.cgi?userID=$userID">[Edit]</a> 
                <a href="user_delete_submit.cgi?userID=$userID">[Del]</a>
                </td>
            </tr>
        };
    }
    print qq{
        </table>
    };

}
