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
        
	%pic;	
	$cgih = new CGI;
	$picID = $cgih->param('picID');
	
       	&get_pic($picID, \%pic);
	  	
	print qq {
            
            <form action="api_upload_submit.cgi" method="post" enctype="multipart/form-data">

	    <table>

            <tr><th colspan="2">upload image</th></tr>
                    
            <tr><td><b>File</b></td>
                <td><input type="file" name="API_FILENAME"></td>
            </tr>

            <tr><td><b>Title</b></td>
                <td><input type="text" name="title"></td>
            </tr>

            <tr><td><b>Timestamp</b></td>
                <td><input type="text" name="timestamp" value="0000-00-00 00:00:00"></td>
            </tr>

            <tr><td><input type="submit" value="Submit"></td>
                <td></td>
            </tr>
	};
        
        print qq{
            <tr><th colspan="2">override default database fields (optional)</th></tr>
        };
	
        foreach $key (keys %pic){
            
            # please don't kill existing images
            next if ($key eq 'picID');
            # already defined above
            next if ($key eq 'timestamp');
            next if ($key eq 'title');
            # we can figure this out ourselves
            next if ($key eq 'width');
            next if ($key eq 'height');
            
            print qq{	
                <tr><td><b>$key</td>
                    <td><input type="text" name="$key" value="$pic{$key}"></td>
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