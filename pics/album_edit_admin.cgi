#!/usr/bin/perl

##################################################################
#	Scott Thompson
##################################################################
### Opening Stuff. Modules and all that. nothin' much interesting.

use lib '/usr/local/apache/tnmc/';
use tnmc;
require 'pics/PICS.pl';

{
	#############
	### Main logic

	&db_connect();
	&header();

	%album;	
	$cgih = new CGI;
	$albumID = $cgih->param('albumID');
	
       	&get_album($albumID, \%album);
	  	
	print qq {
            
		<form action="album_edit_admin_submit.cgi" method="post">
		<table>
	};
	
        foreach $key (keys %album){
       	       print qq{	
			<tr><td><b>$key</td>
                            <td><input type="text" name="$key" value="$album{$key}"></td>
			</tr>
		};
       	}
	
	print qq{
		</table>
		<input type="submit" value="Submit">
		</form>
	}; 

	
	&footer();

	&db_disconnect();
}
